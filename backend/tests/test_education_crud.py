
"""
MAI Nexus AI Education
CRUD, Authentication, and RBAC Tests

Author: MAI Solution Hub
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.education_api import router
from app.config import settings
from app.database import Base, get_db
from app.models.education_school import EducationSchool
from app.models.user import User


# ============================================================
# TEST DATABASE
# ============================================================

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


# ============================================================
# TEST HELPERS
# ============================================================

def create_test_user(
    role="ADMIN",
    is_active=True,
):
    """Create a real test user in the test database."""

    db = TestingSessionLocal()

    try:
        user = User(
            full_name=f"Test User {role}",
            email=f"test-{role.lower()}-{id(object())}@example.com",
            password="test-password-hash",
            role=role,
            is_active=is_active,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user.id

    finally:
        db.close()


def make_test_token(
    user_id,
    role_claim="ADMIN",
):
    """Create a JWT for an existing database user."""

    return jwt.encode(
        {
            "sub": str(user_id),
            "role": role_claim,
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def auth_headers(
    role="ADMIN",
    is_active=True,
    role_claim=None,
):
    user_id = create_test_user(
        role=role,
        is_active=is_active,
    )

    token = make_test_token(
        user_id=user_id,
        role_claim=role_claim or role,
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def create_school(
    name="Sekolah Uji",
    npsn=None,
    headers=None,
):
    payload = {
        "name": name,
        "school_level": "SMA",
    }

    if npsn is not None:
        payload["npsn"] = npsn

    return client.post(
        "/education/schools",
        headers=headers or auth_headers("ADMIN"),
        json=payload,
    )


# ============================================================
# DATABASE RESET
# ============================================================

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ============================================================
# AUTHENTICATION TESTS
# ============================================================

def test_school_crud_requires_authentication():
    response = client.get("/education/schools")

    assert response.status_code == 401


def test_invalid_token_rejected():
    response = client.get(
        "/education/schools",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


def test_unknown_user_token_rejected():
    token = make_test_token(
        user_id=999999,
    )

    response = client.get(
        "/education/schools",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401


def test_inactive_user_rejected():
    headers = auth_headers(
        role="ADMIN",
        is_active=False,
    )

    response = client.get(
        "/education/schools",
        headers=headers,
    )

    assert response.status_code == 403


# ============================================================
# SCHOOL CRUD TESTS
# ============================================================

def test_create_and_list_school():
    headers = auth_headers("ADMIN")

    response = create_school(
        name="Sekolah Uji",
        npsn="12345678",
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Sekolah Uji"
    assert response.json()["npsn"] == "12345678"

    response = client.get(
        "/education/schools",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_update_and_missing_school():
    headers = auth_headers("ADMIN")

    created = create_school(
        name="Sekolah Lama",
        headers=headers,
    )

    assert created.status_code == 201

    school_id = created.json()["id"]

    response = client.get(
        f"/education/schools/{school_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Sekolah Lama"

    response = client.patch(
        f"/education/schools/{school_id}",
        headers=headers,
        json={"name": "Sekolah Baru"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Sekolah Baru"

    response = client.get(
        "/education/schools/99999",
        headers=headers,
    )

    assert response.status_code == 404

    response = client.patch(
        "/education/schools/99999",
        headers=headers,
        json={"name": "Tidak Ada"},
    )

    assert response.status_code == 404


def test_duplicate_npsn_rejected():
    headers = auth_headers("ADMIN")

    payload = {
        "name": "Sekolah Satu",
        "school_level": "SMA",
        "npsn": "87654321",
    }

    first = client.post(
        "/education/schools",
        headers=headers,
        json=payload,
    )

    assert first.status_code == 201

    duplicate = {
        **payload,
        "name": "Sekolah Dua",
    }

    response = client.post(
        "/education/schools",
        headers=headers,
        json=duplicate,
    )

    assert response.status_code == 409


def test_duplicate_npsn_update_rejected():
    headers = auth_headers("ADMIN")

    first = create_school(
        name="Sekolah Satu",
        npsn="11111111",
        headers=headers,
    )

    second = create_school(
        name="Sekolah Dua",
        npsn="22222222",
        headers=headers,
    )

    assert first.status_code == 201
    assert second.status_code == 201

    second_id = second.json()["id"]

    response = client.patch(
        f"/education/schools/{second_id}",
        headers=headers,
        json={"npsn": "11111111"},
    )

    assert response.status_code == 409


def test_delete_school():
    headers = auth_headers("ADMIN")

    created = create_school(
        name="Sekolah Hapus",
        headers=headers,
    )

    assert created.status_code == 201

    school_id = created.json()["id"]

    response = client.delete(
        f"/education/schools/{school_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/education/schools/{school_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_delete_missing_school():
    headers = auth_headers("ADMIN")

    response = client.delete(
        "/education/schools/99999",
        headers=headers,
    )

    assert response.status_code == 404


# ============================================================
# ROLE-BASED ACCESS CONTROL TESTS
# ============================================================

def test_admin_can_create_read_update_and_delete_school():
    headers = auth_headers("ADMIN")

    created = create_school(
        name="Sekolah Admin",
        headers=headers,
    )

    assert created.status_code == 201

    school_id = created.json()["id"]

    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 200

    assert client.patch(
        f"/education/schools/{school_id}",
        headers=headers,
        json={"name": "Sekolah Admin Diubah"},
    ).status_code == 200

    assert client.delete(
        f"/education/schools/{school_id}",
        headers=headers,
    ).status_code == 204


def test_manager_can_create_read_and_update_but_not_delete():
    headers = auth_headers("MANAGER")

    created = create_school(
        name="Sekolah Manager",
        headers=headers,
    )

    assert created.status_code == 201

    school_id = created.json()["id"]

    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 200

    assert client.patch(
        f"/education/schools/{school_id}",
        headers=headers,
        json={"name": "Sekolah Manager Diubah"},
    ).status_code == 200

    response = client.delete(
        f"/education/schools/{school_id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_staff_can_read_but_cannot_create_update_or_delete():
    admin_headers = auth_headers("ADMIN")

    created = create_school(
        name="Sekolah Staff",
        headers=admin_headers,
    )

    assert created.status_code == 201

    school_id = created.json()["id"]
    staff_headers = auth_headers("STAFF")

    assert client.get(
        "/education/schools",
        headers=staff_headers,
    ).status_code == 200

    assert client.get(
        f"/education/schools/{school_id}",
        headers=staff_headers,
    ).status_code == 200

    assert client.post(
        "/education/schools",
        headers=staff_headers,
        json={
            "name": "Sekolah Baru",
            "school_level": "SMA",
        },
    ).status_code == 403

    assert client.patch(
        f"/education/schools/{school_id}",
        headers=staff_headers,
        json={"name": "Perubahan Ditolak"},
    ).status_code == 403

    assert client.delete(
        f"/education/schools/{school_id}",
        headers=staff_headers,
    ).status_code == 403


def test_customer_cannot_access_school_crud():
    headers = auth_headers("CUSTOMER")

    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 403

    assert client.post(
        "/education/schools",
        headers=headers,
        json={
            "name": "Sekolah Customer",
            "school_level": "SMA",
        },
    ).status_code == 403


def test_token_role_claim_cannot_override_database_role():
    # Database role CUSTOMER, tetapi claim token ADMIN.
    # Hak akses harus mengikuti role database.
    headers = auth_headers(
        role="CUSTOMER",
        role_claim="ADMIN",
    )

    response = client.get(
        "/education/schools",
        headers=headers,
    )

    assert response.status_code == 403


# ============================================================
# PUBLIC ENDPOINT TESTS
# ============================================================

def test_education_status_is_public():
    response = client.get("/education/")

    assert response.status_code == 200
    assert response.json()["module"] == "MAI Nexus AI Education"


def test_education_health_is_public():
    response = client.get("/education/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
