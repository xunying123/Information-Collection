<template>
  <div class="help-page">
    <h1>帮助页面</h1>
    <p>欢迎来到帮助页面，这里将为您提供有关本站的功能介绍与使用指南。</p>

    <section class="help-content section">
      <h2>Web 前端</h2>
      <p>Web 前端采用 vue 开发，使用了 vue router，element-ui 和 naive-ui。</p>

      <h2>网站功能介绍</h2>

      <h3>侧边栏</h3>
      <p>
        侧边栏包含了网站的基本信息，可以通过点击侧边栏的链接切换页面。在对应的页面中能够看到相应的内容。
      </p>
      <ul>
        <li><span style="font-weight: bold">首页（全部）：</span>显示所有文章。</li>
        <li><span style="font-weight: bold">今日更新：</span>显示今日更新的文章。</li>
        <li>
          <span style="font-weight: bold">书签列表：</span>显示用户收藏的文章。
          <!-- 支持导出为 word 文档，可以选择导出的文章。支持分页显示。 -->
        </li>
        <li>
          <span style="font-weight: bold">管理组织：</span><strong>组织管理员权限页面</strong>，有以下功能：
          <ul>
            <li>可以增加或删除<strong>后台爬虫程序需要爬取的</strong>网站。</li>
          </ul>
        </li>
        <li>
          <span style="font-weight: bold">专属新闻：</span>显示所有订阅的新闻，可以按照<strong>网站分类</strong>或<strong>文章分类</strong>查看文章。
          <ul>
            <li>
              网站分类：根据订阅的网站进行分类。
              <ul>
                <li>
                  类别页面：显示某一网站大类的所有文章。<strong>此页面支持网站大卡片视图</strong>。
                </li>
                <li>网站页面：显示某一网站的所有文章，可以按照网站查看文章。</li>
              </ul>
            </li>
            <li>
              文章分类：根据文章主题来进行分类。
              <ul>
                <li>类别页面：显示某一主题的所有文章。</li>
              </ul>
            </li>
          </ul>
        </li>
        <li>
          <span style="font-weight: bold">设置：</span>用户设置界面。
          <ul>
            <li>所属组织：显示用户所属的组织。可以选择退出组织，但请谨慎操作。</li>
            <li>
              定制管理：支持用户<strong>个人定制</strong>订阅源和关键词：
              <ul>
                <li>
                  订阅源：可以订阅某些网站的文章，<strong>订阅的网站必须是后台爬虫程序会爬取的网站</strong>，订阅后可以通过开关切换显示全部网页或<strong>仅显示订阅的网页</strong>。
                </li>
                <li>
                  关键词：可以订阅某些关键词，<strong>支持自定义关键词</strong>，但建议优先选择数据库类已有的（给出提示的）关键词。订阅后可以通过开关切换显示全部文章或<strong>仅显示包含订阅关键词的文章</strong>。
                </li>
                <li>
                  订阅源和关键词都支持<strong>导出为 json 文件及导入，便于新用户快速批量配置</strong>。
                </li>
              </ul>
            </li>
            <li>
              侧边栏显示模式：可以选择按照<strong>网站分类</strong>或<strong>文章分类</strong>显示侧边栏。
            </li>
            <li>侧边栏颜色：可以选择侧边栏的颜色。</li>
          </ul>
        </li>
      </ul>

      <h3>顶栏</h3>
      <p>顶栏中包含了对于显示的文章的一些筛选和显示功能：</p>
      <ul>
        <li>
          <span style="font-weight: bold">筛选：</span>对显示的文章进行一些筛选。
          <ul>
            <li>关键词类别复选框：可以点击选择显示的类别。</li>
            <li>网站类别复选框：可以点击选择显示的类别。</li>
            <li>
              时间范围：可以选择显示的时间范围。<strong>选择1天内时，显示的会是上一个工作日内的结果</strong>。
            </li>
            <li>
              排序方式：可以选择对文章按<strong>时间</strong>或<strong>重要度</strong>进行排序。
            </li>
          </ul>
        </li>
        <li><span style="font-weight: bold">搜索框：</span>可以输入关键词搜索文章标题。</li>
        <li>
          <span style="font-weight: bold">视图切换：</span>可以切换文章的显示方式。
          <ul>
            <li>在"标题"视图中，可以点击标题旁显示的网站名称跳转到对应网站页面。</li>
          </ul>
        </li>
      </ul>

      <h3>文章页面</h3>
      <p>在所有显示文章的页面中，点击文章即可查看文章的详细内容。在文章页面中有：</p>
      <ul>
        <li><span style="font-weight: bold">返回：</span>可以返回到文章列表页面。</li>
        <li><span style="font-weight: bold">复制链接：</span>可以复制文章的链接。</li>
        <li><span style="font-weight: bold">加入书签：</span>可以将文章加入书签。</li>
        <li><span style="font-weight: bold">查看原文：</span>可以跳转到文章的原始链接。</li>
        <li>
          <span style="font-weight: bold">文章内容：</span>
          <ul>
            <li>标题</li>
            <li>关键词</li>
            <li>发布时间</li>
            <li>摘要</li>
            <li>全文</li>
          </ul>
        </li>
        <li>拖动左侧的边框可以调整文章内容的显示宽度。</li>
      </ul>

      <h3>注意事项</h3>
      <ul>
        <li>如果在使用过程中遇到问题，可以尝试清除浏览器缓存。</li>
        <li>如果在筛选文章后显示的结果过少，可以多次尝试滚动到页面底部，触发加载更多文章。</li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
/* 整体容器 */
.help-page {
  padding: 20px;
  background: rgba(255, 255, 255, 1); /* 浅灰色背景 */
  border-radius: 12px;
  max-width: 1200px;
  margin: 20px auto;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  color: #333;
}

/* 页面标题 */
.help-page h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: rgb(0, 64, 152);
  border-bottom: 3px solid rgb(0, 64, 152); /* 添加底部蓝色边框 */
  padding-bottom: 8px;
  text-align: center;
}

/* 内容部分 */
.help-content {
  line-height: 1.8;
  font-size: 1.1rem;
  color: #555;
}

.section {
  margin-bottom: 30px;
}

/* 小节标题 */
.help-content h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: rgb(0, 64, 152, 0.9);
  border-bottom: 2px solid rgb(0, 64, 152, 0.9);
  padding-bottom: 6px;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  text-align: left;
  position: relative;
}

/* 三级标题 */
.help-content h2 {
  font-size: 1.6rem;
  font-weight: 500;
  color: rgb(0, 64, 152, 0.9);
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
  text-align: left;
  position: relative;
}

/* 四级标题 */
.help-content h3 {
  font-size: 1.4rem;
  font-weight: 500;
  color: rgb(0, 64, 152, 0.8);
  margin-top: 1.2rem;
  margin-bottom: 0.5rem;
  position: relative;
}

/* 列表样式 */
.help-content ul {
  padding-left: 20px;
  margin-top: 1rem;
  list-style-type: disc;
}

.help-content li {
  margin-bottom: 12px;
  line-height: 1.6;
}

/* 加强对某些列表项的视觉引导 */
.help-content li strong {
  color: rgb(240, 131, 0);
  font-weight: bold;
}

/* 图片样式 */
.help-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 链接样式 */
.help-content a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s ease;
}

.help-content a:hover {
  color: #e74c3c;
  text-decoration: underline;
}

/* 调整段落间距 */
.help-content p {
  margin-top: 1rem;
  line-height: 1.7;
}

/* 样式优化后的按钮 */
button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2980b9;
}
</style>
