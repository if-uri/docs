# Signal KVM, LLM proxy i API adapters — wnioski i plan refaktoryzacji (2026-07-09)

## Kontekst

Prace z 2026-07-08–09 obejmowały trzy linie:

1. **Zewnętrzne API** — repozytoria adapterów pod `if-uri/` (`urirun-api-mcp`, `urirun-api-a2a`, `urirun-api-rest`, `llm-urirun-com`).
2. **Proxy LLM** — `llm.urirun.com` jako cienki HTTPS proxy do OpenRouter z pass-through auth i limitem IP.
3. **Signal E2E** — tickety `IFURI-235` / `IFURI-236` / `IFURI-237` na lenovo (KVM + schema gates + wysyłka do Mateusza).

Ten dokument zbiera **wnioski operacyjne** i **plan refaktoryzacji kodu** wynikający z tych prac.

---

## Co zostało zbudowane

### Repozytoria GitHub (`github.com/if-uri/`)

| Repo | Rola | Widoczność |
|------|------|------------|
| `urirun-api-mcp` | MCP adapter (stdio JSON-RPC, `/routes` → tools, `/run`) | public |
| `urirun-api-a2a` | A2A adapter (agent card + `/invoke`) | public |
| `urirun-api-rest` | REST / OpenAI-compatible proxy (PHP) | public |
| `llm-urirun-com` | Deployment `https://llm.urirun.com` | **private** |

Lokalne ścieżki: `/home/tom/github/if-uri/<repo>/`.

### Proxy `llm-urirun-com` (i kopia w `urirun-api-rest`)

- `proxy_lib.php` — auth, rate limit, helpery HTTP.
- `index.php` — cienki entrypoint.

**Auth (kolejność):**

1. Klient wysyła `Authorization: Bearer <OPENROUTER_API_KEY>` → proxy przekazuje upstream.
2. Brak nagłówka → fallback `OPENROUTER_API_KEY` z `.env` serwera.
3. Brak obu → `401`.

**Rate limit (tylko przy kluczu serwera):**

- Per IP: domyślnie **3 req / godzinę** (`URIRUN_RATE_LIMIT_MAX`, `URIRUN_RATE_LIMIT_WINDOW_SEC`).
- Przekroczenie → `429` + `Retry-After`.
- Własny klucz klienta **nie** zużywa shared quota.

**Integracja w ekosystemie if-uri:**

- `URIRUN_LLM_API_BASE=https://llm.urirun.com/api/v1` w `urirun/.env`.
- `_litellm_call_kwargs()` w `goal.py`, `twin-human/core.py`, `urirun_flow/_util.py`, `urirun_node/_util.py` — transport przez proxy lub bezpośrednio OpenRouter.

### Signal KVM — composer focus (IFURI-237)

Nowe helpery w `urirun-connector-work/urirun_connector_work/goal.py`:

| Funkcja | Odpowiedzialność |
|---------|------------------|
| `_match_center()` | Normalizacja `center` z OCR: `{x,y}` lub `[x,y]` |
| `_locate_composer()` | OCR etykiet composera; wybór **najniższego** dopasowania (Y) |
| `_composer_click_point()` | Offset +28px pod placeholder „Message” |
| `_screen_bottom_center()` | Heurystyczny fallback (środek × 92% wysokości) |
| `_focus_signal_composer()` | focus okna → click → `type-verified` probe |
| `_preflight_signal_compose()` | observe → chat → composer focus |
| `_send_signal_type_verified()` | grounded send; retry z offsetem; fallback `plain-type` |

Harness: `urirun-connector-work/scripts/run_signal_ticket_e2e.py --ticket IFURI-237`.

---

## Wyniki testów Signal

| Ticket | Status | Uwagi |
|--------|--------|-------|
| IFURI-235 | **PASS** | Wiadomość widoczna na ekranie |
| IFURI-236 | **PASS** (wcześniej) | Weryfikacja `_verify_message_visible` vs sam recipient |
| IFURI-237 | **flaky** | Kod composera działa przy widocznym Signal; runy zależą od stanu okna na lenovo |

