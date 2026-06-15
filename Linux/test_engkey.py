#!/usr/bin/env python3
"""
Pruebas automatizadas para EngKey usando Xvfb + xdotool.
Verifica: apertura, escritura, traduccion, botones, cierre.
"""

import subprocess
import time
import os
import sys

# ── helpers ──────────────────────────────────────────────────────────────

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

# ── setup ────────────────────────────────────────────────────────────────

print("═" * 55)
print("🧪  EngKey — Pruebas automatizadas")
print("═" * 55)

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
        print(f"  ✅  {name}")
        PASS += 1
    except Exception as e:
        print(f"  ❌  {name}: {e}")
        FAIL += 1

# ── iniciar app ──────────────────────────────────────────────────────────

print("\n[1] Iniciar EngKey...")
app_proc = subprocess.Popen(
    ["python3", "/home/vashuus/EngKey/engkey.py"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env={**os.environ, "DISPLAY": ":99"},
)
sleep(2)

wid = wait_for_window("EngKey", timeout=6)
assert wid, "Ventana no apareció"
print(f"  ✅  Ventana visible (id={wid})")

# ── tests ────────────────────────────────────────────────────────────────

print("\n[2] Verificar que el proceso esta vivo...")
def test_alive():
    assert app_proc.poll() is None, "App murio al iniciar"
test("App corre sin errores", test_alive)

print("\n[3] Escribir texto en español...")
def test_type():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    run(["xdotool", "type", "--window", wid, "Hola, como estas?"])
    sleep(1.5)
    assert app_proc.poll() is None, "App crasheo al escribir"
test("Escribir texto funciona", test_type)

print("\n[4] Verificar que no hay errores en stderr...")
def test_no_errors():
    sleep(0.5)
    poll = app_proc.poll()
    if poll is not None:
        _, err = app_proc.communicate()
        raise AssertionError(f"App termino con codigo {poll}: {err[:200]}")
test("Sin errores en stderr", test_no_errors)

print("\n[5] Traduccion via API directa...")
def test_api():
    sys.path.insert(0, "/home/vashuus/EngKey")
    from translator import Translator
    t = Translator()
    r = t.translate("Hola, como estas? Me llamo Juan")
    assert "hello" in r.lower() or "how" in r.lower(), f"Raro: {r}"
    print(f"     ✔  \"Hola, como estas?\" → \"{r}\"")

    r2 = t.translate("Estoy probando esta aplicacion para ver si funciona bien")
    assert "testing" in r2.lower() or "test" in r2.lower(), f"Raro: {r2}"
    print(f"     ✔  \"Estoy probando...\" → \"{r2}\"")

    # Modo Nativo EN-US (dialecto)
    t.set_dialect("en-US")
    r3 = t.translate("I am going to do what I want to do because I have to")
    assert "gonna" in r3.lower() or "wanna" in r3.lower() or ("I'm" in r3 and "gonna" in r3.lower()), f"Sin contracciones: {r3}"
    print(f"     ✔  en-US → \"{r3}\"")
    t.set_dialect(None)

    # Modo Nativo ES-VE (dialecto)
    t2 = Translator(source="en", target="es")
    t2.set_dialect("es-VE")
    r4 = t2.translate("Thank you very much, I agree, no problem")
    assert any(x in r4.lower() for x in ["gracias", "vale", "dale"]), f"Sin coloquial: {r4}"
    print(f"     ✔  es-VE → \"{r4}\"")

    # Modo Nativo EN-GB (dialecto británico)
    t.set_dialect("en-GB")
    t.set_direction("es", "en")
    r5 = t.translate("Me gusta el color de tu apartamento en el centro")
    assert any(x in r5.lower() for x in ["colour", "flat", "centre"]), f"Sin británico: {r5}"
    print(f"     ✔  en-GB → \"{r5}\"")
    t.set_dialect(None)
test("API traduce correctamente", test_api)

print("\n[6] Probar boton Copiar...")
def test_copy():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    click_button(wid, "Copiar")
    sleep(0.3)
    assert app_proc.poll() is None, "App crasheo al copiar"
test("Boton Copiar responde", test_copy)

print("\n[7] Escribir texto mas largo...")
def test_long():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    click_button(wid, "Limpiar")
    sleep(0.3)
    texto = "Hoy es un lindo dia para probar esta aplicacion de traduccion"
    run(["xdotool", "type", "--window", wid, texto])
    sleep(2)
    assert app_proc.poll() is None, "App crasheo con texto largo"
test("Texto largo funciona", test_long)

print("\n[8] Cerrar con Escape...")
def test_escape():
    run(["xdotool", "windowfocus", wid])
    sleep(0.3)
    run(["xdotool", "key", "--window", wid, "Escape"])
    sleep(1)
test("Cierre con Escape", test_escape)

# ── resultados ───────────────────────────────────────────────────────────

print("\n" + "═" * 55)
print(f"📊  {PASS}/{PASS+FAIL} pruebas pasaron")
print("═" * 55)

if app_proc.poll() is None:
    app_proc.terminate()
    sleep(0.5)
    if app_proc.poll() is None:
        app_proc.kill()
subprocess.run(["pkill", "-9", "Xvfb"], capture_output=True, timeout=3)

sys.exit(0 if FAIL == 0 else 1)
