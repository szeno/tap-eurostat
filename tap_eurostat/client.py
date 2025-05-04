"""REST client handling, including EuroStatStream base class."""

from __future__ import annotations

import decimal
import typing as t
from importlib import resources

from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

from pyjstat import pyjstat

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
        """Parse a JSON‑stat response and yield records using pyjstat."""
        # Read the JSON‑stat response using pyjstat
        dataset = pyjstat.Dataset.read(response.text)
        # Convert the dataset to a DataFrame then to a list of dictionaries:
        df = dataset.write('dataframe')
        for record in df.iloc[:100].to_dict(orient='records'):
            yield record

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
            new_key = key.lower().replace(" ", "_").replace("(", "").replace(")", "")
            new_row[new_key] = value
        return new_row
