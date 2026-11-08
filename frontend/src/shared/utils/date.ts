import dayjs from 'dayjs';

import { DATE_FORMAT } from '@/shared/constants/date';

/**
 * 格式化日期
 * @param value 日期值（Date / string / number / dayjs 对象），可为空
 * @param format 格式，默认 YYYY-MM-DD
 * @param fallback 值为空时的兜底显示
 */
export function formatDate(
  value?: dayjs.ConfigType,
  format: string = DATE_FORMAT.DATE,
  fallback = '-',
): string {
  if (value === null || value === undefined || value === '') return fallback;
  const d = dayjs(value);
  return d.isValid() ? d.format(format) : fallback;
}
