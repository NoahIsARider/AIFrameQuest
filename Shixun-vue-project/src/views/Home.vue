<template>
  <div class="home">
    <div class="content">
      <h1>欢迎来到首页</h1>
      <div class="content-body">
        <p>这里是首页内容</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Nav from '../components/Nav.vue'
</script>

<style scoped>
.home {
  width: 100%;
}

.content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

h1 {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #2c3e50;
}

.content-body {
  padding: 20px 0;
}
</style>