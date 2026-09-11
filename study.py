import psycopg2
import sys

class PostgresSearchEngine:
    """
    Search engine powered by PostgreSQL Full Text Search (FTS).
    Uses websearch_to_tsquery for natural query parsing and GIN indexes for speed.
    """
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                client_encoding='utf8' # <-- Исправляет ошибку UnicodeDecodeError на Windows
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            sys.exit(1)

    def setup_database(self):
        """
        Creates the documents table with an automatically generated tsvector column
        and a GIN index for lightning-fast full-text searches.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                search_vector tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
            );
            
            -- GIN (Generalized Inverted Index) for fast full-text search
            CREATE INDEX IF NOT EXISTS search_idx ON documents USING GIN (search_vector);
        """)
        
        # Очищаем таблицу при каждом запуске для чистоты теста
        self.cursor.execute("TRUNCATE TABLE documents RESTART IDENTITY;")

    def add_document(self, text: str):
        """Inserts a single document into the database."""
        self.cursor.execute(
            "INSERT INTO documents (content) VALUES (%s) RETURNING id;",
            (text,)
        )
        return self.cursor.fetchone()[0]

    def add_documents(self, docs: list):
        """Inserts multiple documents."""
        for text in docs:
            self.add_document(text)

    def search(self, query: str, top_k: int = 5) -> list:
        """
        Searches documents using websearch_to_tsquery (understands "quotes", OR, -minus)
        and ranks them using ts_rank.
        """
        search_sql = """
            SELECT id, content, ts_rank(search_vector, query) as rank
            FROM documents, websearch_to_tsquery('english', %s) query
            WHERE search_vector @@ query
            ORDER BY rank DESC
            LIMIT %s;
        """
        self.cursor.execute(search_sql, (query, top_k))
        return self.cursor.fetchall()

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()


def main():
    # ==========================================
    # ВАЖНО: Впишите ваши данные от базы данных
    # ==========================================
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "nurik2006" # <-- ЗАМЕНИТЕ НА СВОЙ ПАРОЛЬ!
    
    print("Connecting to PostgreSQL...")
    engine = PostgresSearchEngine(DB_NAME, DB_USER, DB_PASS)
    engine.setup_database()
    
    initial_docs = [
        "Python is a great programming language for beginners and data scientists.",
        "Building a search engine from scratch using Python is a fun project.",
        "Machine learning and artificial intelligence heavily rely on Python.",
        "Web development with Python involves frameworks like Django and Flask.",
        "PostgreSQL features powerful built-in full text search capabilities.",
        "Data science is the sexiest job of the 21st century."
    ]
    
    print("Indexing initial documents...")
    engine.add_documents(initial_docs)
    
    print("=" * 60)
    print("POSTGRESQL SEARCH ENGINE v1.0")
    print("Try operators: python OR django, \"data science\", -machine")
    print("Commands: .add <text> | .exit")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nSearch > ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['.exit', 'quit', 'exit']:
                print("Closing connection and exiting. Goodbye!")
                engine.close()
                sys.exit(0)
                
            if user_input.lower().startswith('.add '):
                new_text = user_input[5:].strip()
                doc_id = engine.add_document(new_text)
                print(f"[+] Document #{doc_id} added and indexed automatically by Postgres!")
                continue
                
            # Perform search
            results = engine.search(user_input, top_k=5)
            
            if not results:
                print("  No matching documents found.")
            else:
                for rank, (doc_id, text, score) in enumerate(results, 1):
                    print(f"  {rank}. [Score: {score:.4f}] (Doc {doc_id}) {text}")
                    
        except KeyboardInterrupt:
            print("\nClosing connection and exiting. Goodbye!")
            engine.close()
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()