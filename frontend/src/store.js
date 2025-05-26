import { createStore } from 'vuex';
import axios from 'axios';

// 真实 API 调用
const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/posts');
    return response.data;
  } catch (error) {
    console.error('获取帖子列表失败:', error);
    return [];
  }
};

const fetchPost = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/posts/${id}`);
    return response.data;
  } catch (error) {
    console.error(`获取帖子 ${id} 详情失败:`, error);
    return {};
  }
};

const fetchComments = async (postId) => {
  try {
    // 获取帖子详情，其中包含评论数据
    const postDetail = await fetchPost(postId);
    
    // 从帖子详情中提取评论数据
    if (postDetail && postDetail.comments) {
      // 将评论数据转换为前端需要的格式
      return postDetail.comments.map((comment, index) => ({
        id: index + 1,
        postId: parseInt(postId),
        content: comment.text,
        author: comment.name,
        rating: comment.rating,
        date: comment.date
      }));
    }
    return [];
  } catch (error) {
    console.error(`获取帖子 ${postId} 评论失败:`, error);
    return [];
  }
};

// 添加获取词条图片的方法
async function fetchPostImages(postId) {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/posts/${postId}/images`);
    return response.data;
  } catch (error) {
    console.error(`获取帖子 ${postId} 图片失败:`, error);
    return [];
  }
};

// 在store中添加相关状态和actions
const store = createStore({
  state: {
    posts: [],
    currentPost: {},
    comments: [],
    postImages: [], // 新增：存储当前帖子的图片
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || '',
    // 搜索结果相关状态
    searchResults: [],
    uploadedImage: '',
    searchQuery: ''
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
    },
    SET_POST_IMAGES(state, images) {
      state.postImages = images;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    SET_USERNAME(state, username) {
      state.username = username;
      localStorage.setItem('username', username);
    },
    // 搜索结果相关mutations
    SET_SEARCH_RESULTS(state, results) {
      state.searchResults = results;
    },
    SET_UPLOADED_IMAGE(state, image) {
      state.uploadedImage = image;
    },
    SET_SEARCH_QUERY(state, query) {
      state.searchQuery = query;
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
    },
    async fetchPostImages({ commit }, postId) {
      const images = await fetchPostImages(postId);
      commit('SET_POST_IMAGES', images);
    },
    async addComment({ commit }, { postId, comment }) {
      try {
        // 发送评论到后端API
        const response = await axios.post(`http://127.0.0.1:5000/api/posts/${postId}/comments`, {
          name: comment.name,
          text: comment.text,
          rating: comment.rating,
          date: comment.date
        });
        
        // 返回后端响应数据
        return response.data;
      } catch (error) {
        console.error('添加评论失败:', error);
        throw error;
      }
    }
  }
});

export default store;