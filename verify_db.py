from __init__ import app, db
from model.foodlog import FoodLog
from sqlalchemy import text

with app.app_context():
    db.create_all()
    print("✅ Tables created.")

    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        print("📋 Tables in DB:")
        for row in result:
            print("-", row[0])
