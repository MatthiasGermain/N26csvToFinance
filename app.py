#app.py
from flask import Flask, render_template, redirect, url_for
from modules.import_csv import import_csv_to_db
from modules.analyse_partner import get_partner_analysis
from modules.db import get_db_connection
from flask import Flask, render_template, redirect, url_for, request
from modules.import_csv import import_csv_to_db
from modules.graph import depense_revenus_mois
from flask import Flask, render_template, request, redirect, url_for
from modules.db import get_db_connection
from modules.manage_categories import load_categories, update_categories, get_unclassified_partners

app = Flask(__name__)
app.config['DATABASE'] = 'data/database.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import')
def import_data():
    try:
        import_csv_to_db(app.config['DATABASE'])
    except Exception as e:
        return f"Erreur lors de l'importation des données : {str(e)}"
    return redirect(url_for('index'))

@app.route('/analyse/partner')
def analyse_partner():
    try:
        data = get_partner_analysis(app.config['DATABASE'])
    except Exception as e:
        return f"Erreur lors de l'analyse par Partner Name : {str(e)}"
    return render_template('analyse_partner.html', data=data)

@app.route('/check_columns')
def check_columns():
    import sqlite3
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()
    conn.close()
    return render_template('check_columns.html', columns=columns)

@app.route('/manage_categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'POST':
        # Récupérer les nouvelles catégories depuis le formulaire
        new_categories = request.form.to_dict()
        update_categories(new_categories)
        return redirect(url_for('manage_categories'))

    # Charger les catégories actuelles
    categories = load_categories()

    # Récupérer les partenaires non classés depuis la base de données
    unclassified_partners = get_unclassified_partners(app.config['DATABASE'])

    return render_template('manage_categories.html', categories=categories, unclassified_partners=unclassified_partners)

@app.route('/transactions')
def show_transactions():
    # Connexion à la base de données
    db_path = app.config['DATABASE']
    conn = get_db_connection(db_path)
    
    # Récupérer toutes les transactions
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY booking_date DESC')
    transactions = cursor.fetchall()

    # Fermer la connexion
    conn.close()

    # Afficher les transactions dans un template HTML
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
