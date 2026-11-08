import { request } from '@/shared/api/request';
import type { Page } from '@/shared/api/types';

import type {
  CharacterDetail,
  CharacterListParams,
  CharacterSummary,
  CharacterUpdatePayload,
} from '../types/characters';

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

/**
 * 获取角色详情
 *
 * @param id 角色 ID
 * @returns 角色详情
 */
export function fetchCharacterDetail(id: string): Promise<CharacterDetail> {
  return request<CharacterDetail>({
    method: 'GET',
    url: `/characters/${id}`,
  });
}

/**
 * 更新角色
 *
 * @param id 角色 ID
 * @param payload 更新数据
 * @returns 角色详情
 */
export function updateCharacter(
  id: string,
  payload: CharacterUpdatePayload,
): Promise<CharacterDetail> {
  return request<CharacterDetail>({
    method: 'PUT',
    url: `/characters/${id}`,
    data: payload,
  });
}
