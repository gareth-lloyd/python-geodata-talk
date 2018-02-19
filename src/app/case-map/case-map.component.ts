import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-case-map',
  templateUrl: './case-map.component.html',
  styleUrls: ['./case-map.component.scss']
})
export class CaseMapComponent implements OnInit {
  styles = LOW_CONTRAST;

  constructor() { }

  ngOnInit() {
  }

}
