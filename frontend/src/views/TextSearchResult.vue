<template>
  <el-container class="text-result-page">
    <el-main>
      <el-row :gutter="20">
        <!-- 左侧：搜索信息和结果列表 -->
        <el-col :span="6">
          <el-card class="search-info-card">
            <div class="section-title">搜索信息</div>
            <div class="search-query">
              <div class="query-label">搜索文本：</div>
              <div class="query-text">{{ searchQuery }}</div>
            </div>
          </el-card>
          <el-card class="result-card" style="margin-top: 20px;">
            <div class="section-title">搜索结果</div>
            <div v-for="(item, index) in resultList" :key="index" class="result-item">
              <el-image 
                :src="getImageUrl(item.image)" 
                style="width: 60px; height: 80px; border-radius: 6px; margin-right: 12px; cursor: pointer;" 
                @click="selectEntry(item)"
              />
              <div class="result-info">
                <!-- 显示词条信息 -->
                <template v-if="item.entry_info">
                  <div class="result-title">{{ item.entry_info.title || '未命名' }}</div>
                  <div v-if="item.entry_info.type">类型：{{ item.entry_info.type }}</div>
                  <div v-if="item.entry_info.description">描述：{{ item.entry_info.description }}</div>
                </template>
                <!-- 如果没有词条信息，只显示图片信息 -->
                <template v-else>
                  <div class="result-title">图片 {{ index + 1 }}</div>
                </template>
                <div class="similarity-info">
                  <span>相似度：</span>
                  <span :style="{ color: getSimilarityColor(getSimilarityLevel(item.similarity)) }">
                    {{ getSimilarityLevel(item.similarity) }}
                  </span>
                </div>
                <el-button 
                  v-if="item.entry_info && item.entry_info.entry_id" 
                  type="primary" 
                  size="small" 
                  style="margin-top: 5px;"
                  @click="viewEntryDetail(item.entry_info.entry_id)"
                >
                  查看词条
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：选中图片详情 -->
        <el-col :span="18">
          <!-- 如果选中了搜索结果，显示大图 -->
          <el-card v-if="selectedEntry" class="selected-entry-card" style="margin-bottom: 20px;">
            <div class="section-title">
              {{ selectedEntry.entry_info ? selectedEntry.entry_info.title || '未命名' : '选中图片' }}
            </div>
            <div class="large-image-container">
              <el-image
                :src="getImageUrl(selectedEntry.image)"
                style="width: 100%; max-width: 600px; max-height: 400px; border-radius: 10px; object-fit: contain;"
                fit="cover"
                :preview-src-list="[getImageUrl(selectedEntry.image)]"
                preview-teleported
              />
            </div>
            <div v-if="selectedEntry.entry_info" class="entry-details">
              <p v-if="selectedEntry.entry_info.type"><strong>类型：</strong>{{ selectedEntry.entry_info.type }}</p>
              <p v-if="selectedEntry.entry_info.description"><strong>描述：</strong>{{ selectedEntry.entry_info.description }}</p>
              <p><strong>相似度分数：</strong>{{ selectedEntry.similarity.toFixed(4) }}</p>
            </div>
          </el-card>
          
          <!-- 如果没有选中结果，显示提示信息 -->
          <el-card v-else class="no-selection-card">
            <div class="no-selection-message">
              <el-icon><InfoFilled /></el-icon>
              <span>请从左侧选择一个搜索结果查看详情</span>
            </div>
          </el-card>

          <!-- 相似度等级说明 -->
          <el-card class="similarity-legend-card">
            <div class="similarity-legend-title">相似度等级说明</div>
            <ul class="similarity-legend-list">
              <li><span class="legend-level" style="color:#67C23A;">A</span>：相似度 ≥ 0.3（高度相似）</li>
              <li><span class="legend-level" style="color:#409EFF;">B</span>：0.2 ≤ 相似度 < 0.3（较高相似）</li>
              <li><span class="legend-level" style="color:#E6A23C;">C</span>：0.1 ≤ 相似度 < 0.2（一般相似）</li>
              <li><span class="legend-level" style="color:#F56C6C;">D</span>：相似度 < 0.1（低相似）</li>
            </ul>
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
import { InfoFilled } from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()

