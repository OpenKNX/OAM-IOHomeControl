# io-homecontrol Anlern- und Debug-Kurzanleitung

Diese Kurzanleitung ist für Anwender mit echter io-homecontrol Hardware. Sie beschreibt, wie Geräte angelernt werden und welche Logs bei Fehlern hilfreich sind.

Die ausführlichere englische Version steht in [PAIRING-DEBUG-GUIDE.md](PAIRING-DEBUG-GUIDE.md).

## Vorbereitung

1. Eine `develop_...` Firmware verwenden, nicht `release_...`.
2. Seriellen Monitor mit `115200` Baud öffnen.
3. In ETS den Zielkanal vorbereiten:
   - richtigen Gerätetyp wählen
   - `2W` oder `1W` wählen
   - bei `1W` die Aktor-Node-ID eintragen
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
7. Nach Abschluss mit `K9 Pairing-Status` oder `iohc status NN` prüfen.

## 1W Anlernen

Wichtige Einschränkung:

- `1W` ist ein Blind-Learn-Verfahren.
- Die Aktor-Node-ID muss vorher bekannt sein.

Schritte:

1. `Protokollmodus` auf `1W` setzen.
2. Die `1W Aktor-Node-ID` in ETS eintragen.
3. `Anlernmodus` auf `Anlernen` setzen.
4. Aktor in Lernmodus versetzen.
5. Anlernen starten:
   - bevorzugt über ETS
   - alternativ mit `iohc pair NN AABBCC`
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

`NN` durch die Kanalnummer ersetzen. Bei `1W` zusätzlich `AABBCC` durch die Aktor-Node-ID ersetzen.

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
iohc pair NN AABBCC
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
iohc pair NN AABBCC
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

## Welche Daten wir brauchen

Bitte mitschicken:

1. Board und Firmware-Umgebung, zum Beispiel `develop_OpenKNX_XIAO_S3_SX1262_IP`
2. Funkbackend: `SX1262` oder `SX1276`
3. Gerätetyp
4. `2W` oder `1W`
5. bei `1W` die verwendete Node-ID
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
   zuerst die Aktor-Node-ID prüfen.