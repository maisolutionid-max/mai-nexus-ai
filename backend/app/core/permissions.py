from app.core.constants import UserRole


PERMISSIONS = {
    UserRole.ADMIN: [
        "*"
    ],

    UserRole.MANAGER: [
        "dashboard",
        "customer",
        "order",
        "product",
        "transaction",
        "payment",
        "report",
    ],

    UserRole.STAFF: [
        "customer",
        "order",
        "product",
        "transaction",
    ],

    UserRole.CASHIER: [
        "transaction",
        "payment",
        "report",
    ],

    UserRole.CUSTOMER: [
        "profile",
    ],
}


def has_permission(role: str, module: str) -> bool:

    permissions = PERMISSIONS.get(role, [])

    if "*" in permissions:
        return True

    return module in permissions
