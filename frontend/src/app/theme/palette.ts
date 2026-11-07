export interface ThemePalette {
  primary: string
  primaryHover: string
  primaryPressed: string
  primarySuppl: string
  bodyColor: string
  cardColor: string
  popoverColor: string
  inputColor: string
  actionColor: string
  borderColor: string
  dividerColor: string
  textColorBase: string
  textColor1: string
  textColor2: string
  textColor3: string
  placeholderColor: string
  hoverColor: string
  pressedColor: string
  fontFamily: string
  fontFamilyMono: string
  fontWeightStrong: string
  borderRadius: string
  borderRadiusSmall: string
  boxShadow1: string
  boxShadow2: string
  boxShadow3: string
}

export const palette: ThemePalette = {
  // 长春花蓝，白字对比度约 4.8:1
  primary: '#5A6FB8',
  // 同色相压暗 14%，用于 hover
  primaryHover: '#4D5F9E',
  // 再压暗一档，用于 pressed
  primaryPressed: '#425288',
  // 与 hover 同值，Naive 在部分强调场景使用
  primarySuppl: '#4D5F9E',

  // 暖白底与承载面
  bodyColor: '#FAF8F4',
  cardColor: '#FFFDF8',
  popoverColor: '#FFFDF8',
  inputColor: '#FFFDFA',
  actionColor: '#F2EDE4',
  borderColor: '#E8E2D8',
  dividerColor: '#EDE7DD',

  // 文本四档与占位符，基于同一暖黑
  textColorBase: '#2B2722',
  textColor1: 'rgba(43, 39, 34, 0.9)',
  textColor2: 'rgba(43, 39, 34, 0.68)',
  textColor3: 'rgba(43, 39, 34, 0.5)',
  placeholderColor: 'rgba(43, 39, 34, 0.38)',
  hoverColor: 'rgba(43, 39, 34, 0.05)',
  pressedColor: 'rgba(43, 39, 34, 0.08)',

  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif`,
  fontFamilyMono: `'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace`,
  fontWeightStrong: '600',

  borderRadius: '8px',
  borderRadiusSmall: '4px',

  boxShadow1: '0 1px 2px rgba(43, 39, 34, 0.06)',
  boxShadow2: '0 4px 12px rgba(43, 39, 34, 0.08)',
  boxShadow3: '0 8px 24px rgba(43, 39, 34, 0.12)',
}
