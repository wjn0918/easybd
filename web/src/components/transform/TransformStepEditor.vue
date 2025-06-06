<template>
  <div>
    <draggable
      v-model="steps"
      item-key="id"
      animation="200"
      handle=".drag-handle"
    >
      <template #item="{ element, index }">
        <div
          class="step-row"
          style="
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            gap: 10px;
          "
        >
          <el-icon class="drag-handle" style="cursor: move"><Menu /></el-icon>

          <el-select
            v-model="element.action"
            placeholder="操作类型"
            style="width: 120px"
          >
            <el-option label="filter" value="filter" />
            <el-option label="assign" value="assign" />
            <el-option label="rename" value="rename" />
            <el-option label="dropna" value="dropna" />
          </el-select>

          <el-input
            v-model="element.expr"
            :placeholder="getPlaceholder(element.action)"
            style="flex: 1"
          />

          <el-button type="danger" @click="removeStep(index)">删除</el-button>
        </div>
      </template>
    </draggable>

    <el-button type="primary" @click="addStep">添加步骤</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from "vue";
import draggable from "vuedraggable";
import { ElIcon } from "element-plus";
import { Menu } from "@element-plus/icons-vue";

// props & emit
const props = defineProps<{
  modelValue: Array<{ action: string; expr: string }>;
}>();
const emit = defineEmits(["update:modelValue"]);

// 内部数据（添加唯一 id 支持 draggable key）
const steps = ref(
  props.modelValue.map((item, i) => ({ ...item, id: i + "_" + Date.now() }))
);

// 双向绑定
watch(
  () => props.modelValue,
  (newVal) => {
    steps.value = newVal.map((item, i) => ({
      ...item,
      id: i + "_" + Date.now(),
    }));
  },
  { deep: true }
);

watch(
  steps,
  (newSteps) => {
    emit(
      "update:modelValue",
      newSteps.map(({ id, action, expr }) => {
        let parsedExpr: any = expr;
        if (action === "rename" || action === "dropna") {
          try {
            parsedExpr = JSON.parse(expr);
          } catch (e) {
            // fallback to string if parse fails
            parsedExpr = expr;
          }
        }
        return { action, expr: parsedExpr };
      })
    );
  },
  { deep: true }
);

// 添加 & 删除
const addStep = () => {
  steps.value.push({
    action: "filter",
    expr: "",
    id: Date.now() + "_" + Math.random(),
  });
};

const removeStep = (index: number) => {
  steps.value.splice(index, 1);
};

const getPlaceholder = (action: string) => {
  switch (action) {
    case "filter":
      return "如：df['age'] > 30";
    case "assign":
      return "如：df['group'] = df['age'] // 10 * 10";
    case "rename":
      return `如：{"old_name": "new_name"}  注意使用双引号`;
    case "dropna":
      return "如：['email', 'phone']";
    default:
      return "请输入表达式";
  }
};
</script>
