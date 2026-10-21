
"""
MAI Nexus AI Education
Education Academic Year Model Tests
Author: MAI Solution Hub
"""

from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.education_academic_year import EducationAcademicYear
from app.models.education_school import EducationSchool
from app.models.tenant import Tenant


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def create_tenant_and_school(db, name, slug, school_name):
    tenant = Tenant(
        name=name,
        slug=slug,
        is_active=True,
    )
    db.add(tenant)
    db.flush()

    school = EducationSchool(
        tenant_id=tenant.id,
        name=school_name,
        school_level="SMA",
        school_type="general",
        is_active=True,
    )
    db.add(school)
    db.flush()

    return tenant, school


def create_academic_year(
    db,
    tenant_id,
    school_id,
    name="2026/2027",
    start_date=date(2026, 7, 1),
    end_date=date(2027, 6, 30),
    is_active=True,
):
    academic_year = EducationAcademicYear(
        tenant_id=tenant_id,
        school_id=school_id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        is_active=is_active,
    )
    db.add(academic_year)
    db.commit()
    db.refresh(academic_year)
    return academic_year


def test_create_academic_year(db_session):
    tenant, school = create_tenant_and_school(
        db_session,
        "Tenant A",
        "tenant-academic-a",
        "Sekolah A",
    )

    academic_year = create_academic_year(
        db_session,
        tenant.id,
        school.id,
    )

    assert academic_year.id is not None
    assert academic_year.tenant_id == tenant.id
    assert academic_year.school_id == school.id
    assert academic_year.name == "2026/2027"
    assert academic_year.start_date == date(2026, 7, 1)
    assert academic_year.end_date == date(2027, 6, 30)
    assert academic_year.is_active is True


def test_academic_year_name_unique_per_school_and_tenant(db_session):
    tenant, school = create_tenant_and_school(
        db_session,
        "Tenant B",
        "tenant-academic-b",
        "Sekolah B",
    )

    create_academic_year(
        db_session,
        tenant.id,
        school.id,
        name="2026/2027",
    )

    duplicate = EducationAcademicYear(
        tenant_id=tenant.id,
        school_id=school.id,
        name="2026/2027",
        start_date=date(2026, 7, 1),
        end_date=date(2027, 6, 30),
        is_active=False,
    )
    db_session.add(duplicate)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_same_academic_year_name_allowed_for_another_school(db_session):
    tenant, school_a = create_tenant_and_school(
        db_session,
        "Tenant C",
        "tenant-academic-c",
        "Sekolah C1",
    )

    school_b = EducationSchool(
        tenant_id=tenant.id,
        name="Sekolah C2",
        school_level="SMA",
        school_type="general",
        is_active=True,
    )
    db_session.add(school_b)
    db_session.commit()
    db_session.refresh(school_b)

    create_academic_year(
        db_session,
        tenant.id,
        school_a.id,
        name="2026/2027",
    )

    second_year = create_academic_year(
        db_session,
        tenant.id,
        school_b.id,
        name="2026/2027",
    )

    assert second_year.school_id == school_b.id


def test_tenant_data_isolation(db_session):
    tenant_a, school_a = create_tenant_and_school(
        db_session,
        "Tenant D",
        "tenant-academic-d",
        "Sekolah D",
    )
    tenant_b, school_b = create_tenant_and_school(
        db_session,
        "Tenant E",
        "tenant-academic-e",
        "Sekolah E",
    )

    year_a = create_academic_year(
        db_session,
        tenant_a.id,
        school_a.id,
    )
    create_academic_year(
        db_session,
        tenant_b.id,
        school_b.id,
    )

    tenant_a_years = (
        db_session.query(EducationAcademicYear)
        .filter(EducationAcademicYear.tenant_id == tenant_a.id)
        .all()
    )

    assert len(tenant_a_years) == 1
    assert tenant_a_years[0].id == year_a.id
    assert all(
        item.tenant_id == tenant_a.id
        for item in tenant_a_years
    )


def test_invalid_academic_year_date_range_rejected_by_database(
    db_session,
):
    tenant, school = create_tenant_and_school(
        db_session,
        "Tenant F",
        "tenant-academic-f",
        "Sekolah F",
    )

    invalid_year = EducationAcademicYear(
        tenant_id=tenant.id,
        school_id=school.id,
        name="2026/2027-invalid",
        start_date=date(2027, 6, 30),
        end_date=date(2026, 7, 1),
        is_active=False,
    )
    db_session.add(invalid_year)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
