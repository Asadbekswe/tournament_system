fastapi:
	fastapi dev app:main.py

run:
	#uvicorn app.main:app --reload
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


create_migrate:
	alembic init migrations

create_async_migrate:
	alembic init -t async alembic

makemigrations:
	alembic revision --autogenerate -m "Initial migration"

migrate:
	alembic upgrade head

down_migrate:
	alembic downgrade -1

test:
	pytest