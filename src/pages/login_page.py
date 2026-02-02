from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self):
        # Suppress EULA dialog (if the app checks this flag)
        self.page.add_init_script("localStorage.setItem('mxviewOneShowEulaDialog', '1');")
        self.page.goto(f"{self.base_url}/#/login")

    def login(self, username: str, password: str):
        self.page.locator("#input-userName").fill(username)
        self.page.locator("#input-password").fill(password)
        self.page.locator("#button-login").click()
