<template>
<div>
  <span>{{ confType }} 配置</span>
      <el-select v-model="selectConfigCommon" placeholder="Select" size="large" style="width: 240px" @change="changeConfCommon">
          <el-option v-for="item in confDataCommon" :key="item.key" :label="item.label" :value="item.value" />
      </el-select>
</div>

</template>
    
<script setup lang="ts">
import { ref, onMounted, defineEmits } from "vue"
import { ConfigApi } from '@/api/api.js'
import _ from 'lodash';

const confType = defineModel()




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
        confDataDolphin.value = groupedAndMappedData['dolphinscheduler'] || []
        confDataCommon.value = groupedAndMappedData[confType.value] || []
        confDataJdbc.value = groupedAndMappedData['jdbc'] || []
        confDataHikapi.value = groupedAndMappedData['hikapi'] || []
        console.log(confDataCommon.value)

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