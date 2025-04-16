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
const selectConfigCommon = defineModel('selectConf')
const confDataCommon = ref([])



onMounted(() => {
    ConfigApi.getConfig().then((res) => {

        const groupedAndMappedData = _.mapValues(_.groupBy(res.data, 'confType'), items =>
            _.map(items, item => ({
                value: item.confContent,
                label: item.confName
            }))
        );
        confDataCommon.value = groupedAndMappedData[confType.value] || []
    })
    
});


const changeConfCommon = () => {
    console.log(selectConfigCommon.value)
}



</script>