#!/usr/bin/env python3
"""
vid-dlp
Downloads by searching, extracting encrypted links, and using yt-dlp
"""

import re
import json
import base64
import asyncio
from typing import List, Dict, Optional
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from playwright.async_api import async_playwright
import yt_dlp


class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

        self.key = "Ak7qrvvH4WKYxV2OgaeHAEg2a5eh16vE"

        # Ad blocker patterns
        self.ad_domains = {
            "googleads.g.doubleclick.net",
            "googlesyndication.com",
            "googleadservices.com",
            "google-analytics.com",
            "googletagmanager.com",
            "facebook.com",
            "fbcdn.net",
            "amazon-adsystem.com",
            "adsystem.amazon.com",
            "ads.yahoo.com",
            "media.net",
            "outbrain.com",
            "taboola.com",
            "adsrvr.org",
            "adsafeprotected.com",
        }

    def search_video(self, video_title: str) -> str:
        """Search for a video and return the first result URL"""
        print(f"🔍 Searching for: {video_title}")

        # Format search query
        search_query = video_title.replace(" ", "+")
        search_url = f"https://sololatino.net/?s={search_query}"

        try:
            resp = self.session.get(search_url, timeout=30)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for the first video result
            # Usually in a div with class "result-item" or similar
            for article in soup.find_all(
                ["article", "div"], class_=re.compile(r"post|item|result")
            ):
                title_link = article.find("a", href=True)
                if title_link and "peliculas" in title_link["href"]:
                    video_url = title_link["href"]
                    if not video_url.startswith("http"):
                        video_url = f"https://sololatino.net{video_url}"

                    print(f"✅ Found video: {video_url}")
                    return video_url

            # Alternative search in search results
            for link in soup.find_all("a", href=True):
                if (
                    "peliculas" in link["href"]
                    and video_title.lower().replace(" ", "-") in link["href"].lower()
                ):
                    video_url = link["href"]
                    if not video_url.startswith("http"):
                        video_url = f"https://sololatino.net{video_url}"

                    print(f"✅ Found video: {video_url}")
                    return video_url

            raise Exception("No video results found")

        except Exception as e:
            raise Exception(f"Failed to search for video: {e}")

    def get_iframe_url(self, page_url: str) -> str:
        """Find embed69 iframe URL from source page"""
        print(f"🔍 Loading page: {page_url}")

        try:
            resp = self.session.get(page_url, timeout=30)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for embed69 iframes
            for iframe in soup.find_all("iframe"):
                src = iframe.get("src", "")
                if "embed69" in src:
                    print(f"✅ Found embed69 iframe: {src}")
                    return src

            # Also check for embed69 links in href attributes
            for link in soup.find_all("a", href=True):
                href = link.get("href", "")
                if "embed69" in href:
                    print(f"✅ Found embed69 link: {href}")
                    return href

            raise Exception("No embed69 iframe or link found on the page")

        except Exception as e:
            raise Exception(f"Failed to load page {page_url}: {e}")

    def get_encrypted_data(self, iframe_url: str) -> List[Dict]:
        """Extract encrypted data from embed69 iframe"""
        print(f"🔗 Loading embed69 iframe: {iframe_url}")

        try:
            resp = self.session.get(iframe_url, timeout=30)
            resp.raise_for_status()

            # Extract the dataLink array from JavaScript
            # Look for the pattern: var dataLink = [...];
            json_match = re.search(
                r"var\s+dataLink\s*=\s*(\[.*?\]);", resp.text, re.DOTALL
            )

            if not json_match:
                # Try alternative patterns
                json_match = re.search(
                    r"dataLink\s*=\s*(\[.*?\]);", resp.text, re.DOTALL
                )

            if not json_match:
                raise Exception("Could not find encrypted dataLink in iframe")

            encrypted_data = json.loads(json_match.group(1))
            print(f"✅ Found {len(encrypted_data)} language versions")
            return encrypted_data

        except Exception as e:
            raise Exception(f"Failed to extract encrypted data: {e}")

    def decrypt_link(self, encrypted_link_base64: str) -> str:
        """Decrypt embed69.org encrypted links using AES-CBC with PKCS7 padding"""
        try:
            # Decode base64
            encrypted_data = base64.b64decode(encrypted_link_base64)

            # Extract IV (first 16 bytes) and encrypted content
            iv = encrypted_data[:16]
            encrypted_content = encrypted_data[16:]

            # Create AES cipher
            cipher = AES.new(self.key.encode("utf-8"), AES.MODE_CBC, iv)

            # Decrypt
            decrypted_padded = cipher.decrypt(encrypted_content)

            # Remove PKCS7 padding
            decrypted = unpad(decrypted_padded, AES.block_size)

            # Convert to string
            return decrypted.decode("utf-8")

        except Exception as e:
            raise Exception(f"Failed to decrypt link: {e}")

    def decrypt_all_urls(self, encrypted_data: List[Dict]) -> List[Dict]:
        """Decrypt all URLs from all language versions"""
        decrypted_urls = []

        for language_data in encrypted_data:
            file_id = language_data.get("file_id")
            video_language = language_data.get("video_language", "Unknown")
            sorted_embeds = language_data.get("sortedEmbeds", [])

            print(f"🔍 Processing {video_language} version (ID: {file_id})")

            for embed in sorted_embeds:
                servername = embed.get("servername", "Unknown")
                encrypted_link = embed.get("link")
                embed_type = embed.get("type", "video")

                if not encrypted_link:
                    continue

                try:
                    decrypted_url = self.decrypt_link(encrypted_link)
                    print(f"  🔓 {servername} ({embed_type}): {decrypted_url}")

                    decrypted_urls.append(
                        {
                            "url": decrypted_url,
                            "server": servername,
                            "language": video_language,
                            "type": embed_type,
                            "quality": self._get_server_quality(servername),
                        }
                    )

                except Exception as e:
                    print(f"  ❌ Failed to decrypt {servername}: {e}")

        return decrypted_urls

    def _get_server_quality(self, servername: str) -> str:
        """Estimate quality based on server name"""
        servername_lower = servername.lower()
        if "hd" in servername_lower or "1080" in servername_lower:
            return "HD"
        elif "720" in servername_lower:
            return "720p"
        elif "480" in servername_lower:
            return "480p"
        else:
            return "Unknown"

    async def block_ads(self, route):
        """Block ads and unwanted requests"""
        url = route.request.url

        # Check if URL contains ad domains
        for ad_domain in self.ad_domains:
            if ad_domain in url:
                await route.abort()
                return

        # Block common ad patterns
        ad_patterns = ["/ads/", "/advertisement/", "/popup/", "/banner/"]
        if any(pattern in url for pattern in ad_patterns):
            await route.abort()
            return

        await route.continue_()

    async def extract_stream_url_from_embed(
        self, embed_url: str, headless: bool = True
    ) -> Optional[str]:
        """
        Navigates to an embed URL, simulates play click, and extracts media stream URL (.m3u8 or .mp4).
        """
        print(f"🔍 Extracting stream URL from embed: {embed_url}")
        print(f"🤖 Headless mode: {'ON' if headless else 'OFF'}")

        found_stream_url = None

        try:
            async with async_playwright() as p:
                browser = await p.firefox.launch(
                    headless=headless,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-web-security",
                        "--disable-features=TranslateUI",
                        "--disable-extensions",
                        "--disable-plugins",
                        "--no-first-run",
                        "--no-default-browser-check",
                        "--ignore-certificate-errors",
                        "--ignore-ssl-errors",
                        "--disable-popup-blocking",
                        "--disable-notifications",
                    ],
                )
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    extra_http_headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br",
                        "DNT": "1",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Cache-Control": "max-age=0",
                    },
                    java_script_enabled=True,
                    bypass_csp=True,
                    ignore_https_errors=True,
                )

                # Register ad blocker and popup blocker BEFORE creating pages
                print("🚫 Setting up ad blocker and popup protection...")
                await context.route("**/*", self.block_ads)

                page = await context.new_page()

                # Handle popup windows and alerts
                page.on("dialog", lambda dialog: asyncio.create_task(dialog.dismiss()))
                page.on("popup", lambda popup: asyncio.create_task(popup.close()))

                # Close any additional tabs/windows that might open
                context.on(
                    "page",
                    lambda new_page: asyncio.create_task(new_page.close())
                    if new_page != page
                    else None,
                )

                # Set referer to the original source page
                referer = "https://sololatino.net/"
                await page.set_extra_http_headers(
                    {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Referer": referer,
                    }
                )

                # Intercept network requests to capture stream URLs
                async def handle_request(request):
                    url = request.url
                    if ".m3u8" in url or ".mp4" in url:
                        nonlocal found_stream_url
                        if not found_stream_url:  # Only capture the first one
                            print(f"🎬 Found stream URL: {url}")
                            found_stream_url = url

                page.on("request", handle_request)

                # Navigate to embed URL
                await page.goto(embed_url, wait_until="domcontentloaded", timeout=30000)

                # Wait for page to load
                await page.wait_for_timeout(3000)

                # In headless mode, skip clicking and just wait for auto-play
                if headless:
                    print("🎬 Headless mode: Waiting for auto-play...")
                else:
                    # Look for play button and click it (only in visible mode)
                    play_selectors = [
                        'button[class*="play"]',
                        'div[class*="play"]',
                        ".play-button",
                        ".play-btn",
                        "#play",
                        'button:has-text("Play")',
                        'div:has-text("▶")',
                        '[aria-label*="play"]',
                    ]

                    play_clicked = False
                    for selector in play_selectors:
                        try:
                            play_button = await page.query_selector(selector)
                            if play_button:
                                print(f"🎬 Clicking play button: {selector}")
                                await play_button.click()
                                play_clicked = True
                                break
                        except Exception as e:
                            continue

                    if not play_clicked:
                        # Try clicking on video element directly
                        try:
                            video = await page.query_selector("video")
                            if video:
                                print("🎬 Clicking video element")
                                await video.click()
                        except Exception as e:
                            print(
                                "⚠️ Could not find play button, waiting for auto-play..."
                            )

                # Wait for stream URL to be captured
                for i in range(30):  # Wait up to 30 seconds
                    if found_stream_url:
                        break
                    await page.wait_for_timeout(1000)

                await browser.close()

        except Exception as e:
            print(f"❌ Error extracting stream URL: {e}")

        return found_stream_url

    def get_download_options(self) -> dict:
        """Get user download preferences"""
        print("\n📥 Download Options:")
        print("   1) Video + Audio (default)")
        print("   2) Audio only (MP3)")

        choice = input("Choose option [1]: ").strip() or "1"

        options = {"audio_only": choice == "2"}

        if options["audio_only"]:
            print("🎵 Audio-only mode selected - will extract MP3 after download")
        else:
            print("🎬 Video + Audio mode selected")

        return options

    def download_with_ytdlp(
        self,
        stream_url: str,
        video_title: str,
        output_dir: str = "downloads",
        download_opts: dict = None,
    ):
        """Download the stream using yt-dlp"""
        print(f"📥 Starting download with yt-dlp...")

        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)

        # Clean video title for filename
        safe_title = re.sub(r'[<>:"/\\|?*]', "_", video_title)

        # Default options
        ydl_opts = {
            "outtmpl": f"{output_dir}/{safe_title}.%(ext)s",
            "format": "best[ext=mp4]/best",
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en", "es"],
            "ignoreerrors": True,
            "no_warnings": False,
            "extract_flat": False,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://sololatino.net/",
            },
        }

        # Apply custom options if provided
        if download_opts:
            if download_opts.get("audio_only"):
                # For audio-only, we'll download the video first then extract audio
                # This ensures we get the best quality audio
                ydl_opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]
                ydl_opts["outtmpl"] = f"{output_dir}/{safe_title}.%(ext)s"
                print("🎵 Audio-only mode: Will extract MP3 after download")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([stream_url])
                print(f"✅ Download completed: {safe_title}")
        except Exception as e:
            print(f"❌ Download failed: {e}")
            raise

    async def download_video(
        self,
        video_title: str,
        preferred_language: str = "Latino",
        output_dir: str = "downloads",
        headless: bool = True,
    ):
        """Main method to download a video"""
        try:
            # Step 1: Search for video
            video_url = self.search_video(video_title)

            # Step 2: Get iframe URL
            iframe_url = self.get_iframe_url(video_url)

            # Step 3: Extract encrypted data
            encrypted_data = self.get_encrypted_data(iframe_url)

            # Step 4: Decrypt URLs
            decrypted_urls = self.decrypt_all_urls(encrypted_data)

            if not decrypted_urls:
                raise Exception("No decrypted URLs found")

            # Step 5: Filter by preferred language
            preferred_urls = [
                url
                for url in decrypted_urls
                if preferred_language.lower() in url["language"].lower()
            ]
            if not preferred_urls:
                print(
                    f"⚠️ {preferred_language} version not found, using first available"
                )
                preferred_urls = decrypted_urls

            # Step 6: Sort by quality (HD first)
            preferred_urls.sort(
                key=lambda x: (x["quality"] == "HD", x["quality"] == "720p"),
                reverse=True,
            )

            # Step 7: Extract stream URL from the best embed
            stream_url = None
            for url_info in preferred_urls:
                print(
                    f"🎯 Trying {url_info['server']} ({url_info['language']}) - {url_info['quality']}"
                )

                stream_url = await self.extract_stream_url_from_embed(
                    url_info["url"], headless
                )
                if stream_url:
                    break

            if not stream_url:
                raise Exception("Could not extract stream URL from any embed")

            # Step 8: Get download preferences
            print(f"\n✅ Stream URL found: {stream_url}")

            choice = (
                input("\nCustomize download options? [y/N]: ").lower().startswith("y")
            )
            if choice:
                download_opts = self.get_download_options()
            else:
                print("📥 Using standard download options (best quality + subtitles)")
                download_opts = None

            # Step 9: Download with yt-dlp
            self.download_with_ytdlp(stream_url, video_title, output_dir, download_opts)

        except Exception as e:
            print(f"❌ Download failed: {e}")
            raise


