<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    :router="true"
    background-color="#f8f9fa"
    text-color="#333"
    active-text-color="#409EFF"
  >
    <!-- 工具类菜单 -->
    <el-sub-menu index="/tools">
      <template #title>
        <el-icon><Tools /></el-icon>
        <span>开发工具</span>
      </template>

      <el-menu-item index="/tools/database-tool">
        <el-icon><Files /></el-icon>
        <span>Excel 转 SQL</span>
      </el-menu-item>
      <el-menu-item index="/tools/excel2datax">
        <el-icon><Upload /></el-icon>
        <span>Excel 转 DataX</span>
      </el-menu-item>
      <el-menu-item index="/tools/excel2json">
        <el-icon><Document /></el-icon>
        <span>Excel 转 JSON</span>
      </el-menu-item>
    </el-sub-menu>

    <!-- 分割线 -->
    <div style="height: 1px; background-color: #ddd; margin: 12px 0;"></div>

    <!-- 配置中心 -->
    <el-sub-menu index="/configCenter">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>配置中心</span>
      </template>

      <el-menu-item index="/configCenter/excel">
        <el-icon><Document /></el-icon>
        <span>Excel 配置</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/datax">
        <el-icon><DataLine /></el-icon>
        <span>DataX 配置</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/dolphinscheduler">
        <el-icon><Clock /></el-icon>
        <span>DolphinScheduler</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/common">
        <el-icon><Grid /></el-icon>
        <span>公共配置</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/jdbc">
        <el-icon><Connection /></el-icon>
        <span>JDBC 连接</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/hikapi">
        <el-icon><Api /></el-icon>
        <span>HIK API</span>
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import {
  Document,
  Setting,
  Tools,
  Clock,
  Grid,
  Upload,
  Files,
  DataLine,
  Connection,
} from '@element-plus/icons-vue'
</script>

<style scoped>
.el-menu-vertical-demo {
  width: 220px;
  min-height: 100vh;
  border-right: 1px solid #ddd;
  font-size: 14px;
}
</style>
