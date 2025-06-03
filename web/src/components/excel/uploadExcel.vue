<template>
  <el-card class="upload-card">
    <template #header>
      <div class="card-header">
        <span>Excel 文件上传</span>
      </div>
    </template>

    <el-upload
      ref="upload"
      class="upload-uploader"
      drag
      action="/api/tools/excel/upload"
      accept=".xls,.xlsx"  
      :before-upload="beforeUpload"
      :limit="1"
      :on-exceed="uploadFile"
      :auto-upload="false"
      :on-success="uploadFinish"
      :on-change="handleFileChange"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">
        拖拽文件到此处，或 <em>点击选择</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">仅支持上传一个 Excel 文件（.xls/.xlsx）</div>
      </template>
    </el-upload>

    <div class="btn-group">
      <el-button type="primary" :disabled="!uploading" @click="submitUpload">开始上传</el-button>
    </div>
  </el-card>
</template>


<script setup lang="ts">

import { ref, defineEmits, reactive } from 'vue'
import { genFileId } from 'element-plus'
import { UploadInstance, UploadProps, UploadRawFile, ElMessageBox ,ElMessage} from 'element-plus'
import axios from 'axios'

const sheets = ref([])
const uploadFilePath = ref('123')
const uploading = ref(false)   // 控制按钮禁用状态

const ifShowSheet = ref(false)
const upload = ref<UploadInstance>()
const emit = defineEmits(['invoke-change-sheet'])

const handleFileChange = (file, fileListNew) => {
  uploading.value = fileListNew.length > 0 // 有文件就启用上传按钮
}


// 暴露给父组件
defineExpose({
  uploadFilePath
})

const checkFileExist = async (fileName) => {
  try {
    const response = await axios.get('/api/tools/excel/check-file-exist', {
      params: { filename: fileName }
    })
    return response.data
  } catch (error) {
    ElMessage.error('检查文件失败，请稍后再试')
    return { exists: false }
  }
}

const beforeUpload = async (file) => {
  try {
    const res = await checkFileExist(file.name) // 自行实现接口调用

    if (res.exists) {
      // 文件存在，弹确认框
      const confirmed = await ElMessageBox.confirm(
        '服务器已有同名文件，是否覆盖？',
        '提示',
        {
          confirmButtonText: '覆盖',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).catch(() => false) // 取消返回false

      if (!confirmed) {
        ElMessage.info('已取消上传')
        return false // 取消上传
      }
      // 确认覆盖，继续上传
      return true
    } else {
      // 文件不存在，直接上传
      return true
    }
  } catch (error) {
    ElMessage.error('检查文件失败，请稍后再试')
    return false
  }
}

const uploadFile = (files) => {
    upload.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload.value!.handleStart(file)
    console.log(111)
}

const uploadFinish =(res) =>{
    console.log(res.file_path)
    uploadFilePath.value = res.file_path

    emit('invoke-change-sheet')

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

<style scope>
.upload-card {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.upload-uploader {
  margin-bottom: 20px;
}

.btn-group {
  text-align: center;
}
</style>