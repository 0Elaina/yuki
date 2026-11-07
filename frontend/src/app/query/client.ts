import { QueryClient } from '@tanstack/vue-query'

const STALE_TIME_MS = 30_000

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: STALE_TIME_MS,
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: false,
    },
  },
})
