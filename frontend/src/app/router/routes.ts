import type { RouteRecordRaw } from 'vue-router';

import { characterRoutes } from '@/features/characters/routes';
import { ROUTE_NAMES, ROUTE_PATHS } from '@/shared/constants/routes';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: { name: ROUTE_NAMES.CHARACTERS },
  },
  ...characterRoutes,
  {
    path: ROUTE_PATHS.NOT_FOUND,
    name: ROUTE_NAMES.NOT_FOUND,
    component: () => import('@/app/views/not-found/index.vue'),
    meta: {
      layout: 'default',
      title: '页面不存在',
    },
  },
];
