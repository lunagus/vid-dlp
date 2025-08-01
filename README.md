# vid-dlp

A simple and powerful Python tool to download files by searching, crawling and extracting encrypted links. 

# WHY?

I wanted an easy way to automatically download video files and extract their audio from multiple websites and without being bothered by ads or unnecessary interaction. This script uses modern technologies and amazing tools like playwright, yt-dlp and ffmpeg to achieve this seamlessly.

## 🚀 Quick Start

### Step 1: Install Python
First, you need Python installed on your computer:
- **Windows**: Download from [python.org](https://python.org) and run the installer
- **Mac**: Download from [python.org](https://python.org) or use `brew install python`
- **Linux**: Usually pre-installed, or run `sudo apt install python3`

### Step 2: Download This Tool
1. Download all the files in this folder to your computer
2. Open a command prompt/terminal in this folder

### Step 3: Install Dependencies
Run these commands one by one:

```bash
# Install Python packages
pip install requests beautifulsoup4 pycryptodome playwright yt-dlp

# Install the browser
playwright install firefox
```

### Step 4: Install FFmpeg (For Audio Downloads)
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract to a folder, and add that folder to your PATH
- **Mac**: Run `brew install ffmpeg` in terminal
- **Linux**: Run `sudo apt install ffmpeg` (Ubuntu) or `sudo yum install ffmpeg` (CentOS)

### Step 5: Run the Tool
```bash
python downloader.py
```

## 📖 How to Use (Step by Step)

1. **Run the script**: Type `python downloader.py` and press Enter
2. **Enter video title**: Type the name of what you want to download (e.g., "Harry Potter 4")
3. **Choose language**: Pick your preferred language (Latino/Español/Inglés)
4. **Customize options** (optional): Choose between:
   - Video + Audio (full video file)
   - Audio only (just the sound as MP3)
5. **Wait**: The tool will automatically:
   - Search for your video
   - Find the best quality version
   - Download it to the `downloads` folder

## 🎯 Features

- 🔍 **Smart Search**: Find videos by title
- 🔓 **Advanced Extraction**: Automatically decrypts protected links
- 🌐 **Multi-Language**: Support for Latino, Español, and Inglés
- 🎬 **Flexible Downloads**: Get full video or audio-only
- 🤖 **Automatic Mode**: Works in the background (no browser window)
- 🚫 **Ad-Free**: Built-in ad blocking
- 📝 **Subtitles**: Automatically downloads subtitles when available
- 📁 **Organized**: Saves everything to a `downloads` folder

### Troubleshooting Common Issues

**"Python not found"**
- Make sure Python is installed and added to your PATH
- Try `python3` instead of `python`

**"Module not found"**
- Run: `pip install requests beautifulsoup4 pycryptodome playwright yt-dlp`

**"Playwright browser not found"**
- Run: `playwright install firefox`

**"FFmpeg not found"**
- Install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
- Make sure it's in your system PATH

**"No results found"**
- Try different search terms
- Check your internet connection
- The video might not be available

**"Download failed"**
- Check your internet connection
- Try again later
- The video source might be temporarily unavailable

## 🔮 Future Implementations

| Feature | Description |
|---------|-------------|
| **Support for Multiple Sites** | Extend the tool to work with various video platforms and sources |
| **Automatic Detection** | Automatically detect and adapt to new video sources and formats |
| **Site-Specific Optimizations** | Customized extraction methods for different websites |
| **Advanced Options** | Quality selection, format choices, and download preferences |
| **Download Queue** | Manage multiple downloads with progress tracking |
| **Batch Downloads** | Download multiple videos simultaneously |

## 🛡️ Legal and Ethical Considerations

This tool is designed for:
- Downloading your own content
- Educational purposes
- Personal use
- Content you have permission to download

Please respect:
- Copyright laws in your country
- Terms of service of video platforms
- Content creators' rights
- Fair use guidelines

---

**Note**: This tool is constantly being improved. Check back regularly for updates and new features!