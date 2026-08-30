# io-homecontrol Anlern- und Debug-Kurzanleitung

Diese Kurzanleitung ist für Anwender mit echter io-homecontrol Hardware. Sie beschreibt, wie Geräte angelernt werden und welche Logs bei Fehlern hilfreich sind.

Die ausführlichere englische Version steht in [PAIRING-DEBUG-GUIDE.md](PAIRING-DEBUG-GUIDE.md).

## Vorbereitung

1. Eine `develop_...` Firmware verwenden, nicht `release_...`.
2. Seriellen Monitor mit `115200` Baud öffnen.
3. In ETS den Zielkanal vorbereiten:
   - richtigen Gerätetyp wählen
   - `2W` oder `1W` wählen
   - bei `1W` Broadcast-/Geräteklasse und Controller-Profil wählen
4. Das Zielgerät während des Anlernens in die Nähe des Gateways bringen.

## 2W Anlernen

1. In ETS den Kanal öffnen.
2. `Protokollmodus` auf `2W` setzen.
3. `Anlernmodus` auf `Anlernen` setzen.
4. Das io-homecontrol Gerät in den herstellerspezifischen Lernmodus versetzen.
5. Anlernen starten:
   - bevorzugt über die ETS-Online-Aktion
   - alternativ über die serielle Konsole mit `iohc pair NN`
6. In einem `develop` Build sollte sofort eine serielle Meldung wie `ETS: pairing started for channel N` erscheinen.
   `iohc pairdiag status` zeigt zusätzlich ein strukturiertes Ergebnis:
   - `no-response`: keine passende Geräteantwort; Lernmodus, Stromversorgung, Reichweite und Funkkanal prüfen.
   - `invalid-response`: ein Frame kam an, passte aber nicht zu Peer, Ziel oder Phase; Gerät und Controller-Identität prüfen.
   - `key-exchange-failure`: Discovery war erfolgreich, aber `0x31/0x3C/0x32/0x33` hat sein Retry-Budget verbraucht; Aktor wach und im Lernmodus halten und erneut versuchen.
   - `configuration-failure`: der Schlüssel wurde gespeichert, die optionale Statuskonfiguration aber nicht abgeschlossen. Danach eine normale Gerätefunktion prüfen.
7. Nach Abschluss mit `K9 Pairing-Status` oder `iohc status NN` prüfen.

## 1W Anlernen

Wichtige Einschränkung:

- `1W` ist ein Blind-Learn-Verfahren.
- Normales `1W`-Anlernen ist klassenadressiert; die Aktor-Node-ID wird nicht übertragen und ist nur optionale Diagnose-Metadaten.
- Die passende Broadcast-/Geräteklasse wählen. Eine falsche Klasse wirkt wie ein fehlgeschlagenes Blind-Anlernen.
- Die Standardsequenz ist authentifiziertes Self-Remove `0x39`, danach Add/Send-Key `0x30` (`remove-add`). `announce-add` bleibt nur ein expliziter Diagnose-Fallback.
- Ein Controller-Profil enthält Remote-Node-ID, Schlüssel, Hersteller und einen monotonen Sequenzzähler. Das Profil dauerhaft speichern; ein zurückgesetzter Zähler kann eine funktionierende Fernbedienung ungültig erscheinen lassen.
- Ein neues Profil lernt eine neue virtuelle Fernbedienung an. Klonen übernimmt dagegen gezielt die Identität einer vorhandenen Fernbedienung aus deren `0x30` SendKey-Frame. Nur eigene Fernbedienungen klonen.
- Manche Fernbedienungen hängen an `0x30` einen optionalen MAC-Trailer an. Die ETS-Option `1W Anmeldung mit MAC-Anhang (0x30)` nur aktivieren, wenn die Gerätefamilie ihn benötigt. Niemals `0x30`-Mitschnitte, Controller- oder extrahierte Schlüssel veröffentlichen.

Schritte:

1. `Protokollmodus` auf `1W` setzen.
2. Controller-Identität/Schlüssel und passende Broadcast-/Geräteklasse konfigurieren. Eine beobachtete Aktor-ID ist kein Erfolgsnachweis.
3. `Anlernmodus` auf `Anlernen` setzen.
4. Aktor in Lernmodus versetzen.
5. Anlernen starten:
   - bevorzugt über ETS
   - alternativ mit der kanal-ersten Syntax `iohcNN pair1w remove-add` (Standard), `iohcNN pair1w add-only`, `iohcNN pair1w announce-add`, `iohcNN pair1w announce-only` oder `iohcNN pair1w remove`
6. In einem `develop` Build sollte sofort eine serielle Meldung wie `ETS: 1W pairing started for channel N` erscheinen.
7. Danach immer mit einer echten Gerätefunktion prüfen.

## Schneller Vorabcheck

Vor dem Anlernen zuerst prüfen:

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
```

Gut ist:

- `iohc radio` zeigt `init=1`
- `iohc radio txtest` zeigt `done=1`
- `iohc radio sweep 3` endet ohne Timeouts

## Copy-Paste Blöcke

`NN` durch die Kanalnummer ersetzen. Ein `1W`-Controller ist klassenadressiert; eine optionale beobachtete Aktor-ID ist nur Diagnose-Metadaten.

### SX1262

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN
iohc status NN
iohc radio
```

Für `1W` auf SX1262:

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohcNN pair1w remove-add
iohc status NN
iohc radio
```

### SX1276

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohc pair NN
iohc status NN
iohc radio
```

Für `1W` auf SX1276:

```text
iohc status
iohc radio
iohc radio raw
iohc radio txtest
iohc radio sweep 3
iohc pairdiag on
iohcNN pair1w remove-add
iohc status NN
iohc radio
```

Wenn das Anlernen nicht funktioniert, zusätzlich:

```text
iohc discover
iohc discover spe
iohc scan start
iohc scan stop
iohc scan dump
iohc scan stats
```

## RS100: leiser Betrieb

Für einen Somfy RS100 im `2W`-Kanal die ETS-Kanaloption `Somfy RS100: leiser Betrieb` aktivieren. Positions- und Favoritbefehle verwenden dann den beobachteten `Execute`-Profilwert `0x05` statt `0x06`. Stopp-, Lüftungs- und Lamellenframes bleiben bewusst unverändert, weil dafür keine verifizierte RS100-Referenz vorliegt.

## Welche Daten wir brauchen

Bitte mitschicken:

1. Board und Firmware-Umgebung, zum Beispiel `develop_OpenKNX_XIAO_S3_SX1262_IP`
2. Funkbackend: `SX1262` oder `SX1276`
3. Gerätetyp
4. `2W` oder `1W`
5. bei `1W` die gewählte Broadcast-/Geräteklasse und Controller-Identität (niemals extrahierte Schlüssel veröffentlichen)
6. die genau verwendeten Konsolenbefehle
7. den kompletten seriellen Log von Boot bis Fehler
8. ob das echte Gerät überhaupt reagiert hat
9. wenn möglich die relevanten ETS-Parameter des Kanals

## Wichtige Interpretation

1. `radio txtest` und `radio sweep 3` funktionieren, aber `pair` nicht:
   wahrscheinlich kein grundlegendes Funkproblem, eher Learn-Mode, Pairing-Ablauf oder Authentifizierung.
2. `discover` sieht Geräte, aber `pair` scheitert:
   RX-Pfad arbeitet wahrscheinlich, Problem eher höher im Protokoll.
3. `1W` reagiert gar nicht:
   zuerst Learn-Mode, Controller-Identität und Broadcast-/Geräteklasse prüfen.
