import { request } from '@/shared/api/request';
import type { Page } from '@/shared/api/types';

import type {
  CharacterDetail,
  CharacterListParams,
  CharacterPayload,
  CharacterSummary,
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
export function updateCharacter(id: string, payload: CharacterPayload): Promise<CharacterDetail> {
  return request<CharacterDetail>({
    method: 'PUT',
    url: `/characters/${id}`,
    data: payload,
  });
}

/**
 * 创建角色
 *
 * @param payload 角色数据
 * @returns 角色详情
 */
export function createCharacter(payload: CharacterPayload): Promise<CharacterDetail> {
  return request<CharacterDetail>({
    method: 'POST',
    url: '/characters',
    data: payload,
  });
}

/**
 * 删除角色
 *
 * @param id 角色 ID
 */
export function deleteCharacter(id: string): Promise<null> {
  return request<null>({
    method: 'DELETE',
    url: `/characters/${id}`,
  });
}

export function batchDeleteCharacters(ids: string[]): Promise<null> {
  return request<null>({
    method: 'POST',
    url: '/characters/batch-delete',
    data: {
      ids,
    },
  });
}
