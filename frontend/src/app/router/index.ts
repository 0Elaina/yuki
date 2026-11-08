import { createRouter, createWebHistory } from 'vue-router';

import { routes } from './routes';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
  scrollBehavior() {
    return {
      top: 0,
      left: 0,
    };
  },
});

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · Yuki` : 'Yuki';
});

export default router;
