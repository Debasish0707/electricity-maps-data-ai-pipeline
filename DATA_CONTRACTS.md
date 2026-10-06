# Data Contracts

## Bronze envelope

| Field | Type | Rule |
|---|---|---|
| payload | JSON | exact source response; immutable |
| ingestion_timestamp | UTC timestamp | required |
| source_url | string | required |
| request_id | UUID | unique per request |
| payload_checksum | SHA-256 | deterministic |

## Silver mix

`timestamp`, `updated_at`, `zone`, `energy_source`, `generation_mw`, `is_estimated`, `unit`, ingestion metadata and `year/month/day`.

Business key: `SHA256(timestamp, zone, energy_source)`.

## Silver flows

`timestamp`, `updated_at`, `zone`, `source_zone`, `destination_zone`, `flow_mw`, `is_estimated`, `unit`, ingestion metadata and `year/month/day`.

Business key: `SHA256(timestamp, source_zone, destination_zone)`.

## Gold mix

`date`, `zone_code`, `energy_source`, `generation_mwh`, `total_generation_mwh`, `generation_percentage`, `reference_timestamp`, `year`, `month`.

## Gold flows

Imports: `date`, `source_zone`, `target_zone`, `net_import_mwh`, `reference_timestamp`, `year`, `month`.

Exports: `date`, `source_zone`, `destination_zone`, `net_export_mwh`, `reference_timestamp`, `year`, `month`.

All Gold schemas are flat.
