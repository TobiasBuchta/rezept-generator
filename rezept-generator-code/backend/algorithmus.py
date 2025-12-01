# algorithmus.py
import random

def berechne_gewicht(rezept):
    """
    Berechnet ein Gesamtgewicht für ein Rezept.
    Je höher das Gewicht, desto höher die Wahrscheinlichkeit für Auswahl.
    """

    # Werte aus CSV kommen als Strings → sicher konvertieren
    def to_int(x, default=1):
        try:
            return int(x)
        except:
            return default

    # Einzelwerte extrahieren (Falls CSv andere Header hat, hier in der Klammer anpassen)

    gesundheit = to_int(rezept.get("Gesund (1 bad, 2 neutral, 3 great)"), 2)
    soul = to_int(rezept.get("Soul (1 meh, 2 normal, satisfying)"), 2)
    aufwand = to_int(rezept.get("Aufwand (1 real cooking, 2 quick cooking, 3just heating)"), 2)
    season = to_int(rezept.get("season (1=spring, 2,3,4)"), 1)

    # Beispiel-Gewichtung:
    # Mehr Gesundheit = besser
    # Mehr Soul = besser
    # Weniger Aufwand = besser (also invertieren)
    # Season derzeit neutral (kannst du verbessern)

    gewicht = (
        gesundheit * 2 +
        soul * 1.5 +
        (4 - aufwand) * 1.2 +  # invertiert: Aufwand 1 = bester Wert
        season * 0.5           # aktuell wenig Einfluss
    )

    return max(gewicht, 0.1)  # niemals 0 zurückgeben


def gewichtetes_zufallsrezept(rezepte):
    """
    Wählt ein Rezept aus, proportional zum Gewicht.
    Nutzt random.choices (Python's weighted choice)
    """
    if not rezepte:
        return None

    gewichte = [berechne_gewicht(r) for r in rezepte]
    return random.choices(rezepte, weights=gewichte, k=1)[0]
