"""
charts.py — построение картинок-графиков (matplotlib) и сохранение их
в static/charts, чтобы Flask мог отдать их прямо в HTML-шаблоне.

Файлы называются по имени пользователя, чтобы графики разных
пользователей не перезаписывали друг друга при параллельных запросах.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CHARTS_DIR = Path(__file__).parent / "static" / "charts"


def _save(fig, filename: str) -> str:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    path = CHARTS_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return f"charts/{filename}"


def build_languages_chart(languages: pd.Series, username: str) -> str | None:
    """Круговая диаграмма топ языков программирования. Возвращает относительный путь к файлу."""
    if languages.empty:
        return None
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(languages.values, labels=languages.index, autopct="%1.0f%%", startangle=90)
    ax.set_title("Топ языков программирования")
    return _save(fig, f"{username}_languages.png")


def build_stars_chart(top_repos: pd.DataFrame, username: str) -> str | None:
    """Горизонтальный бар-чарт самых заряженных по звёздам репозиториев."""
    if top_repos.empty or top_repos["stargazers_count"].sum() == 0:
        return None
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(top_repos["name"], top_repos["stargazers_count"], color="#4C72B0")
    ax.set_xlabel("Звёзды")
    ax.set_title("Топ репозиториев по звёздам")
    ax.invert_yaxis()  # самый заряженный репозиторий — сверху
    return _save(fig, f"{username}_stars.png")


def build_activity_chart(repos_per_year: pd.Series, username: str) -> str | None:
    """Столбчатый график: сколько репозиториев создавалось по годам."""
    if repos_per_year.empty:
        return None
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(repos_per_year.index.astype(str), repos_per_year.values, color="#55A868")
    ax.set_ylabel("Количество репозиториев")
    ax.set_title("Активность по годам (дата создания репозиториев)")
    return _save(fig, f"{username}_activity.png")
