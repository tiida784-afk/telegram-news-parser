from types import SimpleNamespace

import pytest

from cleanyourtv.adb import AdbError, Tv


def fake(outputs):
    calls = []

    def run(cmd, **kw):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout=outputs(cmd), stderr="")

    return run, calls


def test_packages_parsed():
    run, _ = fake(lambda c: "package:com.a\npackage:com.b\n")
    assert Tv("1.2.3.4:5555", run).packages() == ["com.a", "com.b"]


def test_remove_uses_user0_keep_data():
    run, calls = fake(lambda c: "Success")
    Tv("h", run).remove("com.netflix.ninja")
    assert calls[0][-5:] == ["uninstall", "-k", "--user", "0", "com.netflix.ninja"]


def test_protected_refused():
    run, calls = fake(lambda c: "Success")
    with pytest.raises(AdbError):
        Tv("h", run).remove("com.google.android.gms")
    assert not calls


def test_connect_adds_port():
    run, calls = fake(lambda c: "connected to 1.2.3.4:5555")
    tv = Tv("1.2.3.4", run)
    tv.connect()
    assert calls[0] == ["adb", "connect", "1.2.3.4:5555"]
