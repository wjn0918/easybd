<template>
  <div>
    <select-conf-common v-model="confType" v-model:select-conf="selectConf" />
    <excel-info
      v-model="selectConf"
      v-model:ifExtractTable="ifExtractTable"
      @invoke-change-table="changeTable"
      @invoke-change-sheet="changeSheet"
    >
      <template #scripts="">
        <div v-if="ifShow">
          <div>
            <el-button type="primary" @click="() => handleCopy(dataJson)"
              >复制结果</el-button
            >
          </div>
        </div>
      </template>
    </excel-info>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import SelectConfCommon from "@c/configCenter/selectConf/selectConfCommon.vue";
import ExcelInfo from "@c/excel/excelInfo.vue";
import useClipboard from "vue-clipboard3";
import { DBToolsApi } from "@/api/api.js";
import { ElMessage } from "element-plus";

const confType = ref("excel");
const selectConf = ref("");
const ifExtractTable = ref(false);
const ifShow = ref(false);
const dataJson = ref("");

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

const changeSheet = (f, s) => {
  console.log(f, s);
  ifShow.value = false;
  DBToolsApi.process2json({
    filePath: f,
    sheet: s,
  }).then((res) => {
    console.log(res);
    dataJson.value = res.data;
    ifShow.value = true;
  });
};
</script>