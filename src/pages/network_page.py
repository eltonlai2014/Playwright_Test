from playwright.sync_api import Page
from pathlib import Path


class NetworkPage:
    def __init__(self, page: Page):
        self.page = page

    def wait_loaded(self):
        self.page.wait_for_url("**/pages/network")

    def dismiss_login_notification_if_any(self):
        notification_button = self.page.locator("#button-loginNotification-continue")
        notification_button.click()

    def export_config_by_ui(self, download_dir: str) -> str:
        """Click UI controls to export config and save to download_dir."""
        self.page.locator("#device_8").click()
        self.page.locator("#deviceControl").click()
        self.page.locator("//button[.//div[text()=' Export Config ']]").click()

        with self.page.expect_download() as download_info:
            self.page.locator("#button-export-config-export").click()

        download = download_info.value
        Path(download_dir).mkdir(parents=True, exist_ok=True)
        save_path = str(Path(download_dir) / download.suggested_filename)
        download.save_as(save_path)
        return save_path

    def import_config_by_ui(self) -> str:
        self.page.locator("#device_8").click()
        self.page.locator("#deviceControl").click()
        self.page.locator("//button[.//div[text()=' Import Config ']]").click()
        self.page.locator("#input-import-config").set_input_files(
            "./downloads/192.168.123.151.ini"
        )
        self.page.locator("#button-import-config-import").click()
        result = self.page.locator(".mat-simple-snack-bar-content").text_content()
        return result
