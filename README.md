# Information-Collection



1.0 计划：
- Web
  * 基本的数据库和前端
  * 手动添加新内容
  * 添加书签
  * 将书签导出为word
  * 不支持用户
  * 不支持新内容提醒（需先支持用户）
  * 不支持自定义的来源网站
- 爬虫
  * 爬取普通网站的正文数据
  * 获取文章发布时间
  * 部分支持通用网站
  * 不支持网页失效检查
- 总结
  * 对长文章使用llm进行总结
  * 不支持英文标题翻译

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

- 爬虫：
  * 静态网页使用BeautifulSoup与newspaper混合爬取
  * 动态加载网页使用playwright模拟浏览器加载，再使用newspaper爬取
   
- 文本总结
  * 模型：本地qwen2-72b
  * Agent：General Agent
