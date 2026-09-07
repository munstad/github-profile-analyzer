# 🐙 GitHub Profile Analyzer

Веб-приложение на Flask: вводишь GitHub-никнейм — получаешь
визуальную аналитику по публичным репозиториям: топ языков
программирования, самые заряженные по звёздам проекты и динамику
активности по годам.

## Возможности

- Поиск любого публичного GitHub-профиля по нику
- Круговая диаграмма топ языков программирования (по количеству репо)
- Бар-чарт репозиториев с наибольшим числом звёзд
- График активности — сколько репозиториев создавалось по годам
- Общая сводка: репозитории, звёзды, подписчики

## Стек

Python 3.11+, Flask, requests (GitHub REST API), pandas, matplotlib

## Установка и запуск

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/munstad/github-profile-analyzer
   cd github-profile-analyzer
   ```

2. Создай виртуальное окружение и установи зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. (Необязательно, но рекомендуется) скопируй `.env.example` в `.env`
   и добавь свой GitHub Personal Access Token — без него всего
   60 запросов в час на IP, с токеном — 5000:
   ```bash
   cp .env.example .env
   ```
   Создать токен: https://github.com/settings/tokens (без единого
   разрешения — просто "для идентификации" запросов).

4. Запусти сервер:
   ```bash
   python app.py
   ```

5. Открой в браузере http://localhost:5000 и введи любой GitHub-ник
   (например `torvalds` или свой собственный).

## Структура проекта

```
github-profile-analyzer/
├── app.py              # Flask-приложение, маршруты
├── github_api.py       # запросы к GitHub REST API
├── analysis.py         # обработка данных через pandas
├── charts.py           # построение графиков (matplotlib)
├── templates/
│   ├── index.html       # страница с формой ввода
│   └── result.html      # страница с результатами
├── static/charts/       # сюда сохраняются картинки графиков
├── requirements.txt
├── .env.example
└── .gitignore
```

## Возможные доработки

- Кэширование результатов (Redis/SQLite), чтобы не дёргать API повторно
- Сравнение двух профилей на одном экране
- Учитывать реальный объём кода (байты) через API языков репозитория,
  а не просто количество репозиториев на языке
- Экспорт отчёта в PDF
