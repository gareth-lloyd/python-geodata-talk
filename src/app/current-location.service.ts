import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Subject } from 'rxjs/Subject';
import { Coords } from './report';

const DEFAULT_LAT: number = 51.678;
const DEFAULT_LNG: number = 0;

@Injectable()
export class CurrentLocationService {

  public currentLocationSubject: BehaviorSubject<Coords> = new BehaviorSubject(
    {longitude: DEFAULT_LNG, latitude: DEFAULT_LAT}
  );
  public locationErrorMessage: Subject<string> = new Subject<string>();

  update() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          this.currentLocationSubject.next(position.coords);
        },
        error => {
          this.locationErrorMessage.next(error.message);
        }
      );
    }
  }

}
