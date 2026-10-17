<p align="center">
  <img src="assets/nova_logo.png" alt="NOVA logo" width="100%">
</p>

<h1 align="center">NOVA</h1>

<p align="center">
  A terminal AI assistant powered by the FastRouter API.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/API-FastRouter-6C5CE7" alt="FastRouter API">
  <img src="https://img.shields.io/badge/Platforms-Android%20%7C%20Windows%20%7C%20macOS%20%7C%20Linux-2ea44f" alt="Supported platforms">
  <img src="https://img.shields.io/badge/Dependencies-Python%20standard%20library-informational" alt="Standard library">
</p>

NOVA is a lightweight terminal AI assistant designed to run on Android with Termux, Windows, macOS, and Linux. It connects to FastRouter for AI responses and keeps its configuration and conversation memory locally on your device.

## Choose your platform

Select your device to open the relevant setup instructions.

| Platform | Script | Installation guide |
|---|---|---|
| Android / Termux | `nova_android.py` | [Android setup](docs/INSTALLATION.md#android-termux) |
| Windows | `nova_windows.py` | [Windows setup](docs/INSTALLATION.md#windows) |
| macOS | `nova_macos.py` | [macOS setup](docs/INSTALLATION.md#macos) |
| Linux | `nova_linux.py` | [Linux setup](docs/INSTALLATION.md#linux) |

Need help using commands? Read the [NOVA Commands Guide](docs/COMMANDS.md).

## Features

- **FastRouter API** — use models available to your FastRouter account.
- **Automatic model selection** — starts with `fastrouter/auto` and supports switching models.
- **Terminal interface** — chat from a command-line prompt.
- **Local configuration** — saves NOVA settings on your device.
- **Local conversation memory** — stores memory locally rather than in this GitHub repository.
- **Multiple platforms** — separate startup scripts for Android/Termux, Windows, macOS, and Linux.
- **Python standard library** — designed to avoid additional Python package installs.

## Quick start

1. Open the installation guide for your platform above.
2. Download the matching NOVA script from this repository.
3. Install Python 3 if your platform does not already have it.
4. Run the script from the folder where you saved it.
5. Enter your FastRouter API key when NOVA asks for it.

Typical startup commands:

**Android / Termux**
```bash
python nova_android.py
```

**Windows**
```bat
py nova_windows.py
```

**macOS**
```bash
python3 nova_macos.py
```

**Linux**
```bash
python3 nova_linux.py
```

These commands assume you are already in the directory containing the matching script. Full instructions, including how to install Python, are in the [Installation Guide](docs/INSTALLATION.md).

## FastRouter API key

NOVA needs a valid FastRouter API key to request AI responses.

- Get your API key from your FastRouter account.
- Enter it when prompted by NOVA, or follow the configuration instructions in the installation guide.
- Keep your key private.
- **Never** hardcode your real API key in a script or commit it to GitHub.
- If a key is exposed, revoke or rotate it through your FastRouter account.

NOVA uses the FastRouter API endpoint and defaults to the `fastrouter/auto` model. Available models may vary by account and can change over time.

## Commands

The available command set may depend on the version of NOVA you are running. Common commands include:

| Command | Purpose |
|---|---|
| `/help` | Display help, if supported by the current version |
| `/model MODEL_NAME` | Select a specific model |
| `/auto` | Return to automatic model selection |
| `/models` | Request a list of available models |
| `/apikey` | Set or update the API key |
| `/memory` | View memory information |
| `/clear` | Clear the current conversation context |
| `/forget` | Clear saved chat memory, if supported by the current version |
| `/exit` | Exit NOVA |

See the complete [Commands Guide](docs/COMMANDS.md) for examples and notes.

## Local files and privacy

NOVA may save configuration and conversation memory in your home directory:

- `~/.nova.json` — local configuration, including settings needed to connect.
- `~/.nova_memory.json` — local conversation memory.

Keep your device account protected. Do not upload these files or share their contents if they contain private information or API credentials.

## Repository structure

```text
Project-NOVA/
├── README.md
├── nova_android.py
├── nova_windows.py
├── nova_macos.py
├── nova_linux.py
├── assets/
│   └── nova_logo.png
└── docs/
    ├── INSTALLATION.md
    └── COMMANDS.md
```

## Troubleshooting

- **Python is not recognized:** Install Python 3 and reopen your terminal. On Windows, try `py --version`; on macOS/Linux/Termux, try `python3 --version` or `python --version` as appropriate.
- **The script cannot be found:** Navigate to the folder where you downloaded the script and check the filename.
- **Authentication fails:** Check that your FastRouter API key is valid and has not been revoked.
- **A model is unavailable:** Run `/models` and select a model available to your account.
- **The request cannot connect:** Check your internet connection and the FastRouter service.

For step-by-step help, open the [Installation Guide](docs/INSTALLATION.md).

## Project status

NOVA is an ongoing project. Platform scripts and instructions are provided as a starting point; behavior may vary by operating system, Python installation, and FastRouter API availability. Contributions, bug reports, and clear reproduction steps are welcome.

## Contributing

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes.
4. Open a pull request describing what changed.

Please do not include API keys, local configuration files, or private conversation memory in contributions.

## License

See the [`LICENSE`](LICENSE) file for the project's license.
