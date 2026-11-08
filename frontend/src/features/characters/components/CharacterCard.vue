<script setup lang="ts">
import { NCard, NText } from 'naive-ui';
import { computed } from 'vue';

import { DATE_FORMAT } from '@/shared/constants/date';
import { formatDate } from '@/shared/utils/date';

import type { CharacterSummary } from '../types';

const props = defineProps<{
  character: CharacterSummary;
}>();
const updatedAtText = computed(() => formatDate(props.character.updatedAt, DATE_FORMAT.DATE));
</script>

<template>
  <NCard size="small" class="h-full">
    <div class="flex flex-col gap-2">
      <span class="text-base font-medium">{{ character.name }}</span>
      <NText depth="3" class="text-xs">更新于 {{ updatedAtText }}</NText>
    </div>
  </NCard>
</template>
