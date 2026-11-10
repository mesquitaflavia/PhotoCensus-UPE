"""
install.py - Automatic installer for PhotoCensus (full AI mode)

NOTE: the kit ALREADY WORKS without installing anything, using the 48 photos
provided. Run this installer only if your group wants to analyze NEW photos.

Usage:  python install.py      (or double-click install_windows.bat)
"""
import platform
import subprocess
import sys


def run(command):
    print("\n>>>", " ".join(command))
    return subprocess.call(command) == 0


def main():
    print("=" * 60)
    print(" PhotoCensus Installer")
    print("=" * 60)
    version = sys.version_info
    print(f"Python found: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 9):
        print("ERROR: Python 3.9 or newer is required.")
        return 1

    pip = [sys.executable, "-m", "pip", "install", "--upgrade"]
    run(pip + ["pip"])

    # CPU-only PyTorch (much smaller) on Windows and Linux
    if platform.system() in ("Windows", "Linux"):
        ok = run(pip + ["torch", "torchvision",
                        "--index-url", "https://download.pytorch.org/whl/cpu"])
    else:
        ok = run(pip + ["torch", "torchvision"])
    if not ok:
        print("\nERROR installing PyTorch. Check your internet connection and try again.")
        return 1

    if not run(pip + ["ultralytics"]):
        print("\nERROR installing ultralytics. Check your internet connection and try again.")
        return 1

    print("\nTesting the installation...")
    try:
        import ultralytics  # noqa: F401
    except ImportError:
        print("ERROR: ultralytics was not found after installation.")
        return 1

    print("\n" + "=" * 60)
    print(" Installation complete. Now run:  python test_kit.py")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit_code = main()
    if platform.system() == "Windows":
        input("\nPress ENTER to close...")
    sys.exit(exit_code)
