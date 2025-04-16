<template>
    <el-upload ref="upload" class="upload-demo" action="/api/tools/excel/upload" :limit="1" :on-exceed="uploadFile"
        :auto-upload="false" :on-success="uploadFinish">
        <template #trigger>
            <el-button type="primary">选择文件</el-button>
        </template>
        <el-button class="ml-3" type="success" @click="submitUpload">
            上传
        </el-button>
    </el-upload>

</template>

<script setup lang="ts">

import { ref, defineEmits, reactive } from 'vue'
import { genFileId } from 'element-plus'
import { UploadInstance, UploadProps, UploadRawFile, ElMessageBox } from 'element-plus'

const sheets = ref([])
const uploadFilePath = ref('123')

const ifShowSheet = ref(false)
const upload = ref<UploadInstance>()
const emit = defineEmits(['invoke-change-sheet'])

// 暴露给父组件
defineExpose({
  uploadFilePath
})

const uploadFile = (files) => {
    upload.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload.value!.handleStart(file)
}

const uploadFinish =(res) =>{
    console.log(res.file_path)
    uploadFilePath.value = res.file_path

}

const submitUpload = () => {
    upload.value!.submit()
}


const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
    ElMessageBox.confirm('确定关闭当前选择?')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}
</script>