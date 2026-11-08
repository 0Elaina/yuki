export const ROUTE_NAMES = {
  NOT_FOUND: 'not-found',
  CHARACTERS: 'characters',
  CHARACTERS_NEW: 'characters-new',
  CHARACTERS_DETAIL: 'characters-detail',
} as const;

export const ROUTE_PATHS = {
  NOT_FOUND: '/:pathMatch(.*)*',
  CHARACTERS: '/characters',
  CHARACTERS_NEW: '/characters/new',
  CHARACTERS_DETAIL: '/characters/:id(\\d+)',
} as const;
