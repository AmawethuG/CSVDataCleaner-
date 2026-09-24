
.PHONY: install test run clean docker-build

install:
	pip3 install -r requirements.txt

test:
	python3 -m pytest

run:
	python3 src/csv_cleaner.py

clean:
	rm -rf data/processed/*
	rm -rf reports/*
	rm -rf .pytest_cache
	rm -rf src/__pycache__
	rm -rf tests/__pycache__

docker-build:
	docker build -t csv-data-cleaner .
