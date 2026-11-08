<script setup lang="ts">
import { type MenuOption, NLayout, NLayoutSider, NMenu, useThemeVars } from 'naive-ui';
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { navItems } from '../navigation/nav-item';

const route = useRoute();
const router = useRouter();
const themeVars = useThemeVars();
const menuOptions = computed<MenuOption[]>(() =>
  navItems.map((item) => ({
    label: item.label,
    key: item.routeName,
  })),
);
const activeKey = computed<string | null>(() =>
  typeof route.name === 'string' ? route.name : null,
);

function handleMenuSelect(key: string): void {
  void router.push({ name: key });
}
</script>

<template>
  <NLayout has-sider class="h-screen">
    <NLayoutSider :width="224" bordered>
      <div class="flex h-full flex-col">
        <!-- 品牌区 -->
        <div
          class="px-4 pb-3 pt-5 text-base font-semibold"
          :style="{
            color: themeVars.primaryColor,
          }"
        >
          Yuki
        </div>

        <NMenu :value="activeKey" :options="menuOptions" @update:value="handleMenuSelect" />
      </div>
    </NLayoutSider>

    <NLayout class="h-screen">
      <main class="h-full overflow-y-auto p-6">
        <slot />
      </main>
    </NLayout>
  </NLayout>
</template>
