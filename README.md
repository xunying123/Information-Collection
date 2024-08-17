# Information-Collection



1.0 计划：
- Web
  * 基本的数据库和前端
  * 手动添加新内容
  * 不支持用户
  * 不支持新内容提醒（需先支持用户）
  * 不支持自定义的来源网站
- 爬虫 @hastin
- 总结 @xunying

架构设计：

- 数据库：使用 postgresql
  * 类别
    + [style] 图标
  * 网站
    + [relation] 类别
    + [style] 图标 default: url/favicon.ico
  * 文章
    + 内容
    + 标题
    + 来源链接
    + [relation] 类别
    + [relation] 网站
    + [style] 封面图片

- 服务器后端: 使用flask提供api, 负责与前端和数据库的交互。
- 服务器前端：使用vue3，静态。

- 信息维护：TODO: @hastin & @xunying
