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
    token = get_token_from_storage(
        page, settings.token_storage, settings.token_storage_key
    )

    # --- UI import ---
    ui_path = network.import_config_by_ui()
