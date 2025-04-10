<template>
    <div>
        <excel-tools @invoke-change-table="changeTable">
            <template #scripts="">
                <!-- <el-row>
                    <select-conf @invoke-change-conf-datax="changeConfDatax"
                        @invoke-change-conf-dolphin="changeConfDolphin"
                        @invoke-change-conf-common="changeConfCommon"
                        ></select-conf>
                </el-row> -->

                <el-row>
                    <el-col :span="6">
                        选择DDLType
                    </el-col>
                    <el-col :span="8">
                        <el-select v-model="ddlType" placeholder="请选择DDLType" size="large">
                            <el-option v-for="item in ddlTypes" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-col>
                </el-row>

                <el-row :gutter="30">
                    <el-col :span="6">
                        选择reader/writer
                    </el-col>
                    <el-col :span="8">
                        <el-select v-model="readerType" placeholder="请选择reader" size="large">
                            <el-option v-for="item in dataxRaderTypes" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-col>
                    <el-col :span="8">
                        <el-select v-model="writerType" placeholder="请选择writer" size="large">
                            <el-option v-for="item in dataxWriterTypes" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-col>
                    <el-button v-loading.fullscreen.lock="fullscreenLoading" @click="ok"
                        :disabled="!checkstate">确定</el-button>
                </el-row>
                <!-- 
                <el-row v-if=" 'hikapi' == readerType ">
                    <hikapireader ref="hikapiObj"></hikapireader>
                </el-row> -->


                <div v-if="ifShowDatax">
                    <el-input v-model="input_dir" style="width: 240px" placeholder="输入写入目录地址" />
                    <el-button v-loading.fullscreen.lock="fullscreenLoading" @click="saveScript">保存脚本</el-button>
                    <el-button v-loading.fullscreen.lock="fullscreenLoading"
                        @click="saveScript2Dolphin">保存脚本到dolphinscheduler</el-button>

                    <el-row :gutter="30">
                        <el-col :span="12">
                            <div>
                                <button @click="() => handleCopy(datax)">复制datax</button>
                                <highlightjs class="sql" language="SQL" :code="datax"></highlightjs>
                            </div>
                        </el-col>
                        <el-col :span="12">
                            <div>
                                <button @click="() => handleCopy(ddlSql)">复制DDL</button>
                                <highlightjs class="sql" language="SQL" :code="ddlSql"></highlightjs>
                            </div>
                        </el-col>
                    </el-row>
                </div>

            </template>
        </excel-tools>
        <!-- 添加下载模板按钮 -->
        <!-- <el-button type="primary" @click="downloadTemplate" style="float: right;">
            Download Template<el-icon class="el-icon--right">
                <Download />
            </el-icon>
        </el-button> -->
    </div>
</template>

<script setup lang="ts">
import { ref, h, onMounted,defineEmits } from 'vue'
import useClipboard from 'vue-clipboard3'
import { getTemplate, DBToolsApi, ExcelApi } from '@/api/api.js'
import ExcelTools from './exceltools.vue'
import { ElNotification } from 'element-plus'
import hikapireader from './datax/reader/hikapireader/index.vue'
import selectConf from '@c/configCenter/selectConf/index.vue'



const ifShowDatax = ref(false)
const datax = ref('')
const ddlType = ref('Mysql')
const readerType = ref('STREAM')
const writerType = ref('STREAM')
const ddlSql = ref('')
const input_dir = ref('D:\\wjn\\gitee\\jzDataMigrate\\etl\\jz\\hik\\datax')
const fullscreenLoading = ref(false)
const filePath = ref('')
const sheet = ref('')
const selectTable = ref('')
const checkstate = ref(false)
const confContentDatax = ref()
const confContentDolphin = ref()
const confContentCommon= ref()

const dataxRaderTypes = ref(
    [
        {
            value: 'STREAM',
            label: 'STREAM'
        }
    ]
)

const dataxWriterTypes = ref(
    [
        {
            value: 'STREAM',
            label: 'STREAM'
        }
    ]
)

const ddlTypes = ref(
    [
        {
            value: 'STREAM',
            label: 'STREAM'
        }
    ]
)

onMounted(() => {
    ExcelApi.getDataxTypes().then((res) => {
        dataxRaderTypes.value = res.data['datax_reader_type'].map(item => (
            {
                value: item,
                label: item
            }
        ))
        dataxWriterTypes.value = res.data['datax_writer_type'].map(item => (
            {
                value: item,
                label: item
            }
        ))
        ddlTypes.value = res.data['ddl_type'].map(item => (
            {
                value: item,
                label: item
            }
        ))
    })
})

// const changeConfDatax = (param) => {
//     confContentDatax.value = param
//     console.log(confContentDatax.value)
// }
const changeConfDolphin = (param) => {
    confContentDolphin.value = param
}



const closeSql = () => {
    datax.value = ""
    ifShowDatax.value = false
}


const changeTable = (selectTableName, f, s, c) => {
    filePath.value = f
    sheet.value = s
    selectTable.value = selectTableName
    checkstate.value = true
    confContentDatax.value = c
    closeSql()
}

const ok = () => {
    var body = {
        "reader": readerType.value,
        "writer": writerType.value,
        "ddlType": ddlType.value,
        "parameter": confContentDatax.value,
        "confDolphin": confContentDolphin.value,
        "excelInfo": {
            "filePath": filePath.value,
            "sheet": sheet.value,
            "table": selectTable.value
        }
    }

    console.log(
body
    )
    ExcelApi.processTable2Datax(body).then((res) => {
        console.log(res.data)
        ddlSql.value = res.data.sql_ddl
        datax.value = JSON.stringify(JSON.parse(res.data.datax), null, 2)
        ifShowDatax.value = true
    })
}


const { toClipboard } = useClipboard()
const handleCopy = (copyObj) => {
    try {
        toClipboard(copyObj)
        console.log('复制成功')
    } catch (e) {
        console.error(e);
        console.error('复制失败')
    }
}

const saveScript2Dolphin = () => {
    fullscreenLoading.value = true
    let param = {
        "scriptDir": input_dir.value,
        "tableName": selectTable.value,
        "script": datax.value,
        "ddl": ddlSql.value,
        "confContentDolphin": confContentDolphin.value
    }
    console.log(param)
    ExcelApi.saveScript2Dolphin(param).then((res) => {
        fullscreenLoading.value = false
        console.log(res.data)

    })
}

const saveScript = () => {
    console.log("开始保存")
    fullscreenLoading.value = true
    ExcelApi.saveScript({
        "scriptDir": input_dir.value,
        "tableName": selectTable.value,
        "script": datax.value,
    }).then((res) => {
        if (res.status === 200) {
            fullscreenLoading.value = false
            ElNotification({
                title: 'Title',
                message: h('i', { style: 'color: teal' }, `${selectTable.value} 保存成功`),
            });
        } else {
            console.log("构建失败", res);
            ElNotification.error({
                title: 'Error',
                message: `构建失败: ${res.data}`,
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




</script>

<style>
.el-row {
    margin-bottom: 20px !important;
    margin-left: 0px !important;
    margin-right: 0px !important;
}

.sql {
    height: 300px;
}

.table-radio {
    width: 200px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}
</style>
