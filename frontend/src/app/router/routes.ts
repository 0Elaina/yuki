import type { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/not-found/index.vue'),
    meta: {
      layout: 'default',
      title: '页面不存在',
    },
  },
];
