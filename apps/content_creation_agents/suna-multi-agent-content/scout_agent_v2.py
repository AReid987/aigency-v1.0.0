import requests
import psycopg2
from datetime import datetime
from crawl4ai import WebCrawler
from openrouter import OpenRouterClient

# Configuration
STARTUP_GRIND_URL = "https://www.startupgrind.com/forum"
GROWTHMENTOR_URL = "https://www.growthmentor.com/questions"
DATABASE_CONFIG = {
    "dbname": "scout_data",
    "user": "admin",
    "password": "password",
    "host": "localhost"
}
OPENROUTER_API_KEY = "test_api_key"

# Initialize OpenRouter
openrouter = OpenRouterClient(api_key=OPENROUTER_API_KEY)

# Initialize Crawl4AI
crawler = WebCrawler()

def scrape_startup_grind():
    """Scrape Startup Grind forum using Crawl4AI."""
    result = crawler.crawl(STARTUP_GRIND_URL)
    posts = []
    for post in result.extract("div.post"):
        title = post.extract("h3").text.strip()
        content = post.extract("div.content").text.strip()
        posts.append({"title": title, "content": content})
    return posts

def scrape_growthmentor():
    """Scrape GrowthMentor Q&A section using AgentQL."""
    result = crawler.crawl(GROWTHMENTOR_URL)
    questions = []
    for question in result.extract("div.question"):
        title = question.extract("h2").text.strip()
        content = question.extract("div.content").text.strip()
        questions.append({"title": title, "content": content})
    return questions

def analyze_content(content):
    """Analyze content using OpenRouter (Gemini model)."""
    response = openrouter.complete(
        model="gemini-pro",
        prompt=f"Identify pain points and trends in this text: {content}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

def save_to_database(data):
    """Save scraped data to PostgreSQL database."""
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    
    for item in data:
        cursor.execute(
            "INSERT INTO posts (title, content, analysis, timestamp) VALUES (%s, %s, %s, %s)",
            (item["title"], item["content"], analyze_content(item["content"]), datetime.now())
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def main():
    """Main function to run the Scout Agent."""
    startup_grind_posts = scrape_startup_grind()
    growthmentor_questions = scrape_growthmentor()
    
    all_data = startup_grind_posts + growthmentor_questions
    save_to_database(all_data)

if __name__ == "__main__":
    main()