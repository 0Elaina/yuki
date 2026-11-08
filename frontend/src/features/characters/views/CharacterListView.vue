<script setup lang="ts">
import { NButton, NCheckbox, NInput, NModal, NPagination, useMessage } from 'naive-ui';
import { computed, onScopeDispose, ref, watch } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';

import { isApiError } from '@/shared/api/error.ts';
import { DEFAULT_PAGE_PARAMS } from '@/shared/constants/page';
import { ROUTE_NAMES } from '@/shared/constants/routes';
import EmptyState from '@/shared/ui/EmptyState.vue';
import ErrorState from '@/shared/ui/ErrorState.vue';
import LoadingState from '@/shared/ui/LoadingState.vue';
import { parsePositiveInt } from '@/shared/utils/number';

import { useBatchDeleteCharactersMutation } from '../api/mutations.ts';
import { useCharacterListQuery } from '../api/queries';
import CharacterCard from '../components/CharacterCard.vue';
import type { CharacterListParams } from '../types/characters';

const route = useRoute();
const router = useRouter();
const message = useMessage();

const params = computed<CharacterListParams>(() => ({
  page: parsePositiveInt(route.query.page) ?? DEFAULT_PAGE_PARAMS.PAGE,
  size: parsePositiveInt(route.query.size) ?? DEFAULT_PAGE_PARAMS.PAGE_SIZE,
  keyword: typeof route.query.keyword === 'string' ? route.query.keyword : '',
}));
const { data, isPending, isError, error, refetch } = useCharacterListQuery(params);
const { isPending: isBatchDeleting, mutateAsync: batchDeleteAsync } =
  useBatchDeleteCharactersMutation();

const characters = computed(() => data.value?.items ?? []);
const total = computed(() => data.value?.total ?? 0);

const isEmpty = computed(() => !isPending.value && !isError.value && characters.value.length === 0);
const keywordDraft = ref(params.value.keyword);

const isSelecting = ref(false);
const selectedIds = ref<string[]>([]);
const isDeleteDialogVisible = ref(false);
const selectedCount = computed(() => selectedIds.value.length);
const hasSelection = computed(() => selectedIds.value.length > 0);
const allSelected = computed(
  () => characters.value.length > 0 && selectedIds.value.length === characters.value.length,
);

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

function goCreate(): void {
  void router.push({ name: ROUTE_NAMES.CHARACTERS_NEW });
}

function isSelected(id: string): boolean {
  return selectedIds.value.includes(id);
}

function enterSelecting(): void {
  isSelecting.value = true;
  selectedIds.value = [];
}

function exitSelecting(): void {
  isSelecting.value = false;
  selectedIds.value = [];
}

function toggleSelect(id: string, checked: boolean): void {
  if (checked) {
    if (!selectedIds.value.includes(id)) {
      selectedIds.value = [...selectedIds.value, id];
      return;
    }
  }
  selectedIds.value = selectedIds.value.filter((item) => item !== id);
}

function toggleSelectAll(checked: boolean): void {
  selectedIds.value = checked ? characters.value.map((item) => item.id) : [];
}

async function handleBatchDelete(): Promise<void> {
  if (selectedIds.value.length === 0) return;
  try {
    await batchDeleteAsync([...selectedIds.value]);
  } catch (error) {
    if (isApiError(error)) message.error(error.message);
    return;
  }
  isDeleteDialogVisible.value = false;
  message.success('删除成功');
  exitSelecting();
}

watch(params, () => {
  selectedIds.value = [];
});

watch(characters, (list) => {
  const ids = new Set(list.map((item) => item.id));
  selectedIds.value = selectedIds.value.filter((id) => ids.has(id));
});

// 销毁时取消计时器
onScopeDispose(() => {
  clearTimeout(keywordTimer);
});
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- 工具条 -->
    <div class="flex items-center justify-between gap-3">
      <NInput
        v-model:value="keywordDraft"
        clearable
        placeholder="请输入角色名称"
        class="max-w-sm"
      />
      <div class="flex items-center gap-2">
        <template v-if="!isSelecting">
          <NButton @click="enterSelecting">管理</NButton>
          <NButton type="primary" @click="goCreate">新建角色</NButton>
        </template>
        <template v-else>
          <NCheckbox
            :checked="allSelected"
            :indeterminate="hasSelection && !allSelected"
            @update-checked="toggleSelectAll"
            >全选</NCheckbox
          >
          <span class="text-sm">已选 {{ selectedCount }} 项</span>
          <NButton type="error" :disabled="!hasSelection" @click="isDeleteDialogVisible = true"
            >删除</NButton
          >
          <NButton @click="exitSelecting">取消</NButton>
        </template>
      </div>
    </div>

    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" :message="error?.message" @retry="handleRetry" />
    <EmptyState v-else-if="isEmpty" description="没有匹配的角色" />
    <template v-else>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <template v-for="character in characters" :key="character.id">
          <div
            v-if="isSelecting"
            class="relative cursor-pointer"
            @click="toggleSelect(character.id, !isSelected(character.id))"
          >
            <NCheckbox
              class="absolute left-3 top-3 z-10"
              :checked="isSelected(character.id)"
              @click.stop
              @update:checked="toggleSelect(character.id, $event)"
            />
            <CharacterCard :character="character" />
          </div>
          <RouterLink
            v-else
            :to="{ name: ROUTE_NAMES.CHARACTERS_DETAIL, params: { id: character.id } }"
            class="block rounded-xl focus-visible:outline-2 focus-visible:outline-offset-2"
            ><CharacterCard :character="character"
          /></RouterLink>
        </template>
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

    <NModal
      v-model:show="isDeleteDialogVisible"
      preset="dialog"
      title="批量删除"
      :content="`确定删除选中的 ${selectedCount} 个角色吗? 删除后无法恢复。`"
      positive-text="删除"
      negative-text="取消"
      :loading="isBatchDeleting"
      @positive-click="handleBatchDelete"
    />
  </div>
</template>
