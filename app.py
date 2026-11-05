from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from pathlib import Path
from werkzeug.utils import secure_filename
from database.db import init_db, get_db
from routes.materials import materials_bp

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "txt", "md", "zip", "py", "java", "jpg", "png"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024

app = Flask(__name__)
app.config.update(
    SECRET_KEY="change-this-secret-key-before-deployment",
    UPLOAD_FOLDER=str(UPLOAD_DIR),
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH
)
UPLOAD_DIR.mkdir(exist_ok=True)
init_db()
app.register_blueprint(materials_bp)

@app.route("/")
def index():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    categories = db.execute("SELECT COUNT(DISTINCT category) FROM materials WHERE category != ''").fetchone()[0]
    recent = db.execute("SELECT * FROM materials ORDER BY created_at DESC LIMIT 5").fetchall()
    return render_template("index.html", total=total, categories=categories, recent=recent)

@app.route("/uploads/<path:filename>")
def download_file(filename):
    # 仅允许下载 uploads 目录中的文件名，不接受用户提供的任意路径
    safe_name = Path(filename).name
    path = UPLOAD_DIR / safe_name
    if not path.is_file():
        abort(404)
    return send_from_directory(UPLOAD_DIR, safe_name, as_attachment=True)

@app.errorhandler(413)
def too_large(_error):
    flash("文件超过 20 MB，请选择较小的文件。", "error")
    return redirect(request.referrer or url_for("materials.list_materials"))

if __name__ == "__main__":
    app.run(debug=True)
