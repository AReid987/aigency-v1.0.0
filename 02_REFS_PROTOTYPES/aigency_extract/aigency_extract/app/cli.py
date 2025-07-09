"""Command-line interface for AIgency Extract."""

import os
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from aigency_extract.app.tui import run_tui
from aigency_extract.data.database import ExtractDatabase
from aigency_extract.data.models import ContentType
from aigency_extract.utils.article import create_article_content_shell
from aigency_extract.utils.extraction import ContentExtractor, ExtractionPatterns
from aigency_extract.utils.youtube import create_youtube_content_shell, extract_video_id

app = typer.Typer(help="Extract and organize insights from YouTube videos and articles.")
console = Console()


@app.callback()
def callback():
    """AIgency Extract - Extract and organize insights from YouTube videos and articles."""
    pass


@app.command("video")
def extract_video(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    pattern: str = typer.Option(
        ExtractionPatterns.YOUTUBE_SUMMARY,
        "--pattern", "-p",
        help="Extraction pattern to use"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (default: title.md in current directory)"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="OpenAI API key (default: OPENAI_API_KEY environment variable)",
        envvar="OPENAI_API_KEY"
    ),
):
    """Extract insights from a YouTube video."""
    try:
        # Validate URL
        if not extract_video_id(url):
            if len(url) == 11:  # Might be just the video ID
                url = f"https://www.youtube.com/watch?v={url}"
            else:
                console.print("[bold red]Invalid YouTube URL or video ID[/bold red]")
                raise typer.Exit(1)
        
        with console.status("[bold green]Fetching video information...[/bold green]"):
            # Create content shell
            content = create_youtube_content_shell(url)
        
        console.print(f"[bold green]Video found:[/bold green] {content.title}")
        
        # Extract content
        with console.status("[bold green]Extracting insights...[/bold green]"):
            extractor = ContentExtractor(api_key=api_key)
            content = extractor.extract_content(content, pattern=pattern)
        
        # Save to database
        with console.status("[bold green]Saving to database...[/bold green]"):
            db = ExtractDatabase()
            content_id = db.save_content(content)
        
        # Display summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(Panel(content.summary, title=content.title))
        
        # Display key insights
        if content.key_insights:
            console.print("\n[bold]Key Insights:[/bold]")
            for i, insight in enumerate(content.key_insights, 1):
                console.print(f"{i}. {insight}")
        
        # Save to file if requested
        if output:
            output_path = output
        else:
            # Create safe filename from title
            safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in content.title)
            safe_title = safe_title.strip().replace(" ", "_")[:50]
            output_path = Path(f"{safe_title}.md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {content.title}\n\n")
            f.write(f"Source: {content.url}\n")
            if content.channel_name:
                f.write(f"Channel: {content.channel_name}\n")
            if content.author:
                f.write(f"Author: {content.author}\n")
            f.write("\n## Summary\n\n")
            f.write(content.summary)
            
            if content.key_insights:
                f.write("\n\n## Key Insights\n\n")
                for insight in content.key_insights:
                    f.write(f"- {insight}\n")
            
            if content.main_points:
                f.write("\n\n## Main Points\n\n")
                for point in content.main_points:
                    f.write(f"- {point}\n")
            
            if content.quotes:
                f.write("\n\n## Notable Quotes\n\n")
                for quote in content.quotes:
                    f.write(f"> {quote}\n\n")
            
            if content.questions_raised:
                f.write("\n\n## Questions Raised\n\n")
                for question in content.questions_raised:
                    f.write(f"- {question}\n")
            
            if content.action_items:
                f.write("\n\n## Action Items\n\n")
                for item in content.action_items:
                    f.write(f"- {item}\n")
            
            if content.tags:
                f.write("\n\n## Tags\n\n")
                f.write(", ".join(content.tags))
        
        console.print(f"\n[bold green]Extraction complete![/bold green] Saved to {output_path}")
        console.print(f"Content ID in database: {content_id}")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("article")
