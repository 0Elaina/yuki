<script setup lang="ts">
import { NButton, NResult } from 'naive-ui';
import { useRouter } from 'vue-router';

const router = useRouter();

function handleBack(): void {
  router.back();
}
</script>

<template>
  <NResult status="404" title="页面不存在" description="这个地址没有对应页面, 可能已经搬走了">
    <template #footer>
      <NButton @click="handleBack">返回上一页</NButton>
    </template>
  </NResult>
</template>
