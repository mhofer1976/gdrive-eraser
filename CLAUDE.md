# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GDrive File Eraser is a Python CLI tool that helps users find and delete large files from their Google Drive by extension and size. The tool only operates on files owned by the user (excludes shared files for security).

## Key Commands

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt
# Or using uv (recommended)
uv sync

# Run the application
python gdrive_eraser.py [command]

# Check for linting/formatting (not configured yet)
# Note: No linting tools configured in pyproject.toml
```

### Application Commands
```bash
# Setup Google Drive API credentials
python gdrive_eraser.py setup

# List files
python gdrive_eraser.py list [extension] --size [MB]
python gdrive_eraser.py list pdf --size 100

# Delete files (always test with --dry-run first)
python gdrive_eraser.py delete [extension] --size [MB] --dry-run
python gdrive_eraser.py delete pdf --size 100 --force --permanent
```

## Architecture

### Core Components

- **Authentication** (`authenticate()` in gdrive_eraser.py:31): Handles Google OAuth2 flow using `credentials.json` and `token.json`
- **File Search** (`search_files()` in gdrive_eraser.py:131): Queries Google Drive API with filters for extension, size, and ownership
- **Path Resolution** (`get_folder_path()` in gdrive_eraser.py:73): Recursively builds full folder paths with caching
- **File Operations** (`delete_files()` in gdrive_eraser.py:267): Handles file deletion (trash or permanent)
- **Display** (`display_files()` in gdrive_eraser.py:208): Rich table formatting for file listings

### Key Security Features

- **Ownership Filter**: Only operates on files owned by authenticated user (`'me' in owners` query)
- **Required Filters**: Must specify extension OR size to prevent accidental mass operations
- **Trash by Default**: Files moved to trash unless `--permanent` flag used
- **Dry Run Mode**: `--dry-run` flag allows safe preview of operations

### Dependencies

- `google-api-python-client`: Google Drive API access
- `click`: CLI framework
- `rich`: Terminal formatting and progress indicators
- `python-dateutil`: Date parsing for file timestamps

## File Structure

```
gdrive-eraser/
├── gdrive_eraser.py      # Main application (single file)
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies
├── credentials.json      # Google OAuth credentials (user-provided)
├── token.json           # Auto-generated auth token
└── README.md            # Comprehensive documentation
```

## Important Implementation Notes

### Google Drive API Integration
- Uses OAuth2 with local server flow for authentication
- Requires `credentials.json` from Google Cloud Console
- Scopes: `https://www.googleapis.com/auth/drive`
- Implements pagination for large result sets
- Caches folder paths to minimize API calls

### CLI Design Patterns
- Uses Click for command-line interface
- Supports both extension and size filters
- JSON output option for scripting
- Rich console for formatted output and progress indicators

### Error Handling
- Graceful handling of missing credentials
- HTTP error handling for API failures
- Path resolution fallbacks for inaccessible folders
- User confirmation prompts for destructive operations

## Development Considerations

- Single-file application for simplicity
- No test suite currently implemented
- No linting/formatting tools configured
- Windows-compatible (uses pathlib for cross-platform paths)
- Designed for end-user safety with multiple confirmation steps