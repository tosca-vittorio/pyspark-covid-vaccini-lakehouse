# TIMELINE.md — pyspark-covid-vaccini-lakehouse

## Scopo

Questo documento definisce l’ordine operativo completo del progetto **pyspark-covid-vaccini-lakehouse**.
La timeline è organizzata in step sequenziali, ciascuno con **Definition of Done** (DoD) verificabile.
`docs/TIMELINE.md` governa lo **stato corrente** e l’avanzamento, mantenendo allineamento “truth-first” tra lavoro svolto e repository.

## Legenda stati

* ✅ = completato e verificato
* 🟡 = presente ma da verificare/chiudere (parziale)
* ⬜ = da fare

---

## 00 — Baseline repository e struttura (Lakehouse)

**Obiettivo:** disporre di una struttura coerente e stabile su cui costruire pipeline e documentazione minima, fissando regole su layout dati e versionamento.

### 00.0 — Avvio tracciamento progetto

* ✅ Creazione di `docs/TIMELINE.md` come fonte di verità per la sequenza operativa e le DoD.
* ✅ Presenza di `docs/toDo.md` come backlog operativo.

**DoD (00.0):**

* Esiste un documento “owner” che governa la sequenza dei lavori (questa timeline).
* Esiste un backlog operativo separato (`docs/toDo.md`).

### 00.1 — Struttura repository definita

* ✅ Struttura cartelle presente (configs/data/docs/lakehouse/bronze-silver-gold/src/tests).
* ✅ Introduzione layout raw/incremental:

  * `data/raw/` per sorgenti originali
  * `data/incremental/` per simulare carichi periodici (anche vuota in prima istanza)

* ✅ Definizione architettura target e convenzioni in `docs/ARCHITECTURE.md`, includendo:

  * scopo di ogni directory
  * cosa è versionabile e cosa è escluso
  * layout dei path (raw/bronze/silver/gold)
  * naming e regole minime (dataset/job/output)

**DoD (00.1):**

* La struttura è descritta in modo non ambiguo ed è stabile per l’intero progetto.
* `docs/ARCHITECTURE.md` descrive lo **stato obiettivo (target)**; lo stato corrente resta tracciato in TIMELINE.

### 00.2 — Repository hygiene e riproducibilità

* ✅ Presenza di `.gitignore` in root (contenuto da validare rispetto a Spark/data-engineering).
* ⬜ Definizione configurazione centralizzata in `configs/` (path input/output, log level, write mode).
* 🟡 Verifica che `samples/` contenga solo estratti leggeri e riproducibili (cartella presente; contenuti da verificare).
* 🟡 Dataset originali COVID/Vaccini disponibili localmente: verifica che i file “raw” risiedano effettivamente in `data/raw/` secondo la convenzione fissata.

**DoD (00.2):**

* Nessun dataset pesante è tracciato in Git; il repo resta leggero e replicabile.
* Esiste una configurazione centralizzata che evita hardcode nei job.
* `samples/` è utilizzabile per sviluppo/test rapido.

**DoD (00) complessiva:**

* Repo con struttura stabile, regole base di versionamento e convenzioni iniziali definite.
* Prerequisiti pronti per iniziare a scrivere i job PySpark.

---

## 01 — Setup ambiente di esecuzione (local-first)

**Obiettivo:** esecuzione riproducibile in locale di PySpark (senza dipendenze non controllate).

* ⬜ Creazione ambiente Python (venv/conda) e congelamento dipendenze (`requirements.txt` o lock equivalente).
* ⬜ Installazione e verifica Java (requisito Spark) e variabili d’ambiente necessarie.
* ⬜ Installazione PySpark e verifica sessione locale (`SparkSession`) con job di smoke test.
* ⬜ Definizione dei comandi di run (es. `python -m src.jobs.<job>` o script dedicato).
* ⬜ Setup logging minimo (console + livello configurabile).

**DoD (01):**

* Un job di test gira in locale e produce output deterministico (anche minimale).
* Dipendenze dichiarate e installabili da zero.

---

## 02 — Data catalog e layout del dato (RAW → Lakehouse)

**Obiettivo:** fissare una disciplina chiara tra dato grezzo e dato materializzato.

* ⬜ Inventario sorgenti COVID (file, formati, chiavi, date):

  * CSV somministrazioni
  * JSON copertura
  * eventuali file aggiuntivi (guariti, ecc.)

* ⬜ Definizione schema e campi attesi per ogni sorgente (versione iniziale).
* ⬜ Creazione dataset “samples” (estratti piccoli) in `samples/` per sviluppo e test rapidi.
* ⬜ Regole di naming per dataset e versioni (es. `dataset=...`, `ingestion_date=...`).
* ⬜ Decisione su formato lakehouse (Parquet come default).

**DoD (02):**

* È chiaro cosa è “raw” e cosa è “lakehouse”.
* Esistono samples minimi utilizzabili per sviluppo/test senza dataset completi.

---

## 03 — Contratto Bronze/Silver/Gold (disegno dati)

**Obiettivo:** definire cosa produce ogni layer, con confini netti e verificabili.

* ⬜ Bronze (ingestion):

  * tipizzazione minima
  * colonne tecniche (es. `ingestion_ts`, `source_file`)
  * output path e naming definiti

