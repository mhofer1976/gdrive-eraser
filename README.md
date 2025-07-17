# 🗑️ GDrive File Eraser

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful command-line tool to find and delete large files from your Google Drive. Clean up storage efficiently by targeting files by extension and size. **Safely operates only on files you own**—shared files are excluded for security.

## Motivation
For years, deleting large numbers of photos or videos from Google Drive was slow and frustrating—you had to manually select files in a paginated list, making bulk cleanup nearly impossible. This tool was created to solve that problem: it leverages the Google Drive API to quickly find and remove large files you own, streamlining the cleanup process and saving you valuable time.

## ✨ Features

- 🔍 **Find files by extension** (e.g., `.mp4`, `.pdf`, `.zip`)
- 📏 **Filter by file size** (e.g., files >100MB)
- 📁 **Show folder paths** to locate files easily
- 🛡️ **Ownership protection** - only shows/deletes files YOU own (excludes shared files)
- 🗑️ **Safe deletion** (moves to trash by default)
- ⚡ **Permanent deletion option** for when you're sure
- 📊 **Beautiful table output** with Rich formatting
- 🔧 **JSON output** for scripting and automation
- 🛡️ **Dry-run mode** for safe previewing
- 🚫 **Safety guards** to prevent accidental mass deletion

## 🔐 Security & Safety

### ⚠️ **Important: Ownership Restriction**

This tool **ONLY operates on files you own** in your Google Drive. It will **NOT** show or delete:
- Files shared with you by others
- Files in shared drives (Team Drives) owned by others
- Files where you have edit access but are not the owner

This restriction ensures you cannot accidentally delete someone else's important files.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/gdrive-file-eraser.git
cd gdrive-file-eraser

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Google Drive API (see detailed instructions below)
python gdrive_eraser.py setup

# 4. Find large files (only YOUR files)
python gdrive_eraser.py list --size 100

# 5. Clean up (with preview first!)
python gdrive_eraser.py delete --size 500 --dry-run
python gdrive_eraser.py delete --size 500
```

## 📦 Installation

### Option 1: Using pip

```bash
git clone https://github.com/yourusername/gdrive-file-eraser.git
cd gdrive-file-eraser
pip install -r requirements.txt
```

### Option 2: Using uv (recommended)

```bash
git clone https://github.com/yourusername/gdrive-file-eraser.git
cd gdrive-file-eraser
uv sync
```

## 🔐 Google Drive API Setup

To use this tool, you need to set up Google Drive API access. Follow these detailed steps:

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter a project name (e.g., "GDrive File Eraser")
4. Click **"Create"**

### Step 2: Enable Google Drive API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google Drive API"**
3. Click on it and press **"Enable"**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted to configure OAuth consent screen:
   - Choose **"External"** user type
   - Fill in required fields (App name, User support email, Developer email)
   - Add your email to test users
   - Save and continue through all steps
4. Back in Credentials, click **"Create Credentials"** → **"OAuth client ID"**
5. Choose **"Desktop application"** as application type
6. Give it a name (e.g., "GDrive File Eraser")
7. Click **"Create"**

### Step 4: Download Credentials

1. In the credentials list, find your OAuth 2.0 Client ID
2. Click the **download button** (📥) on the right
3. Save the file as `credentials.json` in the project directory

### Step 5: First Run Authentication

```bash
# Run the setup command for guided instructions
python gdrive_eraser.py setup

# Or run any command - it will trigger authentication
python gdrive_eraser.py list --size 100
```

On first run, the tool will:
1. Open your web browser
2. Ask you to sign in to Google
3. Request permission to access your Google Drive
4. Save a `token.json` file for future use

> ⚠️ **Security Note**: Never commit `credentials.json` or `token.json` to version control. They are already excluded in `.gitignore`.

## 📖 Usage

### Finding Files

```bash
# Find all PDF files you own
python gdrive_eraser.py list pdf

# Find large files you own (>100MB)
python gdrive_eraser.py list --size 100

# Find large video files you own (MP4 files >500MB)
python gdrive_eraser.py list mp4 --size 500

# Output as JSON for scripting
python gdrive_eraser.py list --size 1000 --json
```

### Deleting Files

```bash
# Delete all PDF files you own (moves to trash - safe!)
python gdrive_eraser.py delete pdf

# Delete large files with preview first
python gdrive_eraser.py delete --size 1000 --dry-run  # Preview
python gdrive_eraser.py delete --size 1000            # Execute

# Permanently delete (skip trash - be careful!)
python gdrive_eraser.py delete pdf --permanent

# Skip confirmation prompt (for scripts)
python gdrive_eraser.py delete --size 500 --force
```

### Real-World Examples

```bash
# Clean up large downloads you own
python gdrive_eraser.py list zip --size 100     # Find large ZIP files
python gdrive_eraser.py delete zip --size 100   # Delete them

