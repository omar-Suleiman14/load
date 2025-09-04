# downloader.py
"""
Core download logic for the 'load' application.
This version uses a custom logger to completely silence yt-dlp's
default console output for a clean UI experience and is self-contained
using imageio-ffmpeg.
"""
from pathlib import Path
import yt_dlp
import imageio_ffmpeg

# A dummy logger to swallow all of yt-dlp's output.
class SilentLogger:
    """A yt-dlp logger that discards all messages."""
    def debug(self, msg):
        """Ignores debug messages."""
    def warning(self, msg):
        """Ignores warning messages."""
    def error(self, msg):
        """Ignores error messages."""

class Downloader:
    """Manages all interactions with yt-dlp for downloading media."""

    def get_downloads_folder(self):
        """Returns the default downloads folder for the current OS."""
        return Path.home() / "Downloads"

    def fetch_metadata(self, url):
        """Fetches video metadata without downloading."""
        ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.sanitize_info(ydl.extract_info(url, download=False))
        except yt_dlp.utils.DownloadError:
            # Let the CLI handle user-facing errors. Just return None.
            return None

    def get_video_formats(self, metadata):
        """Parses metadata to return a list of user-friendly video formats."""
        formats = []
        if not metadata or 'formats' not in metadata:
            return formats
        for f in metadata['formats']:
            # We look for streams that have video but no audio, as these are the high-quality ones.
            if (f.get('vcodec') != 'none' and f.get('acodec') == 'none'
                    and f.get('ext') == 'mp4' and f.get('height')):
                res = f.get('height')
                note = f.get('format_note', f'{res}p')
                size = f.get('filesize_approx', 0) / (1024 * 1024)
                display = f"{note} ({f.get('ext')}, ~{size:.1f} MB)"
                formats.append({'id': f['format_id'], 'display': display, 'resolution': res})
        # De-duplicate by resolution, keeping the best entry for each, sorted highest to lowest.
        unique_formats = list({
            f['resolution']: f for f in sorted(formats, key=lambda x: x['resolution'], reverse=True)
        }.values())
        return unique_formats

    def download_video(self, url, download_path, format_id, progress_hook):
        """Downloads video and audio, merging them into a single MP4 file."""
        output_template = str(download_path / '%(title)s.%(ext)s')

        ydl_opts = {
            # Select specified video format AND the best available audio
            'format': f'{format_id}+bestaudio/best',
            # Merge into an MP4 container when done
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'logger': SilentLogger(),
            'noprogress': True,
            'quiet': True,
            # CRITICAL FIX: Tell yt-dlp where to find FFmpeg
            'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio(self, url, download_path, audio_format, progress_hook):
        """Downloads and converts audio to the specified format."""
        # FIXED: Use '%(ext)s' to let the post-processor set the final extension.
        output_template = str(download_path / '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': audio_format}],
            'logger': SilentLogger(),
            'noprogress': True,
            'quiet': True,
            # CRITICAL FIX: Tell yt-dlp where to find FFmpeg
            'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
