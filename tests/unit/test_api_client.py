from electricity_maps.ingestion.api_client import TRANSIENT_STATUS

def test_transient_statuses_include_rate_limit_and_server_errors():
    assert {429, 500, 502, 503, 504}.issubset(TRANSIENT_STATUS)
