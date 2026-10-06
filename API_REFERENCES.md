# API References

The assignment requires Electricity Maps sandbox API access and France (`FR`) hourly electricity mix/flow ingestion.

The code keeps API base URL, zone, granularity, retry policy and endpoint paths configuration-driven. The sandbox credential is supplied through `ELECTRICITY_MAPS_API_KEY` and is never stored in the repository.

For the exact API contract/version available to the candidate, validate the endpoint response against the sandbox account before final execution. The transformation layer intentionally expects the documented `zone`, timestamp, mix/flow and estimation fields but isolates source parsing from business logic.
