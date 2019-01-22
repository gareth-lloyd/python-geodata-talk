import { Component, OnInit } from '@angular/core';
import { LOW_CONTRAST } from '../map-constants';
import { ReportingService } from '../reporting.service';
import { Report } from '../report';
import { Observable } from 'rxjs/Observable';


@Component({
  selector: 'app-case-map',
  templateUrl: './case-map.component.html',
  styleUrls: ['./case-map.component.scss']
})
export class CaseMapComponent implements OnInit {
  styles = LOW_CONTRAST;
  reports: Observable<Report[]>;
  lat: number;
  lng: number;
  numReports: number;

  constructor(private reportingService: ReportingService) { }

  ngOnInit() {
    this.reports = this.reportingService.getReports();
    this.reports.subscribe(reports => {
      this.lat = reports[0].coords.latitude;
      this.lng = reports[0].coords.longitude;
      this.numReports = reports.length;
    });
  }

}
