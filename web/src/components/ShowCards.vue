<script setup lang="ts">
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import type { PageItem } from '@/api_interface'
import SearchInput from '@/components/SearchInput.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import ArticleList from '@/components/ArticleList.vue'
import SiteArticleCard from '@/components/SiteArticleCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import { search_keyword_key, all_categories_key } from '@/key'
import { getCategories } from '@/sdk'

const props = defineProps<{ pages: PageItem[]; title: string; loading: boolean }>()
const searchKeyword = inject(search_keyword_key)!
const allCategories = inject(all_categories_key)!
const route = useRoute()

// 新增关键词分类定义
const keywordCategories = ref([
  {
    id: 1,
    name: '头条',
    keywords: [
      '习近平',
      '李强',
      '省份',
      '发布',
      '经济',
      '数据',
      '讲话',
      '社会',
      '热点',
      '事件',
      '民生',
      '政策',
      '舆论',
      '行业',
      '国际',
      '会议',
      '民生',
      '物价',
      '房价',
      '社保',
      '文化',
      '热点',
      '交通',
      '能源',
      '基建',
      '两会',
      '标准',
      '代表',
      '人大',
      '政协',
      '委员',
      '补贴',
      '工程',
      '通知',
      '发布',
      '记者会',
      '中央宣传部',
      '中宣部',
      '外交部',
      '国防部',
      '国家发展和改革委员会',
      '发改委',
      '教育部',
      '科学技术部',
      '科技部',
      '工业和信息化部',
      '工信部',
      '国家民族事务委员会',
      '公安部',
      '国家安全部',
      '国安部',
      '民政部',
      '司法部',
      '财政部',
      '人力资源和社会保障部',
      '人社部',
      '自然资源部',
      '生态环境部',
      '住房和城乡建设部',
      '住建部',
      '交通运输部',
      '交通部',
      '水利部',
      '农业农村部',
      '商务部',
      '文化和旅游部',
      '文旅部',
      '国家卫生健康委员会',
      '卫健委',
      '退役军人事务部',
      '应急管理部',
      '中国人民银行',
      '央行',
      '审计署',
      '国家语言文字工作委员会',
      '国家航天局',
      '国家原子能机构',
      '国家外国专家局',
      '国家海洋局',
      '国家核安全局',
      '国家乡村振兴局',
      '国务院国有资产监督管理委员会',
      '国资委',
      '海关总署',
      '国家税务总局',
      '国税局',
      '国家市场监督管理总局',
      '市监局',
      '国家金融监督管理总局',
      '中国证券监督管理委员会',
      '国家广播电视总局',
      '国家体育总局',
      '国家信访局',
      '国家统计局',
      '国家知识产权局',
      '国家国际发展合作署',
      '国家医疗保障局',
      '国务院参事室',
      '国家机关事务管理局',
      '国家反垄断局',
      '国家认证认可监督管理委员会',
      '国家标准化管理委员会',
      '国家新闻出版署（国家版权局）',
      '国家宗教事务局',
      '国务院研究室',
      '国务院侨务办公室',
      '国务院港澳事务办公室',
      '国务院台湾事务办公室',
      '国家互联网信息办公室',
      '国务院新闻办公室',
      '新华通讯社',
      '新华社',
      '中国科学院',
      '中国社会科学院',
      '中国工程院',
      '国务院发展研究中心',
      '中央广播电视总台',
      '中国气象局',
      '国家行政学院',
      '党校',
      '国家粮食和物资储备局',
      '国家能源局',
      '国家数据局',
      '国家国防科技工业局',
      '国家烟草专卖局',
      '国家移民管理局',
      '国家林业和草原局',
      '国家铁路局',
      '中国民用航空局',
      '国家邮政局',
      '国家文物局',
      '国家中医药管理局',
      '国家疾病预防控制局',
      '国家矿山安全监察局',
      '国家消防救援局',
      '国家外汇管理局',
      '国家药品监督管理局',
      '全国妇联'
    ]
  },
  {
    id: 2,
    name: '教育',
    keywords: [
      '怀进鹏',
      '部长',
      '教育部',
      '教育改革',
      '双减政策',
      '职业教育',
      '高考改革',
      '学科评估',
      '校园安全',
      '教育信息化',
      '在线教育',
      '高校招生',
      '教师待遇',
      '教育公平',
      '青少年',
      '学生',
      '家长',
      '学校',
      '小学',
      '大学',
      '高校',
      '高中',
      '初中',
      '中学',
      '中小学',
      '学前教育',
      '义务教育',
      '高中阶段教育',
      '高等教育',
      '职业教育',
      '特殊教育',
      '继续教育',
      '民办教育',
      '家庭教育',
      '社区教育',
      '教育经费投入',
      '教育数字化',
      '智慧校园',
      '在线教育平台',
      '教育开放',
      '中外合作办学',
      '留学',
      '教师',
      '职称',
      '教育评价',
      '教材',
      '双减落实',
      '乡村教育',
      '产教融合',
      '教育督导',
      '新课标',
      '双一流',
      '学科',
      '教育惩戒规则',
      '校园安全',
      '心理健康',
      '高考',
      '课程',
      '通知',
      '关于',
      '发布'
    ]
  },
  {
    id: 3,
    name: '科技',
    keywords: [
      '科技',
      '新研究',
      '研究',
      '发现',
      '突破',
      '研究院',
      '大学',
      '高校',
      '人工智能',
      '量子计算',
      '技术',
      '芯片研发',
      '元宇宙',
      '区块链',
      '碳中和',
      '生物',
      '医药',
      '自动驾驶',
      '数据安全',
      '专利发布',
      '大模型',
      '脑机接口',
      '卫星互联网',
      '氢能源',
      '疫苗',
      '智能制造',
      '智慧城市',
      '数字孪生',
      '工业',
      '互联网',
      '经费',
      '技术出口管制',
      '专利',
      '伦理',
      '京津冀',
      '粤港澳',
      '长三角',
      '高铁'
    ]
  },
  {
    id: 4,
    name: '人才',
    keywords: [
      '人才',
      '科技人才',
      '人社部',
      '人力资源社会保障部',
      '校园',
      '就业',
      '招聘',
      '失业率',
      '灵活就业',
      '薪资',
      '职业技能',
      '劳动争议',
      '海归',
      '高校毕业生',
      '青年',
      '企业裁员',
      '落户补贴',
      '高层次人才',
      '认定',
      '海外引才',
      '灵活用工',
      '平台经济就业',
      '新职业',
      '996',
      '年龄歧视',
      '职场PUA',
      '求人倍率',
      '青年失业率',
      '人才缺口',
      '社保',
      '报告',
      '大奖',
      '获奖',
      '技能',
      '培训'
    ]
  },
  {
    id: 5,
    name: '国际',
    keywords: [
      '中方',
      '外交部',
      '发言人',
      '联合国',
      '世界银行',
      '世界卫生组织',
      '世卫',
      '国际冲突',
      '外交关系',
      '全球经济',
      '气候',
      '能源',
      '局势',
      '贸易协定',
      '跨国合作',
      '移民政策',
      '制裁',
      '俄乌',
      '中东',
      '南海',
      'RCEP',
      '气候峰会',
      '一带一路',
      '宗教',
      '难民危机',
      '极端主义',
      '美国',
      '韩国',
      '日本',
      '德国',
      '英国',
      '欧盟',
      '加拿大',
      '澳大利亚',
      '澳洲',
      '俄罗斯',
      '学校',
      '大学',
      '中小学'
    ]
  }
])

