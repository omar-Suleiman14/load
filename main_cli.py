# main_cli.py
"""
The command-line interface for the 'load' application.

This script provides a terminal-based interface for downloading videos and audio
from YouTube using the rich library for a polished user experience.
"""
import os
import subprocess
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
)
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from downloader import Downloader

console = Console()
downloader = Downloader()

# A multi-color, gradient text logo for the application.
# pylint: disable=line-too-long
ASCII_LOGO = Text.from_markup(
    """
[#4CAF50]██╗     [/#4CAF50][#68B74A] ██████╗ [/#68B74A][#8BC34A] █████╗ [/#8BC34A][#FFEB3B]██████╗ [/#FFEB3B]
[#4CAF50]██║     [/#4CAF50][#68B74A]██╔═══██╗[/#68B74A][#8BC34A]██╔══██╗[/#8BC34A][#FFEB3B]██╔══██╗[/#FFEB3B]
[#FF9800]██║     [/#FF9800][#F44336]██║   ██║[/#F44336][#F44336]███████║[/#F44336][#F44336]██║  ██║[/#F44336]
[#FF9800]██║     [/#FF9800][#F44336]██║   ██║[/#F44336][#F44336]██╔══██║[/#F44336][#F44336]██║  ██║[/#F44336]
[#FF9800]███████╗[/#FF9800][#F44336]╚██████╔╝[/#F44336][#F44336]██║  ██║[/#F44336][#F44336]██████╔╝[/#F44336]
[#FF9800]╚══════╝[/#FF9800][#F44336] ╚═════╝ [/#F44336][#F44336]╚═╝  ╚═╝[/#F44336][#F44336]╚═════╝ [/#F44336]
""",
    justify="center"
)
# pylint: enable=line-too-long


def display_welcome_screen():
    """Displays a stylized welcome screen with the app logo and system info."""
    console.clear()

    # Define the color palette bar using rich markup based on the screenshot
    palette_markup = (
        "[on #2E3440]  [/][on #BF616A]  [/][on #A3BE8C]  [/][on #EBCB8B]  [/]"
        "[on #5E81AC]  [/][on #B48EAD]  [/][on #88C0D0]  [/][on #E5E9F0]  [/]"
    )

    info_panel_text = Text.assemble(
        ("load ", "bold magenta"), ("- Zainos Project\n\n", "white"),
        ("Mission: ", "bold cyan"), ("Learning & Development\n"),
        ("Author: ", "bold cyan"), ("khomod\n"),
        ("Python: ", "bold cyan"),
        (f"{sys.version_info.major}.{sys.version_info.minor}\n\n"),  # Add spacing
        Text.from_markup(palette_markup)  # Render the markup correctly
    )
    info_panel = Panel(
        info_panel_text,
        title="[green]System Information[/green]",
        border_style="green",
        padding=(1, 2)
    )
    # Restore the original Columns layout for side-by-side view
    layout = Columns(
        [Align.center(ASCII_LOGO, vertical="middle"),
         Align.center(info_panel, vertical="middle")],
        expand=True
    )
    console.print(layout)
    console.print("\n")


def run_download(url, choice, metadata):
    """
    Handles the download and conversion process with a clean, classic progress bar.
    """
    download_path = downloader.get_downloads_folder()
    format_id = None
    audio_format = None

    if choice == '1':
        format_id = get_video_format(metadata)
        if not format_id:
            return  # User canceled or invalid choice, so exit.
    elif choice == '2':
        audio_format = get_audio_format()

    console.print()  # Add a newline for spacing
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="#4CAF50"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    )

    with progress:
        task_id = progress.add_task("[cyan]Preparing...", total=None)

        def progress_hook(d):
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if d['status'] == 'downloading':
                progress.update(
                    task_id,
                    total=total,
                    completed=d.get('downloaded_bytes', 0),
                    description="[cyan]Downloading..."
                )
            elif d['status'] == 'finished':
                progress.update(
                    task_id,
                    total=1, completed=1,
                    description="[magenta]Processing..."
                )

        if choice == '1':
            downloader.download_video(url, download_path, format_id, progress_hook)
        elif choice == '2':
            downloader.download_audio(url, download_path, audio_format, progress_hook)

        progress.update(task_id, description="[bold green]Completed!", completed=1, total=1)
        time.sleep(0.5)


