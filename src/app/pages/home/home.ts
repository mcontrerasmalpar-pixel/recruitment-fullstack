import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  username = '';
  password = '';
  isRegisterMode = false;
  isVerificationMode = false;
  dni = '';
  nombre = '';
  apellido = '';
  correo = '';
  newPassword = '';
  confirmPassword = '';
  verificationCode = '';

  loginError = false;

  constructor(private router: Router, private auth: AuthService) {}

  login() {
    this.loginError = false;
    if (this.auth.login(this.username, this.password)) {
      this.router.navigate([this.auth.getHomeRoute()]);
    } else {
      this.loginError = true;
    }
  }

  register() {
    if (this.dni.trim() && this.dni.length === 8 && this.nombre.trim() && this.apellido.trim() && this.correo.trim() && this.newPassword.trim() && this.newPassword === this.confirmPassword) {
      // Simular envío de código
      this.isVerificationMode = true;
      this.isRegisterMode = false;
    }
  }

  verifyCode() {
    if (this.verificationCode.trim() && this.verificationCode.length === 6) {
      // Simular verificación exitosa
      this.switchToLogin();
    }
  }

  switchToRegister() {
    this.isRegisterMode = true;
    this.isVerificationMode = false;
    this.resetFields();
  }

  switchToLogin() {
    this.isRegisterMode = false;
    this.isVerificationMode = false;
    this.resetFields();
  }

  private resetFields() {
    this.username = '';
    this.password = '';
    this.dni = '';
    this.nombre = '';
    this.apellido = '';
    this.correo = '';
    this.newPassword = '';
    this.confirmPassword = '';
    this.verificationCode = '';
  }

  isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}