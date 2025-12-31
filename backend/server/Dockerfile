FROM node:20-alpine AS frontend
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ ./
RUN npm run build


FROM python:3.10-slim

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync --frozen

COPY backend/server/ ./server
COPY --from=frontend /app/client/dist ./server/static


EXPOSE 8000
CMD ["uv", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM node:20-alpine AS frontend
# WORKDIR /app/client
# COPY client/package*.json ./
# RUN npm ci
# COPY client/ ./
# RUN npm run build


# FROM python:3.10-slim

# WORKDIR /app

# COPY pyproject.toml uv.lock ./

# RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
#     && rm -rf /var/lib/apt/lists/*

# RUN curl -LsSf https://astral.sh/uv/install.sh | sh
# ENV PATH="/root/.local/bin:${PATH}"

# RUN uv sync --frozen

# COPY server/ ./server
# COPY --from=frontend /app/client/dist ./server/static


# EXPOSE 8000
# CMD ["uv", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]



