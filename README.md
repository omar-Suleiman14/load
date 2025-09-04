<div align="center">
  
██╗      ██████╗  █████╗ ██████╗ 
██║     ██╔═══██╗██╔══██╗██╔══██╗
██║     ██║   ██║███████║██║  ██║
██║     ██║   ██║██╔══██║██║  ██║
███████╗╚██████╔╝██║  ██║██████╔╝
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝

**A simple and beautiful command-line tool for downloading YouTube videos and audio.**

</div>

This tool is a proud part of the **ZainOS project**, an initiative by **khomod** focused on learning, development, and creating practical, polished utilities.

---

<!-- 
TODO: Create a short GIF of the app in action and replace the image below.
It should show the welcome screen, entering a URL, selecting video, and the progress bar.
-->
<p align="center">
  <img src="https://i.postimg.cc/gcCT2qS2/Screenshot-2025-09-04-184544.png" alt="Load CLI Demo">
</p>

## Features

*   **Download Video:** Choose from a list of available MP4 video qualities.
*   **Extract High-Quality Audio:** Save audio tracks directly to `mp3`, `wav`, or `flac`.
*   **Beautiful & Interactive UI:** A polished command-line experience powered by the Rich library, complete with progress bars and clear prompts.
*   **Zero Dependencies:** The executables are self-contained. No need to install Python or FFmpeg!
*   **Cross-Platform:** Pre-built binaries are available for Windows, macOS, and Linux.

## Get Started (No Installation Needed)

You can download the latest version of `load` for your operating system directly from the releases page.

**[➡ Go to the Latest Release Page](https://github.com/omar-Suleiman14/load/releases/latest)**

### For Windows Users

1.  Download the `load-windows.exe` file from the latest release assets.
2.  Open a terminal (Command Prompt or PowerShell) in the folder where you saved the file.
3.  Run the application by typing:
    ```bash
    .\load-windows.exe
    ```
> **Note:** Windows Defender SmartScreen might show a warning because the app is not signed. Click "More info" and then "Run anyway" to proceed.

### For macOS Users

1.  Download the `load-macos` file from the latest release assets.
2.  Open a Terminal in the folder where you saved the file.
3.  You need to make the file executable. Run this command once:
    ```bash
    chmod +x ./load-macos
    ```
4.  Now, run the application by typing:
    ```bash
    ./load-macos
    ```
> **Note:** macOS may show a security warning like "'load-macos' cannot be opened because it is from an unidentified developer." To fix this, open **System Settings > Privacy & Security**, scroll down, and you will see a message about "load-macos" being blocked. Click the **"Open Anyway"** button. You only need to do this once.

### For Linux Users

1.  Download the `load-linux` file from the latest release assets.
2.  Open a terminal in the folder where you saved the file.
3.  Make the file executable by running this command:
    ```bash
    chmod +x ./load-linux
    ```
4.  Run the application by typing:
    ```bash
    ./load-linux
    ```

## For Developers (Running from Source)

If you'd like to run the project from the source code, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/omar-Suleiman14/load.git
    cd load
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python main_cli.py
    ```

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for the full license text.

---

Created by **khomod** for the **ZainOS Project**.
