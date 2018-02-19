export class Coords {
  public latitude: number;
  public longitude: number;
}
export class Report {
  public diagnosisOptions = {
    cholera: "Cholera",
    plague: "Plague",
    scarletfever: "Scarlet fever",
    cold: "Common cold",
    hypochondria: "Hypochondria"
  };
  public diagnosisKeys = Object.keys(this.diagnosisOptions);

  public doctorId: string;
  public doctorName: string;

  public patientId: string;
  public patientName: string;
  public diagnosis: string;
  public notes: string;
  public coords: Coords;

  toJsonApiPayload() {
    return {
      doctor_id: this.doctorId,
      doctor_name: this.doctorName,
      patient_id: this.patientId,
      patient_name: this.patientName,
      diagnosis: this.diagnosis,
      notes: this.notes,
      location: {
        latitude: this.coords.latitude,
        longitude: this.coords.longitude
      }
    }
  }
}
