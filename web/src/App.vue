<script setup>
import Index from './components/Index.vue'
</script>

<template>
  <div class="common-layout">
    <el-container class="layout-container-demo">
      <el-header class="custom-header">
        <div class="header-title">🧰 工具库</div>
      </el-header>

      <el-container>
        <el-aside width="220px" class="custom-aside">
          <Index />
        </el-aside>

        <el-main class="custom-main">
          <el-card shadow="hover" class="main-card">
            <router-view></router-view>
          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<style src="./assets/styles/App.css"></style>