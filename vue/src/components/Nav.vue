<template>
  <nav>
    <ul>
      <li><router-link to="/">首页</router-link></li>
      <li><router-link to="/hot">热门</router-link></li>
      <li><router-link to="/my">我的</router-link></li>
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