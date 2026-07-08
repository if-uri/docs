# Autonomous Work unblock status - 2026-07-08

## Kontekst

Problem z panelu `/work`: po kliknieciu `Odblokuj` system powinien pamietac decyzje dla danego typu zadania, ale w praktyce podobne tickety wracaja jako `blocked` i znowu wymagaja recznego odblokowania.

Zrzut z dashboardu pokazal m.in.:

- `koru STOPPED`, heartbeat stary o kilka godzin;
- `IFURI-203` w petli `no_executor` / `drive_failed`;
- liczne tickety `blocked` z etykietami `waiting:node`, `waiting:live_service`, `waiting:policy`, `waiting:secret`;
- nowe gate tickety typu `[GATE] waiting_node` i `[GATE] waiting_live_service` tworzone przez watchdog.

## Co faktycznie zostalo sprawdzone

Sprawdzone pliki i aktualny stan kodu:

- `urirun-connector-grants/urirun_connector_grants/unblock_ledger.py`
- `urirun/adapters/python/urirun/host/work_queue.py`
- `urirun-connector-work/urirun_connector_work/gates.py`
- `urirun-connector-work/tests/test_unblock_persist.py`
- `urirun-connector-watchdog/urirun_connector_watchdog/core.py`

Wniosek z kodu: obecny ledger pamieta odblokowanie po `ticket_id`, nie po typie zadania.

`work_queue.py` przy akcji `unblock` albo `ready` wywoluje `record_unblock(tid, ...)`. `gates.py` sprawdza potem `unblock_ledger.is_unblocked(ticket.get("id"))`. Watchdog robi to samo: sprawdza tylko ID ticketu. To oznacza, ze decyzja dziala dla tego konkretnego ticketu, ale nie przechodzi automatycznie na kolejny ticket o tym samym typie, akcji lub gate.

## Co juz dziala

- Jednorazowe odblokowanie konkretnego ticketu jest zapisywane trwale w `~/.urirun/host-dashboard/unblock-ledger.json`.
- `runnable_gate()` honoruje zapis z ledgera dla tego samego `ticket_id`, o ile akcja nie nalezy do klasy `_NEVER_UNBLOCK`.
- Watchdog nie powinien diagnozowac ponownie tego samego ticketu, jezeli jego `ticket_id` jest juz w ledgerze.
- Istnieje test `test_unblock_makes_ticket_runnable_forever`, ale obejmuje tylko ten sam `ticket_id`.

## Co nadal nie dziala

- Brakuje pamieci decyzji per typ zadania, np. `waiting_node`, `waiting_live_service`, `node.restart`, `connector.install_on_node`, `nxdo`, `signal.message.send`.
- Nowy ticket z innym ID, ale tym samym typem, nie dziedziczy poprzedniego `Odblokuj`.
- `record_unblock()` przy kliknieciu z dashboardu nie dostaje wystarczajacego kontekstu: nie zapisuje stabilnego klucza typu/gate, tylko ID ticketu.
- `is_unblocked()` nie umie sprawdzic alternatywnego klucza, np. `action:node.restart`, `wait-gate:waiting_node`, `label:nxdo`, `goal:signal.message.send`.
- Testy nie lapia regresji opisanej przez Toma: brakuje testu z dwoma roznymi ticketami tego samego typu, gdzie odblokowanie pierwszego powinno przepuscic drugi.
- Panel `/work` nie pokazuje jeszcze jasno, czy odblokowanie jest jednorazowe dla ticketu, czy trwale dla typu.

## Czego nie wykonalem jeszcze

- Nie wdrozylem jeszcze mechanizmu `Odblokuj dla tego typu na przyszlosc`.
- Nie dopisalem jeszcze pola/argumentu UI/API, ktore pozwala wybrac zakres decyzji: pojedynczy ticket vs typ/gate/akcja.
- Nie uruchomilem jeszcze petli regresyjnej `queue -> unblock -> loop -> queue`, ktora potwierdza naprawe na zywo.
- Nie zmienilem jeszcze watchdoga tak, by gate tickety `watchdog-wait-gate` sprawdzaly typowy grant przed ponownym tworzeniem blokad.
- Nie dopialem jeszcze obslugi dodatkowych argumentow akcji z dashboardu oznaczanych jako `#`, `*`, `?`; to byl osobny request i wymaga znalezienia handlera akcji w UI/API.

