<template>
<p>common 配置</p>
    <el-select v-model="selectConfigCommon" placeholder="Select" size="large" style="width: 240px" @change="changeConfCommon">
        <el-option v-for="item in confDataCommon" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
    <p>datax 配置</p>
    <el-select v-model="selectConfig" placeholder="Select" size="large" style="width: 240px" @change="changeConfDatax">
        <el-option v-for="item in confDataDatax" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
    <p>dolphincheduler 配置</p>
    <el-select v-model="selectConfigDolphin" placeholder="Select" size="large" style="width: 240px" @change="changeConfDolphin">
        <el-option v-for="item in confDataDolphin" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
    <p>jdbc 配置</p>
    <el-select v-model="selectConfigJdbc" placeholder="Select" size="large" style="width: 240px" @change="changeConfJdbc">
        <el-option v-for="item in confDataJdbc" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
    <p>hikapi 配置</p>
    <el-select v-model="selectConfigHikapi" placeholder="Select" size="large" style="width: 240px" @change="changeConfHikapi">
        <el-option v-for="item in confDataHikapi" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
</template>
    
<script setup lang="ts">
import { ref, onMounted, defineEmits } from "vue"
import { ConfigApi } from '@/api/api.js'
import _ from 'lodash';
const selectConfig = ref()
const selectConfigDolphin = ref()
const selectConfigCommon = ref()
const selectConfigJdbc = ref()
const selectConfigHikapi = ref()
const confDataDatax = ref([
    {
        key: '1',
        value: 'Option1',
        label: 'Option1222',
    }
])
const confDataDolphin = ref([])
const confDataCommon = ref([])
const confDataJdbc = ref([])
const confDataHikapi = ref([])


const emit = defineEmits(['invoke-change-conf-datax', 'invoke-change-conf-dolphin', 'invoke-change-conf-common', 'invoke-change-conf-jdbc', 'invoke-change-conf-hikapi'])

onMounted(() => {
    ConfigApi.getConfig().then((res) => {

        const groupedAndMappedData = _.mapValues(_.groupBy(res.data, 'confType'), items =>
            _.map(items, item => ({
                value: item.confContent,
                label: item.confName
            }))
        );

        confDataDatax.value = groupedAndMappedData['datax'] || []
        console.log(confDataDatax.value)
        confDataDolphin.value = groupedAndMappedData['dolphinscheduler'] || []
        confDataCommon.value = groupedAndMappedData['common'] || []
        confDataJdbc.value = groupedAndMappedData['jdbc'] || []
        confDataHikapi.value = groupedAndMappedData['hikapi'] || []
    })
    
});


const changeConfDatax = () => {
    emit('invoke-change-conf-datax', selectConfig.value);
}

const changeConfDolphin = () => {
    emit('invoke-change-conf-dolphin', selectConfigDolphin.value);
}

const changeConfCommon = () => {
    emit('invoke-change-conf-common', selectConfigCommon.value);
}

const changeConfJdbc = () => {
    emit('invoke-change-conf-jdbc', selectConfigJdbc.value);
}

const changeConfHikapi = () => {
    console.log(`selectconf 组件 ${selectConfigHikapi.value}`)
    emit('invoke-change-conf-hikapi', selectConfigHikapi.value);
}


</script>