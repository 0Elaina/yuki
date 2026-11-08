<script setup lang="ts">
import { type FormInst, type FormRules, NAlert, NButton, NForm, NFormItem, NInput } from 'naive-ui';
import { ref } from 'vue';

import { type CharacterPayload } from '../types/characters';

const model = defineModel<CharacterPayload>({
  required: true,
});
const props = withDefaults(
  defineProps<{
    submitting?: boolean;
    submitLabel?: string;
    errorMessage?: string;
  }>(),
  {
    submitting: false,
    submitLabel: '保存',
    errorMessage: '',
  },
);
const emit = defineEmits<{
  submit: [];
  cancel: [];
}>();

const formRef = ref<FormInst | null>(null);
const formRules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入角色名称',
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

async function handleSubmit(): Promise<void> {
  if (formRef.value === null) return;
  try {
    await formRef.value.validate();
  } catch {
    return;
  }
  emit('submit');
}
</script>

<template>
  <NForm ref="formRef" :model="model" :rules="formRules" label-placement="top">
    <NFormItem label="角色名称" path="name">
      <NInput v-model:value="model.name" :maxlength="100" show-count placeholder="请输入角色名称" />
    </NFormItem>
    <NFormItem label="角色人设" path="persona">
      <NInput
        v-model:value="model.persona"
        type="textarea"
        :maxlength="20000"
        show-count
        :autosize="{ minRows: 6, maxRows: 20 }"
        placeholder="身份、性格与背景设定"
      />
    </NFormItem>
    <NAlert v-if="props.errorMessage" type="error" :title="props.errorMessage" class="mb-4" />
    <div class="flex gap-3">
      <NButton type="primary" :loading="props.submitting" @click="handleSubmit">
        {{ props.submitLabel }}
      </NButton>
      <NButton :disabled="props.submitting" @click="emit('cancel')"> 取消 </NButton>
    </div>
  </NForm>
</template>
