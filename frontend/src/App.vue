<script setup lang="ts">
import { RouterView } from 'vue-router'

import AppProviders from '@/app/providers/AppProviders.vue'
</script>

<template>
  <AppProviders>
    <RouterView />
  </AppProviders>
</template>
