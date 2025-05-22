<template>
  <el-container class="result-container">
    <el-header class="header">相似图片搜索结果</el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="12">
          <h3>查询图片</h3>
          <el-image :src="queryImage" class="query-img" fit="contain"></el-image>
        </el-col>
        <el-col :span="12">
          <h3>相似图片（前10）</h3>
          <el-row :gutter="10">
            <el-col :span="8" v-for="(img, index) in similarImages" :key="index">
              <el-image :src="img" class="similar-img" fit="cover"></el-image>
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const queryImage = ref('')
const similarImages = ref([])

const route = useRoute()
const resultData = JSON.parse(route.query.result)

onMounted(() => {
  // 拼接查询图片的后端接口地址
  queryImage.value = `/api/static/uploads/${resultData.query_image}`
  // 拼接前10相似图片的后端接口地址（假设results数组按相似度排序）
  similarImages.value = resultData.results.slice(0, 10).map(item => `/api/images/${item.image}`)
})
</script>

<style scoped>
.result-container {
  min-height: 100vh;
  background: #f5f7fa;
}
.header {
  font-size: 24px;
  color: #2c3e50;
  line-height: 60px;
  border-bottom: 1px solid #e4e7ed;
}
.query-img {
  width: 100%;
  max-height: 1000px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
.similar-img {
  width: 100%;
  height: 150px;
  border-radius: 4px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.1);
}
</style>