* ⬜ Silver (clean/standardize):

  * cast e standardizzazione date/regioni
  * deduplica e validazioni base
  * normalizzazione chiavi di join

* ⬜ Gold (serving/KPI):

  * tabelle KPI e aggregati pronti per BI/reporting

**DoD (03):**

* Lista formale di dataset Bronze/Silver/Gold con scopo e path.
* Job list dichiarata con ordine di esecuzione (MVP).

---

## 04 — Implementazione ingestion Bronze (multi-sorgente reale)

**Obiettivo:** portare i dati grezzi nel lakehouse in modo ripetibile.

* ⬜ Job Bronze: ingest CSV somministrazioni → `lakehouse/bronze/...`
* ⬜ Job Bronze: ingest JSON copertura → `lakehouse/bronze/...`
* ⬜ Validazione minima post-write:

  * conteggio righe
  * schema atteso
  * presenza colonne tecniche

* ⬜ Output in formato colonnare (Parquet) con modalità di scrittura definita.

**DoD (04):**

* Due dataset Bronze materializzati correttamente e rileggibili.
* Log di esecuzione e check minimi “pass/fail” espliciti.

---

## 05 — Silver: pulizia, standardizzazione, dedup e join

**Obiettivo:** ottenere dataset affidabili e coerenti per analisi.

* ⬜ Job Silver: clean somministrazioni

  * cast tipi, gestione null, normalizzazione date
  * dedup (criteri dichiarati)

* ⬜ Job Silver: clean copertura

  * parsing JSON e flatten strutture
  * standardizzazione chiavi territoriali e temporali

* ⬜ Job Silver: arricchimento/join (quando utile) per creare una vista “enriched” pronta a KPI.

**DoD (05):**

* Dataset Silver coerenti (schema stabile) e con qualità migliore del Bronze.
* Eventuali join riproducibili e motivati.

---

## 06 — Gold: KPI e tabelle per reporting

**Obiettivo:** produrre output finali “da BI” e facilmente consumabili.

* ⬜ KPI trend temporali (giornaliero/settimanale) a livello nazionale e/o regionale.
* ⬜ KPI ranking regioni (top/bottom) per copertura e/o incrementi.
* ⬜ KPI “campagna 2024–2025” (se rilevante) con slicing temporale e confronti.
* ⬜ Export controllato in `outputs/` (CSV/Parquet) per eventuale demo/BI.

**DoD (06):**

* Almeno 2–3 tabelle Gold complete, leggibili e documentate.
* Output esportabile senza passaggi manuali.

---

## 07 — Qualità dati e test (data engineering rigoroso)

**Obiettivo:** introdurre controlli minimi ma reali su schema e contenuto.

* ⬜ Test su schema (colonne, tipi, nullability attesa).
* ⬜ Test su vincoli semplici (range plausibili, date non future, chiavi non vuote).
* ⬜ Test di regressione su conteggi/aggregati (a partire dai samples).
* ⬜ Data quality report leggero (log + metriche essenziali).

**DoD (07):**

* Suite minima di test eseguibile in locale e riproducibile.
* Errori qualità producono fallimento esplicito (exit code/exception gestita).

---

## 08 — Incrementalità e simulazione “azienda” (opzionale ma consigliato)

**Obiettivo:** avvicinare la pipeline a uno scenario reale (carichi periodici, dedup/upsert).

* ⬜ Simulare ingestion giornaliera (batch incrementali) da `data/incremental/`.
* ⬜ Strategia di dedup/upsert in Silver (chiavi e regole dichiarate).
* ⬜ Partizionamento (solo se necessario) su date/regioni per performance.

**DoD (08):**

* Pipeline capace di gestire nuovi file senza ricostruire tutto ogni volta.
* Regole di incrementalità verificabili.

---

## 09 — Orchestrazione e automazione (local-first → CI)

**Obiettivo:** rendere l’esecuzione semplice e standardizzata.

* ⬜ Runner unico (script o entrypoint) per eseguire job in sequenza (Bronze → Silver → Gold).
* ⬜ Parametrizzazione tramite `configs/` (path input/output, modalità write, log level).
* ⬜ CI baseline (lint/format + test minimi) su push/PR (se il repo è su GitHub).

**DoD (09):**

* Un comando esegue la pipeline end-to-end (su samples o su dataset completo).
* Controlli automatici impediscono regressioni evidenti.

---

## 10 — Documentazione finale e rilascio (GitHub-ready)

**Obiettivo:** rendere il progetto leggibile, valutabile e mantenibile.

* ⬜ README del progetto PySpark (scopo, architettura, come eseguire, dataset, output).
* ⬜ Sezione “risultati” con esempi di KPI (anche con screenshot/estratti).
* ⬜ Pulizia finale documentazione: allineamento tra output prodotti e descrizioni.

**DoD (10):**

* Il repository risulta comprensibile a un revisore esterno.
* Esecuzione, output e scelte tecniche sono tracciati e verificabili.

---

## Stato corrente (truth-first)

* ✅ Step 00.0 completato.
* ✅ Step 00.1 completato (struttura + architettura target definita in `docs/ARCHITECTURE.md`).
* 🟡 Step 00.2 parzialmente completato (`.gitignore` presente; mancano configurazione centralizzata + verifica `samples/` + verifica posizionamento effettivo raw).
* ⬜ Step 01–06 ancora da implementare (setup + pipeline).
