# Information-Collection



1.0 计划：
- Web
  * 基本的数据库和前端
  * 需要 JA 用户登录访问
  * 支持按标题搜索文章
  * 每日更新汇总
  * 书签功能 
    * 本地存储书签
    * 书签页面按收藏日期分页
    * 将书签导出为 word（导出时可再选择文章）
  * 自定义来源网站（需有管理员权限）
  * 按照来源网站分类阅读
- 爬虫
  * 爬取普通网站的正文数据
  * 获取文章发布时间
  * 支持通用网站
  * 网页失效检查
- 总结
  * 对长文章使用llm进行总结
  * 英文标题翻译与正文翻译

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
