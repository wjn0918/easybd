<template>
    <div>
        <el-form :inline="true" :model="props.formData" class="demo-form-inline">
            <el-form-item label="配置名称">
                <el-input v-model="props.formData.confName" placeholder="请输入配置名称" clearable />
            </el-form-item>
            <el-form-item label="host">
                <el-input v-model="props.formData.host" placeholder="host" clearable />
            </el-form-item>
            <el-form-item label="port">
                <el-input v-model="props.formData.port" placeholder="port" clearable />
            </el-form-item>
            <el-form-item label="token">
                <el-input v-model="props.formData.token" placeholder="token" clearable />
            </el-form-item>
     
        </el-form>
    </div>
</template>
<script setup lang="ts">
import { reactive, onMounted, ref, nextTick, h } from 'vue'

const props = defineProps(['formData'])
onMounted(() => {
    console.log(1111111)
    console.log(props.formData);
});


</script>