### Schema gates (offline / live / prompt)

- Offline snapshot `route_schemas_lenovo.json` — OK.
- Live `GET /routes` — `type-verified` z `x`, `text` w schema — OK.
- Prompt LLM zawiera `type-verified` i per-URI schema — OK.
- Gate `type_verified_exec` — flaky bez Signal na pierwszym planie (zależność od GUI).

### Najlepszy run IFURI-237 (po poprawkach)

- `plan_used=preflight-type-verified`
- `verified=True`, `status=done`
- Wysyłka bez pełnej pętli LLM (short-circuit po preflight).

### Typowe przyczyny FAIL

1. **`signal_not_focused`** — Signal niewidoczny w framebufferze (Wayland); observe pada przed composerem.
2. **`signal_window_not_verified`** — redundantny drugi verify po udanym observe (naprawione: observe wystarcza).
3. **`composer_not_located` / zły Y** — OCR trafia w search bar zamiast composer; naprawione częściowo przez bottom-most match + offset.
4. **`type-verified` draft fail** — OCR nie widzi probe w polu; fallback `plain-type` po clicku.
5. **LiteLLM error** — gdy preflight/send pada, pętla LLM jest wołana bez sensu; kosztowna i niestabilna.

---

## Wnioski techniczne

### 1. Composer to osobny problem od „Signal visible”

Udane `observe` (Chats / Search / Signal w OCR) **nie gwarantuje** focusu w polu wiadomości. Trzeba jawnego flow:

```text
click recipient → refocus Signal → OCR composer (bottom-most) → click+offset → type-verified probe → send
```

### 2. `type-verified` vs `input/command/type`

- `kvm://host/ui/command/type-verified` — poprawny kontrakt (click → type → verify draft → optional submit).
- Samo `input/command/type` bez grounded click — tekst ląduje w złym oknie (search, inna aplikacja).
- Draft verify przez OCR w composera bywa **false negative**; potrzebny fallback `plain-type` + `_verify_message_visible`.

### 3. OCR `center` nie jest jednolite

KVM zwraca `center` jako `[x,y]` lub `{x,y}`. Każdy locate/click musi używać wspólnego normalizatora (`_match_center`).

### 4. LLM loop nie powinien być ścieżką wysyłki dla Signal

Po udanym preflight wysyłka powinna być **deterministyczna** (`preflight-type-verified`). LLM zostaje na gap/repair, nie na happy path.

### 5. Proxy LLM — model kosztów

- Klient z własnym kluczem: bez limitu, bez kosztu serwera.
- Shared fallback: limit IP chroni przed nadużyciem; klucz serwera opcjonalny.

### 6. Duplikacja proxy PHP

`llm-urirun-com` i `urirun-api-rest` mają identyczny `proxy_lib.php` + `index.php` — do scalenia.

### 7. `goal.py` jest nadal god-module

Logika Signal (preflight, composer, send, LLM loop, triple-LLM prep) miesza się z work connector, TTS, diagnostics — wymaga ekstrakcji.

---

## Plan refaktoryzacji kodu

### Faza A — Signal compose (wysoki priorytet, mały diff)

| # | Zadanie | Pliki | Efekt |
|---|---------|-------|-------|
| A1 | Wydzielić moduł `signal_compose.py` z `goal.py` | `urirun-connector-work/urirun_connector_work/signal_compose.py`, `goal.py` | Testowalność, patch ≤80 linii per ticket |
| A2 | Przenieść `_match_center` do `signal_kvm.py` lub `urirun-connector-kvm` utils | `signal_kvm.py`, `backends.py` | Jedna implementacja dla locate/click |
| A3 | Udokumentować proces w `route_catalog.yaml` | `urirun-llm-runtime/docs/llm/route_catalog.yaml` | LLM widzi kanoniczny flow compose |
| A4 | Dodać przykład `urirun:processes` „signal-compose-send” | `process_examples.md` | Spójność z runtime loop |
| A5 | Stabilny gate E2E: mock lub `URIRUN_SIGNAL_E2E_REQUIRE_GUI=1` | `run_signal_ticket_e2e.py` | Mniej flaky CI |

