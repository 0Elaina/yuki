import type { CharacterListParams } from './types';

export const characterKeys = {
  all: ['characters'] as const,
  lists: () => [...characterKeys.all, 'list'] as const,
  list: (params: CharacterListParams) => [...characterKeys.lists(), params] as const,
};