const filterOptions = ref({
  selectedCategories: [] as number[],
  selectedTimeRange: 'all',
  selectedSortOption: 'time',
  selectedKeywordCategories: [] as number[] // 新增关键词分类筛选
})

const filteredPages = ref<PageItem[]>(props.pages)

function filterPages() {
  filteredPages.value = [...props.pages]
  const now = new Date()

  if (filterOptions.value.selectedTimeRange !== 'all') {
    const days = parseInt(filterOptions.value.selectedTimeRange)
    let startTime: Date
    if (days === 1) {
      const yesterday = new Date(now)
      const day = now.getDay()
      if (day === 1) {
        yesterday.setDate(now.getDate() - 3)
      } else if (day === 0) {
        yesterday.setDate(now.getDate() - 2)
      } else {
        yesterday.setDate(now.getDate() - 1)
      }
      yesterday.setHours(0, 0, 0, 0)
      startTime = yesterday
    } else {
      startTime = new Date(now)
      startTime.setDate(now.getDate() - days)
      startTime.setHours(0, 0, 0, 0)
    }
    filteredPages.value = filteredPages.value.filter((page) => {
      const publishTime = new Date(page.publish_time)
      return publishTime >= startTime && publishTime <= now
    })
  }

  // 新增关键词分类筛选逻辑
  if (filterOptions.value.selectedKeywordCategories.length > 0) {
    filteredPages.value = filteredPages.value.filter((page) => {
      // page.keywords 是一个包含关键词的 list[Keyword], Keyword 是 id: int, word: str, subject: str
      // 每个选中的关键词分类中都有许多关键词
      // 只要有 page.keywords 中的关键词在选中的关键词分类中，就保留这个 page
      const selectedKeywords = keywordCategories.value
        .filter((category) => filterOptions.value.selectedKeywordCategories.includes(category.id))
        .flatMap((category) => category.keywords)

      // 检查 page.keywords 是否有任意关键词匹配选中的关键词
      return page.keywords.some((keyword) => selectedKeywords.includes(keyword.word))
    })
  }

  if (filterOptions.value.selectedSortOption === 'score') {
    filteredPages.value.sort((a, b) => b.score - a.score)
  } else {
    filteredPages.value.sort(
      (a, b) => new Date(b.publish_time).getTime() - new Date(a.publish_time).getTime()
    )
  }
}

watch(
  () => props.pages,
  (newPages) => {
    filteredPages.value = newPages
    filterPages()
  }
)

