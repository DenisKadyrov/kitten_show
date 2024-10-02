from pydantic import BaseModel, ConfigDict


class KittenBase(BaseModel):
    color: str
    description: str
    age: int
    breed: str


class KittenCreate(KittenBase):
    pass


class KittenRead(KittenBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