def extract_article(
    url: str = typer.Argument(..., help="Article URL"),
    pattern: str = typer.Option(
        ExtractionPatterns.EXTRACT_WISDOM,
        "--pattern", "-p",
        help="Extraction pattern to use"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (default: title.md in current directory)"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="OpenAI API key (default: OPENAI_API_KEY environment variable)",
        envvar="OPENAI_API_KEY"
    ),
):
    """Extract insights from an article."""
    try:
        with console.status("[bold green]Fetching article information...[/bold green]"):
            # Create content shell
            content = create_article_content_shell(url)
        
        console.print(f"[bold green]Article found:[/bold green] {content.title}")
        
        # Extract content
        with console.status("[bold green]Extracting insights...[/bold green]"):
            extractor = ContentExtractor(api_key=api_key)
            content = extractor.extract_content(content, pattern=pattern)
        
        # Save to database
        with console.status("[bold green]Saving to database...[/bold green]"):
            db = ExtractDatabase()
            content_id = db.save_content(content)
        
        # Display summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(Panel(content.summary, title=content.title))
        
        # Display key insights
        if content.key_insights:
            console.print("\n[bold]Key Insights:[/bold]")
            for i, insight in enumerate(content.key_insights, 1):
                console.print(f"{i}. {insight}")
        
        # Save to file if requested
        if output:
            output_path = output
        else:
            # Create safe filename from title
            safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in content.title)
            safe_title = safe_title.strip().replace(" ", "_")[:50]
            output_path = Path(f"{safe_title}.md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {content.title}\n\n")
            f.write(f"Source: {content.url}\n")
            if content.domain:
                f.write(f"Domain: {content.domain}\n")
            if content.author:
                f.write(f"Author: {content.author}\n")
            f.write("\n## Summary\n\n")
            f.write(content.summary)
            
            if content.key_insights:
                f.write("\n\n## Key Insights\n\n")
                for insight in content.key_insights:
                    f.write(f"- {insight}\n")
            
            if content.main_points:
                f.write("\n\n## Main Points\n\n")
                for point in content.main_points:
                    f.write(f"- {point}\n")
            
            if content.quotes:
                f.write("\n\n## Notable Quotes\n\n")
                for quote in content.quotes:
                    f.write(f"> {quote}\n\n")
            
            if content.questions_raised:
                f.write("\n\n## Questions Raised\n\n")
                for question in content.questions_raised:
                    f.write(f"- {question}\n")
            
            if content.action_items:
                f.write("\n\n## Action Items\n\n")
                for item in content.action_items:
                    f.write(f"- {item}\n")
            
            if content.tags:
                f.write("\n\n## Tags\n\n")
                f.write(", ".join(content.tags))
        
        console.print(f"\n[bold green]Extraction complete![/bold green] Saved to {output_path}")
        console.print(f"Content ID in database: {content_id}")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("list")
def list_extracts(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of extracts to show"),
    content_type: Optional[str] = typer.Option(
        None,
        "--type", "-t",
        help="Filter by content type (youtube, article)"
    ),
    tag: Optional[str] = typer.Option(
        None,
        "--tag",
        help="Filter by tag"
    ),
):
    """List extracted content."""
    try:
        db = ExtractDatabase()
        
        # Convert content_type string to enum if provided
        content_type_enum = None
        if content_type:
            if content_type.lower() == "youtube":
                content_type_enum = ContentType.YOUTUBE
            elif content_type.lower() == "article":
                content_type_enum = ContentType.ARTICLE
            else:
                console.print(f"[bold red]Invalid content type:[/bold red] {content_type}")
                console.print("Valid types: youtube, article")
                raise typer.Exit(1)
        
        # Search content
        results = db.search_content(
            content_type=content_type_enum,
            tag=tag,
            limit=limit
        )
        
        if not results:
            console.print("[bold yellow]No extracts found.[/bold yellow]")
            return
        
        # Display results in a table
        table = Table(title=f"Extracted Content ({len(results)} results)")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Date", style="magenta")
        table.add_column("Tags", style="yellow")
        
        for content in results:
            table.add_row(
                str(content.id),
                content.title[:50] + ("..." if len(content.title) > 50 else ""),
                content.content_type.value,
                content.extracted_at.strftime("%Y-%m-%d") if content.extracted_at else "",
                ", ".join(content.tags[:3]) + ("..." if len(content.tags) > 3 else "")
            )
        
        console.print(table)
        
        # Show stats
        stats = db.get_stats()
        console.print(f"\nTotal extracts: {stats['total_content']} (YouTube: {stats['youtube_videos']}, Articles: {stats['articles']})")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("show")