watch(() => filterOptions.value.selectedTimeRange, filterPages)
watch(
  () => filterOptions.value.selectedSortOption,
  (newSortOption) => {
    localStorage.setItem('selectedSortOption', newSortOption)
    filterPages()
  }
)

watch(
  () => filterOptions.value.selectedCategories,
  (newCategories) => {
    localStorage.setItem('selectedCategories', JSON.stringify(newCategories))
    window.dispatchEvent(new Event('selectedCategoriesUpdated'))
  },
  { deep: true }
)

watch(
  () => filterOptions.value.selectedKeywordCategories,
  (newCategories) => {
    localStorage.setItem('selectedKeywordCategories', JSON.stringify(newCategories))
  },
  { deep: true }
)

const view = ref('card')
const options = computed(() => {
  const showSiteCard =
    route.path.includes('category') ||
    route.path.includes('daliyupdate') ||
    route.path.includes('bookmarks')
  return showSiteCard
    ? [
        { label: '网站卡片', value: 'site' },
        { label: '卡片', value: 'card' },
        { label: '标题列表', value: 'list' },
        { label: '摘要列表', value: 'excerpt' }
      ]
    : [
        { label: '卡片', value: 'card' },
        { label: '标题列表', value: 'list' },
        { label: '摘要列表', value: 'excerpt' }
      ]
})

watch(view, (newView) => {
  localStorage.setItem('viewMode', newView)
  if (
    !(
      route.path.includes('category') ||
      route.path.includes('daliyupdate') ||
      route.path.includes('bookmarks')
    )
  ) {
    localStorage.setItem('notCateView', newView)
  }
})

onMounted(() => {
  const savedView = localStorage.getItem('viewMode')
  const savedNotCateView = localStorage.getItem('notCateView')
  const savedSortOption = localStorage.getItem('selectedSortOption')
  if (savedView) view.value = savedView
  if (
    !(
      route.path.includes('category') ||
      route.path.includes('daliyupdate') ||
      route.path.includes('bookmarks')
    ) &&
    view.value === 'site'
  ) {
    view.value = savedNotCateView ? savedNotCateView : 'card'
  }
  if (savedSortOption) filterOptions.value.selectedSortOption = savedSortOption

  const storedKeywordCategories = localStorage.getItem('selectedKeywordCategories')
  if (storedKeywordCategories) {
    filterOptions.value.selectedKeywordCategories = JSON.parse(storedKeywordCategories)
  }

  const fetchCategories = async () => {
    const { data, error } = await getCategories()
    if (error) console.error('获取类别信息失败：', error)
    allCategories.value = data!
  }
  const storedCategories = localStorage.getItem('selectedCategories')
  if (storedCategories) filterOptions.value.selectedCategories = JSON.parse(storedCategories)
  fetchCategories()
})

const filterSidebarRef = ref<any>(null)
const openFilter = () => filterSidebarRef.value?.openDrawer?.()
</script>

<template>
  <el-container class="full-height">
    <FilterSidebar
      ref="filterSidebarRef"
      v-model:filterOptions="filterOptions"
      :allCategories="allCategories"
      :keywordCategories="keywordCategories"
    />
    <el-main class="full-height top-down">
      <div class="header">
        <h1>{{ props.title }}</h1>
        <el-button
          type="primary"
          @click="openFilter"
          style="margin-right: 10px; line-height: normal"
        >
          <el-icon><Filter /></el-icon>
          <span>筛选</span>
        </el-button>
        <SearchInput @update:searchQuery="searchKeyword = $event" />
        <el-segmented v-model="view" :options="options" block class="spaced-segmented" />
      </div>
      <el-scrollbar
        v-if="props.pages && props.pages.length"
        v-loading="props.loading"
        @scroll="$emit('scroll', $event)"
      >
        <div v-if="view === 'card'" class="container-grid">
          <ArticleCard v-for="page in filteredPages" :key="page.id" :page="page" />
        </div>
        <ArticleList :pages="filteredPages" :showExcerpt="false" v-else-if="view === 'list'" />
        <ArticleList :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'excerpt'" />
        <SiteArticleCard :pages="filteredPages" :showExcerpt="true" v-else-if="view === 'site'" />
      </el-scrollbar>
      <el-empty v-else :image-size="200" />
    </el-main>
    <RouterView />
  </el-container>
</template>

<style scoped>
.full-height {
  height: 100vh;
}

.container-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 20em);
  gap: 2em;
  padding: 2em;
  justify-content: center;
}

h1 {
  margin: 1em;
  font-weight: bold;
  font-size: 1.5em;
}

.top-down {
  display: grid;
  grid-template-rows: min-content 1fr;
  align-content: start;
  padding: 0;
}

.header {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 1em;
  padding-right: 2em;
  flex-wrap: wrap;
  gap: 12px;
}

.header > :first-child {
  margin-right: auto;
}

.spaced-segmented {
  margin-left: 1em;
  width: 23em;
}

.header > h1 {
  margin: 0.2em;
}

.el-scrollbar {
  height: calc(100vh - 120px);
}

.el-main {
  display: flex;
  flex-direction: column;
  padding: 0;
}
</style>
