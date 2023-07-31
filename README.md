# Vara backend fastapi

A video backend use fastapi

## run

```bash
uvicorn main:app --reload
```

## alembic

```
alembic init alembic

alembic -c alembic.ini --raiseerr revision -m "create users table"
PYTHONPATH=./ alembic.exe upgrade head
PYTHONPATH=./ alembic.exe upgrade +2
PYTHONPATH=./ alembic.exe downgrade base
PYTHONPATH=./ alembic.exe downgrade -1
```

## initail data

```bash
python initial_data.py
```

## db

```bash
docker-compose -f docker-postgres.yml up -d
```
