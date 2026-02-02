from playwright.sync_api import Page

def get_token_from_storage(page: Page, storage: str, key: str) -> str:
    """Read token from localStorage/sessionStorage. Raise if missing."""
    storage = (storage or "local").lower()
    if storage not in ("local", "session"):
        raise ValueError("storage must be 'local' or 'session'")

    js = (
        f"() => window.localStorage.getItem('{key}')"
        if storage == "local"
        else f"() => window.sessionStorage.getItem('{key}')"
    )
    token = page.evaluate(js)
    if not token:
        raise AssertionError(f"Token not found in {storage}Storage key='{key}'.\n"
                             "Tip: confirm the storage key in DevTools > Application > Storage.")
    return token