### Faza B — URI helper compose (średni priorytet)

| # | Zadanie | Opis |
|---|---------|------|
| B1 | Nowy route `kvm://host/ui/command/focus-compose` | Łączy: focus Signal → locate bottom composer → click+offset → optional probe; jeden POST zamiast 4–6 kroków |
| B2 | Handler w `urirun-connector-kvm/core.py` | Reuse logiki z `_focus_signal_composer` (po przeniesieniu do współdzielonego modułu) |
| B3 | Snapshot schema w `route_schemas_lenovo.json` | Offline gate dla focus-compose |
| B4 | Deprecate duplikaty w `goal.py` | `goal` woła URI zamiast inline Python |

### Faza C — LLM transport i proxy (średni priorytet)

| # | Zadanie | Opis |
|---|---------|------|
| C1 | Wspólny pakiet PHP `urirun-llm-proxy` lub submodule | Jedna kopia `proxy_lib.php` dla `llm-urirun-com` i `urirun-api-rest` |
| C2 | nginx/vhost + deploy doc dla `llm.urirun.com` | `llm-urirun-com/docs/deploy.md` |
| C3 | `env_loader.llm_api_base()` jako single entry | Usunąć rozproszone `_litellm_call_kwargs` kopie |
| C4 | Test integracyjny proxy (curl) w CI | `tests/proxy_integration.sh` |

### Faza D — Uproszczenie `send_via_kvm` (niższy priorytet, większy diff)

| # | Zadanie | Opis |
|---|---------|------|
| D1 | Tryby wysyłki jako enum/strategy | `scripted` / `preflight-tv` / `llm-loop` / `triple-prep` — jedna ścieżka wejścia |
| D2 | `SIGNAL_KVM_MODE` env zamiast kombinacji flag | `URIRUN_LLM_RUNTIME_CONTROL`, `SIGNAL_KVM_PREP` |
| D3 | Przenieść triple-LLM prep do osobnego modułu | `signal_prep.py` |
| D4 | Ograniczyć `goal.py` do delegacji | Cel: <200 linii Signal-related w goal |

### Faza E — API adapters (niski priorytet)

| # | Zadanie | Opis |
|---|---------|------|
| E1 | `.gitignore` `__pycache__` w mcp/a2a | Higiena repo |
| E2 | OpenAPI spec dla `urirun-api-rest` | `openapi.yaml` |
| E3 | Wspólny `URIRUN_RUNTIME_URL` w `.env.example` wszystkich adapterów | Spójna konfiguracja |

---

## Rekomendowany porządek (najbliższe 3 tickety)

1. **A1 + A2** — `signal_compose.py` + `_match_center` w jednym miejscu; regression tests przeniesione z `test_signal_scripted.py`.
2. **B1** — `focus-compose` URI na lenovo; IFURI-237 E2E woła jeden URI zamiast Python orchestration.
3. **C1** — deduplikacja proxy PHP; `llm-urirun-com` pozostaje private deployment repo.

---

## Komendy operacyjne

```bash
# Proxy test (llm-urirun-com)
php llm-urirun-com/tests/proxy_lib_test.php

# Signal unit tests
cd urirun-connector-work && python -m pytest tests/test_signal_scripted.py -q

# Signal E2E — jeden ticket (Signal musi być widoczny na lenovo)
python urirun-connector-work/scripts/run_signal_ticket_e2e.py --ticket IFURI-237 --skip-gates

# Repo visibility
gh repo view if-uri/llm-urirun-com --json visibility
```

---

## Koru headless drive — OpenRouter zamiast Claude (429)

> **Kanoniczna dokumentacja koru:** `semcod/koru/docs/llm-provider-configuration.md`
> (pełna matryca klient × provider × role LLM).

### Objaw

