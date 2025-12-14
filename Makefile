.PHONY: install run test lint format clean docker-build docker-run

# Installation
install:
	pip install -r requirements.txt

# Run application
run:
	streamlit run src/ui/dashboard.py

# Run tests
test:
	pytest tests/ -v

# Linting
lint:
	flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__

# Format code
format:
	black src/ tests/

# Clean cache and temporary files
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf .coverage htmlcov/

# Docker commands
docker-build:
	docker build -t finsight-ai .

docker-run:
	docker run -p 8501:8501 --env-file .env finsight-ai

# Setup data directories
setup-dirs:
	mkdir -p data/raw data/vector_db






