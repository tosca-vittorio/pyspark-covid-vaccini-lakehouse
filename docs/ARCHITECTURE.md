# ARCHITECTURE.md — pyspark-covid-vaccini-lakehouse

## Scopo

Questo documento definisce l’architettura **obiettivo** e le convenzioni tecniche del repository **pyspark-covid-vaccini-lakehouse**.
Stabilisce struttura, naming, confini dei layer e regole di versionamento, in modo da mantenere il progetto riproducibile, verificabile e mantenibile.

## Source of Truth

- `docs/ARCHITECTURE.md` descrive **lo stato obiettivo** (target) dell’architettura e delle convenzioni.
- `docs/TIMELINE.md` governa **stato corrente** e **avanzamento** delle attività (checklist, step, Definition of Done).
- `docs/toDo.md` raccoglie note operative e promemoria (inclusi eventuali approfondimenti concettuali) senza vincolare lo stato architetturale.

---

## Principi guida

1. **Separazione tra dato sorgente e dato materializzato.** Il dato originale non viene modificato; le trasformazioni producono nuove materializzazioni nei layer lakehouse.
2. **Lakehouse a layer (Bronze/Silver/Gold).** Ogni layer ha uno scopo preciso: ingestione tracciabile, pulizia/normalizzazione, aggregazioni finali.
3. **Riproducibilità.** I job devono essere eseguibili senza percorsi hard-coded, usando configurazione centralizzata quando introdotta.
4. **Tracciabilità.** Ogni output deve essere riconducibile a input, configurazione e job che lo hanno generato.
5. **Idempotenza e determinismo.** La pipeline deve poter essere rieseguita senza produrre duplicati o risultati incoerenti a parità di input.
6. **Repository leggero.** Dataset completi e materializzazioni non vengono versionati (salvo samples piccoli e controllati).

---

## Struttura del repository (target)

```text
pyspark-covid-vaccini-lakehouse/
├─ .gitignore
├─ configs/
├─ data/
│  ├─ raw/
│  └─ incremental/
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ TIMELINE.md
│  ├─ toDo.md
│  └─ concepts/
│     
├─ lakehouse/
│  ├─ bronze/
│  ├─ silver/
│  └─ gold/
├─ outputs/
├─ samples/
├─ src/
│  ├─ jobs/
│  └─ lib/
└─ tests/
```

---

## Convenzioni delle directory

### `data/` (sorgenti)

Contiene **solo input**:

* `data/raw/`
  Dati originali (CSV/JSON) così come ottenuti dalla sorgente. Non vengono mai modificati in-place.

* `data/incremental/`
  Pacchetti di input per simulare carichi periodici (es. giornalieri) e riprodurre ingestion incrementale.

### `lakehouse/` (materializzazioni)

Contiene i dataset prodotti dai job PySpark, organizzati a layer.
Formato consigliato: **Parquet**.

* `lakehouse/bronze/`
  Ingestion tracciabile e tipizzazione minima, con aggiunta di colonne tecniche (es. timestamp ingestion, provenienza).

* `lakehouse/silver/`
  Pulizia, standardizzazione, deduplica, normalizzazione chiavi, join/arricchimenti.

* `lakehouse/gold/`
  Dataset finali (KPI, aggregazioni, tabelle di serving) pronti per analisi/reporting.

### `src/` (codice)

* `src/jobs/`
  Entry point eseguibili che implementano le pipeline per layer.

* `src/lib/`
  Libreria interna riusabile (I/O, schema, validazioni, logging, utility comuni).

### `samples/`

Contiene estratti piccoli e riproducibili dei dataset (o dataset sintetici) per sviluppo e test.
Regola: nessun file pesante.

### `outputs/`

Output destinati a consumo esterno (export CSV/Parquet, snapshot risultati, artefatti demo).
Può essere esclusa dal versionamento se voluminosa.

### `tests/`

Test unitari e/o di integrazione leggera focalizzati su:

* schema atteso
* qualità minima (range/null)
* regressioni su samples

### `configs/` (configurazione)

Cartella dedicata a configurazioni centralizzate (path, write mode, log level, parametri runtime).
Il formato e i file specifici vengono introdotti quando necessari alla pipeline.

---

## Flusso dati (ELT in stile Lakehouse)

Il progetto adotta una logica **ELT**:

* **Extract:** acquisizione da sorgenti (MVP: file locali in `data/`).
* **Load:** materializzazione iniziale nel layer Bronze (`lakehouse/bronze/`).
* **Transform:** trasformazioni ripetibili verso Silver e Gold.

Confini per layer:

* **Raw:** sorgente immutabile (`data/raw/`).
* **Bronze:** ingestione tracciabile + tipizzazione minima.
* **Silver:** qualità, normalizzazione, dedup, join.
* **Gold:** KPI e dataset finali per reporting/BI.

---

## Regole di versionamento (Git)

1. Dataset completi in `data/raw/` e materializzazioni in `lakehouse/` **non devono essere committati**.
2. In repo sono ammessi solo:

   * `samples/` piccoli e controllati,
   * documentazione,
   * codice e test.
3. `.gitignore` deve includere almeno:

   * ambienti virtuali (`.venv/`, `venv/`),
   * cache Python (`__pycache__/`),
   * artefatti Spark locali,
   * `lakehouse/` e `outputs/` (se non versionati).

---

## Convenzioni di naming

### Dataset (directory lakehouse)

Formato:

* `lakehouse/<layer>/<dataset_name>/`

Esempi:

* `lakehouse/bronze/somministrazioni_vaccini/`
* `lakehouse/bronze/copertura_vaccinale/`
* `lakehouse/silver/somministrazioni_vaccini_clean/`
* `lakehouse/gold/kpi_trend_giornaliero/`

Regole:

* solo minuscole
* underscore al posto degli spazi
* suffissi espliciti per stato: `_clean`, `_enriched`, `kpi_...`

### Job

Formato:

* `NN_layer_action_name.py` (NN = ordine esecuzione)

Esempi:

* `01_bronze_ingest_somministrazioni.py`
* `02_bronze_ingest_copertura.py`
* `10_silver_clean_somministrazioni.py`
* `20_gold_kpi_trend_giornaliero.py`

---
