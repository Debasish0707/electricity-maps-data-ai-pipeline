from electricity_maps.common.config import load_config

def test_test_config_has_required_contract():
    cfg = load_config("config/test.yaml")
    assert cfg["source"]["zone"] == "FR"
    assert cfg["source"]["temporal_granularity"] == "hourly"
    assert cfg["storage"]["bronze"]
    assert cfg["storage"]["silver"]
    assert cfg["storage"]["gold"]
