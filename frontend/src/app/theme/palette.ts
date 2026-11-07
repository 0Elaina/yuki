export interface ThemePalette {
  primary: string
  primaryHover: string
  primaryPressed: string
  primarySuppl: string
  bodyColor: string
  cardColor: string
  borderColor: string
  fontFamily: string
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
  // 暖白底与卡片色
  bodyColor: '#FAF8F4',
  cardColor: '#FFFDF8',
  borderColor: '#E8E2D8',
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', sans-serif`,
}
