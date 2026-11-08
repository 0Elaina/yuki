<script setup lang="ts">
import { computed } from 'vue';
import { RouterView, useRoute } from 'vue-router';

import DefaultLayout from './app/layouts/DefaultLayout.vue';
import FullScreenLayout from './app/layouts/FullScreenLayout.vue';
import AppProviders from './app/providers/AppProviders.vue';

const route = useRoute();
const layout = computed<'default' | 'fullscreen'>(() => route.meta.layout ?? 'default');
</script>

<template>
  <AppProviders>
    <DefaultLayout v-if="layout === 'default'">
      <RouterView />
    </DefaultLayout>
    <FullScreenLayout v-else>
      <RouterView />
    </FullScreenLayout>
  </AppProviders>
</template>
