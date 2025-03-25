<template>
    <el-form :model="form" label-width="auto" style="max-width: 600px">
      <el-form-item label="host:port">
        <el-input v-model="form.host" />
      </el-form-item>

      <el-form-item label="appKey">
        <el-input v-model="form.appKey" />
      </el-form-item>

      <el-form-item label="appSecret">
        <el-input v-model="form.appSecret" />
      </el-form-item>

      <el-form-item label="headers">
        <el-input v-model="form.headers" type="textarea" />
      </el-form-item>

      <el-form-item label="body">
        <el-input v-model="form.body" type="textarea" />
      </el-form-item>

    </el-form>
  </template>
  
  <script setup lang="ts" >
  import { reactive } from 'vue'
  
  // do not use same name with ref
  const form = reactive({
    host: '172.23.0.253:4431',
    appKey: '20894672',
    appSecret: 'I4MiMmJZupQWr2p5Yq82',
    headers: `{}`,
    body: `{
              pageNo: 1,
              pageSize: 1000,
            }`
  })
  

  </script>
  