<script setup lang="ts">
import { NSkeleton } from 'naive-ui';
withDefaults(
  defineProps<{
    rows?: number;
  }>(),
  {
    rows: 3,
  },
);
</script>

<template>
  <div class="flex flex-col gap-3" role="status" aria-label="正在加载">
    <NSkeleton v-for="index in rows" :key="index" :height="56" :sharp="false" />
  </div>
</template>