// 从store获取搜索结果
const searchResults = computed(() => store.state.searchResults)
const searchQuery = computed(() => store.state.searchQuery)

// 搜索结果列表
const resultList = computed(() => {
  if (searchResults.value && searchResults.value.length > 0) {
    return searchResults.value
  }
  return []
})

// 选中的词条
const selectedEntry = ref(null)

// 获取图片URL
const getImageUrl = (imageName) => {
  return `http://127.0.0.1:5000/images/${imageName}`
}

// 选择词条
const selectEntry = (item) => {
  console.log('选择图片:', item)
  selectedEntry.value = item
}

// 查看词条详情
const viewEntryDetail = (entryId) => {
  if (!entryId) return
  router.push(`/post/${entryId}`)
}

// 页面初始化时，如果有搜索结果，默认选择第一个
const initializeDefaultSelection = () => {
  console.log('初始化默认选择, 搜索结果:', searchResults.value)
  if (searchResults.value && searchResults.value.length > 0) {
    const firstResult = searchResults.value[0]
    console.log('选择第一个结果:', firstResult)
    selectedEntry.value = firstResult
  } else {
    console.log('没有搜索结果可用')
    selectedEntry.value = null
  }
}

// 计算相似度等级 - 针对文字搜图的相似度范围调整
const getSimilarityLevel = (similarity) => {
  if (similarity >= 0.3) return 'A'
  if (similarity >= 0.2) return 'B'
  if (similarity >= 0.1) return 'C'
  return 'D'
}

// 获取相似度等级对应的颜色
const getSimilarityColor = (level) => {
  switch (level) {
    case 'A': return '#67C23A'  // 绿色
    case 'B': return '#409EFF'  // 蓝色
    case 'C': return '#E6A23C'  // 橙色
    case 'D': return '#F56C6C'  // 红色
    default: return '#909399'   // 灰色
  }
}

// 页面加载时初始化
onMounted(() => {
  initializeDefaultSelection()
})

// 监听搜索结果变化，自动选择第一个结果
watch(searchResults, () => {
  initializeDefaultSelection()
}, { immediate: true })
</script>

<style scoped>
.text-result-page {
  background: #f7f8fa;
  min-height: 100vh;
}
.section-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 12px;
}
.search-info-card, .result-card, .selected-entry-card, .no-selection-card, .similarity-legend-card {
  border-radius: 12px;
  margin-bottom: 16px;
  padding: 20px;
}
.search-query {
  margin: 15px 0;
}
.query-label {
  font-weight: bold;
  margin-bottom: 8px;
  color: #606266;
}
.query-text {
  font-size: 1.2rem;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 6px;
  border-left: 4px solid #409EFF;
}
.result-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  padding: 10px;
  border-radius: 8px;
  transition: background-color 0.3s;
}
.result-item:hover {
  background-color: #f5f7fa;
}
.result-info {
  flex: 1;
}
.result-title {
  font-weight: bold;
  font-size: 1.05em;
  margin-bottom: 4px;
}
.similarity-info {
  margin: 8px 0;
  font-size: 0.95em;
  font-weight: 500;
}
.large-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
  min-height: 400px;
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
}
.entry-details {
  color: #666;
  line-height: 1.6;
  margin-top: 20px;
  padding: 0 20px;
}
.entry-details p {
  margin: 12px 0;
}
.no-selection-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #909399;
  font-size: 1.1rem;
}
.no-selection-message .el-icon {
  font-size: 2rem;
  margin-bottom: 16px;
  color: #E6A23C;
}
.similarity-legend-title {
  font-weight: bold;
  margin-bottom: 10px;
}
.similarity-legend-list {
  padding-left: 20px;
  margin: 0;
}
.similarity-legend-list li {
  margin-bottom: 8px;
}
.legend-level {
  font-weight: bold;
  margin-right: 5px;
}
</style>