<template>
  <div class="my-page">
    
    <div class="upload-container">
      <PhotoUploader />
    </div>
  </div>
</template>

<script setup>
import PhotoUploader from '../components/PhotoUploader.vue';
</script>

<style scoped>
.my-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.upload-container {
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}
</style>