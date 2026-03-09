"""
Facility tag model for the Healthsites API.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Amenity = Literal["clinic", "doctors", "hospital", "dentist", "pharmacy"]

Healthcare = Literal[
    "doctor",
    "pharmacy",
    "hospital",
    "clinic",
    "dentist",
    "physiotherapist",
    "alternative",
    "laboratory",
    "optometrist",
    "rehabilitation",
    "blood_donation",
    "birthing_center",
]

Speciality = Literal[
    "allergology",
    "anatomy",
    "anaesthetics",
    "biochemistry",
    "biological_haematology",
    "biology",
    "cardiology",
    "cardiac_surgery",
    "child_psychiatry",
    "community",
    "dental_oral_maxillo_facial_surgery",
    "dermatology",
    "dermatovenereology",
    "diagnostic_radiology",
    "emergency",
    "endocrinology",
    "gastroenterological_surgery",
    "gastroenterology",
    "general",
    "geriatrics",
    "gynaecology",
    "haematology",
    "hepatology",
    "immunology",
    "infectious_diseases",
    "intensive",
    "internal",
    "maxillofacial_surgery",
    "microbiology",
    "nephrology",
    "neurology",
    "neurophysiology",
    "neuropsychiatry",
    "neurosurgery",
    "nuclear",
    "occupational",
    "oncology",
    "ophthalmology",
    "orthodontics",
    "orthopaedics",
    "otolaryngology",
    "paediatric_surgery",
    "paediatrics",
    "palliative",
    "pathology",
    "pharmacology",
    "physiatry",
    "plastic_surgery",
    "podiatry",
    "proctology",
    "psychiatry",
    "pulmonology",
    "radiology",
    "radiotherapy",
    "rheumatology",
    "stomatology",
    "surgery",
    "surgical_oncology",
    "thoracic_surgery",
    "transplant",
    "trauma",
    "tropical",
    "urology",
    "vascular_surgery",
    "vaccination",
    "venereology",
]

OperatorType = Literal[
    "public", "private", "community", "religious", "government", "ngo", "combination"
]

OperationalStatus = Literal["operational", "non_operational", "unknown"]

HealthAmenityType = Literal[
    "ultrasound",
    "mri",
    "x_ray",
    "dialysis",
    "operating_theater",
    "laboratory",
    "imaging_equipment",
    "intensive_care_unit",
    "emergency_department",
]

Insurance = Literal["no", "public", "private", "unknown"]

WaterSource = Literal[
    "well", "water_works", "manual_pump", "powered_pump", "groundwater", "rain"
]

Electricity = Literal["grid", "generator", "solar", "other", "none"]


@dataclass(init=False)
class Tag:
    """
    OSM tags describing a health facility.

    Required fields: amenity, healthcare, name.

    Example:
        tag = Tag(
            amenity="clinic",
            healthcare=["doctor"],
            name="Example Clinic",
            operator_type="public",
            beds=50,
        )
        payload = tag.to_dict()
    """

    # Required
    amenity: Amenity
    healthcare: list[Healthcare]
    name: str

    # Optional identification
    operator: str | None
    operator_type: OperatorType | None
    speciality: list[Speciality]

    # Optional contact / operational info
    contact_number: str | None
    operational_status: OperationalStatus | None
    opening_hours: str | None
    url: str | None

    # Optional capacity
    beds: int | None
    staff_doctors: int | None
    staff_nurses: int | None

    # Optional amenities
    health_amenity_type: list[HealthAmenityType]
    dispensing: bool | None
    wheelchair: bool | None
    emergency: bool | None
    insurance: list[Insurance]

    # Optional infrastructure
    water_source: WaterSource | None
    electricity: Electricity | None

    # Optional administrative
    is_in_health_area: str | None
    is_in_health_zone: str | None

    # Optional address
    addr_housenumber: str | None
    addr_street: str | None
    addr_postcode: str | None
    addr_city: str | None

    def __init__(
            self,
            amenity: Amenity,
            healthcare: list[Healthcare],
            name: str,
            operator: str | None = None,
            operator_type: OperatorType | None = None,
            speciality: list[Speciality] | None = None,
            contact_number: str | None = None,
            operational_status: OperationalStatus | None = None,
            opening_hours: str | None = None,
            url: str | None = None,
            beds: int | None = None,
            staff_doctors: int | None = None,
            staff_nurses: int | None = None,
            health_amenity_type: list[HealthAmenityType] | None = None,
            dispensing: bool | None = None,
            wheelchair: bool | None = None,
            emergency: bool | None = None,
            insurance: list[Insurance] | None = None,
            water_source: WaterSource | None = None,
            electricity: Electricity | None = None,
            is_in_health_area: str | None = None,
            is_in_health_zone: str | None = None,
            addr_housenumber: str | None = None,
            addr_street: str | None = None,
            addr_postcode: str | None = None,
            addr_city: str | None = None,
    ) -> None:
        self.amenity = amenity
        self.healthcare = healthcare
        self.name = name
        self.operator = operator
        self.operator_type = operator_type
        self.speciality = speciality or []
        self.contact_number = contact_number
        self.operational_status = operational_status
        self.opening_hours = opening_hours
        self.url = url
        self.beds = beds
        self.staff_doctors = staff_doctors
        self.staff_nurses = staff_nurses
        self.health_amenity_type = health_amenity_type or []
        self.dispensing = dispensing
        self.wheelchair = wheelchair
        self.emergency = emergency
        self.insurance = insurance or []
        self.water_source = water_source
        self.electricity = electricity
        self.is_in_health_area = is_in_health_area
        self.is_in_health_zone = is_in_health_zone
        self.addr_housenumber = addr_housenumber
        self.addr_street = addr_street
        self.addr_postcode = addr_postcode
        self.addr_city = addr_city

    def to_dict(self) -> dict[str, Any]:
        """Return a dict suitable for the API payload, omitting None and empty lists."""
        result = {}
        for key, value in asdict(self).items():
            if value is None:
                continue
            if isinstance(value, list) and not value:
                continue
            result[key] = value
        return result
