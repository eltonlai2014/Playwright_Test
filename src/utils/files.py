from pathlib import Path

def save_bytes(path: str, data: bytes) -> str:
    if data is None:
        raise AssertionError("save_bytes: data is None (expected bytes)")
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"save_bytes: expected bytes, got {type(data)}")
    if len(data) == 0:
        raise AssertionError("save_bytes: data is empty (0 bytes)")

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(bytes(data))
    return str(p)
