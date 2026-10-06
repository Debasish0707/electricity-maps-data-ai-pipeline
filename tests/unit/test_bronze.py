import json
from electricity_maps.ingestion.bronze_writer import write_raw_payload

def test_bronze_preserves_payload_and_metadata(tmp_path):
    path = write_raw_payload({"zone":"FR","data":[1]}, str(tmp_path), "mix", "https://example.test")
    envelope = json.loads(open(path, encoding="utf-8").read())
    assert envelope["payload"] == {"zone":"FR","data":[1]}
    assert envelope["source_url"] == "https://example.test"
    assert envelope["request_id"]
    assert envelope["payload_checksum"]
