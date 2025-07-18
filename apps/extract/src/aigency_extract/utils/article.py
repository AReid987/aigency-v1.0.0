"""Article extraction utilities."""

import re
from typing import Dict, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from aigency_extract.data.models import ArticleContent, LLMProvider


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove www. if present
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def get_article_info(url: str) -> Dict:
    """Get information about an article."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        if not url.startswith('http://') and not url.startswith('https://'):
            raise ValueError("Invalid URL scheme. Only http:// and https:// are allowed.")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract title
        title = soup.title.text.strip() if soup.title else "Unknown Title"
        
        # Try to extract author
        author = None
        author_elements = soup.select('[rel="author"], .author, .byline')
        if author_elements:
            author = author_elements[0].text.strip()
        
        # Try to extract published date
        published_date = None
        date_elements = soup.select('[property="article:published_time"], time, .date, .published')
        if date_elements:
            date_text = date_elements[0].get("datetime") or date_elements[0].text
            # Note: We'd need more sophisticated date parsing here in a real app
        
        # Count words in the main content
        # This is a simple approach; a real app would use more sophisticated content extraction
        main_content = soup.select("article, .article, .post, .content, main")
        if main_content:
            text = main_content[0].get_text()
        else:
            text = soup.get_text()
        
        # Clean text and count words
        text = re.sub(r'\s+', ' ', text).strip()
        word_count = len(text.split())
        
        return {
            "title": title,
            "author": author,
            "published_date": published_date,
            "domain": get_domain(url),
            "word_count": word_count,
            "html_content": html_content,
            "url": url,
        }
    
    except Exception as e:
        raise ValueError(f"Failed to extract article info: {str(e)}")


def create_article_content_shell(
    url: str,
    provider: LLMProvider = LLMProvider.MISTRAL,
    model: str = "mistral-large-latest",
) -> ArticleContent:
    """Create an ArticleContent object with basic info from a URL."""
    article_info = get_article_info(url)
    
    return ArticleContent(
        title=article_info.get("title", "Unknown Title"),
        url=url,
        domain=article_info.get("domain", get_domain(url)),
        author=article_info.get("author"),
        published_date=article_info.get("published_date"),
        word_count=article_info.get("word_count"),
        html_content=article_info.get("html_content"),
        summary="",  # Will be filled by extraction process
        extraction_pattern="",  # Will be filled by extraction process
        extraction_provider=provider,
        extraction_model=model,
    )
