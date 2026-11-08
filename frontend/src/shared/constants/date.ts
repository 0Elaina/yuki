/** 日期格式常量，统一管理，避免各处硬编码 */
export const DATE_FORMAT = {
  /** 2024-01-05 */
  DATE: 'YYYY-MM-DD',
  /** 2024-01-05 14:30 */
  DATE_TIME: 'YYYY-MM-DD HH:mm',
  /** 01-05 */
  MONTH_DAY: 'MM-DD',
  /** 2024年01月05日 */
  DATE_CN: 'YYYY年MM月DD日',
} as const;

export type DateFormatKey = keyof typeof DATE_FORMAT;
