from dataclasses import dataclass, field
import os


def _env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v if v is not None else default


def _env_bool(name: str, default: str = "false") -> bool:
    return _env(name, default).lower() in ("1", "true", "yes", "y")


@dataclass(frozen=True)
class Settings:
    base_url: str = field(
        default_factory=lambda: _env("BASE_URL", "https://127.0.0.1")
    )  # ✅ 修正 key
    site_id: str = field(default_factory=lambda: _env("SITE_ID", ""))

    mx_username: str = field(default_factory=lambda: _env("MX_USERNAME", "admin"))
    mx_password: str = field(default_factory=lambda: _env("MX_PASSWORD", ""))

    device_ip: str = field(default_factory=lambda: _env("DEVICE_IP", ""))
    device_username: str = field(
        default_factory=lambda: _env("DEVICE_USERNAME", "admin")
    )
    device_password: str = field(default_factory=lambda: _env("DEVICE_PASSWORD", ""))

    token_storage: str = field(
        default_factory=lambda: _env("TOKEN_STORAGE", "local")
    )  # local | session
    token_storage_key: str = field(
        default_factory=lambda: _env("TOKEN_STORAGE_KEY", "mxview_token")
    )

    headless: bool = field(default_factory=lambda: _env_bool("HEADLESS", "false"))
