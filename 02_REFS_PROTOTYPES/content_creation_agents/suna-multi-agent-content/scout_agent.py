import requests
from bs4 import BeautifulSoup
import psycopg2
import openai
from datetime import datetime

# Configuration
STARTUP_GRIND_URL = "https://www.startupgrind.com/forum"
GROWTHMENTOR_URL = "https://www.growthmentor.com/questions"
DATABASE_CONFIG = {
    "dbname": "scout_data",
    "user": "admin",
    "password": "password",
    "host": "localhost"
}
OPENAI_API_KEY = "your_openai_api_key"

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

def scrape_startup_grind():
    """Scrape Startup Grind forum for new posts."""
    response = requests.get(STARTUP_GRIND_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    posts = []
    for post in soup.find_all("div", class_="post"):
        title = post.find("h3").text.strip()
        content = post.find("div", class_="content").text.strip()
        posts.append({"title": title, "content": content})
    
    return posts

def scrape_growthmentor():
    """Scrape GrowthMentor Q&A section for new questions."""
    response = requests.get(GROWTHMENTOR_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    questions = []
    for question in soup.find_all("div", class_="question"):
        title = question.find("h2").text.strip()
        content = question.find("div", class_="content").text.strip()
        questions.append({"title": title, "content": content})
    
    return questions

def analyze_content(content):
    """Analyze content using OpenAI API."""
    response = openai.Completion.create(
        engine="text-davinci-003",
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