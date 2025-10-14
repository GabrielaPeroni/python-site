import os
import sys
from pathlib import Path


def find_python_directories(
    root_path: Path, exclude_dirs: set[str] = None
) -> list[Path]:
    """
    Find all directories that contain Python files (.py).

    Args:
        root_path: The root directory to scan
        exclude_dirs: Set of directory names to exclude from scanning

    Returns:
        List of Path objects representing directories with Python files
    """
    if exclude_dirs is None:
        exclude_dirs = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            "node_modules",
            "env",
            "venv",
            ".venv",
            ".env",
            "staticfiles",
            "media",
            ".tox",
            ".coverage",
            "htmlcov",
            "site-packages",
        }

    python_dirs = []

    for root, dirs, files in os.walk(root_path):
        # Remove excluded directories from dirs list to prevent walking into them
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Check if current directory has any Python files
        has_python_files = any(file.endswith(".py") for file in files)

        if has_python_files:
            python_dirs.append(Path(root))

    return python_dirs


def check_and_create_init_files(
    python_dirs: list[Path],
) -> tuple[list[Path], list[Path]]:
    """
    Check for missing __init__.py files and create them if needed.

    Args:
        python_dirs: List of directories that contain Python files

    Returns:
        Tuple of (existing_init_files, created_init_files)
    """
    existing_init_files = []
    created_init_files = []

    for directory in python_dirs:
        init_file = directory / "__init__.py"

        if init_file.exists():
            existing_init_files.append(init_file)
        else:
            try:
                # Create an empty __init__.py file
                init_file.touch()
                created_init_files.append(init_file)
                print(f"Created: {init_file.relative_to(Path.cwd())}")
            except OSError as e:
                print(f"Failed to create {init_file}: {e}", file=sys.stderr)

    return existing_init_files, created_init_files


def main() -> int:
    """
    Main function to check and create __init__.py files.

    Returns:
        Exit code: 0 if no files were created, 1 if files were created
    """
    project_root = Path.cwd()

    print(f"🔍 Scanning for Python directories in: {project_root}")

    # Find all directories with Python files
    python_dirs = find_python_directories(project_root)

    if not python_dirs:
        print("ℹ️  No Python directories found.")
        return 0

    print(f"📁 Found {len(python_dirs)} directories with Python files")

    # Check and create __init__.py files
    existing_files, created_files = check_and_create_init_files(python_dirs)

    # Report results
    print(f"\n📊 Summary:")
    print(f"   - Directories with existing __init__.py: {len(existing_files)}")
    print(f"   - Created __init__.py files: {len(created_files)}")

    if created_files:
        print(f"\n📝 Created files:")
        for file_path in created_files:
            print(f"   - {file_path.relative_to(project_root)}")

        # Return 1 to indicate changes were made (useful for CI/CD)
        return 1
    else:
        print(f"\n✨ All Python directories already have __init__.py files!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
