import { vueTsConfigs, withVueTs } from '@vue/eslint-config-typescript';
import skipFormatting from 'eslint-config-prettier/flat';
import pluginOxlint from 'eslint-plugin-oxlint';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import pluginVue from 'eslint-plugin-vue';

export default withVueTs(
  {
    name: 'app/ignores',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },

  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,cjs,vue,ts,mts,tsx}'],
  },

  // Vue 官方推荐规则，格式化类冲突由末尾的 skipFormatting 关闭。
  ...pluginVue.configs['flat/recommended'],
  // 带类型信息的 TS 规则，projectService 由该配置自行设置。
  vueTsConfigs.recommendedTypeChecked,

  {
    name: 'app/import-order',
    plugins: {
      'simple-import-sort': simpleImportSort,
    },
    rules: {
      'simple-import-sort/exports': 'error',
      'simple-import-sort/imports': 'error',
    },
  },

  {
    name: 'app/rules',
    rules: {
      // 页面入口与动态路由文件常以 index.vue、[id].vue 命名。
      'vue/multi-word-component-names': 'off',
    },
  },

  ...pluginOxlint.buildFromOxlintConfigFile('.oxlintrc.json'),

  skipFormatting,
);