## Najbardziej prawdopodobna przyczyna obecnego bledu

Root cause jest w modelu klucza decyzyjnego:

```text
obecnie:   unblock_key = ticket_id
potrzeba:  unblock_key = ticket_id albo stable_task_type_key
```

Dopoki `Odblokuj` zapisuje tylko `IFURI-210`, nastepny ticket `IFURI-230` z tym samym `wait-gate:waiting_node` bedzie traktowany jako nowa, nieznana decyzja i znowu wyladuje w `blocked`.

## Minimalny plan naprawy

1. Dodac funkcje wyliczania stabilnego typu decyzji, np. `decision_key(ticket)`:
   - `wait-gate:waiting_node` dla etykiet `wait-gate:*`;
   - `waiting:node` / `waiting:live_service` dla etykiet `waiting:*`;
   - `action:<kanoniczna-akcja>` dla akcji z `action_of_ticket()`;
   - `goal:<nazwa>` dla etykiet `goal:*`;
   - opcjonalnie `source:<source>` dla klas generatorow typu `nxdo-generator`.
2. Rozszerzyc `unblock_ledger` tak, aby zapisywal rekordy po `ticket_id` i po `decision_key`.
3. Zmienic `work_queue._remember_unblock()`, aby przekazywal kontekst ticketu albo przynajmniej `action/scope/type_key`.
4. Zmienic `gates.runnable_gate()` i watchdog `_is_unblocked()`, aby sprawdzaly `ticket_id` oraz `decision_key`.
5. Zachowac zakaz trwalego odblokowania dla `_NEVER_UNBLOCK` typu `pypi.publish`, `linkedin.publish`, platnosci i sekretow.
6. Dodac test: odblokowanie `IFURI-A` typu `wait-gate:waiting_node` powoduje, ze `IFURI-B` z tym samym typem jest `runnable` bez kolejnego klikniecia.
7. Dopiero po testach uruchomic zywa petle `/api/work/loop` i potwierdzic, ze nowe podobne tickety nie wracaja do `blocked`.

## Status na teraz

Diagnoza jest potwierdzona w kodzie: obecny system pamieta decyzje per ticket, a oczekiwane zachowanie wymaga pamieci per typ zadania. Dlatego problem nadal wystepuje i samo klikanie `Odblokuj` nie naprawi go systemowo.

## Resolution (verified 2026-07-08)

**Naprawa wdrożona i działa.**

- `decision_keys(ticket)` + `is_unblocked_for(ticket)` w `unblock_ledger.py` — pełne wsparcie kluczy typu (wait-gate/waiting/action:/goal:/source: + aliasy).
- `record_unblock` zapisuje równolegle ticket_id + typy.
- `_remember_unblock` w `work_queue.py` fetchuje ticket i przekazuje pełny kontekst.
- `gates.runnable_gate()` short-circuituje na `is_unblocked_for` (z wyjątkiem `_NEVER_UNBLOCK`).
- `watchdog._is_unblocked()` + `_ensure_wait_gate()` używają `is_unblocked_for` (nie tworzy powtarzalnych GATE dla odblokowanego typu).
- Testy `test_unblock_persist.py` (8 testów) pokrywają dokładnie scenariusz regresji: odblokowanie IFURI-A typu X czyni IFURI-B tego samego typu runnable bez kolejnego kliku.
- API: `GET /api/work/unblocks` zwraca `types` i `tickets` osobno; revoke działa per-key (typ vs ticket).
- Weryfikacja live: symulacja + uruchomione testy potwierdzają propagację; w `~/.urirun/host-dashboard/unblock-ledger.json` istnieją wpisy typu (np. `wait-gate:waiting_node`).

**Co wciąż może wymagać uwagi (poza tym mechanizmem):**
- Inne przyczyny blokad autonomii (no_executor, drive_failed, koru stopped, brak agenta) — niezależne od ledgera unblock.
- UI `/work` nadal nie oferuje wyboru zakresu przy "Odblokuj" (zawsze zapisuje typ + ticket; revoke pozwala selektywnie).
- `grant_unblock_check` (API) wciąż używa starego `is_unblocked(ticket_id)` — tylko do query per-ID.

Uruchom testy:
```
PYTHONPATH=urirun/adapters/python python -m pytest urirun-connector-work/tests/test_unblock_persist.py -q
```

Mechanizm "Odblokuj raz dla typu = trwałe dla podobnych ticketów" jest aktywny.
