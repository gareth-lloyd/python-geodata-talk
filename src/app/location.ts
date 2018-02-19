export class GeoLocation {
  public coordinates: number[];
}

export class Location {
  public code: string;
  public name: string;
  public type: string;
  public isOrign: boolean;
  public location: GeoLocation;
  public parent: Location;

  fromJSON(json: any) {
    this.code = json.code;
    this.type = json.type;
    this.name = json.name;
    this.location = json.location;
    this.isOrign = json.is_origin;

    return this;
  }
}
