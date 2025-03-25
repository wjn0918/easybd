<template>
    <el-upload ref="upload" class="upload-demo" action="/api/tools/excel/upload" :limit="1" :on-exceed="uploadFile"
        :auto-upload="false" :on-success="showSheet">
        <template #trigger>
            <el-button type="primary">选择文件</el-button>
        </template>
        <el-button class="ml-3" type="success" @click="submitUpload">
            上传
        </el-button>
    </el-upload>

    <el-row :gutter="30">
        <el-col :span="12">
            <div>
                <el-radio-group v-if="ifShowSheet" v-model="selectSheet" size="large" @change="chooseSheet">
                    <el-radio v-for="item in sheets" :value="item" size="large" border style="width: 150px;">{{ item
                        }}</el-radio>
                </el-radio-group>
            </div>
        </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" title="Tips" width="500" :before-close="handleClose">
        <span>是否选择{{ selectSheet }}</span>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="changeSheet">
                    确认
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">

import { ref, defineEmits, reactive } from 'vue'
import { genFileId } from 'element-plus'
import { UploadInstance, UploadProps, UploadRawFile, ElMessageBox } from 'element-plus'

const sheets = ref([])
const selectSheet = ref('')
const ifShowSheet = ref(false)
const upload = ref<UploadInstance>()
const emit = defineEmits(['invoke-change-sheet'])

const uploadFile = (files) => {
    upload.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload.value!.handleStart(file)
}

const showSheet = (res) => {
    sheets.value = res.sheets
    selectSheet.value = sheets[0]
    ifShowSheet.value = true
}
const submitUpload = () => {
    upload.value!.submit()
}

const chooseSheet = () => {
    dialogVisible.value = true
}

const changeSheet = () => {
    emit('invoke-change-sheet', selectSheet.value);
    dialogVisible.value = false
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