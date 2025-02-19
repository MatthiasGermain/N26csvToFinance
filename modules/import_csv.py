import pandas as pd
import json
from modules.db import get_db_connection

def import_csv_to_db(db_path):
    # Lire le fichier CSV
    df = pd.read_csv('data/compte.csv')

    # Renommer la colonne 'Amount (EUR)' en 'amount'
    df.columns = [col.strip().replace(" ", "_").lower() if col != "Amount (EUR)" else "amount" for col in df.columns]

    # Conversion des colonnes booking_date et value_date en format 'YYYY-MM-DD'
    df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce').dt.date
    df['value_date'] = pd.to_datetime(df['value_date'], errors='coerce').dt.date

    # Charger les catégories depuis le fichier JSON
    categories = {}
    try:
        with open('data/categories.json', 'r') as file:
            categories = json.load(file)
    except FileNotFoundError:
        print("Le fichier categories.json n'a pas été trouvé. Les partenaires seront assignés à 'None'.")

    # Ajouter une colonne 'category' en utilisant les catégories chargées
    df['category'] = df['partner_name'].apply(lambda partner: categories.get(partner, "None"))

    # Connexion à la base de données
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Supprimer la table si elle existe déjà
    cursor.execute("DROP TABLE IF EXISTS transactions")

    # Créer la table avec la nouvelle colonne 'category'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_date DATE,
            value_date DATE,
            partner_name TEXT,
            partner_iban TEXT,
            type TEXT,
            payment_reference TEXT,
            account_name TEXT,
            amount REAL,
            original_amount REAL,
            original_currency TEXT,
            exchange_rate REAL,
            category TEXT  -- Nouvelle colonne 'category'
        )
    ''')

    # Insérer les données CSV dans la base de données avec la colonne 'category'
    df.to_sql('transactions', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
