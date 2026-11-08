/** 将任意值安全解析为正整数（>=1） */
export function parsePositiveInt(value: unknown): number | null {
  if (typeof value !== 'string') return null;
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed < 1) return null;
  return parsed;
}
