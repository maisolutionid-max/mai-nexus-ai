from app.models.education_school import EducationSchool


def test_education_school_model_fields():
    assert EducationSchool.__tablename__ == "education_schools"
    assert "id" in EducationSchool.__table__.columns
    assert "name" in EducationSchool.__table__.columns
    assert "npsn" in EducationSchool.__table__.columns
