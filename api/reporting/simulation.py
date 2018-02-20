from datetime import date, datetime, time
import random

import names
from uuid import uuid1

from django.contrib.gis import geos
from django.utils.timezone import make_aware

from reporting.models import Report

DIAGNOSES = [choice[0] for choice in Report.DIAGNOSIS_CHOICES]

# Bounding box
NORTH = 51.5370076789
SOUTH = 51.4899732829
EAST = -0.0795342546329
WEST = -0.174670186257

APPROX_100_M = 0.0005
APPROX_500_M = 0.0025

HOSPITALS = {
    "National Hospital for Neurology and Neurosurgery":	(-0.1223623, 51.5222325),
    "The Hoxton Surgery": (-0.0867676, 51.5334946),
    "Other": (-0.1505685, 51.5201916),
    "Cambian Churchill": (-0.1097437, 51.4971506),
    "Wimpole Dental": (-0.1480978, 51.5183824),
}


OUTBREAK = (-0.136677, 51.513283)


def random_diagnosis(weights=None):
    return random.choice(DIAGNOSES)


def create_uniform_point_field(x1, y1, x2, y2, n):
    """
    Generate n points equally likely to lie anywhere in a bounding box
    """

    return [
        (random.uniform(x1, x2), random.uniform(y1, y2))
        for _ in range(n)
    ]


def create_gaussian_point_cluster(x, y, sigma, n):
    """
    Generate n points clustered around x, y with normal distribution
    """
    return [
        (random.gauss(x, sigma), random.gauss(y, sigma))
        for _ in range(n)
    ]


def normal_day():
    cases = random.randint(6, 12)
    points = create_uniform_point_field(
        WEST, NORTH, EAST, SOUTH, n=cases,
    )
    for hospital_coords in HOSPITALS.values():
        cases = random.randint(10, 12)
        points.extend(create_gaussian_point_cluster(
            x=hospital_coords[0], y=hospital_coords[1],
            sigma=APPROX_100_M, n=cases
        ))

    reports = []
    for coords in points:
        reports.append(Report(
            diagnosis=random_diagnosis(),
            doctor_name=names.get_full_name(),
            doctor_id=uuid1(),
            patient_name=names.get_full_name(),
            patient_id=uuid1(),
            location=geos.Point(*coords),
        ))
    Report.objects.bulk_create(reports)


def outbreak(x, y, disease, min_n, max_n, sigma):
    cases = random.randint(min_n, max_n)
    points = create_gaussian_point_cluster(x, y, sigma, cases)
    reports = []
    for coords in points:
        reports.append(Report(
            diagnosis=disease,
            doctor_name=names.get_full_name(),
            doctor_id=uuid1(),
            patient_name=names.get_full_name(),
            patient_id=uuid1(),
            location=geos.Point(*coords),
        ))
    Report.objects.bulk_create(reports)


def gather_reports_for_day_1():
    Report.objects.all().delete()
    normal_day()


def gather_reports_for_day_2():
    Report.objects.all().delete()
    normal_day()
    outbreak(OUTBREAK[0], OUTBREAK[1], Report.CHOLERA, 10, 20, APPROX_500_M)


def gather_reports_for_day_3():
    outbreak(OUTBREAK[0], OUTBREAK[1], Report.CHOLERA, 80, 100, APPROX_500_M * 1.5)

def gather_reports_for_day_28():
    outbreak(OUTBREAK[0], OUTBREAK[1], Report.CHOLERA, 1000, 1000, APPROX_500_M * 5)
