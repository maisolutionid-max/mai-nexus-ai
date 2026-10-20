from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.models.education_school import EducationSchool
from app.api.education_api import router


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_and_list_school():
    response = client.post(
        "/education/schools",
        json={
            "name": "Sekolah Uji",
            "school_level": "SMA",
            "npsn": "12345678",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Sekolah Uji"

    response = client.get("/education/schools")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_update_and_missing_school():
    created = client.post(
        "/education/schools",
        json={"name": "Sekolah Lama", "school_level": "SMA"},
    )
    school_id = created.json()["id"]

    response = client.get(f"/education/schools/{school_id}")
    assert response.status_code == 200

    response = client.patch(
        f"/education/schools/{school_id}",
        json={"name": "Sekolah Baru"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Sekolah Baru"

    response = client.get("/education/schools/99999")
    assert response.status_code == 404


def test_duplicate_npsn_rejected():
    payload = {
        "name": "Sekolah Satu",
        "school_level": "SMA",
        "npsn": "87654321",
    }
    assert client.post("/education/schools", json=payload).status_code == 201

    duplicate = {
        **payload,
        "name": "Sekolah Dua",
    }
    response = client.post("/education/schools", json=duplicate)
    assert response.status_code == 409
