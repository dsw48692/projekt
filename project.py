import argparse
import json
import yaml
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='Konwersja plików XML, JSON i YAML.')

parser.add_argument('input_file', type=str, help='Nazwa pliku wejściowego.')
parser.add_argument('output_file', type=str, help='Nazwa pliku wyjściowego.')

args = parser.parse_args()

input_file_extension = args.input_file.split('.')[-1]
input_file_extension = input_file_extension.lower()

output_file_extension = args.output_file.split('.')[-1]
output_file_extension = output_file_extension.lower()

# Wczytywanie danych

if input_file_extension == 'json':
    try:
        with open(args.input_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Plik nie istnieje.")
        exit(1)
    except json.JSONDecodeError as e:
        print("Błąd składni pliku JSON:")
        print(e)
        exit(1)
elif input_file_extension == 'yaml' or input_file_extension == 'yml':
    try:
        with open(args.input_file, 'r') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print("Plik nie istnieje.")
        exit(1)
    except yaml.YAMLError as e:
        print("Błąd składni pliku YAML:")
        print(e)
        exit(1)
elif input_file_extension == 'xml':
    try:
        tree = ET.parse(args.input_file)
        root = tree.getroot()
        # Przetwarzanie danych XML
        data = {}
        # Przykładowa konwersja XML na słownik
        for child in root:
            data[child.tag] = child.text
    except FileNotFoundError:
        print("Plik nie istnieje.")
        exit(1)
    except ET.ParseError as e:
        print("Błąd składni pliku XML:")
        print(e)
        exit(1)
else:
    print("Nieobsługiwane rozszerzenie pliku.")
    exit(1)

# Przykładowa weryfikacja danych

if data is not None:
    # Wykonaj operacje na wczytanych danych
    print("Dane zostały poprawnie wczytane.")
    print(data)

    # Zapis danych do pliku XML
    if output_file_extension == 'xml':
        try:
            root = ET.Element("data")
            # Przykładowa konwersja słownika na XML
            for key, value in data.items():
                child = ET.Element(key)
                child.text = str(value)
                root.append(child)
            tree = ET.ElementTree(root)
            tree.write(args.output_file, encoding="utf-8", xml_declaration=True)
            print("Dane zostały zapisane do pliku XML.")
        except FileNotFoundError:
            print("Błąd podczas zapisu do pliku.")
            exit(1)
