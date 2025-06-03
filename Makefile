APP_NAME=main
VENV=.venv

.PHONY: help install makemigrations migrate runserver createapp clean

help:
	@echo "Makefile commands:"
	@echo "  make install       - Create venv and install dependencies"
	@echo "  make makemigrations - Create alembic migration"
	@echo "  make migrate       - Run alembic migrations"
	@echo "  make runserver     - Run FastAPI server with uvicorn"
	@echo "  make createapp     - Stub for creating app (customize)"
	@echo "  make clean         - Remove virtual environment"

install:
	@if [ ! -d "$(VENV)" ]; then \
		python -m venv $(VENV); \
		$(VENV)/bin/pip install --upgrade pip; \
		if [ -f requirements.txt ]; then \
			$(VENV)/bin/pip install -r requirements.txt; \
		else \
			$(VENV)/bin/pip install fastapi uvicorn sqlalchemy alembic pydantic sqladmin; \
		fi \
	else \
		echo "$(VENV) already exists. Skipping venv creation."; \
	fi

makemigrations:
	@read -p "Enter migration message: " msg; \
	$(VENV)/bin/alembic revision --autogenerate -m "$$msg"

migrate:
	$(VENV)/bin/alembic upgrade head

runserver:
	$(VENV)/bin/uvicorn $(APP_NAME):app --reload --port 5000

createapp:
	@echo "Create app command not implemented. Add your script here."

clean:
	rm -rf $(VENV)
