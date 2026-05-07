import pytest
import itertools
from httpx import AsyncClient, ASGITransport
from app.main import app, db
import app.main as main_module   # импортируем модуль, чтобы менять глобальные переменные

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def clean_state():
    """Очистка хранилища и сброс счётчика ID перед каждым тестом."""
    db.clear()
    # Сброс глобального счётчика ID (работаем через модуль, а не через экземпляр app)
    with main_module._id_lock:
        main_module._id_seq = itertools.count(start=1)
    yield