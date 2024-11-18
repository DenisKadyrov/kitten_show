# kitten_show
CRUD for kitten show. DB - PostgreSQL, Alembic and SQLAlchemy
## For run:
```
git clone https://github.com/DenisKadyrov/kitten_show.git
cd kitten_show
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD
docker-compose up -d
alembic upgrade head
fastapi dev --reload app/main.py
```
