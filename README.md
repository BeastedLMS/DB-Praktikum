# DB-Praktikum
Web-Anwendung mit SQLite Datenbank
## Checkliste für DB-Praktikum

### 1. Projektübersicht
- [x] **Projektname**: Lieferspatz
- [x] **Beschreibung**: Eine vereinfachte Plattform für die Lieferung von Speisen und Getränken.
- [x] **Ziel**: Implementierung einer Webanwendung zur Bestellung von Essen bei verschiedenen Restaurants.

### 2. Gruppeninformationen
- [x] **Gruppenmitglieder**: Namen und Matrikelnummern auflisten.
- [x] **Gruppennummer**: Gruppennummer angeben.

### 3. Projektphasen
- [x] **Phase 1**: Konzeptpapier  https://uniduede-my.sharepoint.com/:w:/r/personal/sven_heimbach_stud_uni-due_de/_layouts/15/Doc.aspx?sourcedoc=%7BBFFCD01A-4E9A-4DD2-BC43-5B406BC17604%7D&file=Konzeptpapier.docx
  - [x] Software-Architektur
  - [x] Datenbankdesign
  - [x] UI-Mockups
- [ ] **Phase 2**: Implementierung
  - [ ] Entwicklung der Webanwendung
  - [ ] Datenbankintegration

### 4. Fristen
- [x] **Gruppenanmeldung**: 18.11, 23:59 Uhr
- [x] **Abgabe des Konzeptpapiers**: 02.12, 23:59 Uhr
- [ ] **Mündliche Prüfungen**: Ende der Vorlesungszeit/Anfang der vorlesungsfreien Zeit 29.01 16 Uhr

### 5. Funktionale Anforderungen
- [ ] **Funktionen für Restaurants**:
  - [x] Geschäftskonto erstellen
  - [ ] Menüeinträge verwalten
  - [ ] Öffnungszeiten und Lieferadius festlegen
  - [ ] Bestellbenachrichtigungen
  - [ ] Bestellhistorie einsehen
- [ ] **Funktionen für Kunden**:
  - [x] Kundenkonto erstellen
  - [ ] Restaurants durchsuchen
  - [ ] Bestellungen aufgeben
  - [ ] Bestellstatus einsehen
  - [ ] Bestellhistorie einsehen

### 6. Bezahlsystem
- [ ] **Startguthaben**: 100€ für Neukunden
- [ ] **Umsatzverteilung**: 15% an Lieferspatz, 85% an Restaurants
- [ ] **Guthabenverwaltung**: Aktuelles Guthaben für Kunden und Restaurants einsehbar

### 7. Technische Anforderungen
- [x] **Datenbank**: SQLite (serverseitig)
- [x] **Webanwendung**: Lokales Hosting, empfohlene Frameworks (Flask, Django, etc.)
- [ ] **Beispieldaten**:
  - [ ] 10 Restaurants mit je 10 Items
  - [ ] 5 Kunden mit je 2 abgeschlossenen Bestellungen

### 8. Prüfungsvorbereitung
- [x] **Mockups**: UI-Mockups für wichtige Szenarien erstellen
- [ ] **Codeverständnis**: Sicherstellen, dass alle Gruppenmitglieder den Code verstehen und Fragen beantworten können

### 9. Unterstützung und Ressourcen
- [ ] **Wöchentliche Sprechstunden**: Freitags 14-16 Uhr, LE 104
- [ ] **Moodle-Forum**: https://moodle.uni-due.de/course/view.php?id=47891


Tabellen:
menue: {name, price, image, restaurantEmail}  **DONE**
bestellung: {liste:items, gesamtpreis, status, lieferadresse, datum, zeit, Restaurant.name}   
restaurant: {lieferadius(liste von Postleihzahlen), Guthaben}
        Nach Recherche hat sich ergeben das eine eigene Tabelle für den Lieferadius anbietet:
        delivery_areas: {id(primärschlüssel, autoincrement), restaurant_email(fremdschlüssel), postleitzahl(welche vom restaurant beliefert wird(für jede beliefrte eine Zeile))}
oeffnungszeiten: {Mo(00:00 Uhr), Di, ...., So }

Fatima Settingsseite und Startseite = Bestellungsseite
