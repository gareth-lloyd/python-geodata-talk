import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RequestOptionsArgs } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/Rx';

import { environment } from '../environments/environment';
import { Report } from './report';


@Injectable()
export class ReportingService {
  private url: string = environment.server + '/api/reports/';
  private doctorId: string;
  private doctorName: string;

  constructor(private http: HttpClient) { }

  getReports() : Observable<Report[]> {
    return this.http.get<Report[]>(this.url)
      .map(reportsRaw => reportsRaw.map(r => new Report().fromJsonApiPayload(r)))
  }

  makeReport(report: Report) : Observable<Object> {
    report.doctorId = this.doctorId;
    report.doctorName = this.doctorName;
    return this.http.post<Object>(this.url, report.toJsonApiPayload());
  }

  signInDoctor(doctorId: string, doctorName: string): void {
    this.doctorId = doctorId;
    this.doctorName = doctorName;
  }
}
