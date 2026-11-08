export const SUCCESS_CODE = 'SUCCESS';

export interface ApiResponse<T> {
  data: T;
  code: string;
  message: string;
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PageQuery {
  page?: number;
  size?: number;
}
