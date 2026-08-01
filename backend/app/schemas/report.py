from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_customers: int
    total_orders: int
    total_products: int
    total_transactions: int
    total_payments: int
    total_revenue: float
    outstanding_payment: float


class RevenueReport(BaseModel):
    total_revenue: float
    total_transaction: int
    average_transaction: float


class CustomerReport(BaseModel):
    total_customers: int
    active_customers: int


class OrderReport(BaseModel):
    total_orders: int
    pending_orders: int
    processing_orders: int
    completed_orders: int
    cancelled_orders: int


class ProductReport(BaseModel):
    total_products: int
    total_services: int
    active_products: int
    inactive_products: int


class PaymentReport(BaseModel):
    total_payments: int
    paid_transactions: int
    unpaid_transactions: int
    partial_transactions: int
