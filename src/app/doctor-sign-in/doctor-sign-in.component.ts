import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UUID } from 'angular2-uuid';

import { ReportingService } from '../reporting.service';

@Component({
  selector: 'app-doctor-sign-in',
  templateUrl: './doctor-sign-in.component.html',
  styleUrls: ['./doctor-sign-in.component.scss']
})
export class DoctorSignInComponent {
  doctorId: string = UUID.UUID().slice(0, 16);
  doctorName: string;

  constructor(
    private reportingService: ReportingService,
    private router: Router
  ) { }

  submit(): void {
    this.reportingService.signInDoctor(this.doctorId, this.doctorName);
    this.router.navigate(['reporting']);
  }

}
