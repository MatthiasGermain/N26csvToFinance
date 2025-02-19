from modules.db import get_db_connection

def get_partner_analysis(db_path):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Analyse par Partner Name
    cursor.execute('''
        SELECT partner_name, 
               SUM(amount) AS total
        FROM transactions
        GROUP BY partner_name
        ORDER BY total DESC
    ''')
    data = cursor.fetchall()
    conn.close()
    return data
