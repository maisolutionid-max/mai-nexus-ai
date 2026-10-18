

"""
MAI Nexus AI - Education Module API
Initial API foundation for school management.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/education",
    tags=["Education"],
)


@router.get("/")
async def education_status():
    """Return Education module status."""
    return {
        "module": "MAI Nexus AI Education",
        "status": "development",
        "version": "0.1.0",
    }


@router.get("/health")
async def education_health():
    """Check Education API availability."""
    return {
        "module": "education",
        "status": "ok",
    }
