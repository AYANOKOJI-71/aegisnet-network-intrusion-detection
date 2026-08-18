# Safe Demo Runbook

The default demonstration requires Python and Node.js only. It uses no Docker, no packet capture, no real interface, no external target, and no traffic generation.

```bash
pip install -e '.[dev]'
make api
```

In a second terminal:

```bash
cd apps/web
npx --yes pnpm@10.6.3 install
npx --yes pnpm@10.6.3 dev
```

Open `http://localhost:5183` and select **Run safe demo**. The dashboard evaluates four fixed metadata scenarios and creates three explainable alerts. Select an alert to inspect the feature evidence, then use the human-controlled status actions.

The optional full lab is packaged in Compose:

```bash
docker compose up --build
```

It starts PostgreSQL, FastAPI, and the Nginx-hosted dashboard. Docker is not required to review the portfolio project.
