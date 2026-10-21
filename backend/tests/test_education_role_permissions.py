import pytest

from app.core.education_permissions import has_education_permission


STUDENT_PERMISSIONS = [
    "education:students:create",
    "education:students:read",
    "education:students:update",
    "education:students:delete",
]


@pytest.mark.parametrize(
    ("role", "expected_permissions"),
    [
        ("ADMIN", set(STUDENT_PERMISSIONS)),
        (
            "MANAGER",
            {
                "education:students:create",
                "education:students:read",
                "education:students:update",
            },
        ),
        ("STAFF", {"education:students:read"}),
        ("CUSTOMER", set()),
        ("CASHIER", set()),
    ],
)
def test_student_permissions_by_role(role, expected_permissions):
    for permission in STUDENT_PERMISSIONS:
        assert has_education_permission(
            role, permission
        ) is (permission in expected_permissions)


@pytest.mark.parametrize(
    "role",
    ["ADMIN", "MANAGER", "STAFF", "CUSTOMER", "CASHIER"],
)
def test_student_permissions_are_case_insensitive(role):
    for permission in STUDENT_PERMISSIONS:
        assert has_education_permission(
            role.lower(), permission
        ) is has_education_permission(role, permission)


def test_unknown_role_has_no_student_permissions():
    for permission in STUDENT_PERMISSIONS:
        assert has_education_permission(
            "UNKNOWN_ROLE", permission
        ) is False
