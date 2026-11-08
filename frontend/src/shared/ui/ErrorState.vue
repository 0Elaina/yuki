<script setup lang="ts">
import { NButton, NResult } from 'naive-ui';

withDefaults(
  defineProps<{
    title?: string;
    message?: string;
  }>(),
  {
    title: '加载失败',
    message: '请稍候重试',
  },
);

const emit = defineEmits<{
  retry: [];
}>();
</script>

<template>
  <div class="flex flex-col items-center justify-center px-4 py-12" role="alert">
    <NResult status="error" :title="title" :description="message">
      <template #footer>
        <NButton size="small" @click="emit('retry')">重试</NButton>
      </template>
    </NResult>
  </div>
</template>
