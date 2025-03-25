<template>
    <div>
        <select-conf @invoke-change-conf="changeConf"></select-conf>
    </div>

</template>

<script setup lang="ts">

import selectConf from '@c/configCenter/selectConf/index.vue'


const changeConf =(confContent)=>{
    console.log(confContent)
}

</script>