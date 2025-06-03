<template>
    <div>
        <upload-excel @invoke-change-sheet="reloadConfigShow" 
            />
            <common-config-show
            ref="commonConfigRef"
            :config-api="configApi" 
        conf-type="excel" 
        dialog-title="配置编辑"
            />
    </div>
</template>
<script lang="ts" setup>
import UploadExcel from "@c/excel/uploadExcel.vue";
import CommonConfigShow from "../CommonConfigShow.vue";
import { ConfigApi } from "@/api/api.js";
import { ref } from 'vue'

const configApi = ConfigApi

const commonConfigRef = ref()

const reloadConfigShow = () => {
  commonConfigRef.value?.refreshConfData()
}

</script>

