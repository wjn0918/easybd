<template>
  <el-card class="common-config-card">
    <template #header>
      <div class="card-title">
        <el-icon><setting /></el-icon>
        <span>配置信息列表</span>
      </div>
    </template>

    <el-table
      :data="confData"
      style="width: 100%"
      border
      stripe
      class="config-table"
    >
      <el-table-column prop="confType" label="配置类型" width="180" />
      <el-table-column prop="confName" label="配置名称" width="180" />
      <el-table-column
        prop="confContent"
        label="配置内容"
        min-width="200"
        :show-overflow-tooltip="true"
      />
      <el-table-column fixed="right" label="操作" min-width="160">
        <template #default="scope">
          <el-space wrap>
            <el-button link type="primary" size="small" @click="handleDetail(scope.row)">详情</el-button>
            <el-button link type="success" size="small" @click="editConf(scope.row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="delConf(scope.row)">删除</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogFormVisible"
      :title="dialogTitle"
      width="500"
      class="config-dialog"
    >
      <el-form :model="editFormInline" label-width="90px">
        <el-form-item label="配置名称">
          <el-input
            v-model="editFormInline.confName"
            placeholder="请输入配置名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="配置内容">
          <el-input
            v-model="editFormInline.confContent"
            placeholder="请输入配置内容"
            clearable
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-button type="primary" @click="updateEdit">更新</el-button>
        </div>
      </template>
    </el-dialog>
  </el-card>
</template>


<script lang="ts" setup>
import { reactive, ref, onMounted, nextTick, h } from "vue";
import { ElNotification } from "element-plus";

// 定义 props
const props = defineProps({
  // 配置类型，默认为 'common'
  confType: {
    type: String,
    default: "common",
  },
  // 配置API对象，必须包含 getConfigByConfigType, createConfig, updateConfig 方法
  configApi: {
    type: Object,
    required: true,
  },
  // 对话框标题
  dialogTitle: {
    type: String,
    default: "编辑配置",
  },
});

// 表单数据
const formInline = reactive({
  confType: props.confType,
  confName: "",
  confContent: "",
});

// 编辑表单数据
const editFormInline = ref({
  confType: props.confType,
  confName: "",
  confContent: "",
});

// 配置数据
const confData = ref([]);
const dialogFormVisible = ref(false);
const editRow = ref();

// 初始化加载数据
onMounted(() => {
  refreshConfData();
});

// 刷新配置数据
const refreshConfData = async () => {
  await nextTick();
  props.configApi.getConfigByConfigType(formInline.confType).then((res) => {
    confData.value = res.data;
  });
};

// 清空表单
const clearForm = () => {
  formInline.confName = "";
  formInline.confContent = "";
};

// 编辑配置
const editConf = (row) => {
  editFormInline.value = { ...row };
  dialogFormVisible.value = true;
  editRow.value = row;
};

const delConf = (row) => {
  props.configApi.deleteConfig(row.id).then((res) => {
    if (res.status === 200) {
      dialogFormVisible.value = false;
      ElNotification({
        title: "成功",
        message: h("i", { style: "color: teal" }, "删除成功"),
      });
      refreshConfData();
    }
  });
};

// 更新配置
const updateEdit = () => {
  const updateObj = editFormInline.value;
  props.configApi
    .updateConfig(editRow.value.id, {
      confContent: updateObj.confContent,
    })
    .then((res) => {
      if (res.status === 200) {
        dialogFormVisible.value = false;
        ElNotification({
          title: "成功",
          message: h("i", { style: "color: teal" }, "更新成功"),
        });
        refreshConfData();
      }
    });
};

// 查看详情
const handleDetail = (row) => {
  // 这里可以添加查看详情的逻辑
  console.log("查看详情:", row);
};

// 暴露方法给父组件
defineExpose({
  refreshConfData,
});
</script>

<style scoped>
.common-config-card {
  margin: 20px auto;
  padding: 20px;
  max-width: 1000px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.config-table {
  margin-top: 10px;
}

.dialog-footer {
  text-align: center;
}

.config-dialog .el-input__inner {
  font-size: 14px;
}

</style>