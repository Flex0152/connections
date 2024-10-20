from prompt_toolkit.shortcuts import (radiolist_dialog, 
                                      input_dialog,
                                      message_dialog)
from subprocess import run
import csv


def add_new_connection(displayname: str, fqdn: str):
    """Fügt eine neue Zeile in die Datei ein. Erstellt die Datei, wenn noch nicht vorhanden."""
    with open("connections.csv", "a", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([fqdn, displayname])

def read_connections():
    """Liest alle Zeilen der CSV ein und gibt sie als Liste von Listen zurück.
    Gibt es noch keine csv, wird eine leere Liste zurückgegeben."""
    try:
        with open("connections.csv") as file:
            reader = csv.reader(file, delimiter=";")
            return [x for x in reader]
    except:
        return []

def new_endpoint():
    """Ist der Computer noch nicht in der Auswahl, kann er 
    hier angegeben werden"""
    displayname = input_dialog(
        title="Remote Connections",
        text="Gib den Namen des Endpunkts an"
    ).run()
    fqdn = input_dialog(
        title="Remote Connections",
        text="Gib die Adresse des Endpunkts an"
    ).run()
    add_new_connection(displayname, fqdn)
    message_dialog(
        title="Neuer Endpunkt",
        text="Der neue Endpunkt wurde erstellt."
    ).run()


def main():
    """Liest die connections über die csv ein. Wird der Punkt 'other' gewählt, kann ein
    neuer Endpunkt hinzugefügt werden. Anschließend startet das Programm, mit dem neuen Endpunkt, neu.
    Das Programm endet entweder mit der Wahl eines Endpoints oder über STRG+C."""
    endpoints = read_connections()
    endpoints.append(["other", "other"])
    # Gibt eine Auswahl an Remote Computer
    result = radiolist_dialog(
        title="Remote Connections",
        text="Wähle ein Endpunkt",
        values=endpoints
    ).run()

    if result != "other":
        run(["pwsh", "-c", "mstsc", "-v", result])
    else:
        new_endpoint()
        main()


if __name__ == '__main__':
    main()