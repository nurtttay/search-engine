# PostgreSQL Search Engine

Простой полнотекстовый поисковый движок на Python, построенный поверх встроенного Full Text Search (FTS) в PostgreSQL.

## 🎯 Overview

Проект демонстрирует, как реализовать полноценный полнотекстовый поиск без внешних поисковых систем (Elasticsearch, Solr и т.д.), используя только возможности PostgreSQL:

- **`tsvector`** — автоматически генерируемая колонка с поисковым представлением текста
- **GIN-индекс** — для быстрого полнотекстового поиска по большим объёмам данных
- **`websearch_to_tsquery`** — разбор запросов в привычном для пользователя виде (кавычки, `OR`, минус для исключения слов)
- **`ts_rank`** — ранжирование результатов по релевантности

Интерфейс — простой CLI: добавление документов и поиск по ним в реальном времени.

## ✨ Features

- 🔍 Полнотекстовый поиск с ранжированием по релевантности (`ts_rank`)
- 🧠 Естественный синтаксис запросов через `websearch_to_tsquery`:
  - `python OR django` — поиск по любому из слов
  - `"data science"` — точная фраза
  - `-machine` — исключить документы со словом
- ⚡ GIN-индекс для быстрого поиска даже на больших коллекциях документов
- 🔄 Автоматическая индексация — `tsvector` пересчитывается PostgreSQL при каждой вставке (`GENERATED ALWAYS AS ... STORED`)
- 💻 Интерактивный CLI для добавления документов и поиска "на лету"
- 🌍 Поддержка UTF-8 (явно указана кодировка соединения, что решает `UnicodeDecodeError` на Windows)

## 🛠️ Tech Stack

- **Python 3.8+**
- **PostgreSQL 12+** — база данных с поддержкой Full Text Search
- **psycopg2** — драйвер PostgreSQL для Python

## 📁 Project Structure

```
search-engine/
├── search_engine.py        # Основной класс PostgresSearchEngine + CLI
├── requirements.txt        # Зависимости Python
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Установленный и запущенный PostgreSQL
- pip

### 1. Клонирование репозитория

```bash
git clone https://github.com/nurtttay/search-engine.git
cd search-engine
```

### 2. Установка зависимостей

```bash
pip install psycopg2-binary
```

Либо, если есть `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Настройка подключения к базе данных

Перед запуском укажите свои данные для подключения в `main()`:

```python
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "your_password"
```

> ⚠️ Не храните реальные пароли в коде, который попадает в git. Рекомендуется вынести эти значения в переменные окружения (`.env`) или использовать `os.environ.get(...)`.

### 4. Запуск

```bash
python search_engine.py
```

При первом запуске автоматически:
- создаётся таблица `documents` с колонкой `search_vector` (`tsvector`)
- создаётся GIN-индекс `search_idx`
- таблица очищается (`TRUNCATE`) и заполняется набором демонстрационных документов

## 📖 Usage

После запуска доступен интерактивный режим:

```
============================================================
POSTGRESQL SEARCH ENGINE v1.0
Try operators: python OR django, "data science", -machine
Commands: .add <text> | .exit
============================================================

Search > python
  1. [Score: 0.6931] (Doc 2) Building a search engine from scratch using Python is a fun project.
  2. [Score: 0.5432] (Doc 1) Python is a great programming language for beginners and data scientists.

Search > "data science"
  1. [Score: 0.7500] (Doc 6) Data science is the sexiest job of the 21st century.

Search > python -machine
  ...

Search > .add PostgreSQL is an amazing relational database.
[+] Document #7 added and indexed automatically by Postgres!

Search > .exit
Closing connection and exiting. Goodbye!
```

### Команды

| Команда         | Описание                                  |
|------------------|---------------------------------------------|
| `<текст запроса>` | Полнотекстовый поиск по документам        |
| `.add <текст>`    | Добавить новый документ в индекс          |
| `.exit`           | Завершить работу и закрыть соединение с БД |

### Операторы поиска (websearch_to_tsquery)

| Оператор       | Пример              | Значение                          |
|-----------------|----------------------|-------------------------------------|
| `OR`            | `python OR django`   | Документы с любым из слов          |
| `"..."`         | `"data science"`     | Точная фраза                       |
| `-`             | `python -django`     | Исключить документы со словом      |

## 🧩 How It Works

1. При вставке документа PostgreSQL автоматически строит `tsvector` из его текста (`to_tsvector('english', content)`), сохраняя результат в отдельной колонке.
2. GIN-индекс на этой колонке позволяет искать по миллионам документов почти мгновенно.
3. Поисковый запрос преобразуется в `tsquery` через `websearch_to_tsquery`, что даёт удобный синтаксис без ручного парсинга.
4. Результаты сортируются по `ts_rank` — встроенной метрике релевантности PostgreSQL.

## 🗺️ Roadmap

- [ ] Вынести конфигурацию БД в переменные окружения / `.env`
- [ ] Поддержка нескольких языков (`to_tsvector('russian', ...)` и мультиязычный поиск)
- [ ] Пагинация результатов поиска
- [ ] Хранение метаданных документов (заголовок, источник, дата)
- [ ] Веб-интерфейс / REST API поверх текущего движка (FastAPI)
- [ ] Юнит-тесты
- [ ] Docker Compose для быстрого поднятия PostgreSQL + приложения

## 📝 License

Проект распространяется под лицензией MIT — подробности в файле [LICENSE](./LICENSE).

## 👤 Author

- **Nurtay** — [nurtttay](https://github.com/nurtttay)

## 📖 Additional Resources

- [PostgreSQL Full Text Search Documentation](https://www.postgresql.org/docs/current/textsearch.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
