<template>
  <div class="post-detail">
    <h2>{{ post.title }}</h2>
    <div class="post-meta">
      <span>{{ post.author }}</span>
      <span>{{ post.date }}</span>
    </div>
    <div class="post-content">
      {{ post.content }}
    </div>
    <div class="comments">
      <h3>评论</h3>
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <p>{{ comment.content }}</p>
        <span>{{ comment.author }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const route = useRoute();
const store = useStore();
const post = ref({});
const comments = ref([]);

onMounted(async () => {
  await store.dispatch('fetchPost', route.params.id);
  post.value = store.state.currentPost;
  await store.dispatch('fetchComments', route.params.id);
  comments.value = store.state.comments;
});
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
}

.post-meta {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 20px;
}

.post-content {
  margin-bottom: 30px;
}

.comments {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 10px 0;
}
</style>