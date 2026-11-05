# StudyHub 学习资料管理系统

StudyHub 是一个基于 Python Flask 和 SQLite 的轻量级学习资料管理 Web 应用，面向大学生整理课程课件、笔记、实验报告和电子书。

## 功能特性
- 首页统计资料总数、分类数量和最近添加记录
- 学习资料新增、编辑、删除
- 按资料名称、课程和描述进行关键词搜索
- 按分类筛选
- 支持常见学习文件上传和下载（单文件最大 20 MB）
- SQLite 本地存储，无需单独安装数据库服务

## 技术栈
Python 3.10+、Flask、SQLite、HTML、CSS、JavaScript。

## 本地运行
```bash
# 1. 克隆仓库
git clone https://github.com/<你的GitHub用户名>/<仓库名>.git
cd <仓库名>

# 2. 创建并激活虚拟环境（Windows）
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动
python app.py
```
浏览器访问 http://127.0.0.1:5000 。

首次运行会自动创建 `studyhub.db`。上传文件保存在 `uploads/` 目录，该目录和数据库默认不提交到 Git。

## 项目结构
```text
StudyHub/
├── app.py                 # Flask 入口、首页与文件下载
├── database/db.py         # SQLite 初始化与连接
├── routes/materials.py    # 资料增删改查、搜索和上传
├── templates/             # 页面模板
├── static/css/            # 样式
├── static/js/             # 前端交互
├── docs/                  # 项目与协作文档
├── uploads/               # 本地上传目录
├── requirements.txt
├── LICENSE
└── README.md
```

## 文件安全与使用说明
仅允许 README 中列出的扩展名，上传文件名会经过安全处理并使用随机文件名保存；单文件大小限制为 20 MB。此项目用于课程演示和本地学习，不建议未经安全加固直接部署到公网。正式部署前应更换 `SECRET_KEY`、关闭调试模式，并增加用户身份验证、访问控制、CSRF 防护和更严格的文件内容检查。

## 开源许可
本项目采用 MIT License。使用者可以自由使用、复制、修改和分发，但需要保留版权与许可声明。完整文本见 `LICENSE`。

## 贡献方式
欢迎通过 Issue 反馈问题或提出功能建议。代码修改建议先创建功能分支，再提交 Pull Request。详细规则见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

## 项目状态
课程实践项目，功能持续完善中。请以仓库实际发布版本为准。
