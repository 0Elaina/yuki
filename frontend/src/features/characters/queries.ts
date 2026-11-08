import { keepPreviousData, useQuery } from '@tanstack/vue-query';
import { computed, type MaybeRefOrGetter, toValue } from 'vue';

import { fetchCharacterList } from './api';
import { characterKeys } from './keys';
import type { CharacterListParams } from './types';

/** 查询角色分页列表 */
export function useCharacterListQuery(params: MaybeRefOrGetter<CharacterListParams>) {
  return useQuery({
    queryKey: computed(() => characterKeys.list(toValue(params))),
    queryFn: () => fetchCharacterList(toValue(params)),
    placeholderData: keepPreviousData,
  });
}
