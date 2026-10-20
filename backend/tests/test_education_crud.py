
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.education_api import router
from app.config import settings
from app.database import Base, get_db


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


def make_test_token():
    return jwt.encode(
        {"sub": "test-user", "role": "ADMIN"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def auth_headers():
    return {"Authorization": f"Bearer {make_test_token()}"}


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_school_crud_requires_authentication():
    response = client.get("/education/schools")
    assert response.status_code == 401


def test_create_and_list_school():
    response = client.post(
        "/education/schools",
        headers=auth_headers(),
        json={
            "name": "Sekolah Uji",
            "school_level": "SMA",
            "npsn": "12345678",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Sekolah Uji"

    response = client.get(
        "/education/schools",
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_update_and_missing_school():
    created = client.post(
        "/education/schools",
        headers=auth_headers(),
        json={
            "name": "Sekolah Lama",
            "school_level": "SMA",
        },
    )
    assert created.status_code == 201
    school_id = created.json()["id"]

    response = client.get(
        f"/education/schools/{school_id}",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    response = client.patch(
        f"/education/schools/{school_id}",
        headers=auth_headers(),
        json={"name": "Sekolah Baru"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Sekolah Baru"

    response = client.get(
        "/education/schools/99999",
        headers=auth_headers(),
    )
    assert response.status_code == 404


def test_duplicate_npsn_rejected():
    payload = {
        "name": "Sekolah Satu",
        "school_level": "SMA",
        "npsn": "87654321",
    }

    first = client.post(
        "/education/schools",
        headers=auth_headers(),
        json=payload,
    )
    assert first.status_code == 201

    duplicate = {**payload, "name": "Sekolah Dua"}
    response = client.post(
        "/education/schools",
        headers=auth_headers(),
        json=duplicate,
    )
    assert response.status_code == 409
