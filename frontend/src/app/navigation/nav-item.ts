import { ROUTE_NAMES } from '@/shared/constants/routes';

export interface NavItem {
  label: string;
  routeName: string;
}

export const navItems: NavItem[] = [
  {
    label: '角色',
    routeName: ROUTE_NAMES.CHARACTERS,
  },
];
