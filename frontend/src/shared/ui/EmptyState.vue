<script setup lang="ts">
import { NEmpty } from 'naive-ui';

withDefaults(
  defineProps<{
    description?: string;
  }>(),
  {
    description: '暂无数据',
  },
);
</script>

<template>
  <div class="flex flex-col items-center justify-center px-4 py-12">
    <NEmpty :description="description">
      <template #extra>
        <slot name="action" />
      </template>
    </NEmpty>
  </div>
</template>
