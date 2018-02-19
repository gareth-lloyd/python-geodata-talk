from rest_framework import serializers

from reporting import models as reporting_models


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = reporting_models.Report
        fields = (
            'doctor_id',
            'doctor_name',
            'patient_id',
            'patient_name',
            'diagnosis',
            'notes',
            'location',
        )
