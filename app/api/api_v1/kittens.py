from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.schemes import (
    KittenRead,
    KittenCreate,
    KittenUpdate
)
from app.crud import kittens as kittens_crud

router = APIRouter(tags=["Kittens"], prefix="/kittens")


@router.get("/", response_model=list[KittenRead])
async def get_kttens(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):  
    try:
        kittens = await kittens_crud.get_all_kittens(session=session)
    except:
        raise HTTPException(404, "Can't get kittens")
    return kittens


@router.post("/", response_model=KittenRead)
async def create_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    kitten_create: KittenCreate,
):
    try:
        kitten = await kittens_crud.create_kitten(
            session=session,
            kitten_create=kitten_create,
        )
    except:
        raise HTTPException(404, "Can't create kitten")
    return kitten

@router.get("/{id}", response_model=KittenRead)
async def get_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    id: int,
):
    try:
        kitten = await kittens_crud.get_kitten_by_id(
            session=session,
            id=id,
        )
    except:
        raise HTTPException(404, "Can't get kitten")
    return kitten

@router.get("/breeds/")
async def get_breeds(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
) -> list:
    try:
        breeds = await kittens_crud.get_breeds(
            session=session,
        )
    except:
        raise HTTPException(404, "Can't get breeds")
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
    try:
        kitten = await kittens_crud.update_kitten_by_id(
            session=session,
            id=id,
            new_data=update_kitten,
        )
    except:
        raise HTTPException(404, "Can't update kitten")
    return kitten

@router.get("/breeds/{breed}", response_model=list[KittenRead])
async def get_kittens_by_breed(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    breed: str
):
    try:
        kittens = await kittens_crud.get_kittens_by_breed(
            session=session,
            breed=breed,
        )
    except:
        raise HTTPException(404, "Can't get kitten by id")
    return kittens

@router.delete("/{id}")
async def delete_kitten(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    id: int
) -> dict:
    try:
        result = await kittens_crud.delete_kitten_by_id(
            session=session,
            id=id,
        )
    except:
        raise HTTPException(404, "Can't delete kitten")
    return result

