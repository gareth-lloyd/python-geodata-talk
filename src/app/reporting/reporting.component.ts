import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UUID } from 'angular2-uuid';

import { CurrentLocationService } from '../current-location.service';
import { ReportingService } from '../reporting.service';
import { Report } from '../report';

@Component({
  selector: 'app-reporting',
  templateUrl: './reporting.component.html',
  styleUrls: ['./reporting.component.scss']
})
export class ReportingComponent implements OnInit {
  report: Report = new Report();
  locationErrorMessage?: string = null;

  constructor(
    private reportingService: ReportingService,
    public currentLocationService: CurrentLocationService,
    private router: Router
  ) {
    this.report.patientId = UUID.UUID().slice(0, 16);
  }

  ngOnInit() {
    if(!this.reportingService.doctorId) {
      this.router.navigate([''])
    }
    this.currentLocationService.currentLocationSubject.subscribe(coords => {
      this.report.coords = coords;
      this.locationErrorMessage = null;
    });
    this.currentLocationService.locationErrorMessage.subscribe(
      message => {
        this.locationErrorMessage = "Could not determine location";
      }
    )
    this.currentLocationService.update();
  }

  submit() {
    this.reportingService.makeReport(this.report).subscribe(
      response => this.router.navigate(['case-map'])
    )
  }
}
