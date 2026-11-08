export {};

declare module 'vue-router' {
  interface RouteMeta {
    layout?: 'default' | 'fullscreen';
    title?: string;
  }
}
