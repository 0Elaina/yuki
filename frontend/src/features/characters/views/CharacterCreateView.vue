<script setup lang="ts">
import { useMessage } from 'naive-ui';
import { computed, onMounted, onScopeDispose, ref } from 'vue';
import { onBeforeRouteLeave, useRouter } from 'vue-router';

import { ROUTE_NAMES } from '@/shared/constants/routes';

import { useCreateCharacterMutation } from '../api/mutations';
import CharacterForm from '../components/CharacterForm.vue';
import type { CharacterPayload } from '../types/characters';

const router = useRouter();
const message = useMessage();
const { error: createError, isPending: isCreating, mutateAsync } = useCreateCharacterMutation();
const formModel = ref<CharacterPayload>({
  name: '',
  persona: '',
});
const isDirty = computed(
  () => formModel.value.name.trim() !== '' || formModel.value.persona.trim() !== '',
);

async function handleSubmit(): Promise<void> {
  try {
    const detail = await mutateAsync({
      name: formModel.value.name.trim(),
      persona: formModel.value.persona,
    });
    formModel.value = {
      name: '',
      persona: '',
    };
    message.success('创建成功');
    void router.replace({
      name: ROUTE_NAMES.CHARACTERS_DETAIL,
      params: {
        id: detail.id,
      },
    });
  } catch {
    return;
  }
}

function handleCancel(): void {
  void router.push({
    name: ROUTE_NAMES.CHARACTERS,
  });
}

onBeforeRouteLeave(() => (isDirty.value ? window.confirm('有未保存的修改, 确定离开吗?') : true));

function handleBeforeUnload(event: BeforeUnloadEvent): void {
  if (!isDirty.value) return;
  event.preventDefault();
  event.returnValue = '';
}

onMounted(() => window.addEventListener('beforeunload', handleBeforeUnload));
onScopeDispose(() => window.removeEventListener('beforeunload', handleBeforeUnload));
</script>

<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-xl font-semibold">新建角色</h1>
    <CharacterForm
      v-model="formModel"
      :submitting="isCreating"
      :error-message="createError?.message ?? ''"
      submit-label="创建"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>
