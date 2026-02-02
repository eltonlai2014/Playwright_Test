from pathlib import Path
from src.pages.login_page import LoginPage
from src.pages.network_page import NetworkPage
from src.utils.auth import get_token_from_storage
from src.api.mx_api import MxApi
from src.utils.files import save_bytes

def test_export_device_config_api_and_ui(playwright, page, settings):
    # --- UI login ---
    login = LoginPage(page, settings.base_url)
    login.open()
    login.login(settings.mx_username, settings.mx_password)

    network = NetworkPage(page)
    network.wait_loaded()
    network.dismiss_login_notification_if_any()

    # --- Token (from storage) ---
    token = get_token_from_storage(page, settings.token_storage, settings.token_storage_key)

    # --- API export ---
    api = MxApi.new(playwright, token, settings.base_url)
    try:
        data = api.export_device_config(
            site_id=settings.site_id,
            ip=settings.device_ip,
            username=settings.device_username,
            password=settings.device_password,
        )
        api_path = save_bytes(str(Path("downloads") / f"{settings.device_ip}_api_export.bin"), data)

        # --- UI download ---
        ui_path = network.export_config_by_ui("downloads")

        # Basic sanity checks
        assert Path(api_path).exists()
        assert Path(ui_path).exists()
        assert Path(api_path).stat().st_size > 0
        assert Path(ui_path).stat().st_size > 0

    finally:
        api.close()
