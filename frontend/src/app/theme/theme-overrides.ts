import type { GlobalThemeOverrides } from 'naive-ui'

import { palette, type ThemePalette } from './palette'

/**
 * 把业务色板翻成 Naive 的主题覆盖。
 * 接收入参而不是直接读常量，方便以后按角色换色时只换传入的色板。
 */
export function createThemeOverrides(source: ThemePalette = palette): GlobalThemeOverrides {
  return {
    common: {
      primaryColor: source.primary,
      primaryColorHover: source.primaryHover,
      primaryColorPressed: source.primaryPressed,
      primaryColorSuppl: source.primarySuppl,
      bodyColor: source.bodyColor,
      cardColor: source.cardColor,
      borderColor: source.borderColor,
      fontFamily: source.fontFamily,
    },
  }
}
