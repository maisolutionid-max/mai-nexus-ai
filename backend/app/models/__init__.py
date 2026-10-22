
from .tenant import Tenant
from .education_school import EducationSchool
from .education_tenant_user import EducationTenantUser
from .education_student import EducationStudent
from .education_academic_year import EducationAcademicYear
from app.models.education_class import EducationClass
from .user import User
from .customer import Customer
from .order import Order
from .payment import Payment
from .inventory import Inventory
from .notification import Notification
from .sensor import Sensor
from app.models.education_teacher import EducationTeacher
from app.models.education_subject import EducationSubject
from app.models.education_teacher_assignment import EducationTeacherAssignment
from app.models.education_attendance import EducationAttendance


__all__ = [
    "Tenant",
    "User",
    "Customer",
    "Order",
    "Payment",
    "Inventory",
    "Notification",
    "Sensor",
    "EducationSchool",
    "EducationTenantUser",
    "EducationStudent",
    "EducationAcademicYear",
    "EducationClass",
    "EducationTeacher",
    "EducationSubject",
    "EducationTeacherAssignment",
    "EducationAttendance",
]
