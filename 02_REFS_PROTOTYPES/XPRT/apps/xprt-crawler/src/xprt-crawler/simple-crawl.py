import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode


async def main():
    browser_config = BrowserConfig(
        verbose=True
    )  # Default browser configuration
    run_config = CrawlerRunConfig(
        # Content Processing
        remove_overlay_elements=True,
        # Cache control
        cache_mode=CacheMode.ENABLED  # Use c
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://pdm-project.org/en/latest/",
            config=run_config
        )

        if result.success:
            # Print clean content
            print("Content:", result.markdown[:500])  # First 500 chars

            # Process images
            for image in result.media["images"]:
                print(f"Found image: {image['src']}")

            # Process links
            for link in result.links["internal"]:
                print(f"Internal link: {link['href']}")

        else:
            print(f"Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())

#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         result = await crawler.arun(
#             url="https://pdm-project.org/en/latest/",
#             config=run_config
#         )

#         if not result.success:
#             print(f"Crawl failed: {result.error_message}")
#             print(f"Status code: {result.status_code}")
        
#         # Different Content Formats
#         print("RAW HTML:")
#         print(result.html)  # Raw HTML
#         print("CLEANED HTML:")
#         print(result.cleaned_html)  # Cleaned HTML
#         print("RAW MARKDOWN FROM CLEANED HTML:")
#         print(result.markdown.raw_markdown)  # Raw markdown from cleaned html
#         print("MOST RELEVANT CONTENT IN MARKDOWN:")
#         print(result.markdown.fit_markdown)  # Most relevant content in markdown
        

#         # Check Success Status 
#         print("SUCCESS STATUS:")
#         print(result.success) # True if crawl was successful
#         print("HTTP STATUS CODE:")
#         print(result.status_code) # HTTP status code (e.g., 200, 400, etc.)

#         # Access extracted media and links
#         print("DICTIONARY OF FOUND MEDIA:")
#         print(result.media) # Dictionary of found media (images, videos, audio)
#         print("DICTIONARY OF FOUND LINKS:")
#         print(result.links) # Dictionary of internal and external links

# if __name__ == "__main__":
#     asyncio.run(main())