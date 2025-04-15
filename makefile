install:
	pip install -r requirements.txt

run-local:
	uvicorn app.main:app --reload

