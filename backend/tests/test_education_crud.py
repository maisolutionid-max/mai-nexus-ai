
"""
MAI Nexus AI Education
CRUD, Authentication, RBAC, and Tenant Isolation Tests
Author: MAI Solution Hub
"""

from itertools import count

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
from app.models.education_tenant_user import EducationTenantUser
from app.models.tenant import Tenant
from app.models.user import User


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

_email_counter = count(1)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_test_tenant(name="Tenant Uji", slug=None):
    db = TestingSessionLocal()
    try:
        if slug is None:
            slug = f"tenant-{next(_email_counter)}"

        tenant = Tenant(
            name=name,
            slug=slug,
            is_active=True,
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant.id
    finally:
        db.close()


def create_test_user(
    role="ADMIN",
    is_active=True,
    tenant_id=None,
):
    db = TestingSessionLocal()
    try:
        if tenant_id is None:
            tenant_id = create_test_tenant()

        user = User(
            full_name=f"Test User {role}",
            email=f"test-user-{next(_email_counter)}@example.com",
            password="test-password-hash",
            role=role,
            is_active=is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        assignment = EducationTenantUser(
            user_id=user.id,
            tenant_id=tenant_id,
        )
        db.add(assignment)
        db.commit()

        return user.id
    finally:
        db.close()


def make_test_token(user_id, role_claim="ADMIN"):
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
    tenant_id=None,
):
    user_id = create_test_user(
        role=role,
        is_active=is_active,
        tenant_id=tenant_id,
    )
    token = make_test_token(
        user_id=user_id,
        role_claim=role_claim or role,
    )
    return {"Authorization": f"Bearer {token}"}


def create_school(name="Sekolah Uji", npsn=None, headers=None):
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


def test_school_crud_requires_authentication():
    assert client.get("/education/schools").status_code == 401


def test_invalid_token_rejected():
    response = client.get(
        "/education/schools",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_unknown_user_token_rejected():
    token = make_test_token(user_id=999999)
    response = client.get(
        "/education/schools",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_inactive_user_rejected():
    headers = auth_headers(role="ADMIN", is_active=False)
    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 403


def test_user_without_tenant_assignment_rejected():
    db = TestingSessionLocal()
    try:
        user = User(
            full_name="Unassigned User",
            email=f"unassigned-{next(_email_counter)}@example.com",
            password="test-password-hash",
            role="ADMIN",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    finally:
        db.close()

    headers = {
        "Authorization": f"Bearer {make_test_token(user_id)}"
    }
    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 403


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

    listed = client.get("/education/schools", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_get_update_and_missing_school():
    headers = auth_headers("ADMIN")
    created = create_school(name="Sekolah Lama", headers=headers)
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

    assert client.get(
        "/education/schools/99999",
        headers=headers,
    ).status_code == 404

    assert client.patch(
        "/education/schools/99999",
        headers=headers,
        json={"name": "Tidak Ada"},
    ).status_code == 404


def test_duplicate_npsn_rejected():
    headers = auth_headers("ADMIN")
    payload = {
        "name": "Sekolah Satu",
        "school_level": "SMA",
        "npsn": "87654321",
    }
    assert client.post(
        "/education/schools",
        headers=headers,
        json=payload,
    ).status_code == 201

    response = client.post(
        "/education/schools",
        headers=headers,
        json={**payload, "name": "Sekolah Dua"},
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

    response = client.patch(
        f"/education/schools/{second.json()['id']}",
        headers=headers,
        json={"npsn": "11111111"},
    )
    assert response.status_code == 409


def test_delete_school():
    headers = auth_headers("ADMIN")
    created = create_school(name="Sekolah Hapus", headers=headers)
    assert created.status_code == 201

    school_id = created.json()["id"]
    assert client.delete(
        f"/education/schools/{school_id}",
        headers=headers,
    ).status_code == 204

    assert client.get(
        f"/education/schools/{school_id}",
        headers=headers,
    ).status_code == 404


def test_delete_missing_school():
    headers = auth_headers("ADMIN")
    assert client.delete(
        "/education/schools/99999",
        headers=headers,
    ).status_code == 404


def test_admin_can_create_read_update_and_delete_school():
    headers = auth_headers("ADMIN")
    created = create_school(name="Sekolah Admin", headers=headers)
    assert created.status_code == 201

    school_id = created.json()["id"]
    assert client.get("/education/schools", headers=headers).status_code == 200
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
    created = create_school(name="Sekolah Manager", headers=headers)
    assert created.status_code == 201

    school_id = created.json()["id"]
    assert client.get("/education/schools", headers=headers).status_code == 200
    assert client.patch(
        f"/education/schools/{school_id}",
        headers=headers,
        json={"name": "Sekolah Manager Diubah"},
    ).status_code == 200
    assert client.delete(
        f"/education/schools/{school_id}",
        headers=headers,
    ).status_code == 403


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
        json={"name": "Sekolah Baru", "school_level": "SMA"},
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
        json={"name": "Sekolah Customer", "school_level": "SMA"},
    ).status_code == 403


def test_token_role_claim_cannot_override_database_role():
    headers = auth_headers(role="CUSTOMER", role_claim="ADMIN")
    assert client.get(
        "/education/schools",
        headers=headers,
    ).status_code == 403


def test_tenant_cannot_list_another_tenants_schools():
    tenant_a = create_test_tenant(name="Tenant A")
    tenant_b = create_test_tenant(name="Tenant B")

    headers_a = auth_headers("ADMIN", tenant_id=tenant_a)
    headers_b = auth_headers("ADMIN", tenant_id=tenant_b)

    school_a = create_school(name="Sekolah A", headers=headers_a)
    school_b = create_school(name="Sekolah B", headers=headers_b)
    assert school_a.status_code == 201
    assert school_b.status_code == 201

    response = client.get("/education/schools", headers=headers_a)
    assert response.status_code == 200
    assert [school["name"] for school in response.json()] == ["Sekolah A"]


def test_tenant_cannot_read_update_or_delete_another_tenants_school():
    tenant_a = create_test_tenant(name="Tenant A")
    tenant_b = create_test_tenant(name="Tenant B")

    headers_a = auth_headers("ADMIN", tenant_id=tenant_a)
    headers_b = auth_headers("ADMIN", tenant_id=tenant_b)

    created = create_school(
        name="Sekolah Tenant B",
        headers=headers_b,
    )
    assert created.status_code == 201
    school_id = created.json()["id"]

    assert client.get(
        f"/education/schools/{school_id}",
        headers=headers_a,
    ).status_code == 404

    assert client.patch(
        f"/education/schools/{school_id}",
        headers=headers_a,
        json={"name": "Percobaan Ubah"},
    ).status_code == 404

    assert client.delete(
        f"/education/schools/{school_id}",
        headers=headers_a,
    ).status_code == 404

    # Tenant B's school remains unchanged and accessible to Tenant B.
    own_school = client.get(
        f"/education/schools/{school_id}",
        headers=headers_b,
    )
    assert own_school.status_code == 200
    assert own_school.json()["name"] == "Sekolah Tenant B"


def test_update_cannot_change_school_tenant():
    tenant_a = create_test_tenant(name="Tenant A")
    tenant_b = create_test_tenant(name="Tenant B")
    headers_a = auth_headers("ADMIN", tenant_id=tenant_a)

    created = create_school(name="Sekolah A", headers=headers_a)
    assert created.status_code == 201

    school_id = created.json()["id"]
    response = client.patch(
        f"/education/schools/{school_id}",
        headers=headers_a,
        json={"name": "Sekolah A Diubah", "tenant_id": tenant_b},
    )
    assert response.status_code == 200

    db = TestingSessionLocal()
    try:
        school = db.query(EducationSchool).filter(
            EducationSchool.id == school_id
        ).first()
        assert school.tenant_id == tenant_a
    finally:
        db.close()


def test_education_status_is_public():
    response = client.get("/education/")
    assert response.status_code == 200
    assert response.json()["module"] == "MAI Nexus AI Education"


def test_education_health_is_public():
    response = client.get("/education/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
def test_inactive_tenant_rejected():
    tenant_id = create_test_tenant(name="Tenant Nonaktif")
    headers = auth_headers("ADMIN", tenant_id=tenant_id)

    db = TestingSessionLocal()
    try:
        tenant = db.query(Tenant).filter(
            Tenant.id == tenant_id
        ).first()
        assert tenant is not None

        tenant.is_active = False
        db.commit()
    finally:
        db.close()

    response = client.get(
        "/education/schools",
        headers=headers,
    )
    assert response.status_code == 403
            
