import sqlite3
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

DB_PATH = CURRENT_DIR.parent.joinpath('instance', 'src.sqlite')


def seed_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    print("Cleaning database...")
    cursor.execute("DELETE FROM product")

    cursor.execute("DELETE FROM sqlite_sequence WHERE name='product'")

    print("Adding 10 placeholder products...")
    products = [
        ('Premium Birch Plywood', 'High-density 18mm birch with a void-free core. Ideal for high-end cabinetry.',
         'https://picsum.photos/seed/birch/400/300', 85.50, 'Furniture'),
        ('Marine Grade Okoume', 'BS1088 certified for boat building. Excellent water resistance and durability.',
         'https://picsum.photos/seed/marine/400/300', 120.00, 'Marine'),
        ('CDX Structural Pine', 'Standard construction grade for roofing and subfloors. Exterior glue rated.',
         'https://picsum.photos/seed/structure/400/300', 45.00, 'Construction'),
        ('White Oak Veneer', 'A-grade decorative oak face on a stable poplar core. Ready for staining.',
         'https://picsum.photos/seed/oak/400/300', 95.00, 'Interior'),
        ('Phenolic Film-Faced', 'Hard-wearing film coating for concrete shuttering or trailer flooring.',
         'https://picsum.photos/seed/film/400/300', 65.00, 'Industrial'),
        ('Flexible Bending Ply', 'Italian-made 3-ply that curves to tight radiuses without cracking.',
         'https://picsum.photos/seed/flex/400/300', 78.00, 'Specialty'),
        ('Fire-Retardant Treated', 'Class A rated for commercial interior wall and ceiling applications.',
         'https://picsum.photos/seed/fire/400/300', 110.00, 'Safety'),
        ('Walnut Fancy Panel', 'Double-sided walnut veneer for luxury furniture and architectural accents.',
         'https://picsum.photos/seed/walnut/400/300', 145.00, 'Furniture'),
        ('Hex-Pattern Anti-Slip', 'Textured grip surface for mezzanine floors, staging, and flight cases.',
         'https://picsum.photos/seed/grip/400/300', 89.00, 'Industrial'),
        ('Lauan Underlayment', 'Lightweight 4mm panels for seamless floor preparation and crafts.',
         'https://picsum.photos/seed/thin/400/300', 25.00, 'Interior')
    ]

    # Insert the data
    cursor.executemany(
        "INSERT INTO product (name, description, image_url, price, category) VALUES (?, ?, ?, ?, ?)",
        products
    )

    connection.commit()
    connection.close()
    print(f"Success! 10 products added to {DB_PATH}.")


if __name__ == '__main__':
    seed_database()
