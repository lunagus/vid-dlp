# 📼 vid-dlp

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](#)

A **robust**, **reliable**, and **user-friendly** Python application for **searching**, **decrypting**, and **downloading** video and audio content from a variety of websites — completely **ad-free** and **automated**.

# WHY?

I wanted an easy way to automatically download video files and extract their audio from multiple websites and without being bothered by ads or unnecessary interaction. **vid-dlp** addresses these challenges by providing a seamless, headless experience. Ideal for educators, content creators, researchers, and casual users, this tool ensures **high reliability** through automated link decryption, **minimal intervention** with headless automation and a **clean output** organized in a dedicated `downloads/` directory.

## 🎯 Requirements

First, you need **Python** installed on your computer:
- **Windows**: Download from [python.org](https://python.org) and run the installer
- **Mac**: Download from [python.org](https://python.org) or use `brew install python`
- **Linux**: Usually pre-installed, or run `sudo apt install python3`

---

## 🚀 Quick Start

1. **Clone the Repository**
    ```bash
    git clone https://github.com/lunagus/vid-dlp.git
    cd vid-dlp
    ```
    💡 Alternatively, download the ZIP archive and extract it.

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    playwright install firefox
    ```

3. **Run the Application**
    ```bash
    python downloader.py
    ```

---

## 📖 How to Use (Step by Step)

1. **Run the script**: Type `python downloader.py` and press Enter
2. **Enter video title**: Type the name of what you want to download
3. **Choose language**: Pick your preferred language (Latino/Español/Inglés)
4. **Customize options** (optional): Choose between:
   - Video + Audio (full video file)
   - Audio only (just the sound as MP3)
5. **Wait**: The tool will automatically:
   - Search for your video
   - Find the best quality version
   - Download it to the `downloads` folder

---

## 🎯 Features

- 🔍 **Smart Search**: Find videos by title
- 🔓 **Advanced Extraction**: Automatically decrypts protected links
- 🌐 **Multi-Language**: Support for Latino, Español, and Inglés
- 🎬 **Flexible Downloads**: Get full video or audio-only
- 🤖 **Automatic Mode**: Works in the background (no browser window)
- 🚫 **Ad-Free**: Built-in ad blocking
- 📝 **Subtitles**: Automatically downloads subtitles when available
- 📁 **Organized**: Saves everything to a `downloads` folder

## 🛠️ Technology Stack

- **Python 3.8+**
- **Playwright**: Headless browser automation
- **yt-dlp**: Advanced media downloader
- **FFmpeg**: Media processing and audio conversion
- **BeautifulSoup4**: HTML parsing
- **PyCryptodome**: Cryptographic operations

---

## 🔧 Troubleshooting

| Issue                      | Solution                                                                      |
|----------------------------|-------------------------------------------------------------------------------|
| `python` not recognized    | Ensure Python 3.8+ is installed and added to PATH.                           |
| Missing modules            | Run `pip install -r requirements.txt`.                                        |
| Playwright browser errors  | Execute `playwright install firefox`.                                         |
| FFmpeg not found           | Install FFmpeg and verify in system PATH.                                      |
| No results                | Try broader search terms or check network connectivity.                       |
| Download failures         | Retry later; source may be temporarily unavailable.                           |

---

## 🔮 Future Implementations

| Feature | Description |
|---------|-------------|
| **Support for Multiple Sites** | Extend the tool to work with various video platforms and sources |
| **Automatic Detection** | Automatically detect and adapt to new video sources and formats |
| **Site-Specific Optimizations** | Customized extraction methods for different websites |
| **Advanced Options** | Quality selection, format choices, and download preferences |
| **Download Queue** | Manage multiple downloads with progress tracking |
| **Batch Downloads** | Download multiple videos simultaneously |

---

## 🤝 Contributing

This project is constantly being improved. Check back regularly for updates and new features or reach out to suggest your own!

Any contributions are welcome! To get started:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request.

---

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

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
