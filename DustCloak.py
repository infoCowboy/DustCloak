import os
import platform
import subprocess
import shutil

def detect_os():
    """Detect the current operating system."""
    return platform.system().lower()

def is_root():
    """Check if the script is running as root/admin."""
    if detect_os() == "linux":
        return os.geteuid() == 0
    elif detect_os() == "windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return False

def confirm_action(prompt="Are you sure? [y/N]: "):
    resp = input(prompt).strip().lower()
    return resp == 'y' or resp == 'yes'

def wipe_all_logs_in_dir(log_dir="/var/log", dry_run=False, use_shred=False):
    """Wipe all logs in a directory. Optionally use shred for secure deletion."""
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            log_path = os.path.join(root, file)
            try:
                if dry_run:
                    print(f"[DRY RUN] Would remove: {log_path}")
                    continue
                if use_shred:
                    subprocess.run(["shred", "-u", log_path], check=False)
                    print(f"[+] Securely shredded: {log_path}")
                else:
                    with open(log_path, 'w') as f:
                        f.write("\0" * os.path.getsize(log_path))
                    os.remove(log_path)
                    print(f"[+] Removed log: {log_path}")
            except (PermissionError, IsADirectoryError):
                print(f"[-] Skipped (permission/dir): {log_path}")
            except Exception as e:
                print(f"[-] Error removing {log_path}: {e}")

def wipe_linux_logs(dry_run=False, use_shred=False):
    """Wipe common Linux logs and shell history."""
    logs = [
        "/var/log/wtmp",
        "/var/log/btmp",
        "/var/log/lastlog",
        "/var/log/faillog",
        os.path.expanduser("~/.bash_history")
    ]
    print("[+] Clearing Linux logs...")
    wipe_all_logs_in_dir("/var/log", dry_run=dry_run, use_shred=use_shred)
    for log in logs:
        if os.path.exists(log):
            try:
                if dry_run:
                    print(f"[DRY RUN] Would remove: {log}")
                    continue
                if use_shred:
                    subprocess.run(["shred", "-u", log], check=False)
                    print(f"[+] Securely shredded: {log}")
                else:
                    with open(log, 'w') as file:
                        file.write("\0" * os.path.getsize(log))
                    os.remove(log)
                    print(f"[+] Cleared: {log}")
            except PermissionError:
                print(f"[-] Permission Denied: {log}")
            except Exception as e:
                print(f"[-] Error clearing {log}: {e}")
    # Clear shell history in memory
    bash_history = os.path.expanduser("~/.bash_history")
    if os.path.exists(bash_history) and not dry_run:
        try:
            with open(bash_history, 'w') as file:
                file.write("")
            os.environ['HISTFILE'] = '/dev/null'
            print("[+] Shell history cleared!")
        except Exception as e:
            print(f"[-] Error clearing shell history: {e}")

def wipe_windows_logs(dry_run=False):
    """Wipe Windows event logs and cmd history."""
    print("[+] Clearing Windows Event Logs...")
    if dry_run:
        print("[DRY RUN] Would clear Windows event logs and command history.")
        return
    try:
        logs = subprocess.check_output("wevtutil el", shell=True).decode().split('\r\n')
        for log in logs:
            log = log.strip()
            if log:
                subprocess.call(f"wevtutil cl {log}", shell=True)
                print(f"[+] Cleared: {log}")
    except Exception as e:
        print(f"[-] Error clearing event logs: {e}")
    # Clear cmd history
    os.system("doskey /REINIT")
    print("[+] Command history cleared!")

def main_menu():
    print("""
==== Log Wiper Utility ====
1. Wipe logs (destructive)
2. Dry run (show what would be deleted)
3. Exit
==========================
""")
    return input("Select an option [1-3]: ").strip()

def wipe_logs(dry_run=False, use_shred=False):
    os_type = detect_os()
    if os_type == "linux":
        wipe_linux_logs(dry_run=dry_run, use_shred=use_shred)
    elif os_type == "windows":
        wipe_windows_logs(dry_run=dry_run)
    else:
        print("[-] Unsupported OS detected.")

if __name__ == "__main__":
    print("[+] Running Log Wiper Script...")
    if not is_root():
        print("[!] Warning: You are not running as root/admin. Some logs may not be wiped.")
    while True:
        choice = main_menu()
        if choice == '1':
            if not confirm_action("This will irreversibly delete logs. Continue? [y/N]: "):
                print("[!] Aborted by user.")
                continue
            use_shred = False
            if detect_os() == "linux" and shutil.which("shred"):
                use_shred = confirm_action("Use secure deletion (shred)? [y/N]: ")
            wipe_logs(dry_run=False, use_shred=use_shred)
            print("[+] Log wiping complete!")
        elif choice == '2':
            use_shred = False
            if detect_os() == "linux" and shutil.which("shred"):
                use_shred = confirm_action("Show secure deletion (shred) actions? [y/N]: ")
            wipe_logs(dry_run=True, use_shred=use_shred)
        elif choice == '3':
            print("[+] Exiting.")
            break
        else:
            print("[!] Invalid option. Please select 1, 2, or 3.")