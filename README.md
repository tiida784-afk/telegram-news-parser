# cleanyourtv

Чистит Android TV / Google TV от рекламы и мусорных предустановленных приложений по Wi-Fi через ADB.
Приложения скрываются для пользователя (`pm uninstall -k --user 0`), APK остаётся в системе — всё можно вернуть командой `restore`.

## Подготовка
1. На телевизоре: Настройки → Об устройстве → 7 раз нажать «Сборка» → Параметры разработчика → включить «Отладка по USB/сети».
2. На компьютере: установить [platform-tools](https://developer.android.com/tools/releases/platform-tools) (команда `adb`) и Python 3.8+.
3. Телевизор и компьютер в одной Wi-Fi сети; при первом подключении подтвердить запрос на ТВ.

## Использование
```
python -m cleanyourtv 192.168.1.50 scan            # что найдено
python -m cleanyourtv 192.168.1.50 clean           # пробный запуск
python -m cleanyourtv 192.168.1.50 clean --apply   # удалить
python -m cleanyourtv 192.168.1.50 clean --apply --also com.example.app
python -m cleanyourtv 192.168.1.50 restore com.netflix.ninja
```
Список мусора — `cleanyourtv/bloat.py`; лаунчер, Play Store, GMS и системные пакеты защищены от удаления.

## Тесты
```
pip install pytest && pytest
```
