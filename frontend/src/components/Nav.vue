<template>
  <nav>
    <ul>
      <li><router-link to="/home">首页</router-link></li>
      <li><router-link to="/hot">词条</router-link></li>
      <li><router-link to="/my">以图搜图</router-link></li>
      <li><router-link to="/text-search">文字搜图</router-link></li>
      <li><router-link to="/rank">排行榜</router-link></li>
      <li><router-link to="/version-plan">版本计划</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
nav ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  justify-content: center;
}

nav li {
  margin: 0 10px;
}

nav a {
  text-decoration: none;
  color: #2c3e50;
}

nav a:hover {
  text-decoration: underline;
}
</style>