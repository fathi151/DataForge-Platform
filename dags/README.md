# DAGs - Apache Airflow

## 📋 Vue d'ensemble

Ce répertoire contient tous les DAGs (Directed Acyclic Graphs) pour l'orchestration des pipelines ETL.

## 📁 Structure

```
dags/
├── etl_pipeline.py          # Pipeline ETL principal
├── maintenance_pipeline.py  # Tâches de maintenance
└── README.md               # Cette documentation
```

## 🔄 DAGs disponibles

### 1. ETL Pipeline (`etl_pipeline.py`)

**Description**: Pipeline ETL principal pour l'ingestion et transformation des données

**Planification**: Quotidienne à 2h du matin (`0 2 * * *`)

**Tâches**:
1. **extract_data** - Extraction des données brutes
2. **transform_data** - Transformation et nettoyage
3. **load_analytics** - Chargement en couche analytique

**Dépendances**: `extract_data >> transform_data >> load_analytics`

**Exemple d'utilisation**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def my_extract():
    print("Extracting data...")

dag = DAG(
    'my_etl_pipeline',
    default_args={
        'owner': 'data-platform',
        'start_date': datetime(2024, 1, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule_interval='@daily',
)

extract = PythonOperator(
    task_id='extract',
    python_callable=my_extract,
    dag=dag,
)
```

### 2. Maintenance Pipeline (`maintenance_pipeline.py`)

**Description**: Tâches de maintenance et de qualité des données

**Planification**: Hebdomadaire le dimanche à 3h du matin (`0 3 * * 0`)

**Tâches**:
1. **vacuum_database** - Optimisation de la base de données
2. **check_data_quality** - Vérification de la qualité
3. **generate_report** - Génération de rapports

**Dépendances**: `vacuum_database >> check_data_quality >> generate_report`

## 🛠️ Créer un nouveau DAG

### Étape 1: Créer le fichier

Créer un nouveau fichier Python dans le répertoire `dags/`:

```python
# dags/my_new_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    print("Hello from my DAG!")

default_args = {
    'owner': 'data-platform',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'my_new_dag',
    default_args=default_args,
    description='My new DAG',
    schedule_interval='@daily',
    catchup=False,
)

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag,
)
```

### Étape 2: Vérifier le DAG

```bash
# Vérifier la syntaxe
docker-compose exec airflow-webserver airflow dags list

# Tester le DAG
docker-compose exec airflow-webserver airflow dags test my_new_dag 2024-01-01
```

### Étape 3: Accéder à l'interface

Le DAG apparaît automatiquement dans l'interface Airflow après quelques secondes.

## 📊 Opérateurs disponibles

### PythonOperator

Exécute une fonction Python:

```python
from airflow.operators.python import PythonOperator

def my_function():
    return "Hello"

task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    dag=dag,
)
```

### PostgresOperator

Exécute une requête SQL:

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

task = PostgresOperator(
    task_id='run_query',
    postgres_conn_id='postgres_default',
    sql='SELECT COUNT(*) FROM raw_data.customers;',
    dag=dag,
)
```

### BashOperator

Exécute une commande bash:

```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello from bash"',
    dag=dag,
)
```

### EmailOperator

Envoie un email:

```python
from airflow.operators.email import EmailOperator

task = EmailOperator(
    task_id='send_email',
    to='admin@example.com',
    subject='DAG Completed',
    html_content='<p>The DAG has completed successfully</p>',
    dag=dag,
)
```

## 🔗 Dépendances entre tâches

### Dépendances linéaires

```python
task1 >> task2 >> task3
```

### Dépendances multiples

```python
[task1, task2] >> task3
task3 >> [task4, task5]
```

### Dépendances complexes

```python
task1 >> task2 >> task3
task1 >> task4 >> task3
```

## 🔍 Monitoring et Debugging

### Voir les logs

```bash
# Logs d'un DAG
docker-compose logs -f airflow-webserver

# Logs d'une tâche spécifique
# Via l'interface: DAG → Run → Task → Logs
```

### Tester un DAG

```bash
# Tester une tâche
docker-compose exec airflow-webserver airflow tasks test my_dag my_task 2024-01-01

# Tester le DAG complet
docker-compose exec airflow-webserver airflow dags test my_dag 2024-01-01
```

### Déclencher manuellement

```bash
# Via la CLI
docker-compose exec airflow-webserver airflow dags trigger my_dag

# Via l'interface: Cliquer sur le bouton "Trigger DAG"
```

## 📝 Bonnes pratiques

1. **Nommage**: Utiliser des noms descriptifs et en minuscules
2. **Documentation**: Ajouter des docstrings aux DAGs et tâches
3. **Gestion d'erreurs**: Implémenter des retry et des alertes
4. **Idempotence**: Les tâches doivent être idempotentes
5. **Logging**: Utiliser le logging approprié
6. **Tests**: Tester les DAGs avant de les déployer

## 🚀 Déploiement

### Développement

Les DAGs sont automatiquement chargés depuis le répertoire `dags/`.

### Production

1. Vérifier les DAGs localement
2. Commiter dans le contrôle de version
3. Déployer via CI/CD
4. Monitorer les exécutions

## 📚 Ressources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Operators](https://airflow.apache.org/docs/apache-airflow/stable/operators.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

---

**Dernière mise à jour**: 2024
