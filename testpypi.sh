#!/bin/bash

# Initialize dry run flag
DRY_RUN=0

# Function to build the package
build_package() {
    echo "Building package..."
    python3 -m pip install --upgrade build
    rm -rf dist/ build/ *.egg-info/
    python3 -m build
}

# Function to upload the package
upload_package() {
    echo "Uploading package..."
    python3 -m pip install --upgrade twine
    python3 -m twine upload --repository testpypi dist/* --verbose
}

# Function to bump patch version
bump_patch() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "Bumping patch version (dry run)..."
        bumpver update --patch --dry
    else
        echo "Bumping patch version..."
        bumpver update --patch
    fi
}

# Function to bump minor version
bump_minor() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "Bumping minor version (dry run)..."
        bumpver update --minor --dry
    else
        echo "Bumping minor version..."
        bumpver update --minor
    fi
}

# Function to bump major version
bump_major() {
    if [ $DRY_RUN -eq 1 ]; then
        echo "Bumping major version (dry run)..."
        bumpver update --major --dry
    else
        echo "Bumping major version..."
        bumpver update --major
    fi
}

# Function to show current version
show_version() {
    echo "Current version:"
    bumpver show
}

# Check command line arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 [-b|-u|-p|-n|-j|-v] [-d]"
    echo "  -b: Build the package"
    echo "  -u: Upload the package"
    echo "  -p: Bump patch version"
    echo "  -n: Bump minor version"
    echo "  -j: Bump major version"
    echo "  -v: Show current version"
    echo "  -d: Dry run mode (use with -p, -n, or -j)"
    exit 1
fi

# Process command line arguments
while getopts "bubpnjvd" opt; do
    case $opt in
        b)
            build_package
            ;;
        u)
            upload_package
            ;;
        p)
            bump_patch
            ;;
        n)
            bump_minor
            ;;
        j)
            bump_major
            ;;
        v)
            show_version
            ;;
        d)
            DRY_RUN=1
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            exit 1
            ;;
    esac
done