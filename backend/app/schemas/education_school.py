from pydantic import BaseModel, ConfigDict


class EducationSchoolBase(BaseModel):
    name: str
    npsn: str | None = None
    school_level: str
    school_type: str = "general"
    address: str | None = None
    is_active: bool = True


class EducationSchoolCreate(EducationSchoolBase):
    pass


class EducationSchoolUpdate(BaseModel):
    name: str | None = None
    npsn: str | None = None
    school_level: str | None = None
    school_type: str | None = None
    address: str | None = None
    is_active: bool | None = None


class EducationSchoolResponse(EducationSchoolBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
