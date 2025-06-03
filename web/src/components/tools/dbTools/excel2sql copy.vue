<template>
  <div>
    <!-- 添加下载模板按钮 -->
    <div>
      <el-button type="primary" @click="downloadTemplate" style="float: right">
        Download Template<el-icon class="el-icon--right">
          <Download />
        </el-icon>
      </el-button>

      <select-conf-common v-model="confType" v-model:select-conf="selectConf" />

      <excel-info v-model="selectConf" @invoke-change-table="changeTable">
        <template #scripts="">
          <div v-if="ifShowSql">
            <!-- <el-input
              v-model="input_dir"
              style="width: 240px"
              placeholder="输入写入目录地址"
            />
            <el-button
              v-loading.fullscreen.lock="fullscreenLoading"
              @click="startBuild"
              >构建</el-button
            >
            <el-button
              v-loading.fullscreen.lock="fullscreenLoading"
              @click="startExec"
              >执行</el-button
            > -->

            <el-row :gutter="30">
              <el-col :span="12">
                <div>
                  <button @click="() => handleCopy(dmlSql)">复制DML</button>
                  <highlightjs
                    class="sql"
                    language="SQL"
                    :code="dmlSql"
                  ></highlightjs>
                </div>
              </el-col>
              <el-col :span="12">
                <div>
                  <button @click="() => handleCopy(ddlSql)">复制DDL</button>
                  <button @click="() => execDDL(ddlSql)">执行DDL</button>
                  <highlightjs
                    class="sql"
                    language="SQL"
                    :code="ddlSql"
                  ></highlightjs>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="30">
              <el-col :span="12">
                <div>
                  <button @click="() => handleCopy(fieldComment)">
                    复制fields
                  </button>
                  <highlightjs
                    class="sql"
                    language="SQL"
                    :code="fieldComment"
                  ></highlightjs>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="30">
              <el-col :span="12">
                <div>
                  <button @click="() => handleCopy(fc)">
                    复制
                  </button>
                  <highlightjs
                    class="sql"
                    language="SQL"
                    :code="fc"
                  ></highlightjs>
                </div>
              </el-col>
            </el-row>
            
          </div>
        </template>
      </excel-info>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { h } from "vue";
import { ElNotification } from "element-plus";
import useClipboard from "vue-clipboard3";
import { getTemplate, DBToolsApi, ExcelApi } from "@/api/api.js";
import ExcelTools from "./exceltools.vue";
import SelectConfCommon from "@c/configCenter/selectConf/selectConfCommon.vue";
import ExcelInfo from "@c/excel/excelInfo.vue";

const confType = ref("excel");
const selectConf = ref("");

const cs = () => {
  console.log(selectConf.value);
};

const confContentJdbc = ref("");
const ifShowSql = ref(false);
const selectTable = ref("");
const sourceTables = ref([]);
const ddlSql = ref("");
const dmlSql = ref("");
const fieldComment = ref("");
const fc = ref("");
const fullscreenLoading = ref(false);
const input_dir = ref("D:\\wjn\\gitee\\jzDataMigrate\\etl\\jz");

const closeSql = () => {
  ddlSql.value = "";
  dmlSql.value = "";
  fieldComment.value = "";
  ifShowSql.value = false;
};

const downloadTemplate = () => {
  getTemplate()
    .then((res) => {
      console.log(res);
      let data = res.data;

      // 检查res是否为Blob类型
      if (data instanceof Blob) {
        // 创建隐藏的a标签
        const link = document.createElement("a");
        link.style.display = "none";
        document.body.appendChild(link);

        // 创建Blob URL
        const url = URL.createObjectURL(data);

        // 设置下载属性和文件名
        link.href = url;
        link.download = "ddl_dml生成模板.xlsx"; // 请根据实际情况设置文件名

        // 触发点击
        link.click();

        // 清理URL
        URL.revokeObjectURL(url);

        // 移除a标签
        document.body.removeChild(link);
      } else {
        console.error("返回的数据不是Blob类型");
      }
    })
    .catch((error) => {
      console.error("下载过程中发生错误:", error);
    });
};

const changeTable = (selectTableName, f, s) => {
  closeSql();
  selectTable.value = selectTableName;
  DBToolsApi.processTable({
    filePath: f,
    sheet: s,
    table: selectTableName,
  }).then((res) => {
    console.log(res);
    ddlSql.value = res.data.sql;
    dmlSql.value = res.data.sqlQuery;
    sourceTables.value = res.data.sourceTables;
    fieldComment.value = res.data.fieldComment;
    fc.value = res.data.fc;
    ifShowSql.value = true;
  });
};

const { toClipboard } = useClipboard();
const handleCopy = (copyObj) => {
  try {
    toClipboard(copyObj);
    console.log("复制成功");
  } catch (e) {
    console.error(e);
    console.error("复制失败");
  }
};
const execDDL = (ddl) => {
  // console.log(ddl)
  console.log(confContentJdbc);
};

const startBuild = () => {
  console.log("开始构建");
  fullscreenLoading.value = true;
  console.log(selectTable.value);
  DBToolsApi.buildScript({
    scriptDir: input_dir.value,
    tableName: selectTable.value,
    dmlSql: dmlSql.value,
    sourceTables: sourceTables.value,
  })
    .then((res) => {
      if (res.status === 200) {
        console.log("构建成功");
        fullscreenLoading.value = false;
        ElNotification({
          title: "Title",
          message: h(
            "i",
            { style: "color: teal" },
            `${selectTable.value} 构建成功`
          ),
        });
      } else {
        console.log("构建失败", res);
        ElNotification.error({
          title: "Error",
          message: `构建失败: ${res.data}`,
        });
      }
    })
    .catch((error) => {
      console.log("请求失败", error);
      fullscreenLoading.value = false;
      ElNotification.error({
        title: "Error",
        message: `请求失败: ${error.response.data.message}`,
      });
    });
};

const startExec = () => {
  fullscreenLoading.value = true;
  console.log(selectTable.value);
  DBToolsApi.execScript({
    tableName: selectTable.value,
  })
    .then((res) => {
      if (res.status === 200) {
        fullscreenLoading.value = false;
        ElNotification({
          title: "Title",
          message: h(
            "i",
            { style: "color: teal" },
            `${selectTable.value} 执行成功`
          ),
        });
      } else {
        console.log("执行失败", res);
        ElNotification.error({
          title: "Error",
          message: `执行失败: ${res.data}`,
        });
      }
    })
    .catch((error) => {
      console.log("请求失败", error);
      fullscreenLoading.value = false;
      ElNotification.error({
        title: "Error",
        message: `请求失败: ${error.response.data.message}`,
      });
    });
};
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
