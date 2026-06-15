"""Runtime environment detection - X11, Wayland, desktop environment."""

import os
import subprocess


def detect() -> dict:
    """Detect display server, desktop environment, and windowing capabilities.

    Returns a dict with environment info for adapting app behavior.
    """
    session_type = os.environ.get("XDG_SESSION_TYPE", "")
    wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
    display = os.environ.get("DISPLAY", "")
    desktop = os.environ.get(
        "XDG_CURRENT_DESKTOP",
        os.environ.get("DESKTOP_SESSION", "unknown"),
    )

    # Determine display server
    is_wayland = bool(wayland_display) or session_type == "wayland"
    is_x11 = bool(display) or session_type == "x11"
    is_tty = not display and not wayland_display

    # XWayland: Wayland compositor providing X11 compatibility
    has_xwayland = is_wayland and bool(display) and _xwayland_running()

    # Desktop environment normalization
    de = desktop.lower()
    is_gnome = "gnome" in de
    is_kde = "kde" in de or "plasma" in de
    is_sway = "sway" in de
    is_hyprland = "hyprland" in de
    is_i3 = "i3" in de
    is_xfce = "xfce" in de
    is_cinnamon = "cinnamon" in de
    is_mate = "mate" in de
    is_wlroots = is_sway or is_hyprland or "wlroots" in de

    return {
        "session_type": session_type or "unknown",
        "desktop": desktop,
        "display": display or "",
        "wayland_display": wayland_display or "",
        "is_wayland": is_wayland,
        "is_x11": is_x11,
        "is_tty": is_tty,
        "has_xwayland": has_xwayland,
        "x11_available": is_x11 or has_xwayland,
        "de": de,
        "is_gnome": is_gnome,
        "is_kde": is_kde,
        "is_sway": is_sway,
        "is_hyprland": is_hyprland,
        "is_i3": is_i3,
        "is_xfce": is_xfce,
        "is_cinnamon": is_cinnamon,
        "is_mate": is_mate,
        "is_wlroots": is_wlroots,
        "topmost_reliable": _topmost_reliable(
            is_wayland, has_xwayland, is_gnome, is_kde, is_sway, is_hyprland
        ),
    }


def _xwayland_running() -> bool:
    """Check if XWayland is active."""
    try:
        result = subprocess.run(
            ["xset", "-q"],
            capture_output=True,
            timeout=2,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _topmost_reliable(
    is_wayland: bool,
    has_xwayland: bool,
    is_gnome: bool,
    is_kde: bool,
    is_sway: bool,
    is_hyprland: bool,
) -> str:
    """Determine reliability of always-on-top window hint.

    Returns one of: "reliable", "partial", "unreliable", "unknown".
    """
    if not is_wayland:
        return "reliable"

    if not has_xwayland:
        return "unreliable"

    # Wayland + XWayland - depends on compositor
    if is_gnome:
        # Mutter used to strip -topmost from XWayland; newer versions respect it
        return "partial"
    if is_kde or is_sway or is_hyprland:
        return "reliable"

    return "partial"


def print_summary(env: dict):
    """Print a human-readable environment summary (for --debug)."""
    print(f"Display server:  {'Wayland' if env['is_wayland'] else 'X11' if env['is_x11'] else 'none'}")
    print(f"Desktop:         {env['desktop']}")
    print(f"DISPLAY:         {env['display']}")
    print(f"WAYLAND_DISPLAY: {env['wayland_display']}")
    print(f"XWayland:        {'yes' if env['has_xwayland'] else 'no'}")
    print(f"Topmost hint:    {env['topmost_reliable']}")
