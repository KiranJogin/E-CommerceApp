from app import create_app
from models.models import db, User, Category, Product
from werkzeug.security import generate_password_hash


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Admin user ---
        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin123"),
            phone="9999999999",
            is_admin=True,
        )
        db.session.add(admin)

        # --- Categories ---
        mobiles = Category(name="Mobiles")
        laptops = Category(name="Laptops")
        audio = Category(name="Audio")
        db.session.add_all([mobiles, laptops, audio])
        db.session.flush()  # assign IDs

        # --- Products ---
        p1 = Product(
            name="iPhone 15",
            description="Apple iPhone 15 128GB 5G",
            price=79999,
            stock=15,
            category=mobiles,
            image="iphone15.jpg",
        )
        p2 = Product(
            name="Samsung Galaxy S23",
            description="Flagship Android phone with amazing camera",
            price=74999,
            stock=10,
            category=mobiles,
            image="s23.jpg",
        )
        p3 = Product(
            name="HP Pavilion 14",
            description="12th Gen Intel i5, 16GB RAM, 512GB SSD",
            price=65999,
            stock=8,
            category=laptops,
            image="hp_pavilion.jpg",
        )
        p4 = Product(
            name="Sony WH-1000XM5",
            description="Wireless Noise Cancelling Headphones",
            price=29999,
            stock=20,
            category=audio,
            image="sony_xm5.jpg",
        )

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        print("✅ Database reset and sample data inserted.")


if __name__ == "__main__":
    seed()
