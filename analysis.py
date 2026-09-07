"""
analysis.py — превращаем список репозиториев в удобные для отображения
и для построения графиков структуры данных (через pandas).
"""

import pandas as pd


def repos_to_dataframe(repos: list[dict]) -> pd.DataFrame:
    """Оставляем только те поля, которые нам реально нужны."""
    df = pd.DataFrame(repos)
    if df.empty:
        return df
    columns = ["name", "language", "stargazers_count", "forks_count", "created_at", "fork"]
    df = df[[c for c in columns if c in df.columns]]
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def top_languages(df: pd.DataFrame, top_n: int = 6) -> pd.Series:
    """
    Считает, сколько репозиториев написано на каждом языке.
    Форки не считаем — иначе статистика искажается чужим кодом.
    Репозитории без указанного языка (language = None) пропускаем.
    """
    if df.empty:
        return pd.Series(dtype=int)
    own = df[df["fork"] == False]  # noqa: E712
    counts = own["language"].dropna().value_counts()
    return counts.head(top_n)


def top_starred_repos(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Топ репозиториев по количеству звёзд."""
    if df.empty:
        return df
    return df.sort_values("stargazers_count", ascending=False).head(top_n)


def repos_by_year(df: pd.DataFrame) -> pd.Series:
    """Сколько репозиториев было создано в каждом году — динамика активности."""
    if df.empty:
        return pd.Series(dtype=int)
    return df["created_at"].dt.year.value_counts().sort_index()


def summary_stats(df: pd.DataFrame) -> dict:
    """Пара общих цифр для карточки профиля."""
    if df.empty:
        return {"total_repos": 0, "total_stars": 0, "total_forks": 0}
    return {
        "total_repos": len(df),
        "total_stars": int(df["stargazers_count"].sum()),
        "total_forks": int(df["forks_count"].sum()),
    }
