# Invoice Management Application

A small USD invoice-management application with a FastAPI/SQLite backend and React/Vite frontend.

## Run locally

```sh
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In another terminal:

```sh
cd frontend
npm install
npm run dev
```

Run backend tests with `cd backend && .venv/bin/pytest`; build the frontend with
`cd frontend && npm run build`. See [quickstart.md](specs/001-invoice-management/quickstart.md) for the
full validation workflow.
