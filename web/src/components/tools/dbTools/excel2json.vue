<template>
  <div class="p-4">
    <el-tabs v-model="activeTab" type="card">
      <!-- excel2json TAB -->
      <el-tab-pane label="excel2json" name="excel2json">
        <el-card shadow="never" class="mb-4">
          <el-space wrap size="large">
            <select-conf-common v-model="confType" v-model:select-conf="selectConf" />
            <el-button type="primary" @click="resetFilter">重置</el-button>
          </el-space>
        </el-card>

        <el-card shadow="never" class="mb-4">
          <transform-step-editor v-model="transformSteps" />
        </el-card>

        <el-card shadow="never">
          <excel-info
            v-model="selectConf"
            v-model:ifExtractTable="ifExtractTable"
            @invoke-change-sheet="changeSheet"
          >
            <template #scripts>
              <div v-if="ifShow" class="text-right mt-2">
                <el-button type="primary" @click="() => handleCopy(dataJson)">复制结果</el-button>
              </div>
            </template>
          </excel-info>
        </el-card>
      </el-tab-pane>

      <!-- json2excel TAB -->
      <el-tab-pane label="json2excel" name="json2excel">
        <el-card shadow="never">
          <el-form label-position="top">
            <el-form-item label="JSON 数据输入">
              <el-input
                type="textarea"
                :rows="10"
                placeholder='请输入 JSON 数据（例如：[{"name": "John", "age": 30}]）'
                v-model="jsonInput"
                @input="validateJSON"
              />
            </el-form-item>

            <el-form-item v-if="jsonError">
              <el-alert :title="jsonError" type="error" show-icon />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="exportExcel" :disabled="!isValidJSON">
                导出 Excel
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import SelectConfCommon from "@c/configCenter/selectConf/selectConfCommon.vue";
import TransformStepEditor from "@c/transform/TransformStepEditor.vue";
import ExcelInfo from "@c/excel/excelInfo.vue";
import useClipboard from "vue-clipboard3";
import { DBToolsApi } from "@/api/api.js";
import { ElMessage } from "element-plus";

const confType = ref("excel");
const selectConf = ref("");
const ifExtractTable = ref(false);
const ifShow = ref(false);
const dataJson = ref("");
const pandasFilter = ref("");

const transformSteps = ref([]);
const activeTab = ref("excel2json")


const jsonInput = ref('');
const jsonError = ref('');
const isValidJSON = ref(false);

// 校验 JSON 格式
const validateJSON = () => {
  try {
    JSON.parse(jsonInput.value);
    jsonError.value = '';
    isValidJSON.value = true;
  } catch (e) {
    console.log(e)
    jsonError.value = `JSON 格式错误：${e.message}`;
    isValidJSON.value = false;
  }
};

const exportExcel = () => {
  const data = JSON.parse(jsonInput.value);
  console.log('导出数据：', data);
  DBToolsApi.json2excel({
    jsonData: jsonInput.value
  }).then((res) => {
    const blob = new Blob([res.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'data.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  }).catch(err => {
    console.error("导出失败", err);
  })
}

  const { toClipboard } = useClipboard();
  const handleCopy = (copyObj) => {
    try {
      toClipboard(copyObj);
      console.log("复制成功");
      ElMessage.success("复制成功");
    } catch (e) {
      console.error(e);
      console.error("复制失败");
    }
  };

  const resetFilter = () => {
    selectConf.value = "";
    pandasFilter.value = "";
    dataJson.value = "";
    ifShow.value = false;
    transformSteps.value = [];
  };

  const changeSheet = (f, s) => {
    console.log(f, s);
    ifShow.value = false;
    DBToolsApi.process2json({
      filePath: f,
      sheet: s,
      filterExpr: pandasFilter.value,
      transformSteps: transformSteps.value,
    }).then((res) => {
      console.log(res);
      dataJson.value = res.data;
      ifShow.value = true;
    });
  };
</script>