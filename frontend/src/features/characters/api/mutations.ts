import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRefOrGetter, toValue } from 'vue';

import type { CharacterDetail, CharacterUpdatePayload } from '../types/characters';
import { updateCharacter } from './api';
import { characterKeys } from './keys';

/** 更新角色信息 */
export function useUpdateCharacterMutation(id: MaybeRefOrGetter<string>) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CharacterUpdatePayload) => updateCharacter(toValue(id), payload),
    onSuccess: (detail: CharacterDetail) => {
      queryClient.setQueryData(characterKeys.detail(toValue(id)), detail);
      void queryClient.invalidateQueries({
        queryKey: characterKeys.lists(),
      });
    },
  });
}
