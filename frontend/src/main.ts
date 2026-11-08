import '@/app/styles/main.css';

import { VueQueryPlugin } from '@tanstack/vue-query';
import { createPinia } from 'pinia';
import { createApp } from 'vue';

import { queryClient } from '@/app/query/client';

import App from './App.vue';
import router from './app/router/index.ts';

const app = createApp(App);

app.use(createPinia());
app.use(VueQueryPlugin, { queryClient });
app.use(router);

app.mount('#app');
