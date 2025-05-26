<template>
  <el-container class="result-page">
    <el-main>
      <el-row :gutter="20">
        <!-- 左侧：图片和识别结果 -->
        <el-col :span="8">
          <el-card class="img-card">
            <div class="section-title">搜索图片</div>
            <el-image
              style="width: 100%; max-width: 300px; max-height: 400px; border-radius: 10px; object-fit: contain;"
              :src="imgUrl"
              :preview-src-list="[uploadedImage]"
              fit="cover"
              preview-teleported
            />
            <div class="img-desc">来自 {{ imgDesc }}</div>
          </el-card>
          <el-card class="result-card" style="margin-top: 20px;">
            <div class="section-title">搜索结果</div>
            <div v-for="(item, index) in resultList" :key="index" class="result-item">
              <el-image 
                :src="isSearchResult(item) ? getImageUrl(item.image) : item.cover" 
                style="width: 60px; height: 80px; border-radius: 6px; margin-right: 12px; cursor: pointer;" 
                @click="selectEntry(item)"
              />
              <div class="result-info">
                <!-- 如果是搜索结果，显示词条信息 -->
                <template v-if="isSearchResult(item) && item.entry_info">
                  <div class="result-title">{{ item.entry_info.title }}</div>
                  <div>类型：{{ item.entry_info.type }}</div>
                  <div>描述：{{ item.entry_info.description }}</div>
                  <div>距离：{{ (item.distance).toFixed(2) }}</div>
                  <el-button 
                    type="primary" 
                    size="small" 
                    style="margin-top: 5px;"
                    @click="viewEntryDetail(item.entry_info.entry_id)"
                  >
                    查看词条
                  </el-button>
                </template>
                <!-- 如果是默认数据，显示原有信息 -->
                <template v-else>
                  <div class="result-title">{{ item.title }}</div>
                  <div>导演：{{ item.director }}</div>
                  <div>主演：{{ item.actors }}</div>
                  <div>类型：{{ item.type }}</div>
                  <div>上映时间：{{ item.date }}</div>
                </template>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：评分和评论 -->
        <el-col :span="16">
          <!-- 如果选中了搜索结果，显示大图 -->
          <el-card v-if="selectedEntry && entryDetail" class="selected-entry-card" style="margin-bottom: 20px;">
            <div class="section-title">{{ entryDetail.title }}</div>
            <el-image
              :src="getImageUrl(selectedEntry.image)"
              style="width: 100%; max-width: 400px; max-height: 300px; border-radius: 10px; object-fit: contain; margin-bottom: 15px;"
              fit="cover"
              :preview-src-list="[getImageUrl(selectedEntry.image)]"
              preview-teleported
            />
            <div class="entry-details">
              <p><strong>类型：</strong>{{ entryDetail.type }}</p>
              <p><strong>描述：</strong>{{ entryDetail.description && entryDetail.description.length > 0 ? entryDetail.description.join(' ') : '暂无描述' }}</p>
            </div>
          </el-card>
          
          <el-card class="score-card" v-loading="loading">
            <div class="score-header">
              <span class="score">{{ currentScore }}</span>
              <el-rate v-model="currentScore" disabled show-score :max="10" />
              <span class="score-people">({{ currentScorePeople }} 人评分)</span>
            </div>

          </el-card>
          <el-card class="comment-card" style="margin-top: 20px;" v-loading="loading">
            <div class="section-title">讨论区</div>
            <div v-for="comment in currentComments" :key="comment.id" class="comment-item">
              <el-avatar :src="comment.avatar" size="small" style="margin-right: 8px;">
                <span v-if="!comment.avatar">{{ comment.author[0] }}</span>
              </el-avatar>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="author">{{ comment.author }}</span>
                  <span class="date">{{ comment.date }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
                <div class="comment-footer">
                  <el-icon class="like-icon"><Star /></el-icon>
                  <span class="like-count">{{ comment.likes }}</span>
                  <el-link type="primary" :underline="false" style="margin-left: 16px;">回复</el-link>
                </div>
              </div>
            </div>
            <el-pagination
              background
              layout="prev, pager, next"
              :total="currentComments.length * 2"
              :page-size="3"
              style="margin-top: 16px; text-align: right;"
            />
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import imageUrl from '@/assets/images/image.png'
import image1Url from '@/assets/images/image1.png'
import image2Url from '@/assets/images/image2.png'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()

// 从store获取搜索结果
const searchResults = computed(() => store.state.searchResults)
const uploadedImage = computed(() => store.state.uploadedImage)
const searchQuery = computed(() => store.state.searchQuery)

// 如果没有搜索结果，使用默认数据
const imgUrl = computed(() => uploadedImage.value || imageUrl)
const imgDesc = computed(() => searchQuery.value || '流浪地球2 01:23:45')
const resultList = computed(() => {
  if (searchResults.value && searchResults.value.length > 0) {
    return searchResults.value
  }
  // 默认数据
  return [
    {
      cover: image1Url,
      title: '流浪地球 2',
      director: '郭帆',
      actors: '吴京、刘德华、李雪健',
      type: '科幻 / 冒险 / 灾难',
      date: '2023-01-22'
    },
    {
      cover: image2Url,
      title: '流浪地球',
      director: '郭帆',
      actors: '吴京、屈楚萧、李光洁',
      type: '科幻 / 冒险 / 灾难',
      date: '2019-02-05'
    }
  ]
})
// 选中的词条
const selectedEntry = ref(null)
// 词条详情数据
const entryDetail = ref(null)
// 加载状态
const loading = ref(false)

// 默认评分数据（当没有搜索结果时使用）
const defaultScore = ref(9.2)
const defaultScorePeople = ref('12,345')

const defaultComments = ref([
  {
    id: 1,
    author: '赵志远',
    avatar: '',
    date: '2023-12-15',
    content: '电影的视觉效果令人震撼，特别是月球发动机启动的场景，将科幻与现实完美结合。剧情设定新颖，让人深思。',
    likes: 2345
  },
  {
    id: 2,
    author: '林雨晴',
    avatar: 'https://img2.example.com/avatar1.jpg',
    date: '2023-12-14',
    content: '作为科幻迷，这部电影的细节处理让我惊叹。每个场景都经过精心设计，特效制作精良，剧情紧凑。期待导演的下一部作品。',
    likes: 1876
  },
  {
    id: 3,
    author: '王建国',
    avatar: '',
    date: '2023-12-13',
    content: '这部电影展现了中国科幻电影的实力，无论是特效还是故事情节都达到了国际水准。尤其是太空站爆炸的场景，震撼人心。',
    likes: 1234
  }
])

// 获取词条详情的API函数
const fetchEntryDetail = async (entryId) => {
  try {
    console.log('Fetching entry detail for ID:', entryId)
    loading.value = true
    const response = await fetch(`http://127.0.0.1:5000/api/posts/${entryId}`)
    if (response.ok) {
      const data = await response.json()
      console.log('Entry detail fetched:', data)
      entryDetail.value = data
      return data
    } else {
      console.error('获取词条详情失败:', response.statusText)
      return null
    }
  } catch (error) {
    console.error('获取词条详情时出错:', error)
    return null
  } finally {
    loading.value = false
  }
}



// 计算属性：当前显示的评分和评论
const currentScore = computed(() => {
  if (entryDetail.value && entryDetail.value.avg_rating) {
    return entryDetail.value.avg_rating
  }
  return defaultScore.value
})

const currentScorePeople = computed(() => {
  if (entryDetail.value && entryDetail.value.rating_count) {
    return entryDetail.value.rating_count.toLocaleString()
  }
  return defaultScorePeople.value
})



const currentComments = computed(() => {
  if (entryDetail.value && entryDetail.value.comments) {
    return entryDetail.value.comments.map((comment, index) => ({
      id: index + 1,
      author: comment.name,
      avatar: '',
      date: comment.date,
      content: comment.text,
      likes: Math.floor(Math.random() * 500 + 50) // 暂时使用随机点赞数
    }))
  }
  return defaultComments.value
})

// 选择词条
const selectEntry = async (item) => {
  console.log('selectEntry called with:', item)
  if (isSearchResult(item) && item.entry_info) {
    console.log('Selecting search result:', item.entry_info.entry_id)
    selectedEntry.value = item
    // 获取词条详情
    await fetchEntryDetail(item.entry_info.entry_id)
  } else {
    console.log('Clearing selection')
    // 如果点击的是默认数据，清除选中状态
    selectedEntry.value = null
    entryDetail.value = null
  }
}

// 页面初始化时，如果有搜索结果，默认选择最相似的（第一个）
const initializeDefaultSelection = async () => {
  console.log('Initializing default selection, searchResults:', searchResults.value)
  if (searchResults.value && searchResults.value.length > 0) {
    const mostSimilar = searchResults.value[0]
    console.log('Most similar item:', mostSimilar)
    if (mostSimilar.entry_info) {
      console.log('Selecting most similar entry:', mostSimilar.entry_info.entry_id)
      selectedEntry.value = mostSimilar
      await fetchEntryDetail(mostSimilar.entry_info.entry_id)
    } else {
      console.log('No entry_info found in most similar item')
    }
  } else {
    console.log('No search results available, using default data')
    // 清除选中状态，使用默认数据
    selectedEntry.value = null
    entryDetail.value = null
  }
}

// 辅助函数
// 判断是否为搜索结果
const isSearchResult = (item) => {
  return item.hasOwnProperty('distance') && item.hasOwnProperty('image')
}

// 获取图片URL
const getImageUrl = (imageName) => {
  return `http://127.0.0.1:5000/images/${imageName}`
}

// 查看词条详情
const viewEntryDetail = (entryId) => {
  if (!entryId) return
  router.push(`/post/${entryId}`)
}

// 页面加载时初始化
onMounted(() => {
  initializeDefaultSelection()
})

// 监听搜索结果变化，自动选择最相似的结果
watch(searchResults, () => {
  initializeDefaultSelection()
}, { immediate: true })
</script>

<style scoped>
.result-page {
  background: #f7f8fa;
  min-height: 100vh;
}
.section-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 12px;
}
.img-card, .result-card, .score-card, .comment-card {
  border-radius: 12px;
  margin-bottom: 16px;
}
.img-desc {
  color: #888;
  font-size: 0.95em;
  margin-top: 8px;
}
.result-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}
.result-info {
  flex: 1;
}
.result-title {
  font-weight: bold;
  font-size: 1.05em;
  margin-bottom: 4px;
}
.score-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  margin-bottom: 12px;
}
.score {
  color: #409eff;
  font-size: 2.2rem;
  font-weight: bold;
}
.score-people {
  color: #888;
  font-size: 1rem;
}
.comment-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 18px;
}
.comment-content {
  flex: 1;
}
.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: bold;
  margin-bottom: 4px;
}
.comment-text {
  margin-bottom: 6px;
}
.comment-footer {
  color: #888;
  font-size: 0.95em;
  display: flex;
  align-items: center;
  gap: 8px;
}
.like-icon {
  cursor: pointer;
  transition: color 0.3s;
}
.like-icon:hover {
  color: #409eff;
}
.like-count {
  margin-left: 4px;
}
.selected-entry-card {
  border: 2px solid #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}
.entry-details {
  color: #666;
  line-height: 1.6;
}
.entry-details p {
  margin: 8px 0;
}
.result-item:hover {
  background-color: #f5f7fa;
  border-radius: 8px;
  transition: background-color 0.3s;
}
</style>

