import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ReportingComponent } from './reporting/reporting.component';
import { DoctorSignInComponent } from './doctor-sign-in/doctor-sign-in.component';
import { CaseMapComponent } from './case-map/case-map.component';

const routes: Routes = [
  { path: '', redirectTo: '/doctor-sign-in', pathMatch: 'full' },
  { path: 'doctor-sign-in', component: DoctorSignInComponent },
  { path: 'reporting', component: ReportingComponent },
  { path: 'case-map', component: CaseMapComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
