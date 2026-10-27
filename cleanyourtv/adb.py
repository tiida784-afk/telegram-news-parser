"""Thin wrapper over the `adb` binary (Android TV over Wi-Fi)."""
import subprocess

from .bloat import is_protected


class AdbError(RuntimeError):
    pass


def _run(args, runner=subprocess.run):
    try:
        p = runner(["adb", *args], capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        raise AdbError("adb не найден: установите Android platform-tools")
    out = (p.stdout or "") + (p.stderr or "")
    if p.returncode != 0:
        raise AdbError(out.strip() or f"adb {' '.join(args)} завершился с кодом {p.returncode}")
    return out


class Tv:
    def __init__(self, host=None, runner=subprocess.run):
        self.host, self.runner = host, runner

    def _adb(self, *args):
        pre = ["-s", self.host] if self.host else []
        return _run([*pre, *args], self.runner)

    def connect(self):
        if self.host:
            host = self.host if ":" in self.host else f"{self.host}:5555"
            self.host = host
            out = _run(["connect", host], self.runner)
            if "connected" not in out:
                raise AdbError(out.strip())

    def packages(self, third_party=False):
        out = self._adb("shell", "pm", "list", "packages", *(["-3"] if third_party else []))
        return sorted(l.split(":", 1)[1].strip() for l in out.splitlines() if l.startswith("package:"))

    def remove(self, pkg):
        if is_protected(pkg):
            raise AdbError(f"{pkg}: системный пакет, удаление запрещено")
        out = self._adb("shell", "pm", "uninstall", "-k", "--user", "0", pkg)
        if "Success" not in out:
            raise AdbError(f"{pkg}: {out.strip()}")

    def restore(self, pkg):
        out = self._adb("shell", "cmd", "package", "install-existing", pkg)
        if "installed" not in out:
            raise AdbError(f"{pkg}: {out.strip()}")
