import json
import sqlite3

CATEGORIES_FILE = 'data/categories.json'

def load_categories():
    try:
        with open(CATEGORIES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_categories(categories):
    with open(CATEGORIES_FILE, 'w') as file:
        json.dump(categories, file, indent=4)

def update_categories(form_data):
    categories = load_categories()

    for partner, category in form_data.items():
        if partner != "None" and category:  # Vérifiez que le partenaire et la catégorie ne sont pas vides
            print(f"Updating category for {partner}: {categories.get(partner, 'None')} -> {category}")
            categories[partner] = category

    save_categories(categories)
    print("Categories updated and saved successfully.")

def get_unclassified_partners(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT partner_name FROM transactions WHERE category IS NULL OR category = "None"')
    unclassified_partners = [row[0] for row in cursor.fetchall()]
    conn.close()
    return unclassified_partners
