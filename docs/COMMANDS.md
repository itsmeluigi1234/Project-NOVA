# NOVA Commands

Type these commands in NOVA's terminal chat. Commands are entered at the NOVA prompt, not in your phone's or computer's regular terminal.

| Command | What it does | Example |
|---|---|---|
| `/help` | Shows the built-in help, when available in your version. | `/help` |
| `/model` | Shows or changes the selected model, depending on the arguments. | `/model fastrouter/auto` |
| `/auto` | Switches back to NOVA's automatic model selection. | `/auto` |
| `/models` | Requests the available model list from the configured API. | `/models` |
| `/apikey` | Opens the API-key setup/update flow. | `/apikey` |
| `/memory` | Shows local memory information. | `/memory` |
| `/clear` | Clears the current conversation context handled by the script. | `/clear` |
| `/forget` | Clears NOVA's saved chat memory, if confirmed/implemented by your version. | `/forget` |
| `/exit` | Exits NOVA. | `/exit` |

## Choosing a model

To choose a specific model, enter its exact name after `/model`:

```text
/model fastrouter/auto
```

Use `/models` to see model names available through your FastRouter account. Availability can change, and not every model may be enabled for every account.

## API key safety

- Never share your FastRouter API key publicly.
- Do not commit your key to GitHub.
- If you think your key has been exposed, revoke or rotate it through your FastRouter account.
- NOVA's local configuration and memory files are stored on your device.

## Notes

Commands can differ between NOVA versions. If a command is not recognized, run `/help` in your copy and check the README for the version you downloaded.
