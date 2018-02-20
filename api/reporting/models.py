from django.contrib.gis.db import models
from reporting import geo_utils


class Report(models.Model):
    CHOLERA = "cholera"
    SCARLET_FEVER = "scarletfever"
    TYPHOID = "typhoid"
    RUBELLA = "rubella"
    SMALLPOX = "smallpox"
    DIAGNOSIS_CHOICES = (
        (CHOLERA, "Cholera"),
        (SCARLET_FEVER, "Scarlet fever"),
        (TYPHOID, "Typhoid"),
        (RUBELLA, "Rubella"),
        (SMALLPOX, "Smallpox"),
    )
    created = models.DateTimeField(auto_now_add=True)
    doctor_id = models.CharField(max_length=64)
    doctor_name = models.CharField(max_length=128)
    patient_id = models.CharField(max_length=64)
    patient_name = models.CharField(max_length=128)

    diagnosis = models.CharField(max_length=32, choices=DIAGNOSIS_CHOICES )
    location = models.PointField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return "{} has {} at {}".format(
            self.patient_name,
            self.get_diagnosis_display(),
            self.location,
        )
