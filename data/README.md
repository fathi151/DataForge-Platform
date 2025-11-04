# Données

## 📋 Vue d'ensemble

Ce répertoire contient les fichiers de données pour la plateforme.

## 📁 Structure

```
data/
├── README.md           # Cette documentation
└── [fichiers de données]
```

## 📊 Types de fichiers supportés

- **CSV** (.csv)
- **JSON** (.json)
- **Parquet** (.parquet)
- **Excel** (.xlsx)

## 🔄 Flux de données

```
Fichiers de données
        ↓
    Jupyter
        ↓
    PostgreSQL
        ↓
    Airflow (ETL)
        ↓
    Analytics
        ↓
    Grafana (Visualisation)
```

## 📥 Importer des données

### Via Jupyter

```python
import pandas as pd

# Charger un CSV
df = pd.read_csv('/home/jovyan/data/my_file.csv')

# Charger un JSON
df = pd.read_json('/home/jovyan/data/my_file.json')

# Charger un Parquet
df = pd.read_parquet('/home/jovyan/data/my_file.parquet')

# Charger un Excel
df = pd.read_excel('/home/jovyan/data/my_file.xlsx')
```

### Via PostgreSQL

```bash
# Importer un CSV
docker-compose exec postgres psql -U datauser -d datawarehouse -c "\COPY raw_data.customers FROM '/data/customers.csv' WITH (FORMAT csv, HEADER true);"
```

### Via MinIO

```python
from minio import Minio

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
    '/home/jovyan/data/my-file.csv'
)
```

## 📤 Exporter des données

### Via Jupyter

```python
# Exporter en CSV
df.to_csv('/home/jovyan/data/export.csv', index=False)

# Exporter en JSON
df.to_json('/home/jovyan/data/export.json', orient='records')

# Exporter en Parquet
df.to_parquet('/home/jovyan/data/export.parquet')

# Exporter en Excel
df.to_excel('/home/jovyan/data/export.xlsx', index=False)
```

### Via PostgreSQL

```bash
# Exporter une table
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.customers;" > customers.csv
```

## 🔍 Bonnes pratiques

1. **Nommage**: Utiliser des noms descriptifs et en minuscules
2. **Format**: Préférer CSV ou Parquet pour les données volumineuses
3. **Compression**: Compresser les fichiers volumineux
4. **Versioning**: Utiliser Git LFS pour les fichiers volumineux
5. **Documentation**: Documenter le schéma des données

## 📚 Ressources

- [Pandas I/O Tools](https://pandas.pydata.org/docs/user_guide/io.html)
- [PostgreSQL COPY](https://www.postgresql.org/docs/current/sql-copy.html)
- [MinIO Python SDK](https://docs.min.io/minio/baremetal/developers/python/API.html)

---

**Dernière mise à jour**: 2024
