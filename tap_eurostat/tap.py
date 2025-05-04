"""EuroStat tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_eurostat import streams


class TapEuroStat(Tap):
    """EuroStat tap class."""

    name = "tap-eurostat"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_url",
            th.StringType(nullable=False),
            title="API URL",
            default="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data",
            description="The url for the API service",
        ),
        th.Property(
            "user_agent",
            th.StringType(nullable=True),
            description=(
                "A custom User-Agent header to send with each request. Default is "
                "'<tap_name>/<tap_version>'"
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.EuroStatStream]:
        return [
            streams.GDPStream(self),
            streams.PopulationStream(self),
            streams.EmploymentUnemploymentStream(self),
            streams.InflationRateStream(self),
            streams.GreenHauseGasEmissionsStream(self),
            streams.MeterialDeprivationStream(self),
            streams.RenewableEnergyStream(self),
            streams.GovernmentDebtStream(self),
            streams.InternetUsageStream(self),
            streams.MigrationStream(self),
        ]


if __name__ == "__main__":
    TapEuroStat.cli()
