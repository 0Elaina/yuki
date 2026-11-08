import type { RouteRecordRaw } from 'vue-router';

export const characterRoutes: RouteRecordRaw[] = [
  {
    path: '/characters',
    name: 'characters',
    component: () => import('@/features/characters/views/CharacterListView.vue'),
    meta: {
      layout: 'default',
      title: '角色',
    },
  },
];
