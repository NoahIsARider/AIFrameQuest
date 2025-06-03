<template>
  <div class="text-search-view">
    <TextImageSearch />
  </div>
</template>

<script setup>
import TextImageSearch from '../components/TextImageSearch.vue';
</script>

<style scoped>
.text-search-view {
  /* width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
  display: block !important; 
  position: relative;
  z-index: 10; */
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
</style>