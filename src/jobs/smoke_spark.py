from __future__ import annotations

from pathlib import Path

from pyspark.sql import SparkSession

from src.lib.config import load_config
from src.lib.logger import setup_job_logger


def _project_root() -> Path:
    # src/jobs/ -> repo root = ../../
    return Path(__file__).resolve().parents[2]


def main() -> int:
    root = _project_root()
    config = load_config()

    # Paths da config (root-relative)
    samples_dir = root / Path(config.paths.samples)
    outputs_dir = root / Path(config.paths.outputs) / "01c_smoke_spark"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Logging per-job in outputs/<job>/logs/
    logs_dir = outputs_dir / "logs"
    logger = setup_job_logger(job_name="01c_smoke_spark", log_level=config.log_level, logs_dir=logs_dir)

    input_files = {
        "soggetti_guariti": samples_dir / "soggetti_guariti_sample.csv",
        "somministrazioni": samples_dir / "somministrazioni_sample.csv",
    }

    missing = [str(p) for p in input_files.values() if not p.exists()]
    if missing:
        logger.error("Missing sample files:\n%s", "\n".join(missing))
        raise FileNotFoundError(
            "Missing sample files:\n" + "\n".join(missing) +
            f"\n\nExpected samples directory: {samples_dir}"
        )

    spark = (
        SparkSession.builder
        .appName(config.spark.app_name)
        .getOrCreate()
    )

    try:
        logger.info("Spark session started | version=%s", spark.version)
        logger.info("Samples dir: %s", samples_dir)
        logger.info("Outputs dir: %s", outputs_dir)

        # Read CSVs
        df_guariti = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(input_files["soggetti_guariti"]))
        )

        df_somministrazioni = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(input_files["somministrazioni"]))
        )

        # Print schema (stdout) + row count (logged)
        logger.info("Schema: soggetti_guariti_sample.csv")
        df_guariti.printSchema()
        cnt_guariti = df_guariti.count()
        logger.info("Row count | soggetti_guariti_sample.csv = %s", cnt_guariti)

        logger.info("Schema: somministrazioni_sample.csv")
        df_somministrazioni.printSchema()
        cnt_somministrazioni = df_somministrazioni.count()
        logger.info("Row count | somministrazioni_sample.csv = %s", cnt_somministrazioni)

        # Minimal deterministic output: store just row counts
        out_path = outputs_dir / "row_counts.txt"
        out_path.write_text(
            "row_counts\n"
            f"soggetti_guariti={cnt_guariti}\n"
            f"somministrazioni={cnt_somministrazioni}\n",
            encoding="utf-8",
        )
        logger.info("Wrote minimal output: %s", out_path)

        logger.info("Job completed successfully.")
        return 0

    except Exception:
        logger.exception("Job failed with unexpected error.")
        raise

    finally:
        spark.stop()
        logger.info("Spark session stopped.")


if __name__ == "__main__":
    raise SystemExit(main())
