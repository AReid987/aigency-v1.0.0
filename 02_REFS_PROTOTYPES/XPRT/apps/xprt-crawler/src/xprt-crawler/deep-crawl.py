import asyncio
from crawlai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter, DomainFilter
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy


async def process_result(result):
    """Process each crawled result."""
    if result.success:
        print(f"URL: {result.url}")
        print(f"Depth: {result.meta.get('depth', 0)}")
        # print(f"Content: {result.content[:200]}...")  # Print first 200 chars
    else:
        print(f"Failed to crawl {result.url}: {result.error_message}")


async def main():
    # 1. Define Filters
    url_filter = URLPatternFilter(patterns=["*docs*", "*blog*"])
    domain_filter = DomainFilter(allowed_domains=["example.com"], blocked_domains=["spammysite.net"])
    filter_chain = FilterChain([url_filter, domain_filter])

    # 2. Define Scorer
    keyword_scorer = KeywordRelevanceScorer(
        keywords=["crawl", "python", "data"], weight=0.8
    )

    # 3. Configure Crawler
    config = CrawlerRunConfig(
        deep_crawl_strategy=BestFirstCrawlingStrategy( # Changed to BestFirst
            max_depth=3,
            include_external=False,
            filter_chain=filter_chain,
            url_scorer=keyword_scorer,
            score_threshold=0.5, # Only crawl URLs with a score above 0.5
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        stream=True,  # Enable streaming mode
    )

    # 4. Run Crawler
    start_url = "https://example.com"
    async with AsyncWebCrawler() as crawler:
        # In streaming mode, crawler.crawl returns an async iterator
        async for result in await crawler.crawl(url=start_url, config=config):
            await process_result(result) # Await the processing of each result

if __name__ == "__main__":
    asyncio.run(main())