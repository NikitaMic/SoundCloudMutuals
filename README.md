# SoundCloud Location Filter

Find SoundCloud users by location - available as both a **web app** and **CLI tool**.

## 🌐 Web Interface (No Installation!)

**Try it now:** [https://nikitamic.github.io/SoundCloudMutuals](https://nikitamic.github.io/SoundCloudMutuals)

Perfect for non-technical users:
- ✅ No installation required
- ✅ Works in any browser
- ✅ Simple form interface
- ✅ Paste username & location, get results instantly

## 💻 CLI Installation

```bash
git clone https://github.com/NikitaMic/SoundCloudMutuals.git
cd SoundCloudMutuals
./install.sh
```

That's it! The installer will:
- ✅ Check for Python 3
- ✅ Install dependencies
- ✅ Set up the command for your platform (macOS/Linux/Windows)

## Usage

After installation:

```bash
sc-filter USERNAME LOCATION
```

### Examples

```bash
# Find users in Tbilisi
sc-filter gloomweaver777 Tbilisi

# Find users in Berlin
sc-filter gloomweaver777 Berlin

# Find users in Leipzig
sc-filter gloomweaver777 Leipzig

# Find users in any German city
sc-filter gloomweaver777 Germany

# Quiet mode (minimal output)
sc-filter gloomweaver777 Amsterdam --quiet
```

### Windows

On Windows, use:
```bash
sc-filter.bat gloomweaver777 Berlin
```

Or directly:
```bash
python sc-filter.py gloomweaver777 Berlin
```

## Output

Displays list of matching users with:
- Username
- Full name
- Location
- Follower count
- Profile URL

## How It Works

1. Fetches all users followed by the specified account via SoundCloud API
2. Filters by location (partial match, case-insensitive)
3. Displays results in console

## Features

- ✅ No API credentials needed (auto-extracts)
- ✅ Fast (5-10 seconds for ~150 users)
- ✅ Works with any location
- ✅ Console-only output
- ✅ Cross-platform (macOS/Linux/Windows)
- ✅ Simple one-command install

## Requirements

- Python 3.7+
- Internet connection

## Manual Installation

If you prefer not to use the install script:

```bash
pip3 install -r requirements.txt
chmod +x sc-filter.py
./sc-filter.py gloomweaver777 Berlin
```

## Help

```bash
sc-filter --help
```

## 🚀 Deploy Your Own Web Interface

To deploy the web app on GitHub Pages:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/NikitaMic/SoundCloudMutuals.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository Settings
   - Click "Pages" in sidebar
   - Under "Source", select "main" branch
   - Click Save

3. **Access your app:**
   - Available at: `https://nikitamic.github.io/SoundCloudMutuals`

The web interface runs 100% client-side - no server needed!

## Files

- `index.html` - Web interface (GitHub Pages)
- `sc-filter.py` - CLI tool
- `soundcloud_api.py` - SoundCloud API client
- `install.sh` - Cross-platform installer
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Troubleshooting

**Command not found after installation:**
- On macOS/Linux: Run `source ~/.zshrc` (or `~/.bashrc`)
- Or restart your terminal

**Python not found:**
- Install Python 3 from [python.org](https://www.python.org/downloads/)

**Dependencies error:**
- Run `pip3 install -r requirements.txt`
