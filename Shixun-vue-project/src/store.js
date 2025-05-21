import { createStore } from 'vuex';

// 模拟 API 调用
const fetchPosts = async () => {
  return [
    {
      id: 1,
      title: '示例帖子 1',
      summary: '这是示例帖子 1 的摘要内容。',
      author: '用户 1',
      date: '2024-01-01',
      content: '这是示例帖子 1 的完整内容。'
    },
    {
      id: 2,
      title: '示例帖子 2',
      summary: '这是示例帖子 2 的摘要内容。',
      author: '用户 2',
      date: '2024-01-02',
      content: '这是示例帖子 2 的完整内容。'
    }
  ];
};

const fetchPost = async (id) => {
  const posts = await fetchPosts();
  return posts.find(post => post.id === parseInt(id));
};

const fetchComments = async (postId) => {
  return [
    {
      id: 1,
      postId: postId,
      content: '这是示例评论 1 的内容。',
      author: '评论用户 1'
    },
    {
      id: 2,
      postId: postId,
      content: '这是示例评论 2 的内容。',
      author: '评论用户 2'
    }
  ];
};

const store = createStore({
  state: {
    posts: [],
    currentPost: {},
    comments: []
  },
  mutations: {
    SET_POSTS(state, posts) {
      state.posts = posts;
    },
    SET_CURRENT_POST(state, post) {
      state.currentPost = post;
    },
    SET_COMMENTS(state, comments) {
      state.comments = comments;
    }
  },
  actions: {
    async fetchPosts({ commit }) {
      const posts = await fetchPosts();
      commit('SET_POSTS', posts);
    },
    async fetchPost({ commit }, id) {
      const post = await fetchPost(id);
      commit('SET_CURRENT_POST', post);
    },
    async fetchComments({ commit }, postId) {
      const comments = await fetchComments(postId);
      commit('SET_COMMENTS', comments);
    }
  }
});

export default store;