def show_extract(
    content_id: int = typer.Argument(..., help="Content ID to show"),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (default: display in console)"
    ),
):
    """Show details of an extracted content."""
    try:
        db = ExtractDatabase()
        content = db.get_content(content_id)
        
        if not content:
            console.print(f"[bold red]Content with ID {content_id} not found.[/bold red]")
            raise typer.Exit(1)
        
        # Display content details
        console.print(Panel(f"[bold]{content.title}[/bold]", title=f"ID: {content.id}"))
        console.print(f"URL: {content.url}")
        console.print(f"Type: {content.content_type.value}")
        console.print(f"Extracted: {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'Unknown'}")
        console.print(f"Pattern: {content.extraction_pattern}")
        
        if content.tags:
            console.print(f"Tags: {', '.join(content.tags)}")
        
        console.print("\n[bold]Summary:[/bold]")
        console.print(content.summary)
        
        if content.key_insights:
            console.print("\n[bold]Key Insights:[/bold]")
            for i, insight in enumerate(content.key_insights, 1):
                console.print(f"{i}. {insight}")
        
        if content.main_points:
            console.print("\n[bold]Main Points:[/bold]")
            for i, point in enumerate(content.main_points, 1):
                console.print(f"{i}. {point}")
        
        if content.quotes:
            console.print("\n[bold]Notable Quotes:[/bold]")
            for i, quote in enumerate(content.quotes, 1):
                console.print(f"{i}. \"{quote}\"")
        
        if content.questions_raised:
            console.print("\n[bold]Questions Raised:[/bold]")
            for i, question in enumerate(content.questions_raised, 1):
                console.print(f"{i}. {question}")
        
        if content.action_items:
            console.print("\n[bold]Action Items:[/bold]")
            for i, item in enumerate(content.action_items, 1):
                console.print(f"{i}. {item}")
        
        # Save to file if requested
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(f"# {content.title}\n\n")
                f.write(f"Source: {content.url}\n")
                f.write(f"Type: {content.content_type.value}\n")
                f.write(f"Extracted: {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'Unknown'}\n")
                f.write(f"Pattern: {content.extraction_pattern}\n")
                
                if content.tags:
                    f.write(f"Tags: {', '.join(content.tags)}\n")
                
                f.write("\n## Summary\n\n")
                f.write(content.summary)
                
                if content.key_insights:
                    f.write("\n\n## Key Insights\n\n")
                    for insight in content.key_insights:
                        f.write(f"- {insight}\n")
                
                if content.main_points:
                    f.write("\n\n## Main Points\n\n")
                    for point in content.main_points:
                        f.write(f"- {point}\n")
                
                if content.quotes:
                    f.write("\n\n## Notable Quotes\n\n")
                    for quote in content.quotes:
                        f.write(f"> {quote}\n\n")
                
                if content.questions_raised:
                    f.write("\n\n## Questions Raised\n\n")
                    for question in content.questions_raised:
                        f.write(f"- {question}\n")
                
                if content.action_items:
                    f.write("\n\n## Action Items\n\n")
                    for item in content.action_items:
                        f.write(f"- {item}\n")
            
            console.print(f"\n[bold green]Saved to {output}[/bold green]")
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("patterns")
def list_patterns():
    """List available extraction patterns."""
    patterns = ExtractionPatterns.get_all_patterns()
    
    console.print("[bold]Available Extraction Patterns:[/bold]")
    for pattern in patterns:
        console.print(f"- {pattern}")


@app.command("tui")
def tui():
    """Launch the Text User Interface."""
    try:
        run_tui()
    except Exception as e:
        console.print(f"[bold red]Error launching TUI:[/bold red] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
