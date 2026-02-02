from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from src.app.settings import Settings
from src.pages.login_page import LoginPage
from src.pages.network_page import NetworkPage
from src.utils.auth import get_token_from_storage
from src.api.mx_api import MxApi
from src.utils.files import save_bytes
from pathlib import Path


def main():
    load_dotenv(override=False)
    settings = Settings()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=settings.headless)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        login = LoginPage(page, settings.base_url)
        login.open()
        login.login(settings.mx_username, settings.mx_password)

        network = NetworkPage(page)
        network.wait_loaded()
        network.dismiss_login_notification_if_any()

        token = get_token_from_storage(
            page, settings.token_storage, settings.token_storage_key
        )

        api = MxApi.new(p, token, settings.base_url)
        try:
            data = api.export_device_config(
                site_id=settings.site_id,
                ip=settings.device_ip,
                username=settings.device_username,
                password=settings.device_password,
            )
            out = save_bytes(
                str(Path("downloads") / f"{settings.device_ip}_api_export.bin"), data
            )
            print("API export saved:", out)

            ui_out = network.export_config_by_ui("downloads")
            print("UI download saved:", ui_out)

            ui_out = network.import_config_by_ui()
            print("UI import config:", ui_out)
        finally:
            api.close()
            context.close()
            browser.close()


if __name__ == "__main__":
    main()
