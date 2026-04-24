from datetime import date
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from database import SessionLocal, init_db
from models import Sale


SALES = [
    Sale(id=1, product="Laptop Pro 14", category="Computers", price=1499.0, quantity=2, date=date(2026, 1, 5), customer_id="C-1001"),
    Sale(id=2, product="Noise Canceling Headphones", category="Audio", price=249.0, quantity=5, date=date(2026, 1, 6), customer_id="C-1002"),
    Sale(id=3, product="USB-C Hub", category="Accessories", price=79.0, quantity=9, date=date(2026, 1, 7), customer_id="C-1003"),
    Sale(id=4, product="Laptop Pro 14", category="Computers", price=1499.0, quantity=1, date=date(2026, 1, 8), customer_id="C-1004"),
    Sale(id=5, product="Mechanical Keyboard", category="Accessories", price=139.0, quantity=6, date=date(2026, 1, 9), customer_id="C-1005"),
    Sale(id=6, product="4K Monitor", category="Displays", price=399.0, quantity=4, date=date(2026, 1, 10), customer_id="C-1006"),
    Sale(id=7, product="Wireless Mouse", category="Accessories", price=59.0, quantity=12, date=date(2026, 1, 11), customer_id="C-1007"),
    Sale(id=8, product="Studio Microphone", category="Audio", price=189.0, quantity=3, date=date(2026, 1, 12), customer_id="C-1008"),
    Sale(id=9, product="4K Monitor", category="Displays", price=399.0, quantity=5, date=date(2026, 1, 13), customer_id="C-1009"),
    Sale(id=10, product="Laptop Pro 14", category="Computers", price=1499.0, quantity=3, date=date(2026, 1, 14), customer_id="C-1010"),
    Sale(id=11, product="Tablet Air", category="Computers", price=699.0, quantity=4, date=date(2026, 1, 15), customer_id="C-1011"),
    Sale(id=12, product="Noise Canceling Headphones", category="Audio", price=249.0, quantity=7, date=date(2026, 1, 16), customer_id="C-1012"),
]


def seed() -> None:
    init_db()
    with SessionLocal() as session:
        session.query(Sale).delete()
        session.add_all(SALES)
        session.commit()


if __name__ == "__main__":
    seed()
    print(f"Seeded {len(SALES)} e-commerce sales rows.")
