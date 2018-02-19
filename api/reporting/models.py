from django.contrib.gis.db import models


class Report(models.Model):
    DIAGNOSIS_CHOICES = (
        ("cholera", "Cholera"),
        ("plague", "Plague"),
        ("scarletfever", "Scarlet fever"),
        ("cold", "Common cold"),
        ("hypochondria", "Hypochondria"),
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
