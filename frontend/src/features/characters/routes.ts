import type { RouteRecordRaw } from 'vue-router';

import { ROUTE_NAMES, ROUTE_PATHS } from '@/shared/constants/routes';

export const characterRoutes: RouteRecordRaw[] = [
  {
    path: ROUTE_PATHS.CHARACTERS,
    name: ROUTE_NAMES.CHARACTERS,
    component: () => import('@/features/characters/views/CharacterListView.vue'),
    meta: {
      layout: 'default',
      title: '角色',
    },
  },
  {
    path: ROUTE_PATHS.CHARACTERS_DETAIL,
    name: ROUTE_NAMES.CHARACTERS_DETAIL,
    component: () => import('@/features/characters/views/CharacterDetailView.vue'),
    meta: {
      layout: 'default',
      title: '角色详情',
    },
  },
];
