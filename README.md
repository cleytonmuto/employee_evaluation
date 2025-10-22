### Run Migrations (Alembic):

-   Initialize Alembic.
    ```
    alembic init alembic
    ```
-   Edit the `sqlalchemy.url` attribute on `alembic.ini`
-   Edit the `target_metadata` on `alembic/env.py` from `None` to `Base.metadata`, also need to include:
    ```
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    ```
-   Generate Migration.
    ```
    alembic revision --autogenerate -m "Create all tables"
    ```
-   Apply Migrations.
    ```
    alembic upgrade head
    ```

### Run the Application:

    ```
    uvicorn app.main:app --reload
    ```
