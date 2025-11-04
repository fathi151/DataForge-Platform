# Jupyter Notebooks

## 📋 Vue d'ensemble

Ce répertoire contient les notebooks Jupyter pour l'analyse exploratoire des données.

## 📁 Structure

```
notebooks/
├── data_analysis.ipynb  # Analyse exploratoire des données
└── README.md           # Cette documentation
```

## 🚀 Accès à Jupyter

1. Ouvrir http://localhost:8888
2. Pas de mot de passe requis
3. Naviguer vers le répertoire `work`

## 📓 Notebooks disponibles

### data_analysis.ipynb

**Description**: Analyse exploratoire des données de la plateforme

**Contenu**:
- Connexion à PostgreSQL
- Chargement des données
- Statistiques descriptives
- Visualisations
- Analyses avancées

## 🛠️ Créer un nouveau notebook

### Étape 1: Créer le notebook

1. Dans Jupyter, cliquer sur "New" → "Python 3"
2. Renommer le notebook

### Étape 2: Ajouter du code

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

### Étape 3: Sauvegarder

Le notebook est automatiquement sauvegardé dans le répertoire `notebooks/`.

## 📊 Exemples de code

### Connexion à PostgreSQL

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host='postgres',
    database='datawarehouse',
    user='datauser',
    password='datapass123'
)

# Exécuter une requête
df = pd.read_sql_query('SELECT * FROM raw_data.customers', conn)

# Fermer la connexion
conn.close()
```

### Visualisations

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Configurer le style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# Créer un graphique
df['country'].value_counts().plot(kind='bar')
plt.title('Customers by Country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.show()
```

### Statistiques

```python
# Statistiques descriptives
df.describe()

# Grouper et agréger
df.groupby('country').size()

# Corrélations
df.corr()
```

### Exporter les résultats

```python
# CSV
df.to_csv('/home/jovyan/data/export.csv', index=False)

# JSON
df.to_json('/home/jovyan/data/export.json', orient='records')

# Parquet
df.to_parquet('/home/jovyan/data/export.parquet')

# Excel
df.to_excel('/home/jovyan/data/export.xlsx', index=False)
```

## 🔍 Bonnes pratiques

1. **Nommage**: Utiliser des noms descriptifs
2. **Documentation**: Ajouter des commentaires et des markdown
3. **Modularité**: Diviser le code en cellules logiques
4. **Versioning**: Commiter les notebooks dans Git
5. **Nettoyage**: Nettoyer les cellules avant de commiter

## 📚 Ressources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Seaborn Documentation](https://seaborn.pydata.org/)

---

**Dernière mise à jour**: 2024
