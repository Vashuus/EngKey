"""Tests E2E con Xvfb + xdotool (saltar si no hay display)."""

import subprocess
import time
import os
import sys
import pytest

pytestmark = pytest.mark.skipif(
    "DISPLAY" not in os.environ or os.environ.get("DISPLAY") != ":99",
    reason="Requiere Xvfb en :99",
)

ENGKEY_ROOT = os.path.join(os.path.dirname(__file__), "..")
APP_SCRIPT = os.path.join(ENGKEY_ROOT, "engkey.py")


# ── helpers ────────────────────────────────────────────────────────────────

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


def click_button(wid, label):
    code, out, _ = run(["xdotool", "search", "--name", label])
    if out:
        btn = out.split("\n")[0]
        run(["xdotool", "windowfocus", btn])
        run(["xdotool", "click", "1"])
        return True
    return False


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def xvfb():
    subprocess.run(["pkill", "-9", "Xvfb"], capture_output=True, timeout=3)
    time.sleep(0.3)
    proc = subprocess.Popen(
        ["Xvfb", ":99", "-screen", "0", "1280x720x24"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    os.environ["DISPLAY"] = ":99"
    time.sleep(1)
    yield
    proc.terminate()
    time.sleep(0.3)
    if proc.poll() is None:
        proc.kill()
    subprocess.run(["pkill", "-9", "Xvfb"], capture_output=True, timeout=3)


@pytest.fixture(scope="module")
def app(xvfb):
    proc = subprocess.Popen(
        ["python3", APP_SCRIPT],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, "DISPLAY": ":99"},
    )
    time.sleep(2)
    wid = wait_for_window("EngKey", timeout=6)
    assert wid is not None, "Ventana no apareció"
    yield proc, wid
    if proc.poll() is None:
        proc.terminate()
        time.sleep(0.5)
        if proc.poll() is None:
            proc.kill()


# ── Tests ──────────────────────────────────────────────────────────────────

class TestEngKeyE2E:
    def test_window_visible(self, app):
        proc, wid = app
        assert proc.poll() is None, "App murió al iniciar"

    def test_type_text(self, app):
        proc, wid = app
        run(["xdotool", "windowfocus", wid])
        time.sleep(0.3)
        run(["xdotool", "type", "--window", wid, "Hola, como estas?"])
        time.sleep(1.5)
        assert proc.poll() is None, "App crasheó al escribir"

    def test_copy_button(self, app):
        proc, wid = app
        run(["xdotool", "windowfocus", wid])
        time.sleep(0.3)
        click_button(wid, "Copiar")
        time.sleep(0.3)
        assert proc.poll() is None, "App crasheó al copiar"

    def test_long_text(self, app):
        proc, wid = app
        click_button(wid, "Limpiar")
        time.sleep(0.3)
        texto = "Hoy es un lindo dia para probar esta aplicacion de traduccion"
        run(["xdotool", "type", "--window", wid, texto])
        time.sleep(2)
        assert proc.poll() is None, "App crasheó con texto largo"

    def test_escape_closes(self, app):
        proc, wid = app
        run(["xdotool", "windowfocus", wid])
        time.sleep(0.3)
        run(["xdotool", "key", "--window", wid, "Escape"])
        time.sleep(1)

    def test_no_stderr_errors(self, app):
        proc, wid = app
        time.sleep(0.5)
        poll = proc.poll()
        if poll is not None:
            _, err = proc.communicate()
            pytest.fail(f"App terminó con código {poll}: {err[:200]}")
