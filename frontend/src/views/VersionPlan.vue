<template>
  <div class="version-plan">
    <h1>AIFrameQuest 版本发布计划书</h1>
    
    <section class="section">
      <h2>项目主旨</h2>
      <p>在数字时代，我们被海量拟像（数字图像、虚拟存在）包围。虎扑评分将社会抽象为彻底的景观，符号成为唯一的货币；豆瓣是恢复主体性的挣扎，但是后真相不是真相，主体性成为陈词滥调后大众观点也廉价无比。</p>
      <p>本软件旨在通过将拟像抽象为可作为价值交换卡片（类似于我们小时候玩的赛尔号卡牌）和审慎的管理系统，帮助用户建立与数字拟像的良性互动关系，探索如何在虚实交织的世界中保持认知平衡。当你认可一个符号后，你才有资格了解一个符号。正像当你爱上一个人后，你才能真正了解ta。</p>
      <p>我们用地质时代来为我们的版本命名，因为对于拟像社会的重构是一条漫长的道路，要求我们溯流而上，之后才能顺流而下。我们邀请你和我们一起，在求索世界的过程中中寻找自我，在成为自我的过程中重塑世界。</p>
    </section>

    <hr class="divider">

    <section class="section">
      <h2>开发阶段路线图</h2>
      
      <div class="version-card">
        <h3>太古代·Beta版（Archean: Beta）</h3>
        <p><strong>核心目标</strong>：验证基础交互模型可行性</p>
        <pre><code>📌 技术实现：  
- 原生JavaScript搭建图片上传/检索原型  
- 基础按钮点击、数据展示交互验证  
- 浏览器本地JSON文件模拟数据存储  

🔍 阶段命名逻辑：  
类比地球生命起源初期，建立最原始的系统基础架构雏形</code></pre>
      </div>

      <div class="version-card">
        <h3>寒武纪·V1版（Cambrian: V1）</h3>
        <p><strong>核心目标</strong>：构建基础功能模块框架</p>
        <pre><code>📌 技术实现：  
- Vue3 + ElementPlus搭建前端界面  
- 实现账号注册/图片搜索/五星评分功能  
- 基于Flask开发简易后端API  

🔍 阶段命名逻辑：  
如同寒武纪生命大爆发，实现功能模块的快速迭代</code></pre>
      </div>

      <div class="version-card">
        <h3>奥陶纪·V2版（Ordovician: V2）</h3>
        <p><strong>核心目标</strong>：增强系统稳定性与扩展性</p>
        <pre><code>📌 技术实现：  
- MySQL替代本地JSON存储用户数据  
- 新增词条申请功能  
- 管理员后台（基础权限控制+数据看板）
- 注入1000+条模拟图片/词条数据(小红书爬虫)  
- 基于深度学习的评论情感分析

🔍 阶段命名逻辑：  
对应奥陶纪生态复杂化，系统开始支撑多角色协作</code></pre>
      </div>

      <div class="version-card">
        <h3>全新世·V3版（Holocene: V3）</h3>
        <p><strong>核心目标</strong>：提升用户体验与数据完整性</p>
        <pre><code>📌 技术实现：  
- 界面视觉改版  
- 优化组件加载速度与交互动效  
- 云端部署（灵感来源于第三周探索性任务）
- 多模态搜索功能（灵感来源于第三周探索性任务）
- 用户互动游戏（灵感来源于第三周探索性任务）

🔍 阶段命名逻辑：  
象征人类文明成熟期，系统进入易用稳定阶段</code></pre>
      </div>

      <div class="version-card">
        <h3>人类世·V4版（Anthropocene: V4）</h3>
        <p><strong>核心目标</strong>：引入智能管理机制</p>
        <pre><code>📌 技术实现：   
- 大模型半自动化词条审核流程
- 与各大网站产生关联（暂定MCP）
- 阶段性总结

🔍 阶段命名逻辑：  
呼应人工智能时代，建立人机协同的内容治理边界</code></pre>
      </div>
    </section>

    <section class="section">
      <h2>预期演进路径</h2>
      <div class="mermaid-diagram">
        <pre>
A[原生JS原型验证] --> B[Vue框架功能搭建]
B --> C[数据库与服务升级]
C --> D[体验与数据优化]
D --> E[智能辅助系统]
        </pre>
      </div>
    </section>
        <footer class="footer">
      <p><strong>AIFrameQuest: Ordovician-V2</strong></p>
      <p>图片来自于小红书、豆瓣。</p>
      <p>如果想要申请添加词条可以联系 <a href="mailto:1966322816@qq.com">1966322816@qq.com</a></p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'VersionPlan',
}
</script>

<style scoped>
.version-plan {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
  color: #333;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

h2 {
  color: #34495e;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-top: 40px;
}

h3 {
  color: #2c3e50;
  margin-top: 25px;
}

.section {
  margin-bottom: 40px;
}

.version-card {
  background-color: #f9f9f9;
  border-left: 4px solid #3498db;
  padding: 15px 20px;
  margin: 20px 0;
  border-radius: 0 4px 4px 0;
}

pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
}

.divider {
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
  margin: 40px 0;
}

.mermaid-diagram {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 4px;
  margin-top: 20px;
  text-align: center;
}

.mermaid-diagram pre {
  background: none;
  padding: 0;
  margin: 0;
}

@media (max-width: 768px) {
  .version-plan {
    padding: 10px;
  }
  
  pre {
    font-size: 12px;
  }
}

.footer {
  margin-top: 40px;
  padding: 20px;
  text-align: center;
  background-color: #f9f9f9;
  border-top: 1px solid #ddd;
  color: #555;
  font-size: 14px;
  line-height: 1.6;
}

.footer a {
  color: #3498db;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}
</style>
