from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.schemes import (
    KittenRead,
    KittenCreate,
    KittenUpdate
)
from app.crud import kittens as kittens_crud

router = APIRouter(tags=["Users"], prefix="/kittens")


@router.get("/", response_model=list[KittenRead])
async def get_kttens(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    kittens = await kittens_crud.get_all_kittens(session=session)
    return kittens


@router.post("/", response_model=KittenRead)
async def create_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    kitten_create: KittenCreate,
):
    kitten = await kittens_crud.create_kitten(
        session=session,
        kitten_create=kitten_create,
    )
    return kitten

@router.get("/{id}", response_model=KittenRead)
async def get_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    id: int,
):
    kitten = await kittens_crud.get_kitten_by_id(
        session=session,
        id=id,
    )
    return kitten

@router.get("/breeds/")
async def get_breeds(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
) -> list:
    breeds = await kittens_crud.get_breeds(
        session=session,
    )
    return list(set(breeds))

@router.put("/{id}", response_model=KittenRead)
async def update_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    update_kitten: KittenUpdate,
    id: int
):
    kitten = await kittens_crud.update_kitten_by_id(
        session=session,
        id=id,
        new_data=update_kitten,
    )
    return kitten

@router.get("/breeds/{breed}", response_model=list[KittenRead])
async def get_kittens_by_breed(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    breed: str
):
    kittens = await kittens_crud.get_kittens_by_breed(
        session=session,
        breed=breed,
    )
    return kittens

@router.delete("/{id}")
async def delete_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    id: int
) -> dict:
    result = await kittens_crud.delete_kitten_by_id(
        session=session,
        id=id,
    )
    return result