W `.planfile/.koru/integration-actions.jsonl` powtarza się `client command failed` z:

```text
API Error: Request rejected (429) · Weekly/Monthly Limit Exhausted
```

oraz (osobno) `unsupported execute profile 'automation'` przy próbie aider.

### Przyczyna

1. **Koru ładował tylko `<project>/.env`**, a kanoniczna konfiguracja if-uri jest w **`urirun/.env`** (`OPENROUTER_API_KEY`, `KORU_TILLM_CLIENT=aider`, …).
2. Przy `--ide auto` bez edytora koru brał **pierwszego klienta na PATH** (często `claude-code`) zamiast `KORU_TILLM_CLIENT`.
3. `KORU_TILLM_EXECUTE_PROFILE=automation` było wymuszane dla wszystkich klientów — **aider obsługuje tylko `default`**.

### Naprawa (2026-07-09)

| Warstwa | Zmiana |
|---------|--------|
| `koru` `dotenv_loader` | Ładuje też `urirun/.env` (po `.env` / `.env.local`) |
| `koru` `setup_autonomous_session` | `load_dotenv(project)` na starcie pętli |
| `koru` `cycle_config` | Preferuje `KORU_TILLM_CLIENT` / `URIRUN_KORU_IDE`; profil `automation` tylko gdy klient go wspiera |
| `urirun/.env` | `TILLM_PROVIDER=openrouter` — tillm kieruje aider na OpenRouter |

### Wymagane zmienne (`urirun/.env`)

```bash
OPENROUTER_API_KEY=sk-or-...
TILLM_PROVIDER=openrouter
URIRUN_KORU_IDE=aider
KORU_TILLM_CLIENT=aider
KORU_TILLM_MODEL=openrouter/deepseek/deepseek-v4-pro
KORU_TILLM_EXECUTE_PROFILE=          # puste → default (aider)
KORU_AUTOPILOT_BACKEND=tillm_shell
```

### Inicjalizacja lane aider

```bash
cd /home/tom/github/if-uri
koru --init-agent-lane --agent-lane aider --project .
# opcjonalnie: source .planfile/.koru/shell-env.sh
koru autonomous up --project . --agent-lane aider --ide aider
```

### Weryfikacja (bez pełnego drive)

```bash
cd /home/tom/github/if-uri
python3 -c "from pathlib import Path; from koru.dotenv_loader import load_dotenv; load_dotenv(Path('.')); import os; print('client', os.getenv('KORU_TILLM_CLIENT')); print('or_key', bool(os.getenv('OPENROUTER_API_KEY')))"
tillm provider probe openrouter
tillm drive --client aider --prompt 'say ok' --dry-run --provider openrouter
```

---

## Status na 2026-07-09

| Obszar | Stan |
|--------|------|
| Repozytoria API na GitHub | opublikowane |
| `llm-urirun-com` private | tak |
| Proxy pass-through + rate limit | wdrożone |
| Composer preflight + short-circuit send | wdrożone w `goal.py` |
| IFURI-235 / 236 | PASS |
| IFURI-237 live | flaky (zależność GUI); najlepszy run: `preflight-type-verified` OK |
| Koru headless → OpenRouter (aider) | naprawione w koru + `TILLM_PROVIDER` w `urirun/.env` |
| Refaktoryzacja modułowa | **plan powyżej, nie wdrożona** |

---

## Powiązane pliki (source of truth do czasu refaktoryzacji)

- `urirun-connector-work/urirun_connector_work/goal.py` — orchestracja Signal + LLM loop
- `urirun-connector-work/urirun_connector_work/signal_kvm.py` — stałe, defaults, COMPOSER_LABELS
- `urirun-connector-kvm/urirun_connector_kvm/core.py` — `ui/command/type-verified`
- `urirun-connector-work/scripts/run_signal_ticket_e2e.py` — harness E2E
- `llm-urirun-com/proxy_lib.php` — proxy auth/rate limit
- `urirun/.env.example` — `URIRUN_LLM_API_BASE`, `OPENROUTER_API_KEY`
