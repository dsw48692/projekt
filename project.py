import argparse
import json
import yaml
import xmltodict

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
        with open(args.input_file, 'r') as file:
            data = xmltodict.parse(file.read())
    except FileNotFoundError:
        print("Plik nie istnieje.")
        exit(1)
    except xmltodict.ExpatError as e:
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
            with open(args.output_file, 'w') as file:
                xmltodict.unparse(data, output=file, pretty=True)
            print("Dane zostały zapisane do pliku XML.")
        except FileNotFoundError:
            print("Błąd podczas zapisu do pliku.")
            exit(1)
