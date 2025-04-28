<template>
  <div class="common-config">
    <div>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <!-- <el-form-item label="配置类型">
          <el-select
            v-model="selectConfType"
            placeholder="Select"
            size="large"
            style="width: 240px"
          >
            <el-option
              v-for="item in confTypes"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item> -->

        <el-form-item label="配置名称">
          <el-input
            v-model="formInline.confName"
            placeholder="请输入配置名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="配置内容">
          <el-input
            v-model="formInline.confContent"
            placeholder="配置内容"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">添加</el-button>
        </el-form-item>
      </el-form>
    </div>
    <common-config-show
      :config-api="props.configApi"
      :conf-type="props.confType"
      dialog-title="配置编辑"
    />
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted, nextTick, h } from "vue";
import { ElNotification } from "element-plus";
import CommonConfigShow from "./CommonConfigShow.vue";

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

const selectConfType = ref("common");

const confTypes = [
  {
    value: "common",
    label: "common",
  },
  {
    value: "datax",
    label: "datax",
  },
];

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
  console.log(props);
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
  selectConfType.value = "";
};

// 提交表单
const onSubmit = () => {
  props.configApi
    .createConfig({
      confType: selectConfType.value,
      confName: formInline.confName,
      confContent: formInline.confContent,
    })
    .then((res) => {
      refreshConfData();
      clearForm();
    });
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
.common-config {
  padding: 20px;
}
</style>