import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

import { CurrentLocationService } from '../current-location.service';
import { ReportingService } from '../reporting.service';
import { Report } from '../report';
import { LOW_CONTRAST } from '../map-constants';

@Component({
  selector: 'app-reporting',
  templateUrl: './reporting.component.html',
  styleUrls: ['./reporting.component.scss']
})
export class ReportingComponent implements OnInit {
  styles = LOW_CONTRAST;
  report: Report = new Report();
  locationErrorMessage?: string = null;

  constructor(
    private reportingService: ReportingService,
    private currentLocationService: CurrentLocationService,
    private router: Router,
    public snackBar: MatSnackBar
  ) { }

  ngOnInit() {
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
