.PHONY: setup run-pipeline run-dashboard dbt-run clean

setup:
	pip install -r requirements.txt

run-pipeline:
	python pipelines/crypto_source.py

dbt-run:
	cd dbt_project && dbt run --profiles-dir .

run-dashboard:
	streamlit run app/dashboard.py

clean:
	rm -rf *.duckdb
