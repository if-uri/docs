# `master` → `main` — migracja gałęzi (dla kontrybutorów)

**Kiedy:** 2026-07-15. **Zakres:** wszystkie repozytoria `github.com/if-uri/*`.

Domyślną gałęzią jest teraz **`main`**. Stara `master` została wycofana we wszystkich repo.
Zmiana zrobiona oficjalnym mechanizmem GitHuba, więc: historia zachowana, otwarte PR-y
automatycznie przepięte na `main`, a stare linki/odwołania do `master` są przekierowywane.

## Co musisz zrobić w swoich lokalnych klonach

Jeśli masz repo if-uri sklonowane na dysku, Twój lokalny `master` śledzi gałąź, której już nie
ma na serwerze. Napraw to **raz** w każdym klonie.

### Najszybciej — jednym skryptem (naprawia wszystkie klony naraz)

```bash
cd ~/github/if-uri            # folder, w którym trzymasz repo if-uri
git -C . pull                 # pobierz skrypt (albo skopiuj scripts/adopt-main-local.sh)
bash scripts/adopt-main-local.sh
```

Skrypt jest bezpieczny i idempotentny: zmienia tylko nazwy gałęzi i konfigurację śledzenia,
**nie rusza commitów ani plików**. Repo z niezacommitowanymi zmianami na `master` pominie z
ostrzeżeniem — wtedy zrób `commit`/`stash` i uruchom ponownie.

### Ręcznie — per repo

```bash
git checkout master           # jeśli jesteś na master
git branch -m master main     # zmień nazwę lokalnej gałęzi
git fetch origin --prune      # usuń nieistniejący origin/master
git branch -u origin/main main  # ustaw śledzenie na origin/main
git remote set-head origin -a   # zaktualizuj domyślną HEAD
```

### Na przyszłość (nowe repo)

```bash
git config --global init.defaultBranch main
```

## Ważne — czego GitHub NIE robi

github.com **nie przekierowuje** surowego `git push origin master`. Jeśli ktoś ze starym klonem
zrobi push na `master`, GitHub go odrzuci z komunikatem (nie utworzy po cichu starej gałęzi).
Dlatego:

- pushuj zawsze na `main` (albo używaj `scripts/push.sh`, które samo normalizuje `master`→`main`),
- najpierw napraw klon powyższym skryptem, potem pushuj.

Pytania: pisz do Toma.
