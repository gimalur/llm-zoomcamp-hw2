from __future__ import annotations

import os
from typing import Any

import dlt
from dotenv import load_dotenv
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


load_dotenv()


@dlt.source(name="logfire")
def logfire_source(
    read_token: str | None = None,
    sql: str = "SELECT * FROM records ORDER BY created_at DESC",
    row_limit: int = 1000,
) -> Any:
    read_token = read_token or os.getenv("LOGFIRE_READ_TOKEN") or os.getenv("LOGFIRE_TOKEN")
    if not read_token:
        raise ValueError("Set LOGFIRE_READ_TOKEN (or pass read_token) before running this pipeline.")

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://logfire-api.pydantic.dev/v1/",
            "headers": {
                "authorization": read_token,
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "query_rows",
                "endpoint": {
                    "path": "query",
                    "params": {
                        "sql": sql,
                        "json_rows": "true",
                        "limit": row_limit,
                    },
                    "data_selector": "rows",
                },
            }
        ],
    }

    yield from rest_api_resources(config)


def run() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="agent_traces_pipeline",
        destination="duckdb",
        dataset_name="agent_traces",
    )

    load_info = pipeline.run(logfire_source())
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    run()
