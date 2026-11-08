<script setup lang="ts">
import { NButton, NPopconfirm, NText, useMessage } from 'naive-ui';
import { computed, onMounted, onScopeDispose, ref } from 'vue';
import { onBeforeRouteLeave, useRoute, useRouter } from 'vue-router';

import { isApiError } from '@/shared/api/error';
import { DATE_FORMAT } from '@/shared/constants/date';
import { ROUTE_NAMES } from '@/shared/constants/routes';
import EmptyState from '@/shared/ui/EmptyState.vue';
import ErrorState from '@/shared/ui/ErrorState.vue';
import LoadingState from '@/shared/ui/LoadingState.vue';
import { formatDate } from '@/shared/utils/date';

import { useDeleteCharacterMutation, useUpdateCharacterMutation } from '../api/mutations';
import { useCharacterDetailQuery } from '../api/queries';
import CharacterForm from '../components/CharacterForm.vue';
import { CHARACTERS_CODE } from '../constants/characters-code';
import type { CharacterPayload } from '../types/characters';

const route = useRoute();
const router = useRouter();
const message = useMessage();

const id = computed(() => String(route.params.id));
const { data, isPending, isError, error, refetch } = useCharacterDetailQuery(id);
const {
  error: saveError,
  isPending: isSaving,
  mutateAsync,
  reset,
} = useUpdateCharacterMutation(id);
const { isPending: isDeleting, mutateAsync: deleteAsync } = useDeleteCharacterMutation(id);

const isNotFound = computed(
  () => isApiError(error.value) && error.value.code === CHARACTERS_CODE.CHARACTER_NOT_FOUND,
);
const isEditing = ref(false);

const formModel = ref<CharacterPayload>({
  name: '',
  persona: '',
});

const isDirty = computed(
  () =>
    isEditing.value &&
    data.value !== undefined &&
    (formModel.value.name !== data.value.name || formModel.value.persona !== data.value.persona),
);

function startEdit(): void {
  if (!data.value) return;
  reset();
  formModel.value.name = data.value.name;
  formModel.value.persona = data.value.persona;
  isEditing.value = true;
}

function cancelEdit(): void {
  isEditing.value = false;
}

async function handleSave(): Promise<void> {
  try {
    await mutateAsync({
      name: formModel.value.name.trim(),
      persona: formModel.value.persona,
    });
  } catch {
    return;
  }
  message.success('保存成功');
  isEditing.value = false;
}

async function handleDelete(): Promise<void> {
  try {
    await deleteAsync();
  } catch (err) {
    if (isApiError(err)) message.error(err.message);
    return;
  }
  message.success('删除成功');
  backToList();
}

function handleRetry(): void {
  void refetch();
}

function backToList(): void {
  void router.push({ name: ROUTE_NAMES.CHARACTERS });
}

onBeforeRouteLeave(() => (isDirty.value ? window.confirm('有未保存的修改, 确定离开吗?') : true));

function handleBeforeUnload(event: BeforeUnloadEvent): void {
  if (!isDirty.value) return;
  event.preventDefault();
  event.returnValue = '';
}

onMounted(() => window.addEventListener('beforeunload', handleBeforeUnload));
onScopeDispose(() => window.removeEventListener('beforeunload', handleBeforeUnload));

const createdAtText = computed(() => {
  if (!data.value) return '';
  return formatDate(data.value.createdAt, DATE_FORMAT.DATE_TIME);
});
const updatedAtText = computed(() => {
  if (!data.value) return '';
  return formatDate(data.value.updatedAt, DATE_FORMAT.DATE_TIME);
});
</script>

<template>
  <div class="flex flex-col gap-6">
    <LoadingState v-if="isPending" />
    <EmptyState v-else-if="isNotFound" description="角色不存在">
      <template #action>
        <NButton @click="backToList">返回列表</NButton>
      </template>
    </EmptyState>
    <ErrorState v-else-if="isError" :message="error?.message" @retry="handleRetry" />
    <CharacterForm
      v-if="isEditing && data"
      v-model="formModel"
      :submitting="isSaving"
      :error-message="saveError?.message ?? ''"
      @submit="handleSave"
      @cancel="cancelEdit"
    />
    <template v-else-if="data">
      <!-- 标题行 -->
      <div class="flex items-center justify-between gap-4">
        <h1 class="text-xl font-semibold">{{ data.name }}</h1>
        <div class="flex items-center gap-2">
          <NButton type="primary" @click="startEdit">编辑</NButton>
          <NPopconfirm positive-text="删除" negative-text="取消" @positive-click="handleDelete">
            <template #trigger>
              <NButton type="error" :loading="isDeleting">删除</NButton>
            </template>
            删除后无法恢复, 确定删除「{{ data.name }}」吗?
          </NPopconfirm>
          <NButton @click="backToList">返回列表</NButton>
        </div>
      </div>

      <!-- 人设区 -->
      <p class="whitespace-pre-wrap text-sm leading-6">
        {{ data.persona || '暂无人设' }}
      </p>

      <!-- 时间行 -->
      <div class="flex gap-4 text-xs">
        <NText depth="3">创建于 {{ createdAtText }}</NText>
        <NText depth="3">更新于 {{ updatedAtText }}</NText>
      </div>
    </template>
  </div>
</template>
