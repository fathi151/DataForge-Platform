# Scripts

## 📋 Vue d'ensemble

Ce répertoire contient les scripts utilitaires pour la gestion de la plateforme.

## 📁 Structure

```
scripts/
├── load_sample_data.py  # Charger des données de test
└── README.md           # Cette documentation
```

## 🔧 Scripts disponibles

### load_sample_data.py

**Description**: Charge des données de test dans la base de données

**Utilisation**:
```bash
docker-compose exec postgres python /scripts/load_sample_data.py
```

**Données générées**:
- 50 clients
- 15 produits
- 200 commandes
- 500+ articles de commande

**Fonctionnalités**:
- Génération aléatoire de données réalistes
- Insertion en masse pour la performance
- Logging des opérations

## 🛠️ Créer un nouveau script

### Étape 1: Créer le fichier

```python
# scripts/my_script.py

#!/usr/bin/env python3
"""
Description du script
"""

import psycopg2

def main():
    """Fonction principale"""
    conn = psycopg2.connect(
        host="postgres",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    
    cursor = conn.cursor()
    
    # Votre logique ici
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
```

### Étape 2: Exécuter le script

```bash
docker-compose exec postgres python /scripts/my_script.py
```

## 📝 Exemples de scripts

### Backup de la base de données

```python
#!/usr/bin/env python3
import subprocess
from datetime import datetime

filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

subprocess.run([
    'pg_dump',
    '-h', 'postgres',
    '-U', 'datauser',
    '-d', 'datawarehouse',
    '-f', f'/backups/{filename}'
])

print(f"Backup created: {filename}")
```

### Nettoyage des données

```python
#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host="postgres",
    database="datawarehouse",
    user="datauser",
    password="datapass123"
)

cursor = conn.cursor()

# Supprimer les doublons
cursor.execute("""
    DELETE FROM raw_data.customers
    WHERE customer_id NOT IN (
        SELECT MIN(customer_id)
        FROM raw_data.customers
        GROUP BY email
    )
""")

conn.commit()
print(f"Deleted {cursor.rowcount} duplicate records")

cursor.close()
conn.close()
```

### Génération de rapports

```python
#!/usr/bin/env python3
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="postgres",
    database="datawarehouse",
    user="datauser",
    password="datapass123"
)

cursor = conn.cursor()

# Récupérer les statistiques
cursor.execute("SELECT COUNT(*) FROM raw_data.customers")
customers = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM raw_data.orders")
orders = cursor.fetchone()[0]

cursor.execute("SELECT SUM(total_amount) FROM raw_data.orders")
revenue = cursor.fetchone()[0] or 0

# Générer le rapport
report = f"""
===== RAPPORT DE PLATEFORME =====
Date: {datetime.now()}
Clients: {customers}
Commandes: {orders}
Revenu total: ${revenue:.2f}
==================================
"""

print(report)

# Sauvegarder le rapport
with open('/reports/report.txt', 'a') as f:
    f.write(report + '\n')

cursor.close()
conn.close()
```

## 🔍 Bonnes pratiques

1. **Shebang**: Ajouter `#!/usr/bin/env python3` au début
2. **Documentation**: Ajouter des docstrings
3. **Gestion d'erreurs**: Implémenter try/except
4. **Logging**: Utiliser le logging approprié
5. **Idempotence**: Les scripts doivent être idempotents

## 📚 Ressources

- [Python Documentation](https://docs.python.org/3/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

**Dernière mise à jour**: 2024
