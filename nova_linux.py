#!/usr/bin/env python3
"""NOVA for Linux — FastRouter-powered terminal assistant.

Uses only Python's standard library. Config and chat memory are stored locally.
Never share your API key or ~/.nova.json.
"""
import getpass
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path

APP_NAME = "NOVA"
BASE_URL = "https://api.fastrouter.ai/api/v1"
DEFAULT_MODEL = "fastrouter/auto"
CONFIG_PATH = Path.home() / ".nova.json"
MEMORY_PATH = Path.home() / ".nova_memory.json"
TIMEOUT = 90
MAX_HISTORY_MESSAGES = 40


def read_json(path, fallback):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return fallback


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def load_config():
    data = read_json(CONFIG_PATH, {})
    return data if isinstance(data, dict) else {}


def save_config(config):
    write_json(CONFIG_PATH, config)


def load_memory():
    data = read_json(MEMORY_PATH, [])
    if not isinstance(data, list):
        return []
    return [
        item for item in data
        if isinstance(item, dict)
        and item.get("role") in ("user", "assistant")
        and isinstance(item.get("content"), str)
    ][-MAX_HISTORY_MESSAGES:]


def save_memory(history):
    write_json(MEMORY_PATH, history[-MAX_HISTORY_MESSAGES:])


def banner():
    print("\033[96m")
    print("  ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗")
    print("  ████╗  ██║██╔═══██╗██║   ██║██╔══██╗")
    print("  ██╔██╗ ██║██║   ██║██║   ██║███████║")
    print("  ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║")
    print("  ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║")
    print("  ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝")
    print("\033[0m")
    print("  Terminal AI • Linux • FastRouter")
    print("  Type /help to see commands.\n")


def api_key(config):
    key = os.environ.get("FASTROUTER_API_KEY", "").strip()
    if key:
        return key
    key = str(config.get("api_key", "")).strip()
    if key:
        return key
    print("FastRouter API key is not configured.")
    key = getpass.getpass("Paste API key (input hidden): ").strip()
    if key:
        config["api_key"] = key
        save_config(config)
    return key


def api_request(path, key, payload=None):
    url = BASE_URL + path
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + key,
        "Accept": "application/json",
        "User-Agent": "Project-NOVA-Linux/1.0",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url, data=data, headers=headers, method="GET" if data is None else "POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            raw = response.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise RuntimeError("FastRouter returned a response that was not valid JSON.")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(detail)
            if isinstance(parsed, dict):
                error = parsed.get("error", {})
                detail = (
                    error.get("message") if isinstance(error, dict) else None
                ) or parsed.get("message") or detail
        except json.JSONDecodeError:
            pass
        if exc.code in (401, 403):
            raise RuntimeError("Authentication/permission error. Check your FastRouter API key and account access.")
        if exc.code == 429:
            raise RuntimeError("Rate limit or quota reached. Check your FastRouter account and try again later.")
        raise RuntimeError("FastRouter HTTP " + str(exc.code) + ": " + str(detail)[:700])
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        raise RuntimeError("Could not connect to FastRouter: " + str(reason))
    except TimeoutError:
        raise RuntimeError("Request timed out. Try again when your connection is stable.")


def show_help():
    print("""
Commands
  /help              Show this help
  /model             Show the current model
  /model MODEL_ID    Change the model
  /auto              Use fastrouter/auto
  /models            Fetch models available to your key
  /apikey            Replace the saved API key
  /clear             Clear the current conversation and saved chat memory
  /memory            Show saved memory status and message count
  /forget            Delete saved chat memory
  /exit              Quit NOVA

Anything else you type is sent as a message to the AI.
""")


def list_models(key):
    data = api_request("/models", key)
    models = data.get("data", []) if isinstance(data, dict) else []
    if not models:
        print("No model list was returned by the provider.")
        return
    print("Available models:")
    for model in models:
        if isinstance(model, dict) and model.get("id"):
            print("  " + str(model["id"]))


def chat(key, model, history, user_text):
    messages = history + [{"role": "user", "content": user_text}]
    payload = {"model": model, "messages": messages, "temperature": 0.7}
    data = api_request("/chat/completions", key, payload)
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("FastRouter's response did not contain a chat answer.")
    if isinstance(answer, list):
        answer = "\n".join(
            part["text"] for part in answer
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        )
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("The model returned an empty answer.")
    history.extend([
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": answer},
    ])
    del history[:-MAX_HISTORY_MESSAGES]
    return answer.strip()


def terminal_width():
    try:
        return max(50, min(100, os.get_terminal_size().columns - 4))
    except OSError:
        return 76


def main():
    if sys.version_info < (3, 8):
        print("NOVA requires Python 3.8 or newer.")
        raise SystemExit(1)

    config = load_config()
    model = str(config.get("model") or DEFAULT_MODEL)
    history = load_memory()
    banner()

    while True:
        try:
            user_text = input("\033[92mYou > \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not user_text:
            continue

        command, _, argument = user_text.partition(" ")
        command = command.lower()

        if command == "/help":
            show_help()
            continue
        if command == "/exit":
            print("Goodbye.")
            break
        if command == "/model":
            if argument.strip():
                model = argument.strip()
                config["model"] = model
                save_config(config)
                print("Model set to: " + model)
            else:
                print("Current model: " + model)
                print("Use /model MODEL_ID to change it.")
            continue
        if command == "/auto":
            model = DEFAULT_MODEL
            config["model"] = model
            save_config(config)
            print("Model set to " + DEFAULT_MODEL)
            continue
        if command == "/apikey":
            new_key = getpass.getpass("New FastRouter API key (input hidden): ").strip()
            if new_key:
                config["api_key"] = new_key
                save_config(config)
                print("API key saved locally.")
            else:
                print("No change made.")
            continue
        if command == "/models":
            try:
                key = api_key(config)
                if key:
                    list_models(key)
                else:
                    print("No API key entered.")
            except RuntimeError as exc:
                print("Error: " + str(exc))
            continue
        if command == "/memory":
            print("Saved memory file: " + str(MEMORY_PATH))
            print("Messages saved: " + str(len(history)))
            print("Memory is stored locally on this Linux machine.")
            continue
        if command in ("/clear", "/forget"):
            history = []
            try:
                if MEMORY_PATH.exists():
                    MEMORY_PATH.unlink()
            except OSError as exc:
                print("Could not delete memory file: " + str(exc))
                continue
            print("Saved conversation memory cleared.")
            continue
        if user_text.startswith("/"):
            print("Unknown command. Type /help.")
            continue

        try:
            key = api_key(config)
            if not key:
                print("No API key entered. Use /apikey to configure one.")
                continue
            print("\033[90mNOVA is thinking...\033[0m")
            answer = chat(key, model, history, user_text)
            save_memory(history)
            print("\n\033[96mNOVA >\033[0m")
            print(textwrap.fill(answer, width=terminal_width(), replace_whitespace=False))
            print()
        except RuntimeError as exc:
            print("\nError: " + str(exc) + "\n")
        except KeyboardInterrupt:
            print("\nRequest interrupted. Your saved memory is unchanged.\n")


if __name__ == "__main__":
    main()
