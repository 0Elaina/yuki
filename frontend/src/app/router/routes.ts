import type { RouteRecordRaw } from 'vue-router';

import { characterRoutes } from '@/features/characters/routes';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: { name: 'characters' },
  },
  ...characterRoutes,
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/app/views/not-found/index.vue'),
    meta: {
      layout: 'default',
      title: '页面不存在',
    },
  },
];
