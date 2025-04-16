<template>
  <div>
  <input>{{ confType }}</input>
    <Children  v-model="confType"/>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Children from './Children.vue'
const confType = ref('excel')



</script>