def get_user_url():
    """Prompts the user for a YouTube URL, validates it, and allows exiting."""
    prompt_text = Text.assemble(
        ("Please enter a YouTube video URL", "bold yellow"),
        ("\n(or type 'exit' to quit)\n> ", "dim yellow")
    )
    while True:
        url = console.input(prompt_text).strip()

        if url.lower() == 'exit':
            return None, None  # Signal to the main loop to exit

        if not url:
            continue  # If user enters nothing, just re-prompt

        console.print("Fetching metadata...")
        metadata = downloader.fetch_metadata(url)
        if metadata:
            return url, metadata
        console.print("[bold red]Invalid URL or network error. Please try again.[/bold red]\n")


def display_options(metadata):
    """Displays video info and prompts the user to select a download type."""
    title = metadata.get('title', 'N/A')
    console.print(Panel(
        f"[bold cyan]{title}[/bold cyan]",
        title="Video Title", border_style="magenta"
    ))
    console.print(
        "\n[bold green]Select an option:[/bold green]\n"
        "1. Download Video (Choose Quality)\n"
        "2. Download Audio Only\n"
        "3. Exit"
    )
    while True:
        choice = console.input(
            "[bold yellow]Enter your choice (1-3):[/bold yellow] "
        )
        if choice in ['1', '2', '3']:
            return choice
        console.print("[bold red]Invalid choice.[/bold red]")


def get_video_format(metadata):
    """Displays available video formats and gets the user's choice."""
    formats = downloader.get_video_formats(metadata)
    if not formats:
        console.print("[bold red]No suitable video formats found.[/bold red]")
        return None
    console.print("\n[bold green]Select video quality:[/bold green]")
    for i, fmt in enumerate(formats, 1):
        console.print(f"{i}. {fmt['display']}")
    while True:
        try:
            prompt = f"[bold yellow]Enter choice (1-{len(formats)}):[/bold yellow] "
            choice_str = console.input(prompt)
            choice = int(choice_str) - 1
            if 0 <= choice < len(formats):
                return formats[choice]['id']
            console.print("[bold red]Invalid choice.[/bold red]")
        except ValueError:
            console.print("[bold red]Please enter a number.[/bold red]")


def get_audio_format():
    """Displays available audio formats and gets the user's choice."""
    console.print(
        "\n[bold green]Select audio format:[/bold green]\n"
        "1. mp3 (Standard)\n"
        "2. wav (Lossless)\n"
        "3. flac (Lossless)"
    )
    while True:
        choice = console.input(
            "[bold yellow]Enter your choice (1-3):[/bold yellow] "
        )
        if choice in ['1', '2', '3']:
            return {'1': 'mp3', '2': 'wav', '3': 'flac'}[choice]
        console.print("[bold red]Invalid choice.[/bold red]")


def open_file_in_explorer(download_path):
    """Opens the given path in the system's default file explorer."""
    try:
        if sys.platform == "win32":
            os.startfile(download_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(download_path)], check=False)
        else:
            subprocess.run(["xdg-open", str(download_path)], check=False)
    except OSError as e:
        console.print(f"[bold red]Could not open folder: {e}[/bold red]")


def post_download_options():
    """Displays post-download options and handles user choice."""
    console.print(
        "\n[bold green]What would you like to do next?[/bold green]\n"
        "1. Download another video\n"
        "2. Open the Downloads folder\n"
        "3. Exit"
    )
    while True:
        choice = console.input(
            "[bold yellow]Enter your choice (1-3):[/bold yellow] "
        )
        if choice == '1':
            main()
            return
        if choice == '2':
            open_file_in_explorer(downloader.get_downloads_folder())
            post_download_options()
            return
        if choice == '3':
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice.[/bold red]")


def main():
    """The main function to run the CLI application workflow."""
    display_welcome_screen()
    url, metadata = get_user_url()

    # If user typed 'exit' at the URL prompt, url will be None.
    if not url:
        console.print("\nGoodbye!")
        sys.exit(0)

    choice = display_options(metadata)
    if choice in ['1', '2']:
        run_download(url, choice, metadata)
        post_download_options()
    elif choice == '3':
        sys.exit(0)


if __name__ == "__main__":
    main()
