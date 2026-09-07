"""
app.py — точка входа Flask-приложения.

Страницы:
    GET  /            — форма ввода GitHub-ника
    GET  /analyze/<username> — страница с результатами анализа
"""

import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

import analysis
import charts
from github_api import GithubApiError, fetch_repos, fetch_user

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/go", methods=["POST"])
def go():
    """Обрабатывает форму и перекидывает на страницу анализа конкретного юзера."""
    username = request.form.get("username", "").strip()
    if not username:
        return redirect(url_for("index"))
    return redirect(url_for("analyze", username=username))


@app.route("/analyze/<username>")
def analyze(username: str):
    try:
        user = fetch_user(username)
        repos = fetch_repos(username)
    except GithubApiError as e:
        return render_template("index.html", error=str(e))

    df = analysis.repos_to_dataframe(repos)
    stats = analysis.summary_stats(df)

    languages = analysis.top_languages(df)
    top_repos = analysis.top_starred_repos(df)
    by_year = analysis.repos_by_year(df)

    languages_chart = charts.build_languages_chart(languages, username)
    stars_chart = charts.build_stars_chart(top_repos, username)
    activity_chart = charts.build_activity_chart(by_year, username)

    return render_template(
        "result.html",
        user=user,
        stats=stats,
        top_repos=top_repos.to_dict("records") if not top_repos.empty else [],
        languages_chart=languages_chart,
        stars_chart=stars_chart,
        activity_chart=activity_chart,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, port=port)
