# docs/`TIMELINE.md` — pyspark-covid-vaccini-lakehouse

## Scopo

Questo documento definisce l’ordine operativo completo del progetto **pyspark-covid-vaccini-lakehouse**.
La timeline è organizzata in step sequenziali, ciascuno con **Definition of Done** (DoD) verificabile.
`docs/TIMELINE.md` governa lo **stato corrente** e l’avanzamento, mantenendo allineamento “truth-first” tra lavoro svolto e repository.

## Legenda stati

* ✅ = completato e verificato
* 🟡 = presente ma da verificare/chiudere (parziale)
* ⬜ = da fare

---

## 00 — ☑️ Baseline repository e struttura (Lakehouse)

**Obiettivo:** disporre di una struttura coerente e stabile su cui costruire pipeline e documentazione minima, fissando regole su layout dati e versionamento.

**DoD (00) complessiva:**

* Repo con struttura stabile, regole base di versionamento e convenzioni iniziali definite.
* Prerequisiti pronti per iniziare a scrivere job PySpark in modo pulito.

### ✅ 00.0 — Avvio tracciamento progetto

* ✅ Creazione di `docs/TIMELINE.md` come fonte di verità per la sequenza operativa e le DoD.
* ✅ Presenza di `docs/toDo.md` come backlog operativo.

**DoD (00.0):**

* Esiste un documento “owner” che governa la sequenza dei lavori (questa timeline).
* Esiste un backlog operativo separato (`docs/toDo.md`).

### ✅ 00.1 — Struttura repository definita

* ✅ Struttura cartelle presente (configs/data/docs/lakehouse/outputs/samples/src/tests).
* ✅ Introduzione layout raw/incremental:

  * `data/raw/` per sorgenti originali (LOCAL ONLY)
  * `data/incremental/` per simulare carichi periodici (anche vuota in prima istanza)
* ✅ Definizione architettura target e convenzioni in `docs/ARCHITECTURE.md`, includendo:

  * scopo di ogni directory
  * cosa è versionabile e cosa è escluso
  * layout dei path (raw/bronze/silver/gold)
  * naming e regole minime (dataset/job/output)

**DoD (00.1):**

* La struttura è descritta in modo non ambiguo ed è stabile per l’intero progetto.
* `docs/ARCHITECTURE.md` descrive lo **stato obiettivo (target)**; lo stato corrente resta tracciato in TIMELINE.

### ✅ 00.2 — Git baseline e branching

* ✅ Presenza di `.gitignore` in root (contenuto coerente per Spark/data-engineering).
* ✅ Primo commit su `main` con documentazione base.
* ✅ Push su GitHub (`origin/main`).
* ✅ Creazione branch `development`.
* ✅ Push branch `development` su GitHub (`origin/development`) con tracking.

**DoD (00.2):**

* `main` e `development` esistono su GitHub e sono tracciati in locale.

### ✅ 00.3 — Repository hygiene e riproducibilità

* ✅ Definizione configurazione centralizzata in `configs/` (path input/output, log level, write mode).
* ✅ Documentazione configurazione centralizzata in `docs/configs/00a_appdevjson.md`, `docs/configs/00b_appjson.md` e `docs/src/lib/00c_configpy.md`.
* ✅ Dataset raw disponibili localmente in `data/raw/` (non versionati, LOCAL ONLY).
* ✅ Creazione `samples/` minimi e riproducibili derivati dai RAW (CSV estratti leggeri, versionabili).
* ✅ Triplete Git ChekPoint (Add + Commit + Push) dei samples su branch `development` (solo `samples/`, senza includere dati raw né output lakehouse).
* ✅ Documentazione dei samples centralizzata in `docs/samples/00d_creazione_sample.md` (nessun `samples/README.md` per scelta anti-ridondanza).

**DoD (00.3):**

* Nessun dataset raw, lakehouse o outputs è tracciato in Git; il repo resta leggero e replicabile.
* Esiste una configurazione centralizzata che evita hardcode nei job.
* `samples/` è utilizzabile per sviluppo/test rapido (riproducibile da clone del repo).

---

## 01 — 🟡 Setup ambiente di esecuzione (local-first)

**Obiettivo:** esecuzione riproducibile in locale di PySpark con dipendenze tracciate e run standard.

### ✅ 01.0 — Virtual environment e dipendenze Python

* ✅ Creazione ambiente Python `.venv/` (virtualenv).
* ✅ Attivazione venv e upgrade pip.
* ✅ Documentazione `.venv` completata: `docs/01a_venv.md`.
* ✅ Creazione `requirements.txt` iniziale (minimo, riproducibile).
* ✅ Installazione dipendenze da `requirements.txt`.
* ✅ Verifica import e versione PySpark.
* ✅ Documentazione `requirements.txt` completata: `docs/01b_requirements.md`.

**DoD (01.0):**
* La macchina può installare e importare PySpark partendo da zero con venv + requirements.

### 01.1 — Prerequisito Java (Spark runtime)

* ⬜ Verifica installazione Java presente e funzionante (`java -version`).
* ⬜ Allineamento `JAVA_HOME` se necessario.