async def main():
    """Main function"""
    print("🎬 Downloader")
    print("=" * 40)

    downloader = Downloader()

    # Get user input
    video_title = input("Enter video title: ").strip()
    if not video_title:
        print("❌ Video title cannot be empty")
        return

    language = (
        input("Preferred language (Latino/Español/Inglés) [Latino]: ").strip()
        or "Latino"
    )

    # Set defaults
    output_dir = "downloads"
    headless = True

    print(f"\n🎯 Searching for: {video_title}")
    print(f"🌐 Preferred language: {language}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🤖 Browser mode: Headless")
    print("-" * 40)

    try:
        await downloader.download_video(video_title, language, output_dir, headless)
        print("\n🎉 Video download completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Required dependencies check
    try:
        import requests
        import bs4
        from Crypto.Cipher import AES  # This is from pycryptodome
        import playwright
        import yt_dlp

        print("✅ All dependencies are installed")

        # Check for FFmpeg (required for audio extraction)
        try:
            import subprocess

            result = subprocess.run(
                ["ffmpeg", "-version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                print("✅ FFmpeg is available (required for audio extraction)")
            else:
                print("⚠️  FFmpeg not found - audio extraction will not work")
                print("   Install FFmpeg: https://ffmpeg.org/download.html")
        except FileNotFoundError:
            print("⚠️  FFmpeg not found - audio extraction will not work")
            print("   Install FFmpeg: https://ffmpeg.org/download.html")

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print(
            "Install with: pip install requests beautifulsoup4 pycryptodome playwright yt-dlp"
        )
        print("Then run: playwright install firefox")
        print(
            "For audio extraction, also install FFmpeg: https://ffmpeg.org/download.html"
        )
        exit(1)

    asyncio.run(main())
