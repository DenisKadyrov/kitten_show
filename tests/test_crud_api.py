import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import ID_STRING
from app.core.models import Kitten
from app.crud import kittens as kittens_crud

@pytest.mark.anyio()
async def setup_db(session: AsyncSession) -> None:
    """
    setup test data in DB
    """
    kitten1 = Kitten(
        color="Белый",
        description="Ласковая и воспитанная",
        breed="Сиамская",
        age=2
    )

    kitten2 = Kitten(
        color="Рыжый",
        description="Ласковая и активная",
        breed="Мейн-кун",
        age=3,
    )

    kitten3 = Kitten(
        color="Черный",
        description="Активная и воспитанная",
        breed="Регдол",
        age=4,
    )

    session.add_all([kitten1, kitten2, kitten3])
    await session.flush()

@pytest.mark.anyio
async def test_get_list_of_breeds(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test get list of breeds from test DB
    """
    # setup DataBase
    await setup_db(session)

    # send request
    response = await ac.get("/kittens/breeds/")

    assert 200 == response.status_code
    expected = {
            "Сиамская",
            "Мейн-кун",
            "Регдол",
        }
    assert expected == set(response.json())


@pytest.mark.anyio
async def test_get_list_of_all_kittens(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test get list of all kittens
    """
    # setup DataBase
    await setup_db(session)

    # send request
    response = await ac.get("/kittens/")

    assert 200 == response.status_code
    expected = [
        {
            "id": ID_STRING,
            "color": "Белый",
            "age": 2,
            "description": "Ласковая и воспитанная",
            "breed": "Сиамская",
        },
        {
            "id": ID_STRING,
            "color": "Рыжый",
            "age": 3,
            "description": "Ласковая и активная",
            "breed": "Мейн-кун",
        },
        {
            "id": ID_STRING,
            "color": "Черный",
            "age": 4,
            "description": "Активная и воспитанная",
            "breed": "Регдол",
        },
        ]
    assert expected == response.json()


@pytest.mark.anyio
async def test_get_kittens_by_breed(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test get kittens by breed
    """
    # setup DataBase
    await setup_db(session)

    # send request
    response = await ac.get("/kittens/breeds/Регдол")

    assert 200 == response.status_code
    expected = [
        {
            "id": ID_STRING,
            "color": "Черный",
            "age": 4,
            "description": "Активная и воспитанная",
            "breed": "Регдол",
        },
    ]
    assert expected == response.json()


@pytest.mark.anyio
async def test_get_kitten_by_id(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test get kitten by id
    """
    # setup DataBase
    await setup_db(session)

    # get kitten id for delete
    kittens = await kittens_crud.get_all_kittens(session)
    id = kittens[0].id

    # send request
    response = await ac.get(f"/kittens/{id}")

    assert 200 == response.status_code
    expected = {
        "id": ID_STRING,
        "color": "Белый",
        "age": 2,
        "description": "Ласковая и воспитанная",
        "breed": "Сиамская",
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_create_kitten(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test create kitten
    """
    # send request
    response = await ac.post(
        "/kittens/",
        json={
            "color": "Рыжый",
            "age": 5,
            "description": "Хороший котенок",
            "breed": "Сиамский"
        }
    )

    assert 200 == response.status_code
    expected = {
        "id": ID_STRING,
        "color": "Рыжый",
        "age": 5,
        "description": "Хороший котенок",
        "breed": "Сиамский"
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_update_kitten(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test update kitten
    """
    # setup DataBase
    await setup_db(session)

    # get kitten id for updaete
    kittens = await kittens_crud.get_all_kittens(session)
    id = kittens[0].id

    # send request
    response = await ac.put(
        f"/kittens/{id}",
        json={
            "color": "Рыжый",
            "age": 6,
            "description": "Хороший котенок",
            "breed": "Сиамский"
        }
    )

    assert 200 == response.status_code
    expected = {
        "id": id,
        "color": "Рыжый",
        "age": 6,
        "description": "Хороший котенок",
        "breed": "Сиамский"
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_delete_kitten(ac: AsyncClient, session: AsyncSession) -> None:
    """
    test delete kitten
    """
    # setup DataBase
    await setup_db(session)

    # get kitten id for delete
    kittens = await kittens_crud.get_all_kittens(session)
    id = kittens[0].id

    # send request
    response = await ac.delete(f"/kittens/{id}")

    assert 200 == response.status_code

    expected = {
        "status": "successfully deleted"
    }

    assert expected == response.json()