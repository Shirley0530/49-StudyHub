from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
from database.db import get_db
import uuid

materials_bp = Blueprint("materials", __name__, url_prefix="/materials")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "txt", "md", "zip", "py", "java", "jpg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@materials_bp.route("/")
def list_materials():
    keyword = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    db = get_db()
    sql = "SELECT * FROM materials WHERE 1=1"
    params = []
    if keyword:
        sql += " AND (title LIKE ? OR course LIKE ? OR description LIKE ?)"
        params.extend([f"%{keyword}%"] * 3)
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY created_at DESC"
    rows = db.execute(sql, params).fetchall()
    cats = db.execute("SELECT DISTINCT category FROM materials WHERE category != '' ORDER BY category").fetchall()
    return render_template("materials.html", materials=rows, categories=cats, q=keyword, selected_category=category)

@materials_bp.route("/add", methods=["GET", "POST"])
def add_material():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("资料名称不能为空。", "error")
            return redirect(url_for("materials.add_material"))
        course = request.form.get("course", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        upload = request.files.get("file")
        filename = ""
        file_type = ""
        if upload and upload.filename:
            if not allowed_file(upload.filename):
                flash("暂不支持该文件类型。", "error")
                return redirect(url_for("materials.add_material"))
            original = secure_filename(upload.filename)
            ext = original.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            upload.save(Path(current_app.config["UPLOAD_FOLDER"]) / filename)
            file_type = ext.upper()
        db = get_db()
        db.execute(
            "INSERT INTO materials(title, course, category, file_type, description, filename) VALUES (?, ?, ?, ?, ?, ?)",
            (title, course, category, file_type, description, filename)
        )
        db.commit()
        flash("资料添加成功。", "success")
        return redirect(url_for("materials.list_materials"))
    return render_template("add_material.html")

@materials_bp.route("/<int:material_id>/edit", methods=["GET", "POST"])
def edit_material(material_id):
    db = get_db()
    material = db.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    if material is None:
        return "资料不存在", 404
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("资料名称不能为空。", "error")
            return redirect(url_for("materials.edit_material", material_id=material_id))
        db.execute(
            "UPDATE materials SET title=?, course=?, category=?, description=? WHERE id=?",
            (title, request.form.get("course","").strip(), request.form.get("category","").strip(),
             request.form.get("description","").strip(), material_id)
        )
        db.commit()
        flash("资料修改成功。", "success")
        return redirect(url_for("materials.list_materials"))
    return render_template("edit_material.html", material=material)

@materials_bp.route("/<int:material_id>/delete", methods=["POST"])
def delete_material(material_id):
    db = get_db()
    material = db.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    if material:
        if material["filename"]:
            file_path = Path(current_app.config["UPLOAD_FOLDER"]) / material["filename"]
            if file_path.exists():
                file_path.unlink()
        db.execute("DELETE FROM materials WHERE id = ?", (material_id,))
        db.commit()
        flash("资料已删除。", "success")
    return redirect(url_for("materials.list_materials"))
