import { Injectable } from '@angular/core';

export type UserRole = 'admin' | 'planeamiento' | 'reclutamiento' | 'formacion';

export interface User {
  username: string;
  nombre: string;
  role: UserRole;
}

const USERS: User[] = [
  { username: 'admin',         nombre: 'Administrador',  role: 'admin' },
  { username: 'planeamiento',  nombre: 'María Torres',   role: 'planeamiento' },
  { username: 'reclutamiento', nombre: 'Carlos Ruiz',    role: 'reclutamiento' },
  { username: 'formacion',     nombre: 'Ana Gómez',      role: 'formacion' },
];

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser: User | null = null;

  login(username: string, password: string): boolean {
    if (!password.trim()) return false;
    const user = USERS.find(u => u.username === username.toLowerCase().trim());
    if (user) {
      this.currentUser = user;
      sessionStorage.setItem('currentUser', JSON.stringify(user));
      return true;
    }
    return false;
  }

  logout(): void {
    this.currentUser = null;
    sessionStorage.removeItem('currentUser');
  }

  getUser(): User | null {
    if (this.currentUser) return this.currentUser;
    const stored = sessionStorage.getItem('currentUser');
    if (stored) {
      this.currentUser = JSON.parse(stored);
      return this.currentUser;
    }
    return null;
  }

  isLoggedIn(): boolean {
    return this.getUser() !== null;
  }

  getRole(): UserRole | null {
    return this.getUser()?.role ?? null;
  }

  canAccess(section: 'planeamiento' | 'reclutamiento' | 'formacion'): boolean {
    const role = this.getRole();
    if (role === 'admin') return true;
    return role === section;
  }

  getHomeRoute(): string {
    const role = this.getRole();
    if (role === 'admin' || role === 'planeamiento') return '/planeamiento';
    if (role === 'reclutamiento') return '/reclutamiento';
    if (role === 'formacion') return '/formacion';
    return '/';
  }
}
