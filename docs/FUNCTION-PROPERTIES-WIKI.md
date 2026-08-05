# FunctionProperties Wiki Draft

Vorgeschlagener Eintrag fuer die OpenKNX-Wikiseite [FunctionProperties](https://github.com/OpenKNX/OpenKNX/wiki/FunctionProperties).

## ObjectIndex 0xA0 (160)

| PropertyId | Name | Description |
| --- | --- | --- |
| 10 | OFM-IOHomeControl | Pairing-, Status- und Test-Kommandos fuer das io-homecontrol Modul |

## OFM-IOHomeControl

ObjectIndex `0xA0` (160), PropertyId `10`

Das erste Datenbyte ist das Kommando. Kanalnummern sind nullbasiert.

| Kommando | Name | Request | Response | Beschreibung |
| --- | --- | --- | --- | --- |
| `0x10` | StartPairing | `cmd, channel[, nodeIdHi, nodeIdMid, nodeIdLo]` | `status` | Startet das Pairing fuer den Kanal. Die optionale 3-Byte-Node-ID wird fuer 1W-Pairing verwendet. |
| `0x11` | CancelPairing | `cmd` | `status` | Bricht einen laufenden Pairing-Vorgang ab. |
| `0x12` | QueryPairingStatus | `cmd, channel` | `paired, nodeIdHi, nodeIdMid, nodeIdLo, controllerState, lastPairStartStatus` | Liefert Pairing-Status, gepaarte Node-ID und Diagnoseinformationen fuer einen Kanal. |
| `0x13` | UnpairChannel | `cmd, channel` | `status` | Entfernt Pairing und Schluessel des Kanals und speichert den neuen Zustand im Flash. |
| `0x20` | TestSendPosition | `cmd, channel, percent` | `status` | Testkommando zum Senden einer Positionsvorgabe an ein bereits gepaartes Geraet. |

### Statuscodes

| Wert | Bedeutung |
| --- | --- |
| `0x00` | Kommando erfolgreich angenommen oder ausgefuehrt |
| `0x03` | 1W-Pairing abgelehnt, weil keine Ziel-Node-ID uebergeben wurde |
| `0x04` | Pairing-Start abgelehnt, weil der Controller gerade beschaeftigt ist |
| `0xFF` | Ungueltige Anfrage, Kanal ungueltig oder Kommando im aktuellen Zustand nicht moeglich |

### lastPairStartStatus bei `0x12`

| Wert | Bedeutung |
| --- | --- |
| `0` | Letzter Pairing-Start wurde akzeptiert |
| `1` | Letzter Pairing-Start wurde wegen beschaeftigtem Controller blockiert |
| `2` | Letzter 1W-Pairing-Start wurde wegen fehlender Ziel-Node-ID abgelehnt |
| `3` | Allgemeiner Startfehler |