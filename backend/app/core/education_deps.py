
from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.core.education_permissions import require_education_permission


def get_tenant_id(
    current_user: dict = Depends(get_current_user),
) -> str:
    """Ambil tenant ID dari pengguna yang sudah terautentikasi."""
    tenant_id = (
        current_user.get("tenant_id")
        or current_user.get("education_tenant_id")
    )

    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pengguna belum terhubung ke tenant sekolah.",
        )

    return str(tenant_id)
