#!/usr/bin/env python3
"""
Manual publishing script for openrouter-free package.
"""

import subprocess
import sys
import getpass

def run_command(cmd, check=True):
    """Run a command and return its result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def main():
    print("🚀 Manual PyPI Publishing Script")
    print("================================")
    
    # Clean previous builds
    print("\n1. Cleaning previous builds...")
    run_command("rm -rf dist build *.egg-info", check=False)
    
    # Build the package
    print("\n2. Building package...")
    result = run_command("python -m build")
    if result.returncode != 0:
        print("❌ Build failed!")
        return 1
    
    print("✅ Package built successfully!")
    
    # Show built files
    print("\n3. Built files:")
    run_command("ls -la dist/")
    
    # Ask for PyPI token
    print("\n4. PyPI Authentication")
    print("You'll need your PyPI API token (starts with 'pypi-')")
    print("Get it from: https://pypi.org/manage/account/token/")
    
    token = getpass.getpass("Enter your PyPI API token: ")
    
    if not token.startswith('pypi-'):
        print("❌ Invalid token format. Token should start with 'pypi-'")
        return 1
    
    # Upload to PyPI
    print("\n5. Uploading to PyPI...")
    env = f"TWINE_USERNAME=__token__ TWINE_PASSWORD={token}"
    result = run_command(f"{env} python -m twine upload dist/*", check=False)
    
    if result.returncode == 0:
        print("✅ Successfully uploaded to PyPI!")
        print(f"🎉 Your package is now available at: https://pypi.org/project/openrouter-free/")
        print(f"📦 Install with: pip install openrouter-free")
    else:
        print("❌ Upload failed!")
        print("Common issues:")
        print("- Invalid API token")
        print("- Package with same version already exists")
        print("- Network issues")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
