# TODO List - Signal Hunter

## Phase 1: Product & Architecture (Current)
- [x] Create PRD (`docs/PRD.md`)
- [x] Create Tech Spec (`docs/TECH_SPEC.md`)
- [x] Initialize Git Repo
- [ ] **Approval**: Boss reviews and approves documentation.

## Phase 2: Engineering & Core Logic (Next)
- [ ] **Dependency Management**:
    - [ ] Create `pyproject.toml` (Poetry or standard pip).
    - [ ] Add `httpx`, `playwright`, `typer`, `pydantic`, `loguru`, `beautifulsoup4`.
- [ ] **Core Modules**:
    - [ ] `src/models`: Define `Source`, `Signal`, `Alert` models.
    - [ ] `src/core/fetcher`: Implement `BaseAdapter`, `GenericAdapter`.
    - [ ] `src/core/parser`: Implement text extraction logic.
    - [ ] `src/core/engine`: Implement resonance logic.
- [ ] **CLI**: Implement `typer` entry point (`python src/main.py run`).

## Phase 3: Integration & Testing
- [ ] **Configuration**: Setup `config/settings.toml` (secrets handling).
- [ ] **Notifier**: Implement Telegram Bot integration.
- [ ] **Testing**:
    - [ ] Unit tests for Parsers.
    - [ ] Integration test for Fetcher -> Signal flow.

## Phase 4: Production & Documentation
- [ ] **Docs**: Update README.md with usage guide.
- [ ] **Cron**: Setup periodic execution (Crontab/LaunchAgent).
- [ ] **Memory**: Populate `memory/bloggers.md` with real data.
