<template>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="配置名称">
            <el-input v-model="formInline.confName" placeholder="请输入配置名称" clearable />
        </el-form-item>
        <el-form-item label="host">
            <el-input v-model="formInline.host" placeholder="host" clearable />
        </el-form-item>
        <el-form-item label="appKey">
            <el-input v-model="formInline.appKey" placeholder="appKey" clearable />
        </el-form-item>
        <el-form-item label="appSecret">
            <el-input v-model="formInline.appSecret" placeholder="appSecret" clearable />
        </el-form-item>
    </el-form>
</template>
<script setup lang="ts">
import { reactive, onMounted, ref, nextTick, h } from 'vue'
const formInline = reactive({
    confType: 'datax',
    confName: '',
    host: '',
    appKey: '',
    appSecret: ''
})


</script>