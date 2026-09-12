# PostgreSQL Search Engine

A simple full-text search engine in Python, built on top of PostgreSQL's native Full Text Search (FTS).

## 🎯 Overview

This project demonstrates how to implement a fully functional full-text search without external search systems (Elasticsearch, Solr, etc.), using only PostgreSQL's built-in capabilities:

- **`tsvector`** — an automatically generated column holding the searchable representation of text
- **GIN index** — for fast full-text search over large volumes of data
- **`websearch_to_tsquery`** — parses queries in a user-friendly way (quotes, `OR`, minus to exclude words)
- **`ts_rank`** — ranks results by relevance

The interface is a simple CLI: add documents and search them in real time.

## ✨ Features

- 🔍 Full-text search with relevance ranking (`ts_rank`)
- 🧠 Natural query syntax via `websearch_to_tsquery`:
  - `python OR django` — match documents containing either word
  - `"data science"` — exact phrase match
  - `-machine` — exclude documents containing a word
- ⚡ GIN index for fast search even over large document collections
- 🔄 Automatic indexing — the `tsvector` column is recomputed by PostgreSQL on every insert (`GENERATED ALWAYS AS ... STORED`)
- 💻 Interactive CLI for adding documents and searching on the fly
- 🌍 UTF-8 support (connection encoding is explicitly set, which fixes `UnicodeDecodeError` on Windows)

## 🛠️ Tech Stack

- **Python 3.8+**
- **PostgreSQL 12+** — database with Full Text Search support
- **psycopg2** — PostgreSQL driver for Python

## 📁 Project Structure

```
search-engine/
├── search_engine.py        # Main PostgresSearchEngine class + CLI
├── requirements.txt        # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL installed and running
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/nurtttay/search-engine.git
cd search-engine
```

### 2. Install Dependencies

```bash
pip install psycopg2-binary
```

Or, if a `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

### 3. Configure the Database Connection

Before running, set your connection details in `main()`:

```python
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "your_password"
```

> ⚠️ Don't hardcode real passwords in code that gets committed to git. It's recommended to move these values into environment variables (`.env`) or use `os.environ.get(...)`.

### 4. Run

```bash
python search_engine.py
```

On first run, the script automatically:
- creates the `documents` table with a `search_vector` (`tsvector`) column
- creates the `search_idx` GIN index
- truncates the table and seeds it with a set of demo documents

## 📖 Usage

Once running, an interactive prompt is available:

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

### Commands

| Command          | Description                                |
|-------------------|-----------------------------------------------|
| `<query text>`     | Full-text search across all documents       |
| `.add <text>`      | Add a new document to the index             |
| `.exit`            | Close the database connection and quit      |

### Search Operators (websearch_to_tsquery)

| Operator | Example             | Meaning                             |
|-----------|-----------------------|----------------------------------------|
| `OR`      | `python OR django`    | Documents containing either word    |
| `"..."`   | `"data science"`      | Exact phrase match                  |
| `-`       | `python -django`      | Exclude documents containing a word |

## 🧩 How It Works

1. When a document is inserted, PostgreSQL automatically builds a `tsvector` from its text (`to_tsvector('english', content)`) and stores the result in a dedicated column.
2. A GIN index on that column allows searching across millions of documents almost instantly.
3. The search query is converted into a `tsquery` via `websearch_to_tsquery`, giving a convenient syntax without any manual parsing.
4. Results are sorted by `ts_rank`, PostgreSQL's built-in relevance metric.

## 🗺️ Roadmap

- [ ] Move database configuration into environment variables / `.env`
- [ ] Support multiple languages (`to_tsvector('russian', ...)` and multilingual search)
- [ ] Pagination for search results
- [ ] Store document metadata (title, source, date)
- [ ] Web interface / REST API on top of the current engine (FastAPI)
- [ ] Unit tests
- [ ] Docker Compose for quickly spinning up PostgreSQL + the app

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

## 👤 Author

- **Nurtay** — [nurtttay](https://github.com/nurtttay)

## 📖 Additional Resources

- [PostgreSQL Full Text Search Documentation](https://www.postgresql.org/docs/current/textsearch.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
