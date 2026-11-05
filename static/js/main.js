// 页面交互脚本：删除确认由模板中的 confirm 完成。
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file && file.size > 20 * 1024 * 1024) {
        alert("文件超过 20 MB，请重新选择。");
        fileInput.value = "";
      }
    });
  }
});