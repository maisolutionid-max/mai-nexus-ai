from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    STAFF = "STAFF"
    CASHIER = "CASHIER"
    CUSTOMER = "CUSTOMER"


class OrderStatus(str, Enum):
    PENDING = "Pending"
    RECEIVED = "Received"
    PROCESSING = "Processing"
    READY = "Ready"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class PaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, Enum):
    CASH = "Cash"
    TRANSFER = "Transfer"
    QRIS = "QRIS"
    E_WALLET = "E-Wallet"
    DEBIT_CARD = "Debit Card"
    CREDIT_CARD = "Credit Card"


class ProductCategory(str, Enum):
    PRODUCT = "Product"
    SERVICE = "Service"


class Currency(str, Enum):
    IDR = "IDR"
    USD = "USD"


DEFAULT_COMPANY_NAME = "Mai Nexus AI"

DEFAULT_CURRENCY = Currency.IDR

DEFAULT_TIMEZONE = "Asia/Jakarta"

DEFAULT_LANGUAGE = "id"

DEFAULT_INVOICE_PREFIX = "INV"

DEFAULT_ORDER_PREFIX = "ORD"

DEFAULT_PRODUCT_PREFIX = "PRD"

DEFAULT_PAYMENT_PREFIX = "PAY"
