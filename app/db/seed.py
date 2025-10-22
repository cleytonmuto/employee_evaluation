# app/db/seed.py
from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum
from app.models.sector import Sector
from app.core.security import get_password_hash


def run_seed(db: Session):
    """
    Seeds the database with some initial data:
    - Two sectors
    - One admin user
    - Two employees (one per sector)
    """

    # Check if already seeded
    if db.query(User).first():
        print("Database already seeded. Skipping.")
        return

    # --- Create sectors ---
    engineering = Sector(name="Engineering", description="Software engineering and product development")
    hr = Sector(name="Human Resources", description="People operations and recruitment")
    db.add_all([engineering, hr])
    db.commit()
    db.refresh(engineering)
    db.refresh(hr)

    # --- Create admin user ---
    admin = User(
        username="admin",
        email="admin@example.com",
        full_name="System Administrator",
        hashed_password=get_password_hash("adminpass"),
        role=RoleEnum.admin,
    )

    # --- Create employees ---
    alice = User(
        username="alice",
        email="alice@example.com",
        full_name="Alice Johnson",
        hashed_password=get_password_hash("alicepass"),
        role=RoleEnum.employee,
        sector_id=engineering.id,
    )

    bob = User(
        username="bob",
        email="bob@example.com",
        full_name="Bob Smith",
        hashed_password=get_password_hash("bobpass"),
        role=RoleEnum.employee,
        sector_id=hr.id,
    )

    db.add_all([admin, alice, bob])
    db.commit()
    print("✅ Database seeded successfully.")
