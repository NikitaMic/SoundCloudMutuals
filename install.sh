#!/usr/bin/env bash
# Installation script for SoundCloud Location Filter
# Supports macOS, Linux, and Windows (Git Bash/WSL)

set -e

echo "🎵 SoundCloud Location Filter - Installation"
echo "=============================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*|MINGW*|MSYS*)    PLATFORM=Windows;;
    *)          PLATFORM="Unknown";;
esac

echo "Detected platform: $PLATFORM"
echo ""

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    if python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD=python
    else
        echo "❌ Error: Python 3 is required but not found"
        echo "Please install Python 3 from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "❌ Error: Python 3 is required but not found"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "✓ Found $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install --user -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Make script executable
chmod +x sc-filter.py
echo "✓ Made sc-filter.py executable"
echo ""

# Setup command shortcut based on platform
if [ "$PLATFORM" = "Windows" ]; then
    # For Windows, create a batch wrapper
    cat > sc-filter.bat << 'EOF'
@echo off
python "%~dp0sc-filter.py" %*
EOF
    echo "✓ Created sc-filter.bat for Windows"
    echo ""
    echo "=============================================="
    echo "✅ Installation complete!"
    echo ""
    echo "Usage:"
    echo "  sc-filter.bat gloomweaver777 Berlin"
    echo ""
    echo "Or use directly:"
    echo "  python sc-filter.py gloomweaver777 Berlin"

else
    # For Unix-like systems (macOS/Linux)
    BIN_DIR="$HOME/bin"

    # Create ~/bin if it doesn't exist
    mkdir -p "$BIN_DIR"

    # Create symlink
    ln -sf "$(pwd)/sc-filter.py" "$BIN_DIR/sc-filter"
    echo "✓ Created symlink in $BIN_DIR"
    echo ""

    # Check if ~/bin is in PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo "⚠️  $BIN_DIR is not in your PATH"
        echo ""

        # Detect shell
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        else
            SHELL_RC="$HOME/.profile"
        fi

        echo "Adding to PATH in $SHELL_RC..."
        echo '' >> "$SHELL_RC"
        echo '# Added by SoundCloud Location Filter' >> "$SHELL_RC"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"

        echo "✓ Updated $SHELL_RC"
        echo ""
        echo "⚠️  Run this command to apply changes:"
        echo "  source $SHELL_RC"
        echo ""
        echo "Or restart your terminal"
    else
        echo "✓ $BIN_DIR is already in PATH"
    fi

    echo ""
    echo "=============================================="
    echo "✅ Installation complete!"
    echo ""
    echo "Usage:"
    echo "  sc-filter gloomweaver777 Berlin"
    echo ""
    echo "Or use directly:"
    echo "  ./sc-filter.py gloomweaver777 Berlin"
fi

echo ""
echo "For help:"
if [ "$PLATFORM" = "Windows" ]; then
    echo "  sc-filter.bat --help"
else
    echo "  sc-filter --help"
fi
echo ""
