import os
import sys
import json
import time
import urllib.request
import urllib.error
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv()

def _post_json(url, headers, payload, timeout):
    data = json.dumps(payload).encode("utf-8")
    request_headers = dict(headers)
    request_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=request_headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
        return resp.status, body


def test_endpoint(name, url, headers, payload, timeout=10):
    print(f"🔄 Testing {name}...", end="", flush=True)
    start = time.time()
    try:
        status_code, body = _post_json(url, headers, payload, timeout)
        elapsed = time.time() - start

        if status_code == 200:
            print(f" ✅ Success ({elapsed:.2f}s)")
            return True, f"Success ({elapsed:.2f}s)"

        print(f" ❌ Failed (Status: {status_code})")
        _print_error_body(body)
        return False, f"Failed: {status_code}"
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        print(f" ❌ Failed (Status: {e.code})")
        _print_error_body(e.read())
        return False, f"Failed: {e.code} ({elapsed:.2f}s)"
    except urllib.error.URLError as e:
        print(f" ❌ Error: {str(e)}")
        return False, str(e)
    except Exception as e:
        print(f" ❌ Error: {str(e)}")
        return False, str(e)


def _print_error_body(body):
    if not body:
        return
    try:
        err_json = json.loads(body.decode("utf-8", errors="replace"))
        print(f"   Error: {json.dumps(err_json, indent=2)}")
    except Exception:
        text = body.decode("utf-8", errors="replace")
        print(f"   Error: {text[:200]}")

def test_openrouter():
    key = os.getenv("OPENROUTER_API_KEY")
    # If not in env, check if we can read it from openclaw.json (simulated here by checking known env vars for now)
    # Ideally we should read from config, but for this script let's rely on ENV or ask user to provide it.
    
    # For now, let's assume it might be missing and report it.
    if not key:
        print("⚠️ OPENROUTER_API_KEY not found in .env. Skipping OpenRouter test.")
        return

    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "OpenClaw Diagnostics",
        "Content-Type": "application/json"
    }
    
    # Test 1: DeepSeek V3 via OpenRouter
    test_endpoint(
        "OpenRouter (DeepSeek V3)",
        "https://openrouter.ai/api/v1/chat/completions",
        headers,
        {
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }
    )

    # Test 2: Qwen 2.5 72B via OpenRouter
    test_endpoint(
        "OpenRouter (Qwen 2.5 72B)",
        "https://openrouter.ai/api/v1/chat/completions",
        headers,
        {
            "model": "qwen/qwen-2.5-72b-instruct",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }
    )

def test_deepseek_direct():
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        print("⚠️ DEEPSEEK_API_KEY not found in .env. Skipping DeepSeek Direct test.")
        return

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    test_endpoint(
        "DeepSeek Official API",
        "https://api.deepseek.com/chat/completions",
        headers,
        {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }
    )

def test_local_llm():
    # Assuming config from openclaw.json: http://192.168.1.199:3000/v1
    base_url = "http://192.168.1.199:3000/v1"
    key = "sk-dAtQphrJwsrc3ArIsLA6YtlArhOZckTqliJ8cWCFuIoNITJ3" # From config
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    test_endpoint(
        "Local LLM (GPT-4o Compatible)",
        f"{base_url}/chat/completions",
        headers,
        {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        },
        timeout=5 # Short timeout for local
    )

def main():
    print("🚀 Starting API Connectivity Diagnostics...\n")
    test_deepseek_direct()
    print("-" * 30)
    test_openrouter()
    print("-" * 30)
    test_local_llm()
    print("\n✅ Diagnostics Complete.")

if __name__ == "__main__":
    main()
