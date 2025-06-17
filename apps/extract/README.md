# AIgency Extract

A tool for extracting, condensing, and organizing insights from YouTube videos and articles, inspired by [Fabric](https://github.com/danielmiessler/fabric) patterns.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::'###::::'####::'######:::'########:'##::: ##::'######::'##:::'##:::
::::'## ##:::. ##::'##... ##:: ##.....:: ###:: ##:'##... ##:. ##:'##::::
:::'##:. ##::: ##:: ##:::..::: ##::::::: ####: ##: ##:::..:::. ####:::::
::'##:::. ##:: ##:: ##::'####: ######::: ## ## ##: ##:::::::::. ##::::::
:: #########:: ##:: ##::: ##:: ##...:::: ##. ####: ##:::::::::: ##::::::
:: ##.... ##:: ##:: ##::: ##:: ##::::::: ##:. ###: ##::: ##:::: ##::::::
:: ##:::: ##:'####:. ######::: ########: ##::. ##:. ######::::: ##::::::
::..:::::..::....:::......::::........::..::::..:::......::::::..:::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::'########:'##::::'##:'########:'########:::::'###:::::'######::'########:::
:: ##.....::. ##::'##::... ##..:: ##.... ##:::'## ##:::'##... ##:... ##..::::
:: ##::::::::. ##'##:::::: ##:::: ##:::: ##::'##:. ##:: ##:::..::::: ##::::::
:: ######:::::. ###::::::: ##:::: ########::'##:::. ##: ##:::::::::: ##::::::
:: ##...:::::: ## ##:::::: ##:::: ##.. ##::: #########: ##:::::::::: ##::::::
:: ##:::::::: ##:. ##::::: ##:::: ##::. ##:: ##.... ##: ##::: ##:::: ##::::::
:: ########: ##:::. ##:::: ##:::: ##:::. ##: ##:::: ##:. ######::::: ##::::::
::........::..:::::..:::::..:::::..:::::..::..:::::..:::......::::::..:::::::

## Features

- Extract essential information from YouTube videos and articles using multiple LLM providers
- Organize content in a searchable SQLite database
- TUI interface for easy navigation and management
- CLI commands for quick extraction and querying
- Support for "stitches" - chaining extraction patterns together
- Multiple extraction patterns inspired by Fabric
- Tag generation for better content organization
- Markdown export for sharing and archiving
- Integration with AIgency AI gateway

## Roadmap

1. __MCP Support__: Implement Model Context Protocol support to enable enhanced AI capabilities and tool integration
2. __Batch Processing__: Add support for processing multiple videos or articles in batch
3. __Advanced Search__: Implement semantic search capabilities
4. __Custom Patterns__: Allow users to create and save their own extraction patterns
5. __Export Formats__: Support for exporting to additional formats (PDF, HTML, etc.)
6. __Web Interface__: Create a web-based UI alternative to the TUI
7. __Collaborative Features__: Allow sharing and collaborative annotation of extracts

## Installation

```bash
# Navigate to the project directory
cd apps/extract

# Install with PDM and uv
pdm install

# Set your API keys in .env file
cp .env.example .env
# Edit .env with your preferred LLM provider keys
```

## Usage

### CLI

```bash
# Extract insights from a YouTube video
extract video https://www.youtube.com/watch?v=VIDEO_ID

# Extract insights from an article
extract article https://example.com/article-url

# List your extracts
extract list

# Show details of a specific extract
extract show 1

# Launch the TUI
extract tui

# List available extraction patterns
extract patterns

# Create a stitch (chain of patterns)
extract stitch suggest_pattern,youtube_summary https://www.youtube.com/watch?v=VIDEO_ID
```

### TUI

The TUI provides an interactive interface to:

- Browse your collection of extracted insights
- Search by keywords, tags, or sources
- View detailed information about each extraction
- Extract new content from YouTube or articles
- Configure application settings
- Create and run stitches

## Extraction Patterns

AIgency Extract includes several extraction patterns inspired by Fabric:

- `youtube_summary`: Optimized for YouTube videos with timestamps and quotes
- `extract_wisdom`: Extract wisdom, insights, and practical knowledge
- `summarize`: Create comprehensive yet concise summaries
- `extract_insights`: Focus on novel ideas and unexpected connections
- `extract_main_idea`: Identify and explain the central thesis
- `create_5_sentence_summary`: Summarize content in exactly 5 sentences
- `create_logo`: Generate logo ideas and descriptions
- `improve_art_prompt`: Enhance prompts for image generation
- And many more from the Fabric repository

## LLM Providers

AIgency Extract supports multiple LLM providers:

- Gemini
- Mistral
- Groq
- Together AI
- HuggingFace
- OpenRouter
- Void AI
- Cerebras
- GitHub Models
- Cloudflare Workers AI
- AIgency AI Gateway (custom endpoint)

## Architecture

- __App__: CLI and TUI interfaces built with Typer and Textual
- __Data__: Pydantic models and SQLite database with sqlite-utils
- __Utils__: Helper functions for YouTube, article extraction, and LLM processing
- __Patterns__: Implementation of Fabric-inspired extraction patterns
- __Stitches__: Logic for chaining patterns together
- __LLM__: Adapters for different LLM providers

## Requirements

- Python 3.9+
- API key for at least one supported LLM provider
- Internet connection for YouTube/article fetching and LLM processing

## License

### Gratitude

- Go Check It. FOr me it has the meaning distilled by time, with integrated Nostalgia, Affinity and a dash of
early milestone.

<https://github.com/danielmiessler/fabric?tab=readme-ov-file#usage>

MIT
