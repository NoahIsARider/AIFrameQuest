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
              fit="cover"
            />
            <div class="img-desc">来自 {{ imgDesc }}</div>
          </el-card>
          <el-card class="result-card" style="margin-top: 20px;">
            <div class="section-title">搜索结果</div>
            <div v-for="item in resultList" :key="item.title" class="result-item">
              <el-image :src="item.cover" style="width: 60px; height: 80px; border-radius: 6px; margin-right: 12px;" />
              <div class="result-info">
                <div class="result-title">{{ item.title }}</div>
                <div>导演：{{ item.director }}</div>
                <div>主演：{{ item.actors }}</div>
                <div>类型：{{ item.type }}</div>
                <div>上映时间：{{ item.date }}</div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：评分和评论 -->
        <el-col :span="16">
          <el-card class="score-card">
            <div class="score-header">
              <span class="score">{{ score }}</span>
              <el-rate v-model="score" disabled show-score :max="10" />
              <span class="score-people">({{ scorePeople }} 人评分)</span>
            </div>
            <el-progress
              v-for="item in starList"
              :key="item.star"
              :percentage="item.percent"
              :text-inside="true"
              :stroke-width="18"
              style="margin: 8px 0"
            >
              <template #default>
                <span>{{ item.star }}星</span>
              </template>
            </el-progress>
          </el-card>
          <el-card class="comment-card" style="margin-top: 20px;">
            <div class="section-title">讨论区</div>
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
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
              :total="comments.length * 2"
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
import { ref } from 'vue'
import imageUrl from '@/assets/images/image.png'
import image1Url from '@/assets/images/image1.png'
import image2Url from '@/assets/images/image2.png'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const imgUrl = ref(imageUrl)
const imgDesc = ref('流浪地球2 01:23:45')
const resultList = ref([
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
])
const score = ref(9.2)
const scorePeople = ref('12,345')
const starList = ref([
  { star: 5, percent: 70 },
  { star: 4, percent: 15 },
  { star: 3, percent: 8 },
  { star: 2, percent: 5 },
  { star: 1, percent: 2 }
])
const comments = ref([
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
</style>

