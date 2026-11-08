import type { GlobalThemeOverrides } from 'naive-ui';

import { palette, type ThemePalette } from './palette';

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
      popoverColor: source.popoverColor,
      inputColor: source.inputColor,
      actionColor: source.actionColor,
      borderColor: source.borderColor,
      dividerColor: source.dividerColor,
      textColorBase: source.textColorBase,
      textColor1: source.textColor1,
      textColor2: source.textColor2,
      textColor3: source.textColor3,
      placeholderColor: source.placeholderColor,
      hoverColor: source.hoverColor,
      pressedColor: source.pressedColor,
      fontFamily: source.fontFamily,
      fontFamilyMono: source.fontFamilyMono,
      fontWeightStrong: source.fontWeightStrong,
      borderRadius: source.borderRadius,
      borderRadiusSmall: source.borderRadiusSmall,
      boxShadow1: source.boxShadow1,
      boxShadow2: source.boxShadow2,
      boxShadow3: source.boxShadow3,
    },
    Button: {
      borderRadiusTiny: source.borderRadiusSmall,
      borderRadiusSmall: source.borderRadius,
      borderRadiusMedium: source.borderRadius,
      borderRadiusLarge: '10px',
      fontWeight: '500',
    },
    Card: {
      borderRadius: '12px',
      color: source.cardColor,
      borderColor: source.borderColor,
      actionColor: source.actionColor,
    },
    Input: {
      borderRadius: source.borderRadius,
      color: source.inputColor,
      colorFocus: source.inputColor,
      border: `1px solid ${source.borderColor}`,
      borderHover: `1px solid ${source.primaryHover}`,
      borderFocus: `1px solid ${source.primary}`,
    },
    Dialog: {
      borderRadius: '14px',
    },
    Tag: {
      borderRadius: '9999px',
    },
    Message: {
      borderRadius: '10px',
    },
  };
}
