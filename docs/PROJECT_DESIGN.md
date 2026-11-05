# 项目设计说明

## 1. 项目背景
大学生的学习资料通常分散在聊天记录、网盘和本地文件夹中，容易出现重复保存、分类不统一和查找效率低等问题。StudyHub 尝试提供一个简单统一的资料入口。

## 2. 设计目标
实现学习资料基本信息的持久化管理，支持增删改查、关键词搜索、分类筛选以及附件上传下载。

## 3. 模块划分
- 表现层：Jinja2 模板、CSS 和 JavaScript。
- 路由层：Flask Blueprint 处理 HTTP 请求。
- 数据层：SQLite 保存资料元数据。
- 文件层：uploads 目录保存附件。

## 4. 数据结构
materials 表字段：id、title、course、category、file_type、description、filename、created_at。

## 5. 后续改进
增加用户登录、标签、多条件排序、批量导入导出、云端存储和自动化测试。
