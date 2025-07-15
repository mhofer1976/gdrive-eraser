# Contributing to GDrive File Eraser

Thank you for your interest in contributing to GDrive File Eraser! 🎉

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/gdrive-file-eraser.git
   cd gdrive-file-eraser
   ```
3. **Install dependencies**:
   ```bash
   uv sync  # or pip install -r requirements.txt
   ```
4. **Set up Google Drive API** (see README.md for detailed instructions)

## 🛠️ Development Guidelines

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** where possible
- Add **docstrings** to functions and classes
- Keep functions **small and focused**

### Testing

Before submitting a pull request:

1. **Test your changes**:
   ```bash
   # Test basic functionality
   python gdrive_eraser.py --help
   python gdrive_eraser.py setup
   
   # Test with actual Google Drive (if you have credentials)
   python gdrive_eraser.py list --size 1 --dry-run
   ```

2. **Check for lint issues**:
   ```bash
   # If you have pylint installed
   pylint gdrive_eraser.py
   ```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add support for multiple file extensions"
git commit -m "Fix authentication error handling"
git commit -m "Improve error messages for missing credentials"

# Avoid
git commit -m "Fix bug"
git commit -m "Update code"
```

## 🐛 Reporting Issues

When reporting bugs, please include:

1. **Python version**: `python --version`
2. **Operating system**: Windows/macOS/Linux
3. **Error message**: Full traceback if applicable
4. **Steps to reproduce**: Detailed steps
5. **Expected vs actual behavior**

### Issue Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.5]
- Installation method: [pip/uv]

**Additional context**
Any other context about the problem.
```

## 💡 Suggesting Features

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** clearly
3. **Explain the proposed solution**
4. **Consider backward compatibility**

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context or screenshots about the feature request.
```

## 🔄 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly**:
   - Test with different file types and sizes
   - Test error conditions
   - Test with `--dry-run` mode

4. **Update documentation** if needed:
   - Update README.md for new features
   - Update help text in the code
   - Add examples if applicable

5. **Submit the pull request**:
   - Use a clear title and description
   - Link any related issues
   - Explain what changed and why

### Pull Request Template

```markdown
**Description**
Brief description of what this PR does.

**Changes**
- List of changes made
- Any breaking changes
- New features added

**Testing**
- [ ] Tested locally
- [ ] Tested with real Google Drive
- [ ] Tested error conditions
- [ ] Updated documentation

**Related Issues**
Fixes #123 (if applicable)
```

## 🚨 Security

- **Never commit credentials** (`credentials.json`, `token.json`)
- **Be careful with user data** - always validate inputs
- **Follow OAuth best practices**
- Report security issues privately via email

## 📝 Documentation

Help us keep documentation up to date:

- **README.md**: User-facing documentation
- **Code comments**: Explain complex logic
- **Docstrings**: Document functions and classes
- **Examples**: Add real-world usage examples

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### 🌟 New Features
- Support for additional file formats
- Batch operations
- Configuration file support
- Progress bars for large operations
- File metadata filtering (date, owner, etc.)

### 🐛 Bug Fixes
- Authentication edge cases
- Error handling improvements
- Cross-platform compatibility
- Performance optimizations

### 📚 Documentation
- More usage examples
- Video tutorials
- FAQ section
- Troubleshooting guides

### 🧪 Testing
- Unit tests
- Integration tests
- Mock testing for API calls
- Performance testing

## 🤝 Code of Conduct

Please be respectful and constructive in all interactions. We want this to be a welcoming place for contributors of all experience levels.

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **README.md**: For setup and usage instructions

## 🙏 Recognition

All contributors will be recognized in the project. Thank you for helping make GDrive File Eraser better!

---

Happy coding! 🚀 