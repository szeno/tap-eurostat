"""EuroStat entry point."""

from __future__ import annotations

from tap_eurostat.tap import TapEuroStat

TapEuroStat.cli()
