"""Known removable packages on Android TV / Google TV.

Removal is `pm uninstall -k --user 0`: the app is hidden for the user, the APK stays
on the system partition, so it can be brought back with `restore`.
Never put launcher, Play Store, GMS, settings or system UI packages here.
"""

BLOAT = {
    # Google apps nobody asked for
    "com.google.android.videos": "Google TV (фильмы)",
    "com.google.android.play.games": "Play Игры",
    "com.google.android.youtube.tvmusic": "YouTube Music",
    "com.google.android.youtube.tvunplugged": "YouTube TV",
    "com.google.android.feedback": "Отправка отзывов",
    "com.google.android.tv.bugreportsender": "Отчёты об ошибках",
    "com.google.android.leanbacklauncher.recommendations": "Рекомендации лаунчера",
    # preinstalled streaming / partner apps
    "com.netflix.ninja": "Netflix",
    "com.amazon.amazonvideo.livingroom": "Prime Video",
    "com.disney.disneyplus": "Disney+",
    "com.spotify.tv.android": "Spotify",
    "com.apple.atve.androidtv.appletv": "Apple TV",
    "com.hbo.hbonow": "HBO",
}

# Packages `clean` refuses to touch even if asked.
PROTECTED = (
    "com.android.", "com.google.android.gms", "com.google.android.gsf",
    "com.android.vending", "com.google.android.tvlauncher",
    "com.google.android.apps.tv.launcherx", "com.google.android.tvrecommendations",
    "com.google.android.inputmethod", "com.google.android.permissioncontroller",
    "com.google.android.webview", "com.google.android.tv.remote",
)


def is_protected(pkg: str) -> bool:
    return pkg.startswith(PROTECTED)
