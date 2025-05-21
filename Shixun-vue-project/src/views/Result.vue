<template>
  <el-container class="result-page">
    <el-main>
      <el-row :gutter="20">
        <!-- 图片展示区域 -->
        <el-col :span="24">
          <el-card class="img-card">
            <div class="section-title">搜索图片</div>
            <el-image
              style="width: 100%; max-width: 800px; max-height: 600px; border-radius: 10px; object-fit: contain; margin: 0 auto; display: block;"
              :src="imgUrl"
              fit="cover"
            />
            <div class="img-desc" style="text-align: center; margin-top: 16px;">来自 {{ imgDesc }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import imageUrl from '@/assets/images/image.png'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const route = useRoute()
const resultData = ref(JSON.parse(route.query.result || '{}'))

const imgUrl = ref(resultData.value.results?.[0]?.image || '') // 使用后端返回的image字段
const imgDesc = ref(resultData.value.imgDesc) // 直接使用后端返回的图片描述

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

</style>

