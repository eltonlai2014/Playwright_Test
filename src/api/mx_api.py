from playwright.sync_api import APIRequestContext, Playwright

class MxApi:
    def __init__(self, api: APIRequestContext, base_url: str):
        self.api = api
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def new(playwright: Playwright, token: str, base_url: str) -> "MxApi":
        api = playwright.request.new_context(
            ignore_https_errors=True,
            extra_http_headers={"Authorization": f"Bearer {token}"},
        )
        return MxApi(api, base_url)

    def export_device_config(self, site_id: str, ip: str, username: str, password: str) -> bytes:
        url = (
            f"{self.base_url}/api/devices/ip/{ip}/config/site/{site_id}"
            f"?username={username}&password={password}"
        )

        resp = self.api.get(url, headers={"Accept": "*/*"})
        if not resp.ok:
            raise AssertionError(f"Unexpected status {resp.status}: {resp.text()}")
        data = resp.body()
        if not data:
            # Provide headers for diagnosis
            raise AssertionError(
                "Export config body is empty.\n"
                f"content-type={resp.headers.get('content-type')}\n"
                f"content-length={resp.headers.get('content-length')}\n"
                f"content-disposition={resp.headers.get('content-disposition')}"
            )
        return data

    def close(self):
        self.api.dispose()
