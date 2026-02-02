# Playwright Test Project (Refactored)

## Quick start
1. Create virtualenv and install deps:
   - `pip install -r requirements.txt`
2. Install browsers:
   - `playwright install`
3. Copy `.env.example` -> `.env` and adjust values.
4. Run tests:
   - `pytest`

## What this project includes
- UI login (Page Object)
- Optional EULA suppression via localStorage init script
- API export config using `APIRequestContext` with Bearer token
- Browser-based download using `expect_download()`
- Files saved under `downloads/` (or per-test tmp dir)

## Notes
- If your token is not stored in localStorage, adjust `TOKEN_STORAGE` and `TOKEN_STORAGE_KEY` in `.env`.
- If your system relies on cookies instead of a Bearer token, you can switch API context creation to use `storage_state`.
