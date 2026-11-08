import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRefOrGetter, toValue } from 'vue';

import type { CharacterDetail, CharacterPayload } from '../types/characters';
import { batchDeleteCharacters, createCharacter, deleteCharacter, updateCharacter } from './api';
import { characterKeys } from './keys';

/** 更新角色信息 */
export function useUpdateCharacterMutation(id: MaybeRefOrGetter<string>) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CharacterPayload) => updateCharacter(toValue(id), payload),
    onSuccess: (detail: CharacterDetail) => {
      queryClient.setQueryData(characterKeys.detail(toValue(id)), detail);
      void queryClient.invalidateQueries({
        queryKey: characterKeys.lists(),
      });
    },
  });
}

/** 创建角色 */
export function useCreateCharacterMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CharacterPayload) => createCharacter(payload),
    onSuccess: (detail: CharacterDetail) => {
      queryClient.setQueryData(characterKeys.detail(detail.id), detail);
      void queryClient.invalidateQueries({
        queryKey: characterKeys.lists(),
      });
    },
  });
}

/** 根据 id 删除角色 */
export function useDeleteCharacterMutation(id: MaybeRefOrGetter<string>) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => deleteCharacter(toValue(id)),
    onSuccess: () => {
      queryClient.removeQueries({
        queryKey: characterKeys.detail(toValue(id)),
      });
      void queryClient.invalidateQueries({
        queryKey: characterKeys.lists(),
      });
    },
  });
}

/** 批量删除角色 */
export function useBatchDeleteCharactersMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (ids: string[]) => batchDeleteCharacters(ids),
    onSuccess: (_data, ids) => {
      for (const id of ids) {
        queryClient.removeQueries({
          queryKey: characterKeys.detail(id),
        });
      }
      void queryClient.invalidateQueries({
        queryKey: characterKeys.lists(),
      });
    },
  });
}