**DoD (01.1):**
* Spark può avviarsi senza errori di runtime legati a Java.

### 01.2 — Smoke test Spark locale

* ⬜ Creazione job `src/jobs/00_smoke_spark.py`:
  * avvio `SparkSession`
  * lettura `samples/` (almeno i 2 CSV)
  * stampa schema + conteggio righe
  * scrittura output minimale in `outputs/` (non versionato)
* ⬜ Run locale completato (exit code 0).

**DoD (01.2):**
* Un job PySpark gira in locale e produce output deterministico (anche minimale).

### 01.3 — Standardizzazione comandi di run e logging

* ⬜ Definizione comandi di run standard (es. `python -m src.jobs.00_smoke_spark` o equivalente).
* ⬜ Setup logging minimo (console + livello configurabile da config).

**DoD (01.3):**
* Esiste un modo unico e pulito di eseguire i job.
* Logging leggibile e coerente.

### 01.4 — README.md v0.1 (entrypoint minimo, stabile)
Il file `README.md` in root rappresenta l’**entrypoint ufficiale** del repository: è la prima interfaccia di comunicazione verso chiunque cloni o visiti il progetto (recruiter, colleghi, revisori, o lo stesso autore nel tempo). In un contesto ingegneristico, rimandare la sua creazione esclusivamente a fasi finali (es. Step 10) è tecnicamente possibile, ma introduce un rischio pratico: nelle prime iterazioni il repository appare “incompleto” e manca un punto di ingresso che renda immediatamente chiari **scopo**, **setup** ed **esecuzione minima riproducibile**.

Per questo motivo si adotta un approccio a **due livelli di maturità documentale**, coerente con le best practices di progettazione incrementale:

* **README v0.1 (Step 01.4)**: versione **minimale e stabile**, progettata per essere aggiornata raramente. Ha l’obiettivo di garantire un onboarding rapido e corretto, includendo esclusivamente informazioni “certe” e già verificabili: contesto del progetto, struttura essenziale, setup ambiente e comando di esecuzione dello smoke test.
* **README v1.0 (Step 10)**: versione **completa e portfolio-ready**, focalizzata su risultati, pipeline end-to-end, KPI, output finali, esempi e materiali dimostrativi (screenshot o estratti).

La collocazione di questo step **dopo lo smoke test locale (01.2) e la standardizzazione dei comandi (01.3)** non è casuale: solo in quel punto il progetto dispone di un comportamento minimo realmente riproducibile e quindi documentabile in modo “truth-first”. Il README v0.1 non deve diventare una documentazione narrativa estesa, ma un **contratto di utilizzo**: chi clona il repo deve poter eseguire almeno un job reale in locale con pochi passaggi e senza ambiguità.

Inoltre, la presenza di una nota esplicita su `data/raw/` e `samples/` è parte integrante della qualità del repository: si evita la pubblicazione di dataset pesanti o non versionabili, mantenendo al tempo stesso un set di input leggero e replicabile per sviluppo e test. Questo rende il progetto **pulito, dimostrabile e sostenibile**, senza compromettere la disciplina tipica di un workflow data engineering.

* ⬜ Creazione `README.md` in root (v0.1) con:
  * scopo del progetto (2–3 righe)
  * struttura repo (breve)
  * setup rapido (venv + requirements)
  * comando di run smoke test
  * nota su `data/raw/` (local-only) e `samples/` (versionabili)

**DoD (01.4):**
* Il repo ha un entrypoint minimo leggibile e sufficiente a eseguire lo smoke test in locale.

---

## 02 — 🟡 Data catalog e layout del dato (RAW → Lakehouse)

**Obiettivo:** fissare una disciplina chiara tra dato grezzo e dato materializzato.

* ⬜ Inventario sorgenti COVID/Vaccini (file, formati, chiavi, date).
* ⬜ Definizione schema “iniziale” atteso per ogni sorgente (versione 0).
* ✅ Creazione dataset “samples” (estratti piccoli) in `samples/` per sviluppo e test rapidi.
* ⬜ Regole di naming per dataset e versioni (minimo comune).
* ⬜ Decisione formato lakehouse (Parquet come default).

**DoD (02):**

* È chiaro cosa è “raw” e cosa è “lakehouse”.
* Esistono samples minimi utilizzabili per sviluppo/test senza dataset completi.

---

## 03 — ⬜ Contratto Bronze/Silver/Gold (disegno dati)

**Obiettivo:** definire cosa produce ogni layer, con confini netti e verificabili.

* ⬜ Definizione output Bronze (ingestion):

  * colonne tecniche (es. `ingestion_ts`, `source_file`)
  * naming e path definiti
* ⬜ Definizione output Silver (clean/standardize):

  * cast tipi + standardizzazione date/regioni
  * deduplica e validazioni base
  * normalizzazione chiavi di join
* ⬜ Definizione output Gold (serving/KPI):

  * tabelle KPI e aggregati pronti per reporting

**DoD (03):**

* Lista formale di dataset Bronze/Silver/Gold con scopo e path.
* Job list dichiarata con ordine di esecuzione (MVP).

---

