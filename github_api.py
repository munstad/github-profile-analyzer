"""
github_api.py — обёртка над публичным GitHub REST API.

Без токена GitHub даёт 60 запросов в час на IP — этого достаточно
для пары анализов, но легко упереться в лимит. Если добавить
Personal Access Token в .env (даже без единого разрешения — просто
для идентификации), лимит вырастает до 5000 запросов в час.
Токен создаётся тут: https://github.com/settings/tokens
"""

import os

import requests

API_URL = "https://api.github.com"


class GithubApiError(Exception):
    """Кидаем, когда пользователь не найден или API вернул ошибку."""


def _headers():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_user(username: str) -> dict:
    """Основная информация о пользователе: имя, био, подписчики и т.д."""
    response = requests.get(f"{API_URL}/users/{username}", headers=_headers(), timeout=10)
    if response.status_code == 404:
        raise GithubApiError(f"Пользователь '{username}' не найден на GitHub")
    if response.status_code == 403:
        raise GithubApiError("Превышен лимит запросов к GitHub API. Добавь GITHUB_TOKEN в .env")
    response.raise_for_status()
    return response.json()


def fetch_repos(username: str) -> list[dict]:
    """
    Все публичные репозитории пользователя (с пагинацией — GitHub отдаёт
    максимум 100 штук за раз).
    """
    repos = []
    page = 1
    while True:
        response = requests.get(
            f"{API_URL}/users/{username}/repos",
            headers=_headers(),
            params={"per_page": 100, "page": page, "type": "owner"},
            timeout=10,
        )
        if response.status_code == 403:
            raise GithubApiError("Превышен лимит запросов к GitHub API. Добавь GITHUB_TOKEN в .env")
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos
