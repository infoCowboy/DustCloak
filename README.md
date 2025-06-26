# DustCloak

A cross-platform Python tool to securely wipe system logs and shell history on Linux and Windows. Inspired by Dune: “The desert erases all traces.”

## Features
- Wipes system logs and shell histories on Linux and Windows
- Supports secure deletion with `shred` (Linux)
- Dry run mode to preview actions without deleting
- Root/admin privilege detection and warnings
- Interactive menu and confirmation prompts for safety

## Usage
1. **Run the script:**
   ```bash
   python3 DustCloak.py
   ```
2. **Follow the interactive menu:**
   - Wipe logs (destructive)
   - Dry run (show what would be deleted)
   - Exit

3. **Secure deletion:**
   - On Linux, if `shred` is available, you can choose to use it for secure file removal.

## Requirements
- Python 3.x
- (Optional for secure deletion on Linux) `shred` utility

## Notes
- You must run as root/admin to wipe all logs.
- Use with caution: this script irreversibly deletes log files.
- For GitHub authentication, use a Personal Access Token or SSH key (see [GitHub Docs](https://docs.github.com/en/authentication)).

## License
MIT
