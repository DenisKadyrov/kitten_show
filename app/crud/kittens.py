from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Kitten
from app.core.schemes import (
    KittenCreate,
    KittenUpdate,
)


async def get_all_kittens(
    session: AsyncSession,
) -> Sequence[Kitten]:
    stmt = select(Kitten).order_by(Kitten.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_kitten(
    session: AsyncSession,
    kitten_create: KittenCreate,
) -> Kitten:
    kitten = Kitten(**kitten_create.model_dump())
    session.add(kitten)
    await session.commit()
    await session.refresh(kitten)
    return kitten



async def get_kittens_by_breed(
        session: AsyncSession,
        breed: str,
) -> list[Kitten]:
    stmt = select(Kitten).where(Kitten.breed == breed)
    result = await session.scalars(stmt)
    return result


async def get_breeds(
        session: AsyncSession,
) -> list[str]:
    result = await get_all_kittens(session)
    return [i.breed for i in result]


async def get_kitten_by_id(
        session: AsyncSession,
        id: int,
) -> Kitten:
    stmt = select(Kitten).where(Kitten.id == id)
    result = await session.scalar(stmt)
    return result

async def update_kitten_by_id(
        session: AsyncSession,
        id: int,
        new_data: KittenUpdate,
) -> Kitten:
    kitten = await get_kitten_by_id(session, id)

    kitten.age = new_data.age
    kitten.color = new_data.color
    kitten.breed = new_data.breed
    kitten.description = new_data.description

    session.add(kitten)
    await session.commit()
    await session.refresh(kitten)

    return kitten


async def delete_kitten_by_id(
        session: AsyncSession,
        id: int,
) -> dict:
    kitten = await get_kitten_by_id(session, id)
    await session.delete(kitten)
    await session.commit()

    return {"status": "successfully deleted"}