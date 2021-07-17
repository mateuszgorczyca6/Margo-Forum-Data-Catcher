# Margo Forum Data Catcher

Margo Forum Data Catcher to program, który pobiera dane z różnych stron (forum margonem)[https://forum.margonem.pl], przerabia je i umieszcza w pliku excel.

Projekt został stworzony do nauki data-scrappingu.

Dane pobierane są aktualnie z:
+ [ABC Questów](https://forum.margonem.pl/?task=forum&show=posts&id=453382)

Aby zobacyzć log zmian gry wejdź do pliku [CHANGELOG.md](CHANGELOG.md).

Aby samemu zaktualizować plik [test.xlsx](test.xlsx) należy posiadać:
+ Python 3.x ([download link](https://www.python.org/downloads/))
+ moduły:
    + pandas
    + requests
    + bs4

Instalacja modułów w Python odbywa się poprzez wpisanie komendy: `pip install <module> ` lub `pip3 install <module>`.
