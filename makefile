install:
	pip install -r requirements.txt

install-test:
	pip install -r requirements_test.txt

run-local:
	uvicorn app.main:app --reload

test:
	pytest --disable-warnings