# Remove old video files you created
python gdrive_eraser.py list mp4 --size 500 --dry-run  # Preview
python gdrive_eraser.py delete mp4 --size 500          # Delete

# Find space hogs in your drive
python gdrive_eraser.py list --size 1000        # Files >1GB you own

# Batch operations for cleanup
python gdrive_eraser.py delete --size 2000 --dry-run   # Preview 2GB+ files
python gdrive_eraser.py delete --size 2000             # Clean them up
```

## 🛡️ Safety Features

- **🔒 Ownership protection**: Only operates on files YOU own (excludes shared files)
- **📋 Required filters**: Must specify extension OR size (prevents accidental mass operations)
- **🗑️ Trash by default**: Files are moved to trash, not permanently deleted
- **👀 Dry-run mode**: Use `--dry-run` to preview what would be deleted
- **✋ Confirmation prompts**: Asks for confirmation before destructive operations
- **🔒 Permanent deletion protection**: Use `--permanent` flag only when you're sure

## 📊 Output Format

The tool displays files in a beautiful, formatted table with **full folder paths**:

```
Google Drive Files with Extension '.pdf' Larger than 100MB (Owned by You)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Name                                 ┃ Size     ┃ Folder Path                                    ┃ Modified           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ Large Document.pdf                   │ 245.2 MB │ /Documents/Projects/2024                      │ 2024-01-15 14:23:12 │
│ Presentation Archive.pdf             │ 156.7 MB │ /Work/Meetings/Q1                             │ 2024-01-10 09:45:33 │
│ Manual.pdf                           │ 89.1 MB  │ /Downloads                                     │ 2024-01-05 16:12:45 │
└──────────────────────────────────────┴──────────┴────────────────────────────────────────────────┴────────────────────┘

Total files: 3
Total size: 491.0 MB
```

**Security Feature**: The tool now shows **(Owned by You)** in the title to clearly indicate only your files are displayed.

## 🔧 Command Reference

### `list` command

```bash
python gdrive_eraser.py list [EXTENSION] [OPTIONS]

Options:
  -s, --size FLOAT    Minimum file size in MB
  --json              Output as JSON for scripting
  --help              Show help message

Note: Only shows files you own, excludes shared files.
```

### `delete` command

```bash
python gdrive_eraser.py delete [EXTENSION] [OPTIONS]

Options:
  -s, --size FLOAT    Minimum file size in MB
  -f, --force         Skip confirmation prompt
  --dry-run           Preview without deleting
  --permanent         Permanently delete (skip trash)
  --help              Show help message

Note: Only deletes files you own, cannot delete shared files.
```

### `setup` command

```bash
python gdrive_eraser.py setup

Shows detailed setup instructions for Google Drive API.
```

## 📁 Project Structure

```
gdrive-file-eraser/
├── gdrive_eraser.py      # Main application
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Project configuration
├── README.md            # This file
├── .gitignore          # Git ignore patterns
├── credentials.json    # Your OAuth credentials (download from Google)
└── token.json          # Auto-generated auth token (first run)
```

## 🔍 Troubleshooting

### Common Issues

**❌ "credentials.json not found"**
```bash
# Run setup for detailed instructions
python gdrive_eraser.py setup
```

**❌ Authentication errors**
```bash
# Delete token and re-authenticate
rm token.json
python gdrive_eraser.py list --size 100
```

**❌ "API not enabled"**
- Go to Google Cloud Console → APIs & Services → Library
- Search for "Google Drive API" and enable it

**❌ "Access denied" errors**
- Ensure your OAuth app has the correct scopes
- Check if you added yourself as a test user (for external apps)

**❌ "No files found" but you know files exist**
- The tool only shows files **you own**, not shared files
- Check if the files are actually owned by you or just shared with you
- Shared files from others will not appear in results (this is intentional for safety)

**❌ Slow folder path lookup**
- The tool fetches folder paths for each file, which may take time for large result sets
- Paths are cached to minimize API calls
- Consider using size filters to reduce the number of results

### Getting Help

1. Run `python gdrive_eraser.py --help` for command overview
2. Run `python gdrive_eraser.py COMMAND --help` for command-specific help
3. Check the [Google Drive API documentation](https://developers.google.com/drive/api)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool modifies files in your Google Drive. While it includes safety features:
- **Only operates on files you own** (excludes shared files automatically)
- **Always use `--dry-run` first** to preview changes
- **Test with small sets** before large operations  
- **Understand the difference** between trash and permanent deletion
- **Keep backups** of important data

The authors are not responsible for any data loss. Use at your own risk.
