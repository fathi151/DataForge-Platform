# Guide d'utilisation - Data Platform

## 📖 Table des matières

1. [Démarrage](#démarrage)
2. [Airflow](#airflow)
3. [Grafana](#grafana)
4. [Jupyter](#jupyter)
5. [PostgreSQL](#postgresql)
6. [MinIO](#minio)
7. [Cas d'usage](#cas-dusage)

---

## 🚀 Démarrage

### Première utilisation

```bash
# 1. Naviguer vers le répertoire du projet
cd c:\Users\TUF\Desktop\docker

# 2. Démarrer les services
docker-compose up -d

# 3. Vérifier le statut
docker-compose ps

# 4. Attendre que tous les services soient "healthy"
# Cela peut prendre 2-3 minutes
```

### Vérifier que tout fonctionne

```bash
# Vérifier PostgreSQL
docker-compose exec postgres pg_isready -U datauser

# Vérifier Airflow
curl http://localhost:8080

# Vérifier Grafana
curl http://localhost:3000

# Vérifier Jupyter
curl http://localhost:8888
```

---

## 🔄 Airflow

### Accès à l'interface

1. Ouvrir http://localhost:8080
2. Identifiants: `admin` / `admin`

### Créer un nouveau DAG

1. Créer un fichier Python dans `dags/`
2. Exemple minimal:

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    print("Hello from Airflow!")

dag = DAG(
    'my_first_dag',
    default_args={
        'owner': 'data-platform',
        'start_date': datetime(2024, 1, 1),
    },
    schedule_interval='@daily',
)

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag,
)
```

3. Le DAG apparaît automatiquement dans l'interface

### Déclencher un DAG manuellement

1. Dans l'interface Airflow
2. Cliquer sur le DAG
3. Cliquer sur le bouton "Trigger DAG"

### Consulter les logs

```bash
# Logs d'un DAG spécifique
docker-compose logs -f airflow-webserver

# Logs détaillés d'une exécution
# Via l'interface: DAG → Run → Task → Logs
```

### Créer une connexion PostgreSQL

1. Admin → Connections
2. Créer une nouvelle connexion:
   - Conn Id: `postgres_default`
   - Conn Type: `Postgres`
   - Host: `postgres`
   - Database: `datawarehouse`
   - Login: `datauser`
   - Password: `datapass123`
   - Port: `5432`

### Utiliser les opérateurs PostgreSQL

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

query_task = PostgresOperator(
    task_id='run_query',
    postgres_conn_id='postgres_default',
    sql='SELECT COUNT(*) FROM raw_data.customers;',
    dag=dag,
)
```

---

## 📊 Grafana

### Accès à l'interface

1. Ouvrir http://localhost:3000
2. Identifiants: `admin` / `admin`

### Ajouter une source de données

1. Configuration → Data Sources
2. Ajouter PostgreSQL:
   - Name: `PostgreSQL`
   - Host: `postgres:5432`
   - Database: `datawarehouse`
   - User: `datauser`
   - Password: `datapass123`
   - SSL Mode: `disable`

### Créer un dashboard

1. Créer → Dashboard
2. Ajouter un panel:
   - Cliquer sur "Add a new panel"
   - Sélectionner la source de données PostgreSQL
   - Écrire une requête SQL

### Exemple de requête pour un panel

```sql
-- Ventes quotidiennes
SELECT 
    order_date,
    SUM(total_amount) as total_sales,
    COUNT(*) as order_count
FROM raw_data.orders
GROUP BY order_date
ORDER BY order_date DESC
LIMIT 30;
```

### Créer une alerte

1. Panel → Alert
2. Configurer les conditions
3. Ajouter un canal de notification

---

## 📓 Jupyter

### Accès à l'interface

1. Ouvrir http://localhost:8888
2. Pas de mot de passe requis

### Charger les données

```python
import pandas as pd
import psycopg2

# Connexion à PostgreSQL
conn = psycopg2.connect(
    host='postgres',
    database='datawarehouse',
    user='datauser',
    password='datapass123'
)

# Charger les données
df = pd.read_sql_query(
    'SELECT * FROM raw_data.customers',
    conn
)

print(df.head())
```

### Analyser les données

```python
# Statistiques descriptives
df.describe()

# Grouper et agréger
df.groupby('country').size()

# Visualiser
import matplotlib.pyplot as plt
df['country'].value_counts().plot(kind='bar')
plt.show()
```

### Exporter les résultats

```python
# CSV
df.to_csv('/home/jovyan/data/export.csv', index=False)

# JSON
df.to_json('/home/jovyan/data/export.json', orient='records')

# Parquet
df.to_parquet('/home/jovyan/data/export.parquet')
```

---

## 🗄️ PostgreSQL

### Accès via Adminer

1. Ouvrir http://localhost:8081
2. Remplir les informations:
   - Serveur: `postgres`
   - Utilisateur: `datauser`
   - Mot de passe: `datapass123`
   - Base de données: `datawarehouse`

### Accès via psql

```bash
# Connexion interactive
docker-compose exec postgres psql -U datauser -d datawarehouse

# Exécuter une requête
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.customers LIMIT 5;"

# Exporter les résultats
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.customers;" > customers.csv
```

### Requêtes utiles

```sql
-- Voir tous les schémas
SELECT schema_name FROM information_schema.schemata;

-- Voir toutes les tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw_data';

-- Voir la structure d'une table
\d raw_data.customers

-- Compter les lignes
SELECT COUNT(*) FROM raw_data.customers;

-- Voir les index
SELECT * FROM pg_indexes WHERE schemaname = 'raw_data';

-- Voir l'utilisation du disque
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Charger des données

```bash
# Depuis un fichier CSV
docker-compose exec postgres psql -U datauser -d datawarehouse -c "\COPY raw_data.customers FROM '/path/to/file.csv' WITH (FORMAT csv, HEADER true);"
```

---

## 🪣 MinIO

### Accès à la console

1. Ouvrir http://localhost:9001
2. Identifiants: `minioadmin` / `minioadmin123`

### Créer un bucket

1. Cliquer sur "Create Bucket"
2. Entrer un nom (ex: `data-platform`)
3. Cliquer sur "Create"

### Uploader des fichiers

1. Sélectionner le bucket
2. Cliquer sur "Upload"
3. Sélectionner les fichiers

### Utiliser MinIO avec Python

```python
from minio import Minio

# Connexion
client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin123',
    secure=False
)

# Uploader un fichier
client.fput_object(
    'data-platform',
    'my-file.csv',
    '/path/to/local/file.csv'
)

# Télécharger un fichier
client.fget_object(
    'data-platform',
    'my-file.csv',
    '/path/to/local/file.csv'
)

# Lister les fichiers
objects = client.list_objects('data-platform')
for obj in objects:
    print(obj.object_name)
```

---

## 💡 Cas d'usage

### Cas 1: Charger des données externes

1. **Préparer les données** (CSV, JSON, etc.)
2. **Uploader dans MinIO** ou directement en PostgreSQL
3. **Créer un DAG Airflow** pour l'ingestion
4. **Transformer les données** en staging
5. **Charger en analytics** pour la visualisation

### Cas 2: Créer un rapport quotidien

1. **Créer un DAG** qui s'exécute chaque jour
2. **Extraire les données** de PostgreSQL
3. **Générer un rapport** (PDF, Excel)
4. **Envoyer par email** ou stocker dans MinIO

### Cas 3: Analyser les tendances

1. **Ouvrir Jupyter**
2. **Charger les données** depuis PostgreSQL
3. **Créer des visualisations**
4. **Exporter les résultats**
5. **Créer un dashboard** dans Grafana

### Cas 4: Monitorer la qualité des données

1. **Créer des DAGs de validation**
2. **Vérifier les valeurs NULL**
3. **Détecter les doublons**
4. **Alerter en cas de problème**
5. **Générer des rapports de qualité**

---

## 🔧 Maintenance

### Sauvegarder les données

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U datauser datawarehouse > backup.sql

# Restaurer depuis un backup
docker-compose exec -T postgres psql -U datauser datawarehouse < backup.sql
```

### Nettoyer les logs

```bash
# Supprimer les logs Airflow
docker-compose exec airflow-webserver rm -rf /opt/airflow/logs/*

# Voir la taille des logs
du -sh logs/
```

### Optimiser la base de données

```bash
# VACUUM et ANALYZE
docker-compose exec postgres psql -U datauser -d datawarehouse -c "VACUUM ANALYZE;"

# Réindexer
docker-compose exec postgres psql -U datauser -d datawarehouse -c "REINDEX DATABASE datawarehouse;"
```

---

## 📞 Dépannage

### Les services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier les ports
netstat -ano | findstr :8080

# Redémarrer les services
docker-compose restart
```

### Erreur de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL est prêt
docker-compose exec postgres pg_isready -U datauser

# Vérifier les logs PostgreSQL
docker-compose logs postgres
```

### Airflow ne charge pas les DAGs

```bash
# Vérifier les permissions
docker-compose exec airflow-webserver ls -la /opt/airflow/dags/

# Redémarrer Airflow
docker-compose restart airflow-webserver
```

### Problèmes de mémoire

```bash
# Voir l'utilisation des ressources
docker stats

# Augmenter les ressources Docker
# Docker Desktop → Preferences → Resources
```

---

## 📚 Ressources supplémentaires

- [Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [Grafana Getting Started](https://grafana.com/docs/grafana/latest/getting-started/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [MinIO Quickstart](https://docs.min.io/minio/baremetal/quickstart/quickstart.html)

---

**Dernière mise à jour:** 2024
