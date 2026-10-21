
"""
MAI Nexus AI Education
Role-Based Access Control (RBAC)
Author: MAI Solution Hub
"""

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.core.education_auth import get_education_current_user


# Role disesuaikan dengan model User yang sudah ada.
# Admin aplikasi tidak otomatis menjadi admin setiap sekolah.
EDUCATION_ROLE_PERMISSIONS = {
    "ADMIN": {
        # School management
        "education:schools:read",
        "education:schools:create",
        "education:schools:update",
        "education:schools:delete",

        # Student management
        "education:students:read",
        "education:students:create",
        "education:students:update",
        "education:students:delete",
    },
    "MANAGER": {
        # School management
        "education:schools:read",
        "education:schools:create",
        "education:schools:update",

        # Student management
        "education:students:read",
        "education:students:create",
        "education:students:update",
    },
    "STAFF": {
        # Read-only access
        "education:schools:read",
        "education:students:read",
    },
    "CUSTOMER": set(),
    "CASHIER": set(),
}


def has_education_permission(
    role: str,
    permission: str,
) -> bool:
    """Check whether a role has the requested Education permission."""
    normalized_role = str(role).upper()

    permissions = EDUCATION_ROLE_PERMISSIONS.get(
        normalized_role,
        set(),
    )

    return permission in permissions


def require_education_permission(
    permission: str,
) -> Callable:
    """Create a dependency that protects an Education endpoint."""

    def permission_checker(
        current_user: dict = Depends(
            get_education_current_user
        ),
    ) -> dict:
        role = current_user.get("role", "")

        if not has_education_permission(role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Anda tidak memiliki izin untuk tindakan ini",
            )

        return current_user

    return permission_checker
