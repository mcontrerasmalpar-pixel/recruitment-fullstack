import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { Planeamiento } from './pages/planeamiento/planeamiento';
import { CrearRq } from './pages/planeamiento/crear-rq';
import { Reclutamiento } from './pages/reclutamiento/reclutamiento';
import { RqDetalle } from './pages/reclutamiento/rq-detalle';
import { ReclutamientoCandidatos } from './pages/reclutamiento/reclutamiento-candidatos/reclutamiento-candidatos';
import { Postular } from './pages/postular/postular';
import { Formacion } from './pages/formacion/formacion';
import { FormacionDetalle } from './pages/formacion/formacion-detalle';
import { planeamientoGuard, reclutamientoGuard, formacionGuard } from './guards/role.guard';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'planeamiento',             component: Planeamiento,             canActivate: [planeamientoGuard] },
  { path: 'planeamiento/crear-rq',    component: CrearRq,                  canActivate: [planeamientoGuard] },
  { path: 'reclutamiento',            component: Reclutamiento,            canActivate: [reclutamientoGuard] },
  { path: 'reclutamiento/rq/:codigo/candidatos', component: ReclutamientoCandidatos, canActivate: [reclutamientoGuard] },
  { path: 'reclutamiento/rq/:codigo', component: RqDetalle,                canActivate: [reclutamientoGuard] },
  { path: 'postular/:codigo',         component: Postular },
  { path: 'formacion',                component: Formacion,                canActivate: [formacionGuard] },
  { path: 'formacion/rq/:codigo',     component: FormacionDetalle,         canActivate: [formacionGuard] },
];
