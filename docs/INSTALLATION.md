# NOVA Installation Guide

NOVA is a terminal AI assistant that connects to the FastRouter API. Choose the section for your device.

## Before you start

- A working internet connection
- A FastRouter account and API key
- The NOVA script for your operating system

Keep your API key private. Do not paste it into public code, screenshots, or GitHub files.

## Android (Termux)

1. Install **Termux** from a trusted source.
2. Open Termux and update its packages:

   ```bash
   pkg update && pkg upgrade
   ```

3. Install Python:

   ```bash
   pkg install python
   ```

4. Download `nova_android.py` from this repository to your phone. Put it in a folder you can access from Termux.
5. In Termux, navigate to that folder. For example, if it is in Downloads:

   ```bash
   termux-setup-storage
   cd ~/storage/downloads
   ```

6. Start NOVA:

   ```bash
   python nova_android.py
   ```

7. When prompted, enter your FastRouter API key. NOVA saves its local configuration in your home directory.

If the script is in a different folder, use `cd` to enter that folder first.

## Windows

1. Install Python 3 from [python.org](https://www.python.org/downloads/windows/). During setup, enable **Add Python to PATH** if that option appears.
2. Download `nova_windows.py` from this repository.
3. Put the file in a folder such as `Downloads\NOVA`.
4. Open that folder in File Explorer, tap the address bar, type `cmd`, and press Enter. This opens Command Prompt in that folder.
5. Check Python:

   ```bat
   py --version
   ```

6. Start NOVA:

   ```bat
   py nova_windows.py
   ```

7. When prompted, enter your FastRouter API key.

If `py` is not recognized, try `python --version`. If neither command works, reopen the terminal after installing Python or repair the Python installation.

## macOS

1. Check whether Python 3 is installed:

   ```bash
   python3 --version
   ```

2. If it is missing, install Python 3 from [python.org](https://www.python.org/downloads/macos/).
3. Download `nova_macos.py` from this repository.
4. Open Terminal and use `cd` to enter the folder where you saved the file. For example:

   ```bash
   cd ~/Downloads
   ```

5. Start NOVA:

   ```bash
   python3 nova_macos.py
   ```

6. When prompted, enter your FastRouter API key.

## Linux

1. Check whether Python 3 is installed:

   ```bash
   python3 --version
   ```

2. If Python 3 is missing, install it with your distribution's package manager. For Debian or Ubuntu:

   ```bash
   sudo apt update
   sudo apt install python3
   ```

3. Download `nova_linux.py` from this repository.
4. Open a terminal and use `cd` to enter the folder where you saved it.
5. Start NOVA:

   ```bash
   python3 nova_linux.py
   ```

6. When prompted, enter your FastRouter API key.

## API key and configuration

NOVA asks for an API key when one is not already configured. You can also use the environment variable `FASTROUTER_API_KEY` where supported by your shell. Never hardcode a real key into the script or commit it to GitHub.

NOVA stores local settings and chat memory in files in your home directory, including `~/.nova.json` and `~/.nova_memory.json`. Keep your device account protected if you want that local data to remain private.

## Troubleshooting

- **Python command not found:** Install Python 3 and reopen the terminal.
- **Script not found:** Run `cd` to the folder containing the downloaded script, and check that the filename matches the command.
- **API authentication error:** Check that your FastRouter API key is valid and entered correctly.
- **Connection error:** Check your internet connection and FastRouter service status.
- **Model error:** Use NOVA's `/models` command to inspect available models, then select one with `/model MODEL_NAME`.

For command descriptions, see [`COMMANDS.md`](COMMANDS.md).
