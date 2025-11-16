#!/usr/bin/env python3
"""
Quick test to check if the package builds correctly and includes all files.
"""

import subprocess
import sys
import zipfile
import tarfile
import glob
import os

def run_command(cmd):
    """Run a command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    print("🔧 Cleaning previous builds...")
    run_command("rm -rf dist build *.egg-info")
    
    print("📦 Building package...")
    output = run_command("python -m build")
    if output is None:
        print("❌ Build failed!")
        return 1
    
    print("✅ Build successful!")
    
    # Check dist contents
    print("\n📂 Built files:")
    dist_files = glob.glob("dist/*")
    for file in dist_files:
        size = os.path.getsize(file)
        print(f"  {file} ({size:,} bytes)")
    
    # Check wheel contents
    wheel_files = glob.glob("dist/*.whl")
    if wheel_files:
        wheel_file = wheel_files[0]
        print(f"\n🎡 Wheel contents ({wheel_file}):")
        with zipfile.ZipFile(wheel_file, 'r') as z:
            for info in z.infolist():
                print(f"  {info.filename}")
                
        # Check for key_state.py
        with zipfile.ZipFile(wheel_file, 'r') as z:
            filenames = [info.filename for info in z.infolist()]
            if any('key_state.py' in f for f in filenames):
                print("✅ key_state.py found in wheel!")
            else:
                print("❌ key_state.py NOT found in wheel!")
                return 1
    
    # Test basic structure
    print("\n🧪 Testing basic package structure...")
    try:
        # Just test that we have the expected files structure
        expected_files = [
            'openrouter_free/__init__.py',
            'openrouter_free/client.py', 
            'openrouter_free/key_state.py',
            'openrouter_free/models.py',
            'openrouter_free/exceptions.py'
        ]
        
        wheel_file = glob.glob("dist/*.whl")[0]
        with zipfile.ZipFile(wheel_file, 'r') as z:
            filenames = [info.filename for info in z.infolist()]
            
        missing = []
        for expected in expected_files:
            if not any(expected in f for f in filenames):
                missing.append(expected)
        
        if missing:
            print(f"❌ Missing files: {missing}")
            return 1
        else:
            print("✅ All expected files present!")
        
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        return 1
    
    print("\n🎉 All checks passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
