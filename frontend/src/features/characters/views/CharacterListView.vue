<script setup lang="ts">
import { NInput, NPagination } from 'naive-ui';
import { computed, onScopeDispose, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { DEFAULT_PAGE_PARAMS } from '@/shared/constants/page';
import EmptyState from '@/shared/ui/EmptyState.vue';
import ErrorState from '@/shared/ui/ErrorState.vue';
import LoadingState from '@/shared/ui/LoadingState.vue';
import { parsePositiveInt } from '@/shared/utils/number';

import { useCharacterListQuery } from '../api/queries.ts';
import CharacterCard from '../components/CharacterCard.vue';
import type { CharacterListParams } from '../types/characters.ts';

const route = useRoute();
const router = useRouter();

const params = computed<CharacterListParams>(() => ({
  page: parsePositiveInt(route.query.page) ?? DEFAULT_PAGE_PARAMS.PAGE,
  size: parsePositiveInt(route.query.size) ?? DEFAULT_PAGE_PARAMS.PAGE_SIZE,
  keyword: typeof route.query.keyword === 'string' ? route.query.keyword : '',
}));
const { data, isPending, isError, error, refetch } = useCharacterListQuery(params);

const characters = computed(() => data.value?.items ?? []);
const total = computed(() => data.value?.total ?? 0);

const isEmpty = computed(() => !isPending.value && !isError.value && characters.value.length === 0);
const keywordDraft = ref(params.value.keyword);

let keywordTimer: ReturnType<typeof setTimeout> | undefined;

/**
 * 把角色列表的筛选参数写回 URL
 *
 * @param next 角色列表参数，包含分页信息及可选的关键词
 */
function replaceQuery(next: CharacterListParams): void {
  const query: Record<string, string> = {
    page: String(next.page),
    size: String(next.size),
  };
  if (next.keyword) query.keyword = next.keyword;
  void router.replace({ query });
}

// 监听关键词输入
watch(keywordDraft, (value) => {
  clearTimeout(keywordTimer);
  keywordTimer = setTimeout(() => {
    const keyword = value.trim();
    if (keyword === params.value.keyword) return;
    replaceQuery({
      page: 1,
      size: params.value.size,
      keyword,
    });
  }, 300);
});

// 监听 URL 中 keyword 参数的变化（如浏览器前进/后退），同步回输入框
watch(
  () => params.value.keyword,
  (newValue) => {
    if (newValue !== keywordDraft.value.trim()) {
      keywordDraft.value = newValue;
    }
  },
);

function handlePageChange(page: number): void {
  replaceQuery({
    ...params.value,
    page,
  });
}

function handleRetry(): void {
  void refetch();
}

// 销毁时取消计时器
onScopeDispose(() => {
  clearTimeout(keywordTimer);
});
</script>

<template>
  <div class="flex flex-col gap-6">
    <NInput v-model:value="keywordDraft" clearable placeholder="请输入角色名称" class="max-w-sm" />
    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" :message="error?.message" @retry="handleRetry" />
    <EmptyState v-else-if="isEmpty" description="没有匹配的角色" />
    <template v-else>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <CharacterCard v-for="character in characters" :key="character.id" :character="character" />
      </div>
      <div class="flex justify-end">
        <NPagination
          :page="params.page"
          :page-size="params.size"
          :item-count="total"
          @update-page="handlePageChange"
        />
      </div>
    </template>
  </div>
</template>
