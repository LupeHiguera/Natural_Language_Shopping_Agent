"""
Script to package the FastAPI backend for Lambda deployment.
Creates a zip file with all dependencies compatible with Lambda (Linux x86_64).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
BUILD_DIR = PROJECT_ROOT / "build" / "lambda"
OUTPUT_FILE = BACKEND_DIR / "lambda_package.zip"


def clean_build_dir():
    """Remove and recreate build directory."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)
    print(f"Created build directory: {BUILD_DIR}")


def install_dependencies():
    """Install Python dependencies for Linux Lambda environment."""

    # Production dependencies only
    prod_requirements = [
        "fastapi",
        "boto3",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "mangum",
    ]

    # Create temporary requirements file
    temp_req = BUILD_DIR / "requirements_lambda.txt"
    temp_req.write_text("\n".join(prod_requirements))

    print("Installing Linux-compatible dependencies for Lambda...")

    # Use --platform to get Linux-compatible packages
    # Use --only-binary :all: to ensure we get pre-compiled wheels
    result = subprocess.run([
        sys.executable, "-m", "pip", "install",
        "-r", str(temp_req),
        "-t", str(BUILD_DIR),
        "--platform", "manylinux2014_x86_64",
        "--implementation", "cp",
        "--python-version", "3.11",
        "--only-binary", ":all:",
        "--upgrade",
        "--quiet"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Warning: Some packages may not have pre-built wheels: {result.stderr}")
        # Fallback: try without --only-binary for packages that need it
        print("Retrying with source packages allowed...")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "-r", str(temp_req),
            "-t", str(BUILD_DIR),
            "--platform", "manylinux2014_x86_64",
            "--implementation", "cp",
            "--python-version", "3.11",
            "--upgrade",
            "--quiet"
        ], check=True)

    # Remove temp file
    temp_req.unlink()
    print("Dependencies installed.")


def copy_application_code():
    """Copy application code to build directory."""
    # Copy app module
    app_src = BACKEND_DIR / "app"
    app_dest = BUILD_DIR / "app"

    if app_dest.exists():
        shutil.rmtree(app_dest)
    shutil.copytree(app_src, app_dest)
    print(f"Copied app module to {app_dest}")

    # Copy lambda handler
    handler_src = BACKEND_DIR / "lambda_handler.py"
    handler_dest = BUILD_DIR / "lambda_handler.py"
    shutil.copy2(handler_src, handler_dest)
    print(f"Copied lambda_handler.py")


def cleanup_build():
    """Remove unnecessary files to reduce package size."""
    # Directories to remove
    dirs_to_remove = [
        "pip",
        "setuptools",
        "wheel",
        "pkg_resources",
        "_distutils_hack",
        "distutils-precedence.pth",
    ]

    for dir_name in dirs_to_remove:
        dir_path = BUILD_DIR / dir_name
        if dir_path.exists():
            if dir_path.is_dir():
                shutil.rmtree(dir_path)
            else:
                dir_path.unlink()
            print(f"Removed {dir_name}")

    # Remove __pycache__ directories
    for pycache in BUILD_DIR.rglob("__pycache__"):
        shutil.rmtree(pycache)

    # Remove .dist-info directories (keep minimal)
    for dist_info in BUILD_DIR.rglob("*.dist-info"):
        shutil.rmtree(dist_info)

    print("Cleanup complete.")


def create_zip():
    """Create the Lambda deployment package."""
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    print(f"Creating {OUTPUT_FILE}...")
    shutil.make_archive(
        str(OUTPUT_FILE.with_suffix("")),
        "zip",
        BUILD_DIR
    )

    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"Created {OUTPUT_FILE} ({size_mb:.2f} MB)")

    if size_mb > 50:
        print("WARNING: Package exceeds 50MB direct upload limit.")
        print("Consider using S3 upload or Lambda layers.")
    elif size_mb > 250:
        print("ERROR: Package exceeds 250MB unzipped limit!")


def main():
    """Main packaging workflow."""
    print("=" * 60)
    print("Packaging FastAPI backend for Lambda (Linux x86_64)")
    print("=" * 60)

    clean_build_dir()
    install_dependencies()
    copy_application_code()
    cleanup_build()
    create_zip()

    print("=" * 60)
    print("Packaging complete!")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
