from electricity_maps.common.hash import stable_hash

def test_stable_hash_is_deterministic():
    assert stable_hash({"b": 2, "a": 1}) == stable_hash({"a": 1, "b": 2})
