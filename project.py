import argparse

# Tworzenie parsera
parser = argparse.ArgumentParser(description='Opis programu')

# Dodawanie argumentów
parser.add_argument('-f', '--file', help='Ścieżka do pliku')
parser.add_argument('-v', '--verbose', action='store_true', help='Tryb szczegółowy')

# Parsowanie argumentów
args = parser.parse_args()

# Przykładowe użycie argumentów
if args.file:
    print('Ścieżka do pliku:', args.file)

if args.verbose:
    print('Tryb szczegółowy jest włączony')
