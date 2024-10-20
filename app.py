from prompt_toolkit.shortcuts import (radiolist_dialog, 
                                      input_dialog,
                                      message_dialog)
from subprocess import run
import csv


def add_new_connection(displayname: str, fqdn: str):
    """Adds a new line to the file. Creates the file if it doesn't exist"""
    with open("connections.csv", "a", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([fqdn, displayname])

def read_connections():
    """Reads the lines of the file and returns them as a list of lists.
    If the file does not exist, an empty list is returned."""
    try:
        with open("connections.csv") as file:
            reader = csv.reader(file, delimiter=";")
            return [x for x in reader]
    except FileNotFoundError:
        return []

def new_endpoint():
    """Adds a new Endpoint to the csv file."""
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
    """Reads all endpoints from the file. If "other" is selected, a new endpoint can be added. 
    The program then restarts with the new endpoint. If no endpoints exist, "other" is the only option."""
    endpoints = read_connections()
    endpoints.append(["other", "other"])
    # Creates a selection of remote Computers
    result = radiolist_dialog(
        title="Remote Connections",
        text="Wähle ein Endpunkt",
        values=endpoints
    ).run()

    # If 'Cancel' was selected, the program will abort 
    if result == None:
        return

    if result != "other":
        run(["pwsh", "-c", "mstsc", "-v", result])
    else:
        new_endpoint()
        main()


if __name__ == '__main__':
    main()