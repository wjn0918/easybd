<template>
    <div>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="配置名称">
                <el-input v-model="formInline.confName" placeholder="请输入配置名称" clearable />
            </el-form-item>
            <el-form-item label="host">
                <el-input v-model="formInline.host" placeholder="host" clearable />
            </el-form-item>
            <el-form-item label="port">
                <el-input v-model="formInline.port" placeholder="port" clearable />
            </el-form-item>
            <el-form-item label="token">
                <el-input v-model="formInline.token" placeholder="token" clearable />
            </el-form-item>
            <el-form-item label="pid">
                <el-input v-model="formInline.pid" placeholder="pid" clearable />
            </el-form-item>
            <el-form-item label="currentDir">
                <el-input v-model="formInline.currentDir" placeholder="currentDir" clearable />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="onSubmit">添加</el-button>
            </el-form-item>
        </el-form>

    </div>
    <div>
        <el-button plain type="danger" @click="dialogVisible = true">
            一键清空
        </el-button>

        <el-dialog v-model="dialogVisible" title="Tips" width="500" :before-close="handleClose">
            <span>确认清空数据库？</span>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="clearAllConf">
                        确认
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
    <div>
        <el-table :data="confData" style="width: 100%">
            <el-table-column prop="conf_type" label="配置类型" width="180" />
            <el-table-column prop="conf_name" label="配置名称" width="180" />
            <el-table-column prop="conf_content" label="配置内容" width="180" />
            <el-table-column fixed="right" label="Operations" min-width="120">
                <template #default="scope">
                    <el-button link type="primary" size="small" @click="handleClick">
                        Detail
                    </el-button>
                    <el-button link type="primary" size="small" @click="editConf(scope.row)">Edit</el-button>
                </template>
            </el-table-column>
        </el-table>


        <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
            <el-form :model="editFormInline">
                <el-form-item label="host">
                    <el-input v-model="editFormInline.host" placeholder="host" clearable />
                </el-form-item>
                <el-form-item label="port">
                    <el-input v-model="editFormInline.port" placeholder="port" clearable />
                </el-form-item>
                <el-form-item label="token">
                    <el-input v-model="editFormInline.token" placeholder="token" clearable />
                </el-form-item>
                <el-form-item label="pid">
                    <el-input v-model="editFormInline.pid" placeholder="pid" clearable />
                </el-form-item>
                <el-form-item label="currentDir">
                    <el-input v-model="editFormInline.currentDir" placeholder="currentDir" clearable />
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="updateEdit">
                        更新
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { reactive, onMounted, ref, nextTick, h } from 'vue'
import { ConfigApi } from '@/api/api.js'
import { ElMessageBox, ElNotification } from 'element-plus'
import { ro } from 'element-plus/es/locale';

const confData = ref([])
const myComponentRef = ref(null);
const dialogVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const formInline = reactive({
    confType: 'dolphinscheduler',
    confName: '',
    host: '',
    port: '',
    token: ''
})
const editFormInline = ref({
    host: '',
    appKey: '',
    appSecret: ''
})
const editRow = ref()
const changeConfType = () => {
    console.log
}

const clearAllConf = () => {
    console.log("清空")
    ConfigApi.deleteConfig().then((res) => {
        console.log(res.data)
    })
    dialogVisible.value = false
    refreshConfData()
}

const editConf = (row) => {
    editFormInline.value = JSON.parse(row['conf_content'])
    dialogFormVisible.value = true
    editRow.value = row
}

const updateEdit = () => {
    var updateObj = editFormInline.value
    ConfigApi.updateConfig(editRow.value.id,
        {
            "confContent": `{"host": "${updateObj.host}", "port": "${updateObj.port}", "token": "${updateObj.token}", "pid": "${updateObj.pid}", "currentDir": "${updateObj.currentDir}"}`
        }
    ).then((res) => {
        if (res.status === 200) {
            dialogFormVisible.value = false
            ElNotification({
                title: 'Title',
                message: h('i', { style: 'color: teal' }, `更新成功`),
            });
            refreshConfData()
        }
    })
}


const handleClick = () => { }


const handleClose = (done: () => void) => {
    ElMessageBox.confirm('确定关闭？')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

const refreshConfData = async () => {
    await nextTick(); // 确保DOM已更新
    ConfigApi.getConfigByConfigType(formInline.confType).then((res) => {
        console.log(res.data)
        confData.value = res.data
    })
}

onMounted(() => {
    console.log(formInline);
    refreshConfData();
});


const clearForm = () => {
    // 清空表单
    formInline.confName = ""
    formInline.host = ''
    formInline.appKey = ''
    formInline.appSecret = ''
}

const onSubmit = () => {
    ConfigApi.createConfig({
        "confType": formInline.confType,
        "confName": formInline.confName,
        "confContent": `{"host": "${formInline.host}", "port": "${formInline.port}", "token": "${formInline.token}", "pid": "${formInline.pid}", "currentDir": "${formInline.currentDir}"}`
    }).then((res) => {
        console.log(res.data)
        refreshConfData()
        clearForm()
    })
}


</script>

<style>
.demo-form-inline .el-input {
    --el-input-width: 220px;
}

.demo-form-inline .el-select {
    --el-select-width: 220px;
}
</style>