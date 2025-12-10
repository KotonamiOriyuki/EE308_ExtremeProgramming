<!-- Version 1.0
Time: Wed Dec 10,16:55
frontend -->

<template>
  <div class="app-container">
    <el-container>
      <!-- Bingtian Qiao:应用图标和标题 -->
      <el-header class="main-header">
        <div class="logo">
          <el-icon :size="24"><Notebook /></el-icon>
          <span>通讯录系统</span>
        </div>
      </el-header>
      <el-main>
      <!-- Bingtian Qiao:占位，后续添加Contact List -->
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
// Bingtian Qiao:占位
</script>

<style>
:root {
  --el-color-primary: #0f766e;
  --el-color-primary-light-9: #f0fdfa;
  --bg-color: #f8fafc;
}
body { margin: 0; background-color: var(--bg-color); font-family: 'Helvetica Neue', sans-serif; }
.app-container { height: 100vh; }
.main-header {
  background-color: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  padding: 0 40px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.logo { display: flex; align-items: center; gap: 10px; font-weight: bold; color: #334155; font-size: 1.2rem; }
</style>