# toDo.md — Core concepts (pyspark-covid-vaccini-lakehouse)

Un backlog è un elenco dinamico e prioritario di tutte le attività, funzionalità, requisiti o bug da affrontare per un progetto o prodotto, rappresentando una sorta di "lista dei desideri" di tutto ciò che deve essere fatto, ma non ancora completato, con l'obiettivo di gestire in modo efficiente e ordinato il lavoro futuro. 

## Core concepts da conoscere (lista)

### Data engineering fundamentals
- Data Lake (raw zone, immutabilità del dato sorgente)
- Data Warehouse (modello a tabelle per analisi)
- Lakehouse (ibrido lake + warehouse)
- ETL vs ELT (e perché in lakehouse spesso è ELT)
- Medallion architecture: Bronze / Silver / Gold
- Data catalog / data inventory (sorgenti, formati, chiavi, granularità temporale)
- KPI (definizione, granularità, dimensioni vs misure)
- Metriche di pipeline (row count, null rate, duplicate rate)

### PySpark / Spark fundamentals
- SparkSession e job lifecycle
- DataFrame API (select/filter/withColumn)
- Aggregazioni (groupBy, agg: count/sum/min/max)
- Join (inner/left, chiavi, gestione duplicati)
- Schema e tipi (cast, date/timestamp)
- Transformations vs Actions (lazy evaluation)
- Shuffle (quando avviene e perché costa)
- Partitioning (concetto e impatto su performance)
- Read/Write (CSV/JSON/Parquet) e write modes (overwrite/append)

### Affidabilità “azienda”
- Idempotenza (riesecuzione senza duplicati)
- Incremental loads (batch giornalieri/periodici)
- Deduplica (chiavi + regola deterministica)
- Data quality checks (schema, vincoli, range plausibili)
- Logging e tracciabilità (input → job → output)
- Separazione configurazione vs codice (no hardcode)

### Reporting / serving
- Gold tables (tabelle “consumabili” per BI)
- Export controllato (CSV/Parquet per demo/report)
- Interpretazione KPI (trend, ranking, confronto periodi)
