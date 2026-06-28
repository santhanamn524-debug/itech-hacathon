from .connection import SessionLocal, Base
from database.models import User


def seed():
    # Create tables
    Base.metadata.create_all(bind=SessionLocal().bind)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_user = db.query(User).first()

        if not existing_user:
            user = User(
                name="Admin",
                email="admin@example.com"
            )

            db.add(user)
            db.commit()

            print("✅ Database seeded successfully!")

        else:
            print("⚠️ Data already exists, skipping seed.")

    except Exception as e:
        db.rollback()
        print("❌ Error while seeding:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    seed()