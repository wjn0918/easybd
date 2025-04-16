<template>
<div>
 <el-row>
                    <select-conf @invoke-change-conf-datax="changeConfDatax"
                        @invoke-change-conf-dolphin="changeConfDolphin"
                        @invoke-change-conf-common="changeConfCommon"
                        @invoke-change-conf-jdbc="changeConfJdbc"
                        @invoke-change-conf-hikapi="changeConfHikapi"
                        ></select-conf>
                </el-row>
</div>

    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="请输入文件地址">
                <el-input autosize type="textarea" v-model="formInline.filePath" placeholder="请输入文件地址" clearable />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Query</el-button>
            </el-form-item>
        </el-form>

        <el-upload ref="upload" class="upload-demo" action="/api/tools/excel/upload" :limit="1" :on-exceed="uploadFile"
            :auto-upload="false" :on-success="showSheet">
            <template #trigger>
                <el-button type="primary">select file</el-button>
            </template>
            <el-button class="ml-3" type="success" @click="submitUpload">
                upload to server
            </el-button>
        </el-upload>

        <el-row :gutter="10">
            
            <el-col :span="10">
                <el-row :gutter="30">
                    <el-col>
                        <div>
                            <el-radio-group v-if="ifShowSheet" v-model="selectSheet" size="large" @change="changeSheet">
                                <el-radio v-for="item in sheets" :value="item" size="large" border style="width: 150px;">{{
                                    item
                                }}</el-radio>
                            </el-radio-group>
                        </div>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col>
                        <div>
                            <el-scrollbar max-height="600px">
                                <el-radio-group v-if="ifShowTables" v-model="selectTable" @change="changeTable">
                                    <el-radio v-for="item in sheetTables" :value="item[0]" size="large" border
                                        class="table-radio">{{
                                            item[1]
                                        }}</el-radio>
                                </el-radio-group>
                            </el-scrollbar>
                        </div>
                    </el-col>

                </el-row>
            </el-col>


            <el-col :span="12">
                <slot name="scripts" :ifShowSql=ifShowSql :confContentJdbc=confContentJdbc :hikapiConf=hikapiConf></slot>
            </el-col>

        </el-row>




    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, reactive } from 'vue'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { genFileId } from 'element-plus'
import { getTemplate, DBToolsApi, ExcelApi } from '@/api/api.js'
import selectConf from '@c/configCenter/selectConf/index.vue'

const sheets = ref([])
const selectSheet = ref('')
const ifShowSheet = ref(false)
const sheetTables = ref([])
const ifShowTables = ref(false)
const selectTable = ref('')
const ddlSql = ref('')
const dmlSql = ref('')
const ifShowSql = ref(false)
const sourceTables = ref([])
const confContentDatax = ref()
const confContentJdbc = ref()
const hikapiConf = ref()

const formInline = reactive({
    filePath: `D:\\wjn\\work_info\\docs\\src\\tx\\表结构_特校.xlsx`
})

const changeConfCommon = (param) => {
    console.log(`${param}` )
    formInline.filePath = param

}

const changeConfHikapi = (param) => {
    console.log(`index: ${param}` )
    hikapiConf.value = param

}

const changeConfJdbc = (param) => {
    console.log(`${param}` )
    confContentJdbc.value = param

}
const changeFilePath = (path) =>{
    this.formInline.filePath.value = path
}
const changeConfDatax = (param) => {
    confContentDatax.value = param
    console.log(confContentDatax.value)
}

const onSubmit = () => {
    ExcelApi.readLocalFile(formInline).then((res) => {
        if (res.status === 200) {
            showSheet(res.data)
        }
    })
}

const upload = ref<UploadInstance>()
const emit = defineEmits(['invoke-change-table'])
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
    ifShowTables.value = false
}

const closeSql = () => {
    ddlSql.value = ""
    dmlSql.value = ""
    ifShowSql.value = false
}

const closeTable = () => {
    ifShowTables.value = false
    sheetTables.value = []
    selectTable.value = ""
    closeSql()
}

const changeSheet = () => {
    closeTable()
    ExcelApi.getTablesInSheet(
        {
            filePath: formInline.filePath,
            sheet: selectSheet.value
        }
    ).then((res) => {
        if (res.data.tables.length > 0) {
            ifShowTables.value = true
            sheetTables.value = res.data.tables
        }
    })
}

const changeTable = () => {
    console.log(selectTable.value, formInline.filePath, selectSheet.value, confContentDatax.value)
    emit('invoke-change-table', selectTable.value, formInline.filePath, selectSheet.value, confContentDatax.value, hikapiConf.value);
}

</script>