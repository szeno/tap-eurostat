"""REST client handling, including EuroStatStream base class."""

from __future__ import annotations

import decimal
import typing as t
import os
from importlib import resources
from itertools import product

from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EuroStatStream(RESTStream):
    """EuroStat stream class without pagination."""

    records_jsonpath = "$[*]"
    # Disable pagination since the API response doesn't include pagination info:
    next_page_token_jsonpath = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return {}

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None
        
    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:

        json_stat_data = response.json()
        dimensions = json_stat_data["dimension"]
        ids = json_stat_data["id"]
        values = json_stat_data["value"]

        # Map internal IDs (like 'freq') to their full labels (like 'Time frequency')
        id_to_label = {dim: dimensions[dim].get("label", dim) for dim in ids}

        categories = {}

        for dim in ids:
            cat = dimensions[dim]["category"]
            labels = cat.get("label", {})

            if "index" in cat:
                keys = cat["index"]
            elif isinstance(labels, dict):
                keys = list(labels.keys())
            else:
                raise ValueError(f"Cannot determine order for dimension: {dim}")

            label_values = [labels.get(k, k) for k in keys]
            categories[dim] = label_values

        # Create readable column names and prepare row generation
        readable_dim_names = [id_to_label[dim] for dim in ids]
        dimension_combinations = product(*[categories[dim] for dim in ids])
        is_values_dict = isinstance(values, dict)

        # Read limit from environment variable for testing
        # This is a workaround for the test suite to limit the number of records
        # returned by the API. In production, this should be set to None or a
        # reasonable number
        limit_str = os.environ.get("EUROSTAT_YIELD_LIMIT")
        limit = int(limit_str) if limit_str and limit_str.isdigit() else None

        for i, combination in enumerate(dimension_combinations):
            if limit is not None and i >= limit:
                break
            val = values.get(str(i)) if is_values_dict else (
                values[i] if i < len(values) else None
            )
            yield {dim_name: label for dim_name, label in zip(readable_dim_names, combination)} | {"value": val}

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Transform raw data to match expected structure.

        Downcase keys, remove spaces, and delete parentheses.
        
        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary.
        """
        new_row = {}
        for key, value in row.items():
            # Lowercase keys, remove spaces, and remove parentheses
            new_key = key.lower().replace(" ", "_").replace("(", "").replace(")", "")[:63] # Postgres not allowed longer string as column name
            new_row[new_key] = value
        return new_row
