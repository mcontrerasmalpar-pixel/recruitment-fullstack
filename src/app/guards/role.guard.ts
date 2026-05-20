import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.isLoggedIn()) {
    router.navigate(['/']);
    return false;
  }
  return true;
};

export const planeamientoGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.isLoggedIn()) { router.navigate(['/']); return false; }
  if (!auth.canAccess('planeamiento')) { router.navigate([auth.getHomeRoute()]); return false; }
  return true;
};

export const reclutamientoGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.isLoggedIn()) { router.navigate(['/']); return false; }
  if (!auth.canAccess('reclutamiento')) { router.navigate([auth.getHomeRoute()]); return false; }
  return true;
};

export const formacionGuard: CanActivateFn = (route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (!auth.isLoggedIn()) { router.navigate(['/']); return false; }
  if (!auth.canAccess('formacion')) { router.navigate([auth.getHomeRoute()]); return false; }
  return true;
};
