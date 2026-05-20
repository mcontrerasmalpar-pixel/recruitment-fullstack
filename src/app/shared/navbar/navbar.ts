import { Component, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar implements OnDestroy {
  isCollapsed = false;

  constructor(private router: Router, public auth: AuthService) {}

  get userName(): string {
    return this.auth.getUser()?.nombre ?? 'Usuario';
  }

  get userRole(): string {
    const role = this.auth.getRole();
    const labels: Record<string, string> = {
      admin: 'Administrador',
      planeamiento: 'Planeamiento',
      reclutamiento: 'Reclutamiento',
      formacion: 'Formación',
    };
    return role ? labels[role] : '';
  }

  toggleCollapsed(): void {
    this.isCollapsed = !this.isCollapsed;
    document.body.classList.toggle('sidebar-collapsed', this.isCollapsed);
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/']);
  }

  reportIssue(): void {
    alert('Funcionalidad de reportar problema próximamente disponible.');
  }

  ngOnDestroy(): void {
    document.body.classList.remove('sidebar-collapsed');
  }
}
