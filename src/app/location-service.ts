import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs/Observable';
import 'rxjs/Rx';

import { Location } from './location';


@Injectable()
export class LocationService {
  public allLocations: Location[];
  private locationsByCode: {};
  private locationUrl: string = environment.server + '/api/locations/cities/';

  constructor(private http: HttpClient) {
    this.getLocations();
    this.locationsByCode = {};
    this.allLocations = new Array<Location>();
  }

  byCode(code): Location {
    return this.locationsByCode[code];
  }

  getLocations() {
    return this.http.get<Location[]>(this.locationUrl)
      .map(locationsRaw => locationsRaw.map(l => new Location().fromJSON(l)))
      .subscribe(locations => {
        locations.map(l => {
          this.locationsByCode[l.code] = l;
          this.allLocations.push(l);
        })
      })
  }

}
