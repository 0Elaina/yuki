import { keepPreviousData, useQuery } from '@tanstack/vue-query';
import { computed, type MaybeRefOrGetter, toValue } from 'vue';

import type { CharacterListParams } from '../types/characters';
import { fetchCharacterDetail, fetchCharacterList } from './api';
import { characterKeys } from './keys';

/** 查询角色分页列表 */
export function useCharacterListQuery(params: MaybeRefOrGetter<CharacterListParams>) {
  return useQuery({
    queryKey: computed(() => characterKeys.list(toValue(params))),
    queryFn: () => fetchCharacterList(toValue(params)),
    placeholderData: keepPreviousData,
  });
}

/** 查询角色详情 */
export function useCharacterDetailQuery(id: MaybeRefOrGetter<string>) {
  return useQuery({
    queryKey: computed(() => characterKeys.detail(toValue(id))),
    queryFn: () => fetchCharacterDetail(toValue(id)),
  });
}
