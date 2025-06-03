<template>
  <!-- <div>
    <el-row>
      <select-conf
        @invoke-change-conf-datax="changeConfDatax"
        @invoke-change-conf-dolphin="changeConfDolphin"
        @invoke-change-conf-common="changeConfCommon"
        @invoke-change-conf-jdbc="changeConfJdbc"
        @invoke-change-conf-hikapi="changeConfHikapi"
      ></select-conf>
    </el-row>
  </div> -->
  <div>
  <el-button type="primary" @click="onSubmit">Query</el-button>
    <el-row :gutter="10">
      <el-col :span="10">
        <el-row :gutter="30">
          <el-col>
            <div>
              <el-radio-group
                v-if="ifShowSheet"
                v-model="selectSheet"
                size="large"
                @change="changeSheet"
              >
                <el-radio
                  v-for="item in sheets"
                  :value="item"
                  size="large"
                  border
                  style="width: 150px"
                  >{{ item }}</el-radio
                >
              </el-radio-group>
            </div>
          </el-col>
        </el-row>

        <el-row>
          <el-col>
            <div>
              <el-scrollbar max-height="600px">
                <el-radio-group
                  v-if="ifShowTables"
                  v-model="selectTable"
                  @change="changeTable"
                >
                  <el-radio
                    v-for="item in sheetTables"
                    :value="item[0]"
                    size="large"
                    border
                    class="table-radio"
                    >{{ item[1] }}</el-radio
                  >
                </el-radio-group>
              </el-scrollbar>
            </div>
          </el-col>
        </el-row>
      </el-col>

      <el-col :span="12">
        <slot
          name="scripts"
          :ifShowSql="ifShowSql"
          :confContentJdbc="confContentJdbc"
          :hikapiConf="hikapiConf"
        ></slot>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, reactive } from "vue";
import type { UploadInstance, UploadProps, UploadRawFile } from "element-plus";
import { genFileId } from "element-plus";
import { getTemplate, DBToolsApi, ExcelApi } from "@/api/api.js";
import selectConf from "@c/configCenter/selectConf/index.vue";

const sheets = ref([]);
const selectSheet = ref("");
const ifShowSheet = ref(false);
const sheetTables = ref([]);
const ifShowTables = ref(false);
const selectTable = ref("");
const ddlSql = ref("");
const dmlSql = ref("");
const ifShowSql = ref(false);
const sourceTables = ref([]);
const confContentDatax = ref();
const confContentJdbc = ref();
const hikapiConf = ref();

const filePath = defineModel()

const ifExtractTable = defineModel('ifExtractTable',{ default: true }) // 是否解析到表

const changeConfCommon = (param) => {
  console.log(`${param}`);
  filePath.value = param;
};

const changeConfHikapi = (param) => {
  console.log(`index: ${param}`);
  hikapiConf.value = param;
};

const changeConfJdbc = (param) => {
  console.log(`${param}`);
  confContentJdbc.value = param;
};
const changeFilePath = (path) => {
  filePath.value = path;
};
const changeConfDatax = (param) => {
  confContentDatax.value = param;
  console.log(confContentDatax.value);
};

const onSubmit = () => {
  console.log({
    filePath:filePath.value
  })
  ExcelApi.readLocalFile({
    filePath:filePath.value
  }).then((res) => {
    if (res.status === 200) {
      showSheet(res.data);
    }
  });
};

const upload = ref<UploadInstance>();
const emit = defineEmits(["invoke-change-table","invoke-change-sheet"]);
const uploadFile = (files) => {
  upload.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  upload.value!.handleStart(file);
};

const showSheet = (res) => {
  sheets.value = res.sheets;
  selectSheet.value = sheets[0];
  ifShowSheet.value = true;
};


const closeSql = () => {
  ddlSql.value = "";
  dmlSql.value = "";
  ifShowSql.value = false;
};

const closeTable = () => {
  ifShowTables.value = false;
  sheetTables.value = [];
  selectTable.value = "";
  closeSql();
};

const changeSheet = () => {
  if(ifExtractTable.value){
  closeTable();
  ExcelApi.getTablesInSheet({
      filePath: filePath.value,
      sheet: selectSheet.value,
    }).then((res) => {
      if (res.data.tables.length > 0) {
        ifShowTables.value = true;
        sheetTables.value = res.data.tables;
      }
    });
  }else{
    console.log("不解析到表");
    emit(
    "invoke-change-sheet",
    filePath.value,
    selectSheet.value
  );
  }
  
};

const changeTable = () => {
  console.log(
    selectTable.value,
    filePath.value,
    selectSheet.value,
    confContentDatax.value
  );
  emit(
    "invoke-change-table",
    selectTable.value,
    filePath.value,
    selectSheet.value,
    confContentDatax.value,
    hikapiConf.value
  );
};
</script>