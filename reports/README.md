# Rapports

## 📋 Vue d'ensemble

Ce répertoire contient les rapports générés par la plateforme.

## 📁 Structure

```
reports/
├── README.md           # Cette documentation
└── [fichiers de rapports]
```

## 📊 Types de rapports

### Rapports de qualité des données

Générés par le pipeline de maintenance:

- Nombre de valeurs NULL
- Doublons détectés
- Violations de contraintes
- Anomalies détectées

### Rapports de performance

- Temps d'exécution des DAGs
- Utilisation des ressources
- Requêtes lentes
- Taille des tables

### Rapports d'analyse

Générés par les notebooks Jupyter:

- Statistiques descriptives
- Tendances
- Corrélations
- Prévisions

## 🛠️ Générer un rapport

### Via Airflow

```python
from airflow.operators.python import PythonOperator

def generate_report():
    import pandas as pd
    import psycopg2
    
    conn = psycopg2.connect(
        host='postgres',
        database='datawarehouse',
        user='datauser',
        password='datapass123'
    )
    
    # Générer le rapport
    df = pd.read_sql_query(
        'SELECT * FROM analytics.customer_metrics',
        conn
    )
    
    # Sauvegarder
    df.to_csv('/reports/customer_metrics.csv', index=False)
    
    conn.close()

task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)
```

### Via Jupyter

```python
import pandas as pd
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host='postgres',
    database='datawarehouse',
    user='datauser',
    password='datapass123'
)

# Générer le rapport
df = pd.read_sql_query(
    'SELECT * FROM analytics.daily_sales ORDER BY sale_date DESC LIMIT 30',
    conn
)

# Sauvegarder
filename = f"daily_sales_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(f'/home/jovyan/data/{filename}', index=False)

conn.close()
```

## 📈 Formats de rapport

### CSV

```python
df.to_csv('report.csv', index=False)
```

### JSON

```python
df.to_json('report.json', orient='records')
```

### Excel

```python
df.to_excel('report.xlsx', index=False)
```

### HTML

```python
df.to_html('report.html', index=False)
```

### PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
data = [df.columns.tolist()] + df.values.tolist()
table = Table(data)
doc.build([table])
```

## 📧 Envoyer un rapport

### Via email

```python
from airflow.operators.email import EmailOperator

task = EmailOperator(
    task_id='send_report',
    to='admin@example.com',
    subject='Daily Report',
    html_content='<p>See attached report</p>',
    files=['/reports/daily_sales.csv'],
    dag=dag,
)
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

client.fput_object(
    'reports',
    'daily_sales.csv',
    '/reports/daily_sales.csv'
)
```

## 📅 Planification des rapports

### Rapport quotidien

```python
dag = DAG(
    'daily_report',
    schedule_interval='0 8 * * *',  # 8h du matin
)
```

### Rapport hebdomadaire

```python
dag = DAG(
    'weekly_report',
    schedule_interval='0 9 * * 1',  # Lundi à 9h
)
```

### Rapport mensuel

```python
dag = DAG(
    'monthly_report',
    schedule_interval='0 10 1 * *',  # 1er du mois à 10h
)
```

## 🔍 Bonnes pratiques

1. **Nommage**: Inclure la date dans le nom du fichier
2. **Format**: Utiliser des formats standards (CSV, JSON)
3. **Compression**: Compresser les rapports volumineux
4. **Archivage**: Archiver les anciens rapports
5. **Versioning**: Conserver l'historique des rapports

## 🧹 Nettoyage des rapports

### Supprimer les anciens rapports

```bash
# Linux/Mac
find reports/ -name "*.csv" -mtime +90 -delete

# Windows PowerShell
Get-ChildItem reports/ -Filter "*.csv" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-90)} | Remove-Item
```

## 📚 Ressources

- [Pandas I/O Tools](https://pandas.pydata.org/docs/user_guide/io.html)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Airflow Email Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/email.html)

---

**Dernière mise à jour**: 2024
