from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class PathsConfig:
    raw: str
    bronze: str
    silver: str
    gold: str
    outputs: str
    samples: str


@dataclass(frozen=True)
class SparkConfig:
    app_name: str


@dataclass(frozen=True)
class AppConfig:
    paths: PathsConfig
    write_mode: str
    log_level: str
    spark: SparkConfig


def load_config(
    base_path: str | Path = "configs/app.json",
    override_path: str | Path = "configs/app.dev.json",
) -> AppConfig:
    base_config = _load_json(Path(base_path), required=True)
    override_config = _load_json(Path(override_path), required=False)
    merged = _merge_config(base_config, override_config)
    _validate_config(merged)
    return _to_app_config(merged)


def _load_json(path: Path, required: bool) -> Dict[str, Any]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Config file not found: {path}")
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in {"paths", "spark"} and isinstance(value, Mapping):
            merged[key] = _deep_merge_dict(merged.get(key, {}), value)
        else:
            merged[key] = value
    return merged


def _deep_merge_dict(base: Mapping[str, Any], override: Mapping[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        result[key] = value
    return result


def _validate_config(config: Mapping[str, Any]) -> None:
    paths = _require_mapping(config, "paths")
    for key in ("raw", "bronze", "silver", "gold", "outputs", "samples"):
        _require_non_empty_string(paths, key, context="paths")

    _require_non_empty_string(config, "write_mode")
    _require_non_empty_string(config, "log_level")

    spark = _require_mapping(config, "spark")
    _require_non_empty_string(spark, "app_name", context="spark")


def _require_mapping(config: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = config.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"Missing or invalid mapping for '{key}'.")
    return value


def _require_non_empty_string(
    config: Mapping[str, Any],
    key: str,
    context: Optional[str] = None,
) -> None:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        prefix = f"{context}." if context else ""
        raise ValueError(f"Missing or empty configuration value: '{prefix}{key}'.")


def _to_app_config(config: Mapping[str, Any]) -> AppConfig:
    paths = config["paths"]
    spark = config["spark"]
    return AppConfig(
        paths=PathsConfig(
            raw=paths["raw"],
            bronze=paths["bronze"],
            silver=paths["silver"],
            gold=paths["gold"],
            outputs=paths["outputs"],
            samples=paths["samples"],
        ),
        write_mode=config["write_mode"],
        log_level=config["log_level"],
        spark=SparkConfig(app_name=spark["app_name"]),
    )