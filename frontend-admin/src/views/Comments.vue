<template>
  <div class="comments-container">
    <div class="page-header">
      <div class="sentiment-buttons">
        <el-button-group>
          <el-button type="primary" @click="analyzeSentiment('snownlp')" :loading="analyzing.snownlp">SnowNLP 情感分析</el-button>
          <el-button type="warning" @click="analyzeSentiment('bert')" :loading="analyzing.bert">BERT 情感分析</el-button>
          <el-button type="success" @click="analyzeSentiment('ai_moderation')" :loading="analyzing.ai_moderation">AI 审核评论</el-button>
        </el-button-group>
      </div>
    </div>

    <el-form :inline="true" class="filter-form">
      <el-form-item label="词条筛选">
        <el-select v-model="filterEntry" placeholder="选择词条" clearable style="width: 300px;">
          <el-option
            v-for="entry in entriesList"
            :key="entry.key"
            :label="entry.title"
            :value="entry.key">
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <div v-loading="loading">
      <el-empty v-if="filteredComments.length === 0" description="暂无评论"></el-empty>
      <el-table v-else :data="filteredComments" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="entryTitle" label="所属词条" width="150" />
        <el-table-column prop="name" label="用户名" width="120" />
        <el-table-column prop="text" label="评论内容" />
        <el-table-column label="情感分析" width="200">
          <template #default="scope">
            <div v-if="scope.row.sentiment">
              <div v-if="scope.row.sentiment.method === 'snownlp' || scope.row.sentiment.method === 'bert'">
                <el-progress 
                  :percentage="Math.round(scope.row.sentiment.score * 100)" 
                  :status="scope.row.sentiment.score >= 0.6 ? 'success' : scope.row.sentiment.score >= 0.4 ? 'warning' : 'exception'"
                  :format="() => scope.row.sentiment.score.toFixed(2)"
                />
                <div class="sentiment-label">{{ scope.row.sentiment.label || getSentimentLabel(scope.row.sentiment.score) }}</div>
              </div>
              <div v-else-if="scope.row.sentiment.method === 'baidu'">
                <div v-if="scope.row.sentiment.items && scope.row.sentiment.items.length > 0">
                  <el-progress 
                    :percentage="Math.round(scope.row.sentiment.items[0].positive_prob * 100)" 
                    :status="scope.row.sentiment.items[0].sentiment === 2 ? 'success' : scope.row.sentiment.items[0].sentiment === 1 ? 'warning' : 'exception'"
                    :format="() => scope.row.sentiment.items[0].positive_prob.toFixed(2)"
                  />
                  <div class="sentiment-label">{{ getBaiduSentimentLabel(scope.row.sentiment.items[0].sentiment) }}</div>
                </div>
                <div v-else>分析失败</div>
              </div>
            </div>
            <span v-else>未分析</span>
          </template>
        </el-table-column>
        <el-table-column label="AI审核" width="200">
          <template #default="scope">
            <div v-if="scope.row.ai_moderation">
              <div v-if="!scope.row.ai_moderation.error">
                <el-tag 
                  :type="scope.row.ai_moderation.content_analysis && scope.row.ai_moderation.content_analysis.is_appropriate ? 'success' : 'danger'"
                  effect="dark"
                >
                  {{ scope.row.ai_moderation.content_analysis && scope.row.ai_moderation.content_analysis.is_appropriate ? '通过' : '不通过' }}
                </el-tag>
                <el-popover
                  placement="top"
                  width="300"
                  trigger="hover"
                >
                  <template #reference>
                    <el-button type="text">查看详情</el-button>
                  </template>
                  <template #default>
                    <div v-if="scope.row.ai_moderation.content_analysis">
                      <p><strong>审核结果:</strong> {{ scope.row.ai_moderation.content_analysis.is_appropriate ? '通过' : '不通过' }}</p>
                      <p v-if="scope.row.ai_moderation.content_analysis.issues && scope.row.ai_moderation.content_analysis.issues.length">
                        <strong>存在问题:</strong>
                        <el-tag 
                          v-for="(issue, index) in scope.row.ai_moderation.content_analysis.issues" 
                          :key="index"
                          type="danger"
                          effect="plain"
                          style="margin: 2px"
                        >
                          {{ issue }}
                        </el-tag>
                      </p>
                      <p><strong>解释:</strong> {{ scope.row.ai_moderation.content_analysis.explanation }}</p>
                      <p><strong>建议:</strong> {{ scope.row.ai_moderation.content_analysis.recommendation }}</p>
                    </div>
                    <div v-else-if="scope.row.ai_moderation.moderation">
                      <p><strong>审核结果:</strong> {{ scope.row.ai_moderation.moderation.flagged ? '不通过' : '通过' }}</p>
                      <div v-if="scope.row.ai_moderation.moderation.flagged">
                        <p><strong>违规类别:</strong></p>
                        <div v-for="(value, key) in scope.row.ai_moderation.moderation.categories" :key="key">
                          <el-tag 
                            v-if="value"
                            type="danger"
                            effect="plain"
                            style="margin: 2px"
                          >
                            {{ key }}
                          </el-tag>
                        </div>
                      </div>
                    </div>
                  </template>
                </el-popover>
              </div>
              <div v-else>
                <el-tag type="info">分析失败</el-tag>
              </div>
            </div>
            <span v-else>未审核</span>
          </template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="200">
          <template #default="scope">
            <el-rate
              :model-value="scope.row.rating / 2"
              :max="5"
              disabled
              text-color="#ff9900"
              show-score
              :score-template="`${scope.row.rating}/10`">
            </el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="评论时间" width="180" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              @click="deleteComment(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'CommentsView',
  setup() {
    const loading = ref(false)
    const commentsList = ref([])
    const entriesList = ref([])
    const filterEntry = ref('')
    const analyzing = ref({
      snownlp: false,
      bert: false,
      baidu: false,
      ai_moderation: false
    })
    
    const filteredComments = computed(() => {
      if (!filterEntry.value) {
        return commentsList.value
      }
      return commentsList.value.filter(comment => comment.entryKey === filterEntry.value)
    })
    
    // 获取所有评论
    const fetchComments = async () => {
      try {
        loading.value = true
        const response = await axios.get('/api/admin/comments')
        // 将后端返回的post_title映射为前端需要的entryTitle
        commentsList.value = response.data.comments.map(comment => ({
          ...comment,
          entryTitle: comment.post_title,
          entryKey: `entry${comment.post_id}`
        }))
        console.log('获取到的评论:', commentsList.value)
      } catch (error) {
        console.error('获取评论失败:', error)
        ElMessage.error('获取评论失败')
      } finally {
        loading.value = false
      }
    }
    
    // 获取所有词条
    const fetchEntries = async () => {
      try {
        const response = await axios.get('/api/admin/entries')
        const entries = response.data.entries
        
        // 转换为数组格式
        entriesList.value = Object.entries(entries).map(([key, entry]) => {
          return {
            key,
            ...entry
          }
        })
      } catch (error) {
        console.error('获取词条失败:', error)
        ElMessage.error('获取词条失败')
      }
    }
    
    // 删除评论
    const deleteComment = (comment) => {
      ElMessageBox.confirm(`确定要删除用户「${comment.name}」的评论吗?`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await axios.delete(`/api/admin/comments/${comment.id}?entry_key=${comment.entryKey}`)
          ElMessage.success('删除成功')
          fetchComments()
        } catch (error) {
          console.error('删除评论失败:', error)
          ElMessage.error('删除评论失败')
        }
      }).catch(() => {})
    }
    
    onMounted(async () => {
      await fetchEntries()
      fetchComments()
    })
    
    // 情感分析
    const analyzeSentiment = async (method) => {
      try {
        analyzing.value[method] = true
        const response = await axios.get(`/api/admin/analyze/comments/${method}`)
        
        if (response.data.status === 'success') {
          // 将分析结果添加到评论列表中
          if (method === 'ai_moderation') {
            // AI审核返回results数组
            const results = response.data.results
            commentsList.value = commentsList.value.map(comment => {
              const result = results.find(r => r.id === comment.id)
              if (result) {
                return {
                  ...comment,
                  ai_moderation: result
                }
              }
              return comment
            })
          } else {
            // SnowNLP和BERT返回comments数组
            const analyzedComments = response.data.comments
            commentsList.value = commentsList.value.map(comment => {
              const analyzedComment = analyzedComments.find(c => c.id === comment.id)
              if (analyzedComment) {
                return {
                  ...comment,
                  sentiment: {
                    score: analyzedComment.sentiment_score,
                    label: analyzedComment.sentiment,
                    method
                  }
                }
              }
              return comment
            })
          }
          ElMessage.success(`${method === 'ai_moderation' ? 'AI审核' : method.toUpperCase() + ' 情感分析'}完成`)
        } else {
          throw new Error(response.data.message || '分析失败')
        }
      } catch (error) {
        console.error(`${method} 分析失败:`, error)
        ElMessage.error(`分析失败: ${error.message || '未知错误'}`)
      } finally {
        analyzing.value[method] = false
      }
    }
    
    // 获取情感标签
    const getSentimentLabel = (score) => {
      if (score >= 0.7) return '积极'
      if (score >= 0.4) return '中性'
      return '消极'
    }
    
    // 获取百度情感标签
    const getBaiduSentimentLabel = (sentiment) => {
      switch (sentiment) {
        case 2: return '积极'
        case 1: return '中性'
        case 0: return '消极'
        default: return '未知'
      }
    }
    
    return {
      loading,
      commentsList,
      entriesList,
      filterEntry,
      filteredComments,
      deleteComment,
      analyzing,
      analyzeSentiment,
      getSentimentLabel,
      getBaiduSentimentLabel
    }
  }
}
</script>

<style scoped>
.comments-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 20px;
}

.analysis-buttons {
  display: flex;
  gap: 10px;
}

.sentiment-label {
  text-align: center;
  margin-top: 5px;
  font-size: 12px;
  font-weight: bold;
}
</style>