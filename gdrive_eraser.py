#!/usr/bin/env python3
"""
GDrive File Eraser
A CLI tool to find and delete large files from Google Drive by extension and size.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
import json

import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from dateutil import parser as date_parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

console = Console()


def authenticate():
    """Authenticate and return Google Drive service instance."""
    creds = None
    token_path = Path('token.json')
    credentials_path = Path('credentials.json')
    
    # Token file stores the user's access and refresh tokens
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                console.print("[red]Error: credentials.json not found![/red]")
                console.print("\nTo use this tool, you need to:")
                console.print("1. Go to https://console.cloud.google.com/")
                console.print("2. Create a project or select existing one")
                console.print("3. Enable Google Drive API")
                console.print("4. Create OAuth 2.0 credentials")
                console.print("5. Download the credentials as 'credentials.json'")
                console.print("6. Place it in the same directory as this script")
                sys.exit(1)
                
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        console.print(f"[red]An error occurred: {error}[/red]")
        sys.exit(1)


def get_folder_path(service, file_id: str, path_cache: Optional[Dict[str, str]] = None) -> str:
    """Get the full folder path for a file or folder."""
    if path_cache is None:
        path_cache = {}
    
    # If we've already calculated this path, return it
    if file_id in path_cache:
        return path_cache[file_id]
    
    try:
        # Get file metadata including parents
        file_metadata = service.files().get(
            fileId=file_id, 
            fields='id,name,parents'
        ).execute()
        
        file_name = file_metadata.get('name', 'Unknown')
        parents = file_metadata.get('parents', [])
        
        # If no parents, this is in the root directory
        if not parents:
            path = "/"
        else:
            # Recursively get the parent path
            parent_id = parents[0]  # Take the first parent
            parent_path = get_folder_path(service, parent_id, path_cache)
            
            # Build the full path
            if parent_path == "/":
                path = f"/{file_name}"
            else:
                path = f"{parent_path}/{file_name}"
        
        # Cache the result
        path_cache[file_id] = path
        return path
        
    except HttpError as error:
        console.print(f"[dim]Warning: Could not get path for {file_id}: {error}[/dim]")
        return "/Unknown"


def get_file_folder_path(service, file_data: dict, path_cache: Optional[Dict[str, str]] = None) -> str:
    """Get the folder path where a file is located (not including the file itself)."""
    if path_cache is None:
        path_cache = {}
    
    parents = file_data.get('parents', [])
    
    if not parents:
        return "/"
    
    parent_id = parents[0]
    parent_path = get_folder_path(service, parent_id, path_cache)
    
    return parent_path if parent_path else "/"


def search_files(service, extension: Optional[str] = None, min_size_mb: Optional[float] = None) -> List[dict]:
    """Search for files with specific criteria."""
    try:
        # Build query for regular files (not trashed, not folders, owned by user)
        query_parts = [
            "trashed=false",
            "mimeType != 'application/vnd.google-apps.folder'",
            "'me' in owners"  # Only files owned by the authenticated user
        ]
        
        # Extension filter
        if extension:
            query_parts.append(f"name contains '.{extension}'")
        
        query = " and ".join(query_parts)
        
        results = []
        page_token = None
        
        while True:
            response = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime, parents, owners)',
                pageToken=page_token,
                pageSize=100
            ).execute()
            
            files = response.get('files', [])
            results.extend(files)
            
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        
        # Post-process filters
        filtered_results = []
        
        for f in results:
            # Exact extension match
            if extension and not f.get('name', '').lower().endswith(f'.{extension.lower()}'):
                continue
            
            # Size filter
            if min_size_mb is not None:
                size_str = f.get('size')
                if size_str:
                    size_bytes = int(size_str)
                    size_mb = size_bytes / (1024 * 1024)
                    if size_mb < min_size_mb:
                        continue
                else:
                    # Skip files without size info if size filter is active
                    continue
            
            filtered_results.append(f)
        
        return filtered_results
        
    except HttpError as error:
        console.print(f"[red]An error occurred while searching: {error}[/red]")
        return []


def format_size(size_str: str) -> str:
    """Format file size in human-readable format."""
    if not size_str:
        return "Unknown"
    
    size = int(size_str)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def display_files(service, files: List[dict], extension: Optional[str] = None, min_size_mb: Optional[float] = None):
    """Display files in a formatted table."""
    if not files:
        filters = []
        if extension:
            filters.append(f"extension '.{extension}'")
        if min_size_mb:
            filters.append(f"size >{min_size_mb}MB")
        
        filter_text = " and ".join(filters) if filters else "specified criteria"
        console.print(f"[yellow]No files matching {filter_text} found in your Google Drive.[/yellow]")
        return
    
    # Build title
    title_parts = ["Google Drive Files"]
    if extension:
        title_parts.append(f"with Extension '.{extension}'")
    if min_size_mb:
        title_parts.append(f"Larger than {min_size_mb}MB")
    
    table = Table(title=" ".join(title_parts))
    table.add_column("Name", style="cyan", max_width=40)
    table.add_column("Size", style="green", max_width=10)
    table.add_column("Folder Path", style="blue", max_width=50)
    table.add_column("Modified", style="yellow", max_width=20)
    
    # Cache for folder paths to avoid repeated API calls
    path_cache = {}
    total_size = 0
    
    with console.status("[bold blue]Getting folder paths...", spinner="dots") as status:
        for i, file in enumerate(files):
            status.update(f"[bold blue]Processing file {i+1}/{len(files)}...")
            
            name = file.get('name', 'Unknown')
            size_str = file.get('size', '0')
            size = format_size(size_str)
            if size_str:
                total_size += int(size_str)
            
            # Get folder path
            folder_path = get_file_folder_path(service, file, path_cache)
            
            # Use modified date
            file_date = file.get('modifiedTime', 'Unknown')
            if file_date != 'Unknown':
                try:
                    dt = date_parser.parse(file_date)
                    file_date = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            
            table.add_row(name, size, folder_path, file_date)
    
    console.print(table)
    console.print(f"\n[bold]Total files:[/bold] {len(files)}")
    console.print(f"[bold]Total size:[/bold] {format_size(str(total_size))}")


def delete_files(service, files: List[dict], force: bool = False, move_to_trash: bool = True):
    """Delete or trash files from Drive."""
    if not files:
        return
    
    action = "move to trash" if move_to_trash else "permanently delete"
    
    if not force:
        console.print(f"\n[bold red]Warning:[/bold red] This will {action} {len(files)} file(s)!")
        if not move_to_trash:
            console.print("Permanently deleted files cannot be recovered!")
        
        if not Confirm.ask("Are you sure you want to continue?"):
            console.print("[yellow]Operation cancelled.[/yellow]")
            return
    
    deleted_count = 0
    failed_count = 0
    
    action_verb = "Trashing" if move_to_trash else "Deleting"
    
    with console.status(f"[bold green]{action_verb} files...", spinner="dots") as status:
        for file in files:
            file_name = file.get('name', 'Unknown')
            file_id = file.get('id')
            
            if not file_id:
                console.print(f"[red]Skipping {file_name}: No file ID[/red]")
                failed_count += 1
                continue
            
            try:
                if move_to_trash:
                    service.files().update(fileId=file_id, body={'trashed': True}).execute()
                else:
                    service.files().delete(fileId=file_id).execute()
                deleted_count += 1
                status.update(f"[bold green]{action_verb.replace('ing', 'ed')} {deleted_count}/{len(files)} files...")
            except HttpError as error:
                console.print(f"[red]Failed to {action} {file_name}: {error}[/red]")
                failed_count += 1
    
    verb = "moved to trash" if move_to_trash else "permanently deleted"
    console.print(f"\n[green]Successfully {verb} {deleted_count} file(s)[/green]")
    if failed_count > 0:
        console.print(f"[red]Failed to {action} {failed_count} file(s)[/red]")


@click.group()
@click.version_option(version='1.0.2', prog_name='gdrive-file-eraser')
def cli():
    """GDrive File Eraser - Find and delete large files from Google Drive by extension and size."""
    pass


@cli.command()
@click.argument('extension', required=False)
@click.option('--size', '-s', type=float, help='Minimum file size in MB (e.g., 100 for files >100MB)')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON for scripting')
def list(extension: str, size: float, output_json: bool):
    """List files with optional extension and size filters."""
    if not extension and size is None:
        console.print("[red]Error: You must specify either an extension or a size filter.[/red]")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  gdrive-eraser list pdf                    # List all PDF files")
        console.print("  gdrive-eraser list --size 100             # List files >100MB")
        console.print("  gdrive-eraser list mp4 --size 500         # List MP4 files >500MB")
        return
    
    service = authenticate()
    
    filters = []
    if extension:
        filters.append(f"'.{extension}' files")
    if size:
        filters.append(f"files >{size}MB")
    
    filter_text = " and ".join(filters)
    console.print(f"[bold]🔍 Searching for {filter_text} in your Google Drive...[/bold]")
    
    files = search_files(service, extension, size)
    
    if output_json:
        # For JSON output, we still get paths but don't need the fancy display
        path_cache = {}
        for file in files:
            file['folder_path'] = get_file_folder_path(service, file, path_cache)
        
        output = {
            'extension': extension,
            'min_size_mb': size,
            'count': len(files),
            'total_size_bytes': sum(int(f.get('size', 0)) for f in files if f.get('size')),
            'files': files
        }
        print(json.dumps(output, indent=2))
    else:
        display_files(service, files, extension, size)


@cli.command()
@click.argument('extension', required=False)
@click.option('--size', '-s', type=float, help='Minimum file size in MB (e.g., 100 for files >100MB)')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation prompt')
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without deleting')
@click.option('--permanent', is_flag=True, help='Permanently delete files (default: move to trash)')
def delete(extension: str, size: float, force: bool, dry_run: bool, permanent: bool):
    """Delete files with optional extension and size filters."""
    if not extension and size is None:
        console.print("[red]Error: You must specify either an extension or a size filter.[/red]")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  gdrive-eraser delete pdf                  # Delete all PDF files")
        console.print("  gdrive-eraser delete --size 100           # Delete files >100MB")
        console.print("  gdrive-eraser delete mp4 --size 500       # Delete MP4 files >500MB")
        console.print("  gdrive-eraser delete --size 1000 --dry-run # Preview large files")
        return
    
    service = authenticate()
    
    filters = []
    if extension:
        filters.append(f"'.{extension}' files")
    if size:
        filters.append(f"files >{size}MB")
    
    filter_text = " and ".join(filters)
    console.print(f"[bold]🔍 Searching for {filter_text} in your Google Drive...[/bold]")
    
    files = search_files(service, extension, size)
    
    if not files:
        console.print(f"[yellow]No files matching criteria found in your Google Drive.[/yellow]")
        return
    
    move_to_trash = not permanent
    
    if dry_run:
        action = "move to trash" if move_to_trash else "permanently delete"
        console.print(f"\n[bold yellow]🔍 DRY RUN MODE - No files will be {action}[/bold yellow]")
        display_files(service, files, extension, size)
        console.print(f"\n[yellow]Would {action} {len(files)} file(s)[/yellow]")
    else:
        display_files(service, files, extension, size)
        delete_files(service, files, force, move_to_trash)


@cli.command()
def setup():
    """Interactive setup guide for Google Drive API credentials."""
    console.print("[bold]🚀 GDrive File Eraser Setup[/bold]\n")
    
    console.print("To use this tool, you need to set up Google Drive API access:")
    console.print("\n[bold]Step 1:[/bold] Go to https://console.cloud.google.com/")
    console.print("[bold]Step 2:[/bold] Create a new project or select an existing one")
    console.print("[bold]Step 3:[/bold] Enable the Google Drive API:")
    console.print("         • In the left menu, go to 'APIs & Services' > 'Library'")
    console.print("         • Search for 'Google Drive API' and enable it")
    console.print("[bold]Step 4:[/bold] Create OAuth 2.0 credentials:")
    console.print("         • Go to 'APIs & Services' > 'Credentials'")
    console.print("         • Click 'Create Credentials' > 'OAuth client ID'")
    console.print("         • Choose 'Desktop app' as application type")
    console.print("         • Give it a name (e.g., 'GDrive File Eraser')")
    console.print("[bold]Step 5:[/bold] Download the credentials:")
    console.print("         • Click the download button next to your credential")
    console.print("         • Save it as 'credentials.json' in this directory")
    console.print(f"         • Current directory: {os.getcwd()}")
    
    credentials_path = Path('credentials.json')
    if credentials_path.exists():
        console.print("\n[green]✅ credentials.json found![/green]")
        console.print("You can now use the 'list' or 'delete' commands.")
        console.print("\n[bold]Quick start:[/bold]")
        console.print("  gdrive-eraser list --size 100    # Find large files")
        console.print("  gdrive-eraser delete --size 500 --dry-run  # Preview deletion")
    else:
        console.print("\n[red]❌ credentials.json not found[/red]")
        console.print("Please complete the setup steps above.")


if __name__ == '__main__':
    cli() 