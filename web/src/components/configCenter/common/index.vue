<template>
通用配置
<div>
            <el-form :inline="true" :model="formInline" class="demo-form-inline">
                <el-form-item label="配置名称">
                    <el-input v-model="formInline.confName" placeholder="请输入配置名称" clearable />
                </el-form-item>
                <el-form-item label="配置内容">
                    <el-input v-model="formInline.confContent" placeholder="配置内容" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">添加</el-button>
                </el-form-item>
            </el-form>

        </div>

          <div>
            <el-table :data="confData" style="width: 100%">
                <el-table-column prop="confType" label="配置类型" width="180" />
                <el-table-column prop="confName" label="配置名称" width="180" />
                <el-table-column prop="confContent" label="配置内容" width="180" />
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
                    <el-form-item label="confName">
                        <el-input v-model="editFormInline.confName" placeholder="confName" clearable />
                    </el-form-item>
                    <el-form-item label="appSecret">
                        <el-input v-model="editFormInline.confContent" placeholder="confContent" clearable />
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
import { ConfigApi } from '@/api/api.js'
import { reactive, onMounted, ref, nextTick, h } from 'vue'
import { ElMessageBox, ElNotification } from 'element-plus'

const formInline = reactive({
    confType: 'common',
    confName: '',
    confContent: ''
})
const editFormInline = ref({
    confType: 'common',
    confName: '',
    confContent: ''
})
const confData = ref([])
const dialogVisible = ref(false)
const dialogFormVisible = ref(false)
const editRow = ref()



onMounted(() => {
    console.log("组件挂载完成");
    refreshConfData();
});

const handleClick = () => { }

const clearForm = () => {
    // 清空表单
    formInline.confName = ""
    formInline.confContent = ''
}

const refreshConfData = async () => {
    await nextTick(); // 确保DOM已更新
    ConfigApi.getConfigByConfigType(formInline.confType).then((res) => {
        console.log(res.data)
        confData.value = res.data
    })
}

const onSubmit = () => {
    ConfigApi.createConfig({
        "confType": formInline.confType,
        "confName": formInline.confName,
        "confContent": formInline.confContent
    }).then((res) => {
        console.log(res.data)
        refreshConfData()
        clearForm()
    })
}



const editConf = (row) => {
    console.log(row)
    editFormInline.value = row
    dialogFormVisible.value = true
    editRow.value = row
}

const updateEdit = () => {
    var updateObj = editFormInline.value
    ConfigApi.updateConfig(editRow.value.id,
        {
        "confContent": updateObj.confContent
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

</script>