# Quiz Master

A full-stack quiz web app: Flask backend, server-rendered HTML/CSS/JS frontend,
SQLite database, session-based authentication. Built from the Quiz Master
spec (`quiz_master_details_web_site.pdf`) and the provided UI screenshots.

## Quick start

```bash
cd quizmaster
pip install -r requirements.txt
python run.py
```

Open **http://localhost:5000**, register an account, and start playing.

On the very first run, the app automatically imports the three quiz
datasets from `app/data_source/` into `instance/quizmaster.db`. This
takes 15–30 seconds (there are ~713,000 questions total across all three
datasets). Every run after that is instant.

## What's included

- **Normal Quiz 1** — all 56 categories from `quiz_dataset_56_categories.zip`,
  each played independently, browsable/searchable on the Quizzes page.
- **Normal Quiz 2** ("Play All Quiz") — its own dataset
  (`all_quiz_category_is_normal_quiz_2.csv`), started from the Home page.
- **Daily Quiz** — its own dataset (`daily_quiz.csv`), 50 questions/day,
  one attempt per calendar day, no hints.
- Scoring: +10 correct / −5 wrong (never below 0 within a single game),
  hints don't affect score, max 5 hints per game for Normal Quiz 1 & 2,
  0 hints for Daily Quiz.
- Sequential, non-repeating question delivery per category/dataset per
  user, wrapping back to the start once a dataset is exhausted.
- Pages: Home, Quizzes (56 categories), History, Leaderboard, Profile
  (Normal Quiz 1 stats + Daily Quiz streak), All Quiz (Normal Quiz 2
  stats), Quiz Playing page (shared by Normal Quiz 1 & 2), Daily Quiz
  Playing page, Login, Register.
- Dark mode (persisted per account), left sidebar nav matching the
  provided screenshots, logout confirmation modal.

## Data scope per page (as specified)

| Page | Data source |
|---|---|
| Profile | **Normal Quiz 1 only** (stats, category performance) + Daily Quiz streak |
| All Quiz | **Normal Quiz 2 only** |
| History | All 3 quiz types, searchable/filterable |
| Leaderboard | All 3 quiz types combined, across all users |
| Home | Normal Quiz 1 category breakdown + shortcuts to Play All Quiz / Daily Challenge |

## Design decisions & how the spec was interpreted

The spec (80-page doc) was occasionally ambiguous or internally
inconsistent (e.g. it says "38 categories" in one place but lists — and
the ZIP contains — 56; example question counts in the mockups don't
match the real datasets). Where that happened, this build:

- Uses the **real counts** from your datasets, not the mockup's example
  numbers (e.g. Science has ~6,600 questions, not 250 — the design
  *layout* is unchanged, only the live numbers differ).
- Shows **all 56 categories** on the Quizzes page (the ZIP's actual
  contents), since the spec's full category list (spread across a few
  pages) enumerates exactly 56 names matching the 56 CSV files.
- Implements **Normal Quiz 1 & 2 games as 15 questions**, and **Daily
  Quiz as up to 50 questions/day**, per the spec's explicit examples.
- "Category" column for Normal Quiz 2 history rows reads **"Over All"**
  (spec's literal wording) since that mode isn't tied to one category.
- **Finish & Save** persists exactly what was answered so far (so an
  early save never silently skips unanswered questions in future games);
  **Exit** discards the whole in-progress game, matching the spec.

## Database: SQLite (with a note on MySQL)

The spec asks for MySQL. This package uses **SQLite via Python's
built-in `sqlite3` module** instead, for one practical reason: it makes
the whole project runnable with just `pip install -r requirements.txt`
and no external database server to install/configure — genuinely
"unzip and run."

All the SQL in `app/db.py`, `app/quiz_engine.py`, `app/stats.py`,
`app/auth.py`, and `app/import_data.py` is plain, portable SQL (no
SQLite-only features beyond `AUTOINCREMENT`). To run this on MySQL
instead:

1. `pip install pymysql`
2. Swap the `sqlite3.connect(...)` calls in `app/db.py` for a PyMySQL
   connection (and adjust `?` placeholders to `%s`).
3. Point it at a MySQL server via connection settings of your choice.

## Cross-device sync

Because all quiz progress, scores, history, and settings are written to
the server-side database (not local storage), logging into the same
account from a different device/browser picks up exactly where you left
off — this is inherent to the server-backed design, no extra code
needed.

## Project structure

```
quizmaster/
  run.py                  # entry point: python run.py
  requirements.txt
  app/
    __init__.py            # app factory, auto-imports data on first run
    config.py
    db.py                  # sqlite3 connection helper
    schema.sql              # database schema
    categories_meta.py      # the 56 categories: key, display name, icon
    import_data.py          # CSV -> database importer
    quiz_engine.py           # gameplay logic: scoring, hints, sessions
    stats.py                 # aggregation for Profile/All Quiz/Leaderboard/Home
    auth.py                  # register/login/logout
    routes.py                # page routes
    api.py                   # JSON API used by the quiz-playing page
    data_source/              # the 3 datasets (copied in from your uploads)
    static/
      css/style.css
      js/app.js               # dark mode + logout modal
      js/quiz.js               # quiz-playing page logic
      img/logo.png
    templates/                 # all HTML pages
  instance/                    # quizmaster.db is created here on first run
```

## Notes / things you may want to adjust

- `SECRET_KEY` in `app/config.py` defaults to a dev value — set the
  `QUIZMASTER_SECRET_KEY` environment variable in production.
- The dev server (`python run.py`) is for local use; deploy behind a
  real WSGI server (gunicorn, waitress, etc.) for production.
- The Quiz Playing page's timer/pause is client-side JavaScript; the
  final time is sent to the server only when you click Finish & Save.
