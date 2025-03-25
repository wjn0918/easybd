<template>
    <div>
        交职2.0菜单名称更新
        <el-button type="warning" @click="rollbackConfig">重置配置</el-button>
        <upload-excel @invoke-change-sheet="changeSheet">

        </upload-excel>
    </div>

</template>
<script setup lang="ts">
import uploadExcel from '@/components/excel/uploadExcel.vue'
import {ShingiJZApi} from '@/api/api.js'
import { ElNotification } from 'element-plus'
import { ref, h } from 'vue'

const fullscreenLoading = ref(false)

const changeSheet =(sheetName) =>{
    console.log(sheetName)
    ShingiJZApi.changeName({
        sheet: sheetName
    }).then((res) => {
        if (res.status === 200) {
            fullscreenLoading.value = false
            ElNotification({
                title: 'Title',
                message: h('i', { style: 'color: teal' }, `${sheetName} 配置成功`),
            });
        } else {
            ElNotification.error({
                title: 'Error',
                message: `配置失败: ${res.data}`,
            });
        }
    }).catch((error) => {
        console.log("请求失败", error);
        fullscreenLoading.value = false
        ElNotification.error({
            title: 'Error',
            message: `请求失败: ${error.response.data.message}`,
        });
    });
}

const rollbackConfig = () => {
    console.log("111")
    ShingiJZApi.rollbackConfig().then((res) => {
        if (res.status === 200) {
            fullscreenLoading.value = false
            ElNotification({
                title: 'Title',
                message: h('i', { style: 'color: teal' }, `重置成功`),
            });
        } else {
            ElNotification.error({
                title: 'Error',
                message: `配置失败`,
            });
        }
    }).catch((error) => {
        console.log("请求失败", error);
        fullscreenLoading.value = false
        ElNotification.error({
            title: 'Error',
            message: `请求失败`,
        });
    });
}
</script>