"""Stream type classes for tap-eurostat."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_eurostat.client import EuroStatStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

class GDPStream(EuroStatStream):
    """Gross domestic product (GDP) and main components (output, expenditure and income)"""

    name = "nama_10_gdp_data"
    path = "/nama_10_gdp"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "nama_10_gdp.json"

class PopulationStream(EuroStatStream):
    """Population on 1 January by age"""
    name = "demo_pjan"
    path = "/demo_pjan"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "demo_pjan.json"

class EmploymentUnemploymentStream(EuroStatStream):
    """Labor force survey data — unemployment rate by region, age group, education level."""
    name = "lfsa_urgan"
    path = "/lfsa_urgan"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "lfsa_urgan.json"

class InflationRateStream(EuroStatStream):
    """Harmonised index of consumer prices (HICP)"""
    name = "prc_hicp_aind"
    path = "/prc_hicp_aind"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "prc_hicp_aind.json"

class GreenHauseGasEmissionsStream(EuroStatStream):
    """Greenhouse gas emissions by source"""
    name = "env_air_gge"
    path = "/env_air_gge"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "env_air_gge.json"

class MeterialDeprivationStream(EuroStatStream):
    """Material deprivation rate by age group"""
    name = "ilc_mddd11"
    path = "/ilc_mddd11"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "ilc_mddd11.json"

class RenewableEnergyStream(EuroStatStream):
    """Renewable energy consumption by type of energy"""
    name = "nrg_ind_ren"
    path = "/nrg_ind_ren"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "nrg_ind_ren.json"

class GovernmentDebtStream(EuroStatStream):
    """Government debt by sector"""
    name = "gov_10dd_edpt1"
    path = "/gov_10dd_edpt1"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "gov_10dd_edpt1.json"

class InternetUsageStream(EuroStatStream):
    """Individuals using the Internet by age group"""
    name = "isoc_ci_ifp_iu"
    path = "/isoc_ci_ifp_iu"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "isoc_ci_ifp_iu.json"

class MigrationStream(EuroStatStream):
    """Migration by age group"""
    name = "migr_imm1ctz"
    path = "/migr_imm1ctz"
    # primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "migr_imm1ctz.json"
