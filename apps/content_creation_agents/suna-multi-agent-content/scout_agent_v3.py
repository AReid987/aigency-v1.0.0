import logging
import psycopg2
from datetime import datetime
from crawl4ai import WebCrawler
from openrouter import OpenRouterClient
from psycopg2 import OperationalError as PostgresError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scout_agent.log'),
        logging.StreamHandler()
    ]
)

class ScoutAgent:
    def __init__(self):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.config = {
            "startup_grind_url": "https://www.startupgrind.com/forum",
            "growthmentor_url": "https://www.growthmentor.com/questions",
            "database": {
                "dbname": config['database']['dbname'],
                "user": config['database']['user'],
                "password": config['database']['password'],
                "host": config['database']['host']
            },
            "openrouter_api_key": config['api_keys']['openrouter']
        }
        self.crawler = WebCrawler()
        self.openrouter = OpenRouterClient(api_key=self.config["openrouter_api_key"])
        self.db_conn = None

    def setup_database(self):
        """Initialize database connection and create tables if needed"""
        try:
            self.db_conn = psycopg2.connect(**self.config["database"])
            cursor = self.db_conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    analysis TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source VARCHAR(50)
                )
            """)
            self.db_conn.commit()
            cursor.close()
            logging.info("Database setup completed successfully")
            
        except PostgresError as e:
            logging.error(f"Database connection failed: {str(e)}")
            raise

    def scrape_site(self, url, selector, source_name):
        """Generic scraping function with error handling"""
        try:
            result = self.crawler.crawl(url)
            items = []
            for item in result.extract(selector):
                title = item.extract("h3").text.strip() if source_name == "startup_grind" else item.extract("h2").text.strip()
                content = item.extract("div.content").text.strip()
                items.append({
                    "title": title,
                    "content": content,
                    "source": source_name
                })
            logging.info(f"Successfully scraped {len(items)} items from {source_name}")
            return items
            
        except Exception as e:
            logging.error(f"Failed to scrape {source_name}: {str(e)}")
            return []

    def analyze_content(self, content):
        """Content analysis with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.openrouter.complete(
                    model="gemini-pro",
                    prompt=f"Identify pain points and trends in this text: {content}",
                    max_tokens=100
                )
                return response.choices[0].text.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"Analysis failed after {max_retries} attempts: {str(e)}")
                    return "Analysis failed"
                logging.warning(f"Analysis attempt {attempt + 1} failed, retrying...")

    def save_to_database(self, data):
        """Batch database insert with error handling"""
        if not self.db_conn:
            logging.error("No database connection available")
            return False

        try:
            cursor = self.db_conn.cursor()
            query = """
                INSERT INTO posts (title, content, analysis, source, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """
            records = [
                (item["title"], item["content"], 
                 self.analyze_content(item["content"]),
                 item["source"], datetime.now())
                for item in data
            ]
            cursor.executemany(query, records)
            self.db_conn.commit()
            cursor.close()
            logging.info(f"Successfully saved {len(data)} records to database")
            return True
            
        except PostgresError as e:
            logging.error(f"Database operation failed: {str(e)}")
            self.db_conn.rollback()
            return False

    def run(self):
        """Main execution flow"""
        try:
            self.setup_database()
            
            startup_grind_posts = self.scrape_site(
                self.config["startup_grind_url"],
                "div.post",
                "startup_grind"
            )
            
            growthmentor_questions = self.scrape_site(
                self.config["growthmentor_url"],
                "div.question",
                "growthmentor"
            )
            
            all_data = startup_grind_posts + growthmentor_questions
            self.save_to_database(all_data)
            
        except Exception as e:
            logging.critical(f"Scout agent failed: {str(e)}")
        finally:
            if self.db_conn:
                self.db_conn.close()

if __name__ == "__main__":
    agent = ScoutAgent()
    agent.run()