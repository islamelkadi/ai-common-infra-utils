FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY ai_infra_common/ ai_infra_common/
COPY tests/ tests/

RUN pip install --no-cache-dir -e ".[dev]"

CMD ["pytest", "-v"]
