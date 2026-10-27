import argparse
import sys

from .adb import AdbError, Tv
from .bloat import BLOAT


def main(argv=None):
    ap = argparse.ArgumentParser(prog="cleanyourtv", description="Чистка Android TV / Google TV от рекламы и мусора по Wi-Fi.")
    ap.add_argument("host", help="IP телевизора, например 192.168.1.50 (порт по умолчанию 5555)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan", help="показать найденный мусор и сторонние приложения")
    c = sub.add_parser("clean", help="удалить найденный мусор (без --apply только показывает)")
    c.add_argument("--apply", action="store_true")
    c.add_argument("--also", nargs="*", default=[], help="доп. пакеты для удаления")
    r = sub.add_parser("restore", help="вернуть удалённые пакеты")
    r.add_argument("packages", nargs="+")
    a = ap.parse_args(argv)

    tv = Tv(a.host)
    try:
        tv.connect()
        if a.cmd == "restore":
            for p in a.packages:
                tv.restore(p)
                print("восстановлен", p)
            return 0
        installed = set(tv.packages())
        found = [p for p in BLOAT if p in installed] + [p for p in a.__dict__.get("also", []) if p in installed]
        if a.cmd == "scan":
            for p in found:
                print(f"{p}  # {BLOAT.get(p, '')}")
            print("\nСторонние приложения:", *tv.packages(third_party=True), sep="\n  ")
            return 0
        if not found:
            print("Мусор не найден.")
            return 0
        for p in found:
            if not a.apply:
                print("удалил бы", p)
                continue
            try:
                tv.remove(p)
                print("удалён", p)
            except AdbError as e:
                print("ошибка:", e, file=sys.stderr)
        if not a.apply:
            print("\nЭто пробный запуск. Добавьте --apply, чтобы удалить.")
    except AdbError as e:
        print("ошибка:", e, file=sys.stderr)
        return 1
    return 0


sys.exit(main())
