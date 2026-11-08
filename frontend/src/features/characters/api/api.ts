import { request } from '@/shared/api/request';
import type { Page } from '@/shared/api/types';

import type { CharacterListParams, CharacterSummary } from '../types';

/**
 * 获取角色列表
 *
 * @param params 查询参数
 * @returns 角色列表
 */
export function fetchCharacterList(params: CharacterListParams): Promise<Page<CharacterSummary>> {
  return request<Page<CharacterSummary>>({
    method: 'GET',
    url: '/characters',
    params: {
      page: params.page,
      size: params.size,
      keyword: params.keyword || undefined,
    },
  });
}
