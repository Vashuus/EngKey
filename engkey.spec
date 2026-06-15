# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for EngKey portable build (onefile)."""

import os

PROJECT_ROOT = os.getcwd()

a = Analysis(
    [os.path.join(PROJECT_ROOT, "engkey.py")],
    pathex=[PROJECT_ROOT, os.path.join(PROJECT_ROOT, "core")],
    binaries=[],
    datas=[
        (os.path.join(PROJECT_ROOT, "core", "native"), "core/native"),
    ],
    hiddenimports=[
        "deep_translator",
        "deepl",
        "requests",
        "openai",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter.test",
        "unittest",
        "email",
        "http.server",
        "venv",
        "pydoc",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="EngKey",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
