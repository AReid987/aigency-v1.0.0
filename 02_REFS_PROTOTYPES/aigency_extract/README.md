# AIgency Extract

A tool for extracting, condensing, and organizing insights from YouTube videos and articles, inspired by [Fabric](https://github.com/danielmiessler/fabric) patterns.

![AIgency Extract](https://via.placeholder.com/800x450.png?text=AIgency+Extract+TUI)

## Features

- Extract essential information from YouTube videos and articles using AI
- Organize content in a searchable SQLite database
- TUI interface for easy navigation and management
- CLI commands for quick extraction and querying
- Persistent storage with automatic file generation
- Multiple extraction patterns inspired by Fabric
- Tag generation for better content organization
- Markdown export for sharing and archiving

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aigency-extract.git
cd aigency-extract

# Install with Poetry
poetry install

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key"
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
```

### TUI

The TUI provides an interactive interface to:
- Browse your collection of extracted insights
- Search by keywords, tags, or sources
- View detailed information about each extraction
- Extract new content from YouTube or articles
- Configure application settings

## Extraction Patterns

AIgency Extract includes several extraction patterns inspired by Fabric:

- `youtube_summary`: Optimized for YouTube videos with timestamps and quotes
- `extract_wisdom`: Extract wisdom, insights, and practical knowledge
- `summarize`: Create comprehensive yet concise summaries
- `extract_insights`: Focus on novel ideas and unexpected connections
- `extract_main_idea`: Identify and explain the central thesis
- `create_5_sentence_summary`: Summarize content in exactly 5 sentences

## Architecture

- **App**: CLI and TUI interfaces built with Typer and Textual
- **Data**: Pydantic models and SQLite database with sqlite-utils
- **Utils**: Helper functions for YouTube, article extraction, and AI processing
- **Patterns**: Implementation of Fabric-inspired extraction patterns

## Requirements

- Python 3.9+
- OpenAI API key
- Internet connection for YouTube/article fetching and AI processing

## License

MIT
