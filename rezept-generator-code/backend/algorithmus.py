import random
from config import GEWICHT_GESUND, GEWICHT_SOUL, GEWICHT_AUFWAND, GEWICHT_SEASON

def berechne_gewicht(rezept):
    """Berechnet Gewicht eines Rezepts mit konfigurierbaren Faktoren."""
    def to_int(x, default=1):
        try:
            return int(x)
        except:
            return default

    gesundheit = to_int(rezept.get("Gesund (1 bad, 2 neutral, 3 great)"), 2)
    soul = to_int(rezept.get("Soul (1 meh, 2 normal, satisfying)"), 2)
    aufwand = to_int(rezept.get("Aufwand (1 real cooking, 2 quick cooking, 3 just heating)"), 2)
    season = to_int(rezept.get("season (1=spring, 2,3,4)"), 1)

    gewicht = (
        gesundheit * GEWICHT_GESUND +
        soul * GEWICHT_SOUL +
        (4 - aufwand) * GEWICHT_AUFWAND +
        season * GEWICHT_SEASON
    )

    return max(gewicht, 0.1)

def gewichtetes_zufallsrezept(rezepte):
    if not rezepte:
        return {"Rezept Name": "Keine Rezepte vorhanden", "Details": ""}
    gewichte = [berechne_gewicht(r) for r in rezepte]
    return random.choices(rezepte, weights=gewichte, k=1)[0]
