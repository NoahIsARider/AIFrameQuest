<template>
  <div class="quiz-container">
    <el-card>
      <div class="quiz-header">
        <span>本题剩余机会：{{ maxTries - tries }}</span>
        <span v-if="answered && isCorrect" style="color: #67c23a;">答对了！</span>
        <span v-if="answered && !isCorrect" style="color: #f56c6c;">
          机会用完，正确答案：{{ abcd[question.answer] }}. {{ question.options[question.answer] }}
        </span>
      </div>
      <div class="quiz-flex">
        <div class="quiz-image">
          <el-image
            :src="question.imageUrl"
            :preview-src-list="[question.imageUrl]"
            fit="contain"
            style="max-width: 260px; border-radius: 8px; cursor: zoom-in;"
          />
        </div>
        <!-- 右侧区域：选项和AI提示并排 -->
        <div class="quiz-main-right">
          <div class="quiz-options">
            <div class="options-group">
              <div
                v-for="(option, idx) in question.options"
                :key="idx"
                class="option-box"
                :class="getOptionClass(idx)"
                @click="!answered && !disabledOptions.includes(idx) && handleAnswer(idx)"
              >
                {{ abcd[idx] }}. {{ option }}
              </div>
            </div>
            <el-button
              @click="nextQuestion"
              style="margin-top: 20px;"
              :disabled="!answered"
              v-if="answered"
            >
              下一题
            </el-button>
          </div>
          <div class="ai-hint-sidebar">
            <el-alert
              v-if="loading"
              title="AI正在思考提示，请稍候..."
              type="info"
              show-icon
            />
            <el-alert
              v-else-if="aiHint"
              :title="aiHint"
              type="info"
              show-icon
            />
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const API_BASE = 'http://localhost:5000'
const abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
const maxTries = 3

const question = ref({ imageUrl: '', options: [], answer: null })
const tries = ref(0)
const disabledOptions = ref([])
const answered = ref(false)
const isCorrect = ref(false)
const aiHint = ref('')
const correctCount = ref(0)
const loading = ref(false)
const lastWrongIdx = ref(null)

const loadQuestion = async () => {
  tries.value = 0
  disabledOptions.value = []
  answered.value = false
  isCorrect.value = false
  aiHint.value = ''
  loading.value = false
  lastWrongIdx.value = null
  const res = await axios.get(API_BASE + '/api/quiz/image-entry-8')
  question.value = {
    imageUrl: API_BASE + res.data.image_url,
    options: res.data.options,
    answer: res.data.answer
  }
}

const handleAnswer = async (idx) => {
  if (loading.value) {
    ElMessage.info('请等待AI提示返回后再作答')
    return
  }
  if (answered.value || disabledOptions.value.includes(idx)) return
  if (idx === question.value.answer) {
    answered.value = true
    isCorrect.value = true
    correctCount.value++
  } else {
    tries.value++
    disabledOptions.value.push(idx)
    lastWrongIdx.value = idx
    if (tries.value < maxTries) {
      loading.value = true
      aiHint.value = ''
      try {
        const resp = await axios.post(API_BASE + '/api/quiz/ai-hint', {
          options: question.value.options,
          selected: disabledOptions.value,
          answer: question.value.answer
        })
        aiHint.value = resp.data.hint
      } catch (e) {
        aiHint.value = 'AI提示服务暂时不可用，请稍后再试。'
      }
      loading.value = false
    } else {
      answered.value = true
      isCorrect.value = false
    }
  }
}

const nextQuestion = () => {
  if (answered.value) loadQuestion()
}

loadQuestion()

function getOptionClass(idx) {
  if (!answered.value) {
    if (disabledOptions.value.includes(idx)) {
      return lastWrongIdx.value === idx ? 'option-wrong' : 'option-disabled'
    }
    return ''
  }
  if (idx === question.value.answer) return 'option-correct'
  if (disabledOptions.value.includes(idx)) return 'option-wrong'
  return ''
}
</script>

<style scoped>
.quiz-container { max-width: 900px; margin: 40px auto; }
.quiz-header { display: flex; justify-content: space-between; margin-bottom: 18px; font-size: 16px; color: #666; }
.quiz-flex { display: flex; align-items: flex-start; gap: 40px; }
.quiz-image img, .quiz-image .el-image { max-width: 260px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); cursor: zoom-in; transition: box-shadow 0.3s; }
.quiz-image img:hover, .quiz-image .el-image:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.18); }
.quiz-main-right { display: flex; flex: 1; gap: 32px; }
.quiz-options { flex: 2; display: flex; flex-direction: column; justify-content: flex-start; }
.options-group { display: flex; flex-direction: column; gap: 16px; }
.option-box { border: 2px solid #dcdfe6; border-radius: 8px; padding: 14px 18px; font-size: 16px; cursor: pointer; background: #fff; transition: border-color 0.3s, background 0.3s, color 0.3s; user-select: none; }
.option-box:hover { border-color: #409eff; background: #f4faff; }
.option-correct { border-color: #67c23a !important; background: #f0f9eb !important; color: #67c23a !important; }
.option-wrong { border-color: #f56c6c !important; background: #fef0f0 !important; color: #f56c6c !important; }
.option-disabled { opacity: 0.6; pointer-events: none; }
.ai-hint-sidebar { flex: 1; min-width: 220px; max-width: 300px; }
</style>