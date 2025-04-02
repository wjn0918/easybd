<template>
    <div>
        <el-select v-model="selectType" placeholder="请选择reader" size="large">
            <el-option v-for="item in supportTypes" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <div>
            <template v-for="item in supportTypes">
                <component :is="item[selectType]">
                </component>
            </template>
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, ref, computed, defineAsyncComponent } from "vue"
import { getTemplate, DBToolsApi, ExcelApi } from '@/api/api.js'

const selectType = ref('STREAM')
const supportTypes = ref([])

const formSelect = ref(null)


onMounted(() => {
    ExcelApi.getDataxTypes().then((res) => {
        res.data['datax_reader_type'].map(item => {

            let supportT = {}
            supportT["value"] = item
            supportT["label"] = item
            supportT[item] = defineAsyncComponent(
                () => import(`./form/${item}.vue`)
            )
            supportTypes.value.push(supportT)
        });



    })
})
</script>