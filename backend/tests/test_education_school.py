from app.models.education_school import EducationSchool
from app.schemas.education_school import (
    EducationSchoolCreate,
    EducationSchoolUpdate,
    EducationSchoolResponse,
)


def test_education_school_model_fields():
    assert EducationSchool.__tablename__ == "education_schools"
    assert "id" in EducationSchool.__table__.columns
    assert "name" in EducationSchool.__table__.columns
    assert "npsn" in EducationSchool.__table__.columns


def test_education_school_create_defaults():
    school = EducationSchoolCreate(
        name="Sekolah Uji",
        school_level="SMA",
    )
    assert school.school_type == "general"
    assert school.is_active is True
    assert school.npsn is None


def test_education_school_update_partial():
    school = EducationSchoolUpdate(name="Sekolah Baru")
    changes = school.model_dump(exclude_unset=True)
    assert changes == {"name": "Sekolah Baru"}


def test_education_school_response():
    school = EducationSchoolResponse(
        id=1,
        name="Sekolah Uji",
        school_level="SMA",
    )
    assert school.id == 1
    assert school.name == "Sekolah Uji"
