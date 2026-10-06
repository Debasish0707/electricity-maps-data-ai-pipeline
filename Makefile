install:
	python -m pip install -e '.[dev]'

lint:
	ruff check src tests

test:
	pytest -q

security:
	bandit -q -r src

sample:
	PYTHONPATH=src python -m electricity_maps.main --config config/test.yaml --mode sample

all: lint test security
