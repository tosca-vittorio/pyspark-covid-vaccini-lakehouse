from __future__ import annotations

from pathlib import Path

from pyspark.sql import SparkSession


def _project_root() -> Path:
    # src/jobs/ -> repo root = ../../
    return Path(__file__).resolve().parents[2]


def main() -> int:
    root = _project_root()

    samples_dir = root / "samples"
    outputs_dir = root / "outputs" / "01_smoke_spark"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    input_files = {
        "soggetti_guariti": samples_dir / "soggetti_guariti_sample.csv",
        "somministrazioni": samples_dir / "somministrazioni_sample.csv",
    }

    missing = [str(p) for p in input_files.values() if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing sample files:\n" + "\n".join(missing) +
            f"\n\nExpected samples directory: {samples_dir}"
        )

    spark = (
        SparkSession.builder
        .appName("00_smoke_spark_local")
        .getOrCreate()
    )

    try:
        print(f"Spark OK: {spark.version}")
        print(f"Samples dir: {samples_dir}")

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

        # Print schema + row count
        print("\n=== soggetti_guariti_sample.csv ===")
        df_guariti.printSchema()
        print("Row count:", df_guariti.count())

        print("\n=== somministrazioni_sample.csv ===")
        df_somministrazioni.printSchema()
        print("Row count:", df_somministrazioni.count())

        # Minimal deterministic output: store just row counts
        out_path = outputs_dir / "row_counts.txt"
        out_path.write_text(
            "row_counts\n"
            f"soggetti_guariti={df_guariti.count()}\n"
            f"somministrazioni={df_somministrazioni.count()}\n",
            encoding="utf-8",
        )

        print(f"\nWrote minimal output: {out_path}")
        return 0
    finally:
        spark.stop()


if __name__ == "__main__":
    raise SystemExit(main())