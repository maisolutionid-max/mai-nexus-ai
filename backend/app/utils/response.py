from typing import Any, Optional


def success_response(
    message: str = "Success",
    data: Optional[Any] = None
):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    message: str = "Error",
    errors: Optional[Any] = None
):

    return {
        "success": False,
        "message": message,
        "errors": errors
    }


def paginated_response(
    data: Any,
    page: int,
    limit: int,
    total: int
):

    return {
        "success": True,
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (
                (total + limit - 1) // limit
            )
        }
    }
