import typer

app = typer.Typer()

@app.command()
def main():
    """Main entry point for the extract CLI."""
    typer.echo("Extract command running...")
    # Add your extraction logic here

if __name__ == "__main__":
    app()
