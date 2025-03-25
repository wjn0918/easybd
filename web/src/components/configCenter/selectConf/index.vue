<template>
    <p>datax 配置</p>
    <el-select v-model="selectConfig" placeholder="Select" size="large" style="width: 240px" @change="changeConfDatax">
        <el-option v-for="item in confDataDatax" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
    <p>dolphincheduler 配置</p>
    <el-select v-model="selectConfigDolphin" placeholder="Select" size="large" style="width: 240px" @change="changeConfDolphin">
        <el-option v-for="item in confDataDolphin" :key="item.key" :label="item.label" :value="item.value" />
    </el-select>
</template>
    
<script setup lang="ts">
import { ref, onMounted, defineEmits } from "vue"
import { ConfigApi } from '@/api/api.js'
import _ from 'lodash';
const selectConfig = ref()
const selectConfigDolphin = ref()
const confDataDatax = ref([
    {
        key: '1',
        value: 'Option1',
        label: 'Option1',
    }
])
const confDataDolphin = ref([])

const emit = defineEmits(['invoke-change-conf-datax', 'invoke-change-conf-dolphin'])

onMounted(() => {
    ConfigApi.getConfig().then((res) => {

        const groupedAndMappedData = _.mapValues(_.groupBy(res.data, 'conf_type'), items =>
            _.map(items, item => ({
                value: item.conf_content,
                label: item.conf_name
            }))
        );

        confDataDatax.value = groupedAndMappedData['datax'] || []
        confDataDolphin.value = groupedAndMappedData['dolphinscheduler'] || []
    })
    
});


const changeConfDatax = () => {
    emit('invoke-change-conf-datax', selectConfig.value);
}

const changeConfDolphin = () => {
    emit('invoke-change-conf-dolphin', selectConfigDolphin.value);
}



</script>