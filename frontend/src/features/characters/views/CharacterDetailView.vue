<script setup lang="ts">
import {
  type FormInst,
  type FormRules,
  NAlert,
  NButton,
  NForm,
  NFormItem,
  NInput,
  NText,
  useMessage,
} from 'naive-ui';
import { computed, onMounted, onScopeDispose, reactive, ref } from 'vue';
import { onBeforeRouteLeave, useRoute, useRouter } from 'vue-router';

import { isApiError } from '@/shared/api/error';
import { DATE_FORMAT } from '@/shared/constants/date';
import { ROUTE_NAMES } from '@/shared/constants/routes';
import EmptyState from '@/shared/ui/EmptyState.vue';
import ErrorState from '@/shared/ui/ErrorState.vue';
import LoadingState from '@/shared/ui/LoadingState.vue';
import { formatDate } from '@/shared/utils/date';

import { useUpdateCharacterMutation } from '../api/mutations';
import { useCharacterDetailQuery } from '../api/queries';
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
const isNotFound = computed(
  () => isApiError(error.value) && error.value.code === CHARACTERS_CODE.CHARACTER_NOT_FOUND,
);
const isEditing = ref(false);

const formRef = ref<FormInst | null>(null);
const formModel = reactive<CharacterPayload>({
  name: '',
  persona: '',
});
const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入角色名称',
      trigger: ['blur', 'input'],
    },
    {
      max: 100,
      message: '角色名称不能超过100个字符',
      trigger: ['blur', 'input'],
    },
    {
      validator: (_, value: string) => {
        if (!value || value.trim().length === 0) {
          return Promise.reject(new Error('角色名称不能为空'));
        }
        return Promise.resolve();
      },
      trigger: ['blur', 'input'],
    },
  ],
  persona: [
    {
      max: 20000,
      message: '人设最多 20000 个字符',
      trigger: ['blur', 'input'],
    },
  ],
};

const isDirty = computed(
  () =>
    isEditing.value &&
    data.value !== undefined &&
    (formModel.name !== data.value.name || formModel.persona !== data.value.persona),
);

function startEdit(): void {
  if (!data.value) return;
  reset();
  formModel.name = data.value.name;
  formModel.persona = data.value.persona;
  isEditing.value = true;
}

function cancelEdit(): void {
  isEditing.value = false;
}

async function handleSave(): Promise<void> {
  if (formRef.value === null) return;
  try {
    await formRef.value.validate();
  } catch {
    return;
  }
  try {
    await mutateAsync({
      name: formModel.name.trim(),
      persona: formModel.persona,
    });
  } catch {
    return;
  }
  message.success('保存成功');
  isEditing.value = false;
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
    <NForm
      v-else-if="isEditing && data"
      ref="formRef"
      :model="formModel"
      :rules="formRules"
      label-placement="top"
    >
      <NFormItem label="角色名称" path="name">
        <NInput
          v-model:value="formModel.name"
          :maxlength="100"
          show-count
          placeholder="请输入角色名称"
        />
      </NFormItem>
      <NFormItem label="角色人设" path="persona">
        <NInput
          v-model:value="formModel.persona"
          type="textarea"
          :maxlength="20000"
          show-count
          :autosize="{ minRows: 6, maxRows: 20 }"
          placeholder="身份、性格与背景设定"
        />
      </NFormItem>
      <NAlert v-if="saveError" type="error" :title="saveError.message" class="mb-4" />
      <div class="flex gap-3">
        <NButton type="primary" :loading="isSaving" @click="handleSave">保存</NButton>
        <NButton :disabled="isSaving" @click="cancelEdit">取消</NButton>
      </div>
    </NForm>
    <template v-else-if="data">
      <!-- 标题行 -->
      <div class="flex items-center justify-between gap-4">
        <h1 class="text-xl font-semibold">{{ data.name }}</h1>
        <div class="flex items-center gap-2">
          <NButton type="primary" @click="startEdit">编辑</NButton>
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
