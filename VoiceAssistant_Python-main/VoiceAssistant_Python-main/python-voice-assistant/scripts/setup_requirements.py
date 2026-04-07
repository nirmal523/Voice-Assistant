"""
Setup script to install required packages for the Voice Assistant
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    """Install all required packages"""
    print("Setting up Voice Assistant requirements...")
    print("=" * 50)
    
    required_packages = [
        "speechrecognition",
        "pyttsx3",
        "requests",
        "pyaudio"  # Required for microphone input
    ]
    
    success_count = 0
    
    for package in required_packages:
        print(f"Installing {package}...")
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"Installation complete: {success_count}/{len(required_packages)} packages installed successfully")
    
    if success_count == len(required_packages):
        print("✓ All packages installed successfully!")
        print("\nYou can now run the voice assistant with:")
        print("python voice_assistant.py")
    else:
        print("⚠ Some packages failed to install. Please install them manually:")
        print("pip install speechrecognition pyttsx3 requests pyaudio")
    
    print("\nNote: If you encounter issues with pyaudio on Windows, try:")
    print("pip install pipwin")
    print("pipwin install pyaudio")

if __name__ == "__main__":
    main()
