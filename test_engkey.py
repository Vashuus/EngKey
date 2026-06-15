#!/usr/bin/env python3
"""
E2E tests for EngKey using Xvfb + xdotool.

DEPRECATED: Use `pytest tests/` instead.
Kept for backward compatibility.
"""

import subprocess
import time
import os
import sys

CORE_DIR = os.path.join(os.path.dirname(__file__), "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))

# ── helpers ──

def run(cmd, timeout=8):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def wait_for_window(name, timeout=8):
    for _ in range(timeout * 5):
        code, out, _ = run(["xdotool", "search", "--name", name])
        if out:
            return out.split("\n")[0]
        time.sleep(0.2)
    return None

def sleep(t=0.4):
    time.sleep(t)

def click_button(wid, label):
    code, out, _ = run(["xdotool", "search", "--name", label])
    if out:
        btn = out.split("\n")[0]
        run(["xdotool", "windowfocus", btn])
        run(["xdotool", "click", "1"])
        return True
    return False

# ── setup ──

print("=" * 55)
print(" EngKey - Automated Tests")
print("=" * 55)

subprocess.run(["pkill", "-9", "Xvfb"], capture_output=True, timeout=3)
sleep(0.3)

xvfb = subprocess.Popen(
    ["Xvfb", ":99", "-screen", "0", "1280x720x24"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
os.environ["DISPLAY"] = ":99"
sleep(1)

PASS, FAIL = 0, 0

def test(name, fn):
    global PASS, FAIL
    try:
        fn()
        print(f"  [PASS] {name}")
        PASS += 1
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        FAIL += 1

# ── launch app ──

print("\n[1] Launch EngKey...")
app_proc = subprocess.Popen(
    ["python3", os.path.join(os.path.dirname(__file__), "engkey.py")],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env={**os.environ, "DISPLAY": ":99"},
)
sleep(2)

wid = wait_for_window("EngKey", timeout=6)
assert wid, "Window did not appear"
print(f"  [PASS] Window visible (id={wid})")

# ── tests ──

print("\n[2] Check process is alive...")
def test_alive():
    assert app_proc.poll() is None, "App died on startup"
test("App runs without errors", test_alive)

print("\n[3] Type text...")
def test_type():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    run(["xdotool", "type", "--window", wid, "Hola, como estas?"])
    sleep(1.5)
    assert app_proc.poll() is None, "App crashed while typing"
test("Typing text works", test_type)

print("\n[4] Check stderr...")
def test_no_errors():
    sleep(0.5)
    poll = app_proc.poll()
    if poll is not None:
        _, err = app_proc.communicate()
        raise AssertionError(f"App exited with code {poll}: {err[:200]}")
test("No errors on stderr", test_no_errors)

print("\n[5] Translation via API...")
def test_api():
    from translator import Translator
    t = Translator()
    r = t.translate("Hola, como estas? Me llamo Juan")
    assert "hello" in r.lower() or "how" in r.lower(), f"Unexpected: {r}"
    print(f'     -> "Hola, como estas?" -> "{r}"')

    r2 = t.translate("Estoy probando esta aplicacion para ver si funciona bien")
    assert "testing" in r2.lower() or "test" in r2.lower(), f"Unexpected: {r2}"
    print(f'     -> "Estoy probando..." -> "{r2}"')

    # Native Mode EN-US
    t.set_dialect("en-US")
    r3 = t.translate("I am going to do what I want to do because I have to")
    assert "gonna" in r3.lower() or "wanna" in r3.lower() or ("I'm" in r3 and "gonna" in r3.lower()), f"No contractions: {r3}"
    print(f'     -> en-US -> "{r3}"')
    t.set_dialect(None)

    # Native Mode ES-VE
    t2 = Translator(source="en", target="es")
    t2.set_dialect("es-VE")
    r4 = t2.translate("Thank you very much, I agree, no problem")
    assert any(x in r4.lower() for x in ["gracias", "vale", "dale"]), f"No colloquial: {r4}"
    print(f'     -> es-VE -> "{r4}"')

    # Native Mode EN-GB
    t.set_dialect("en-GB")
    t.set_direction("es", "en")
    r5 = t.translate("Me gusta el color de tu apartamento en el centro")
    assert any(x in r5.lower() for x in ["colour", "flat", "centre"]), f"No British: {r5}"
    print(f'     -> en-GB -> "{r5}"')
    t.set_dialect(None)
test("API translates correctly", test_api)

print("\n[6] Test Copy button...")
def test_copy():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    click_button(wid, "Copy")
    sleep(0.3)
    assert app_proc.poll() is None, "App crashed on copy"
test("Copy button responds", test_copy)

print("\n[7] Type longer text...")
def test_long():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    click_button(wid, "Clear")
    sleep(0.3)
    texto = "Hoy es un lindo dia para probar esta aplicacion de traduccion"
    run(["xdotool", "type", "--window", wid, texto])
    sleep(2)
    assert app_proc.poll() is None, "App crashed with long text"
test("Long text works", test_long)

print("\n[8] Close with Escape...")
def test_escape():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    run(["xdotool", "key", "--window", wid, "Escape"])
    sleep(1)
test("Close with Escape", test_escape)

# ── results ──

print("\n" + "=" * 55)
print(f" {PASS}/{PASS+FAIL} tests passed")
print("=" * 55)

if app_proc.poll() is None:
    app_proc.terminate()
    sleep(0.5)
    if app_proc.poll() is None:
        app_proc.kill()
subprocess.run(["pkill", "-9", "Xvfb"], capture_output=True, timeout=3)

sys.exit(0 if FAIL == 0 else 1)