## 04 — ⬜ Implementazione ingestion Bronze (multi-sorgente reale)

**Obiettivo:** portare i dati grezzi nel lakehouse in modo ripetibile.

* ⬜ Job Bronze: ingest CSV somministrazioni → `lakehouse/bronze/...`
* ⬜ Job Bronze: ingest copertura (CSV/JSON a seconda della sorgente reale) → `lakehouse/bronze/...`
* ⬜ Validazione minima post-write:

  * conteggio righe
  * schema atteso
  * presenza colonne tecniche
* ⬜ Output in formato colonnare (Parquet) con modalità write definita (config).

**DoD (04):**

* Dataset Bronze materializzati correttamente e rileggibili.
* Log di esecuzione e check minimi “pass/fail” espliciti.

---

## 05 — ⬜ Silver: pulizia, standardizzazione, dedup e join

**Obiettivo:** ottenere dataset affidabili e coerenti per analisi.

* ⬜ Job Silver: clean somministrazioni

  * cast tipi, gestione null, normalizzazione date
  * dedup (criteri dichiarati)
* ⬜ Job Silver: clean copertura

  * parsing e normalizzazione campi
  * standardizzazione chiavi territoriali e temporali
* ⬜ Job Silver: arricchimento/join (se utile) per creare una vista “enriched”.

**DoD (05):**

* Dataset Silver coerenti (schema stabile) e con qualità migliore del Bronze.
* Join riproducibili e motivati.

---

## 06 — ⬜ Gold: KPI e tabelle per reporting

**Obiettivo:** produrre output finali “da BI” e facilmente consumabili.

* ⬜ KPI trend temporali (giornaliero/settimanale) nazionale e/o regionale.
* ⬜ KPI ranking regioni (top/bottom) per copertura e/o incrementi.
* ⬜ KPI confronti temporali (periodi differenti) se rilevante.
* ⬜ Export controllato in `outputs/` (CSV/Parquet) per demo/report.

**DoD (06):**

* Almeno 2–3 tabelle Gold complete, leggibili e documentate.
* Output esportabile senza passaggi manuali.

---

## 07 — ⬜ Qualità dati e test (data engineering rigoroso)

**Obiettivo:** introdurre controlli minimi ma reali su schema e contenuto.

* ⬜ Test schema (colonne, tipi, nullability attesa).
* ⬜ Test vincoli semplici (range plausibili, date non future, chiavi non vuote).
* ⬜ Test regressione su conteggi/aggregati (a partire dai samples).
* ⬜ Data quality report leggero (log + metriche essenziali).

**DoD (07):**

* Suite minima di test eseguibile in locale e riproducibile.
* Errori qualità producono fallimento esplicito (exit code/exception gestita).

---

## 08 — ⬜ Incrementalità e simulazione “azienda” (opzionale ma consigliato)

**Obiettivo:** avvicinare la pipeline a uno scenario reale (carichi periodici, dedup/upsert).

* ⬜ Simulare ingestion periodica (batch incrementali) da `data/incremental/`.
* ⬜ Strategia di dedup/upsert in Silver (chiavi e regole dichiarate).
* ⬜ Partizionamento (solo se necessario) su date/regioni per performance.

**DoD (08):**

* Pipeline capace di gestire nuovi file senza ricostruire tutto ogni volta.
* Regole di incrementalità verificabili.

---

## 09 — ⬜ Orchestrazione e automazione (local-first → CI)

**Obiettivo:** rendere l’esecuzione semplice e standardizzata.

* ⬜ Runner unico (script o entrypoint) per eseguire job in sequenza (Bronze → Silver → Gold).
* ⬜ Parametrizzazione tramite `configs/` (path, write mode, log level).
* ⬜ CI baseline (lint/format + test minimi) su push/PR (se repo su GitHub).

**DoD (09):**

* Un comando esegue la pipeline end-to-end (su samples o su dataset completo).
* Controlli automatici impediscono regressioni evidenti.

---

## 10 — ⬜ Documentazione finale e rilascio (GitHub-ready)

**Obiettivo:** rendere il progetto leggibile, valutabile e mantenibile.

* ⬜ README finale del progetto (setup reale + run + output + risultati).
* ⬜ Sezione “risultati” con esempi di KPI (anche screenshot/estratti).
* ⬜ Pulizia finale documentazione: allineamento tra output prodotti e descrizioni.

**DoD (10):**

* Il repository risulta comprensibile a un revisore esterno.
* Esecuzione, output e scelte tecniche sono tracciati e verificabili.

---

## Stato corrente ⬜ → 🟡 → ✅ (truth-first) 

* ✅ Step 00.0 completato.
* ✅ Step 00.1 completato (struttura + architettura target definita in `docs/ARCHITECTURE.md`).
* ✅ Step 00.2 completato (Git baseline + branching completati e tracciati).
* ✅ Step 00.3 completato (configs + samples + verifica raw).
* ✅ Step 01.0 completato (venv + requirements + install + import PySpark verificato).
* ⬜ Step 01.1 da iniziare (Java runtime).
* ⬜ 
* ⬜ 
* ⬜ 
