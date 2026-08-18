.PHONY: api web test lint demo compose-up compose-down

api:
	uvicorn aegisnet.app:app --app-dir apps/api/src --host 0.0.0.0 --port 4500

web:
	cd apps/web && npx --yes pnpm@10.6.3 dev

test:
	pytest -q && cd apps/web && npx --yes pnpm@10.6.3 test

lint:
	ruff check . && cd apps/web && npx --yes pnpm@10.6.3 lint

demo:
	curl -X POST http://127.0.0.1:4500/api/demo/seed

compose-up:
	docker compose up --build

compose-down:
	docker compose down -v
