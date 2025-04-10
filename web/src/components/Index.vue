<template>
  <el-menu default-active="1" class="el-menu-vertical-demo" :router=true>
    <el-sub-menu index="/tools/database-tool">
      <template #title>
        <el-icon>
          <location />
        </el-icon>
        <span>数据库工具</span>
      </template>
      <el-menu-item index="/tools/database-tool">
        <el-icon>
          <setting />
        </el-icon>
        <span>execl转sql</span>
      </el-menu-item>
      <el-menu-item index="/tools/excel2datax">
        <el-icon>
          <setting />
        </el-icon>
        <span>execl转datax</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/company">
      <template #title>
        <el-icon>
          <location />
        </el-icon>
        <span>新怡</span>
      </template>
      <el-menu-item index="/company/hik">
        <el-icon>
          <setting />
        </el-icon>
        <span>海康api</span>
      </el-menu-item>
      <el-menu-item index="/company/jz">
        <el-icon>
          <setting />
        </el-icon>
        <span>交职工具</span>
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/company/source">
      <el-icon>
        <setting />
      </el-icon>
      <span>其他工具</span>
    </el-menu-item>
    <el-menu-item index="/dbCenter">
      <el-icon>
        <Coin />
      </el-icon>
      <span>数据源中心</span>
    </el-menu-item>
    <el-sub-menu index="">
      <template #title>
        <el-icon>
          <location />
        </el-icon>
        <span>配置中心</span>
      </template>
      <el-menu-item index="/configCenter/datax">
        <el-icon>
          <setting />
        </el-icon>
        <span>datax</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/dolphinscheduler">
        <el-icon>
          <setting />
        </el-icon>
        <span>dolphinscheduler</span>
      </el-menu-item>
      <el-menu-item index="/configCenter/common">
        <el-icon>
          <setting />
        </el-icon>
        <span>common</span>
      </el-menu-item>
       <el-menu-item index="/configCenter/jdbc">
        <el-icon>
          <setting />
        </el-icon>
        <span>jdbc</span>
      </el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>
<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'



</script>
