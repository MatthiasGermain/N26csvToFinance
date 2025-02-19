import io
import base64
import matplotlib.pyplot as plt

def depense_revenus_mois(depenses_cumulees, revenus_cumules):
    # Créer une figure sans afficher la GUI
    fig, ax = plt.subplots()

    # Extraire les dates et montants pour les dépenses et les revenus
    depenses_dates = [txn['date'] for txn in depenses_cumulees]
    depenses_totaux = [txn['total'] for txn in depenses_cumulees]
    revenus_dates = [txn['date'] for txn in revenus_cumules]
    revenus_totaux = [txn['total'] for txn in revenus_cumules]

    # Tracer les lignes pour les dépenses et les revenus
    ax.plot(depenses_dates, depenses_totaux, label='Dépenses', color='red')
    ax.plot(revenus_dates, revenus_totaux, label='Revenus', color='green')

    # Ajouter des labels et un titre
    ax.set_xlabel('Date')
    ax.set_ylabel('Montant (€)')
    ax.set_title('Cumul des Dépenses et Revenus')
    ax.legend()

    # Sauvegarder l'image dans un buffer (sans afficher la fenêtre)
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)  # Revenir au début du buffer

    # Encoder l'image en base64
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    return img_base64
