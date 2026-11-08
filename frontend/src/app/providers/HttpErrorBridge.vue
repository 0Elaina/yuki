<script setup lang="ts">
import { useMessage } from 'naive-ui';
import { onScopeDispose } from 'vue';

import { setErrorNotifier } from '@/shared/api/notifier';

const message = useMessage();

setErrorNotifier((text) => message.error(text));

onScopeDispose(() => {
  setErrorNotifier(null);
});
</script>

<template>
  <slot />
</template>
