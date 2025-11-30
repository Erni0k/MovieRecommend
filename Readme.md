# System Rekomendacji Filmów 🎬

Prosty system rekomendacji filmów wykorzystujący content-based filtering (filtrowanie oparte na treści).

## Opis projektu

System analizuje gatunki filmów i rok produkcji, aby rekomendować filmy podobne do wybranego tytułu. Wykorzystuje algorytm TF-IDF oraz miarę podobieństwa cosinusowego do znajdowania filmów o podobnych cechach.

## Funkcjonalności

- **Rekomendacje dla filmu** - znajdź filmy podobne do wybranego tytułu
- **Najpopularniejsze filmy** - wyświetl top filmy według ocen
- **Wyszukiwanie według gatunku** - filtruj filmy po gatunku (Drama, Action, Sci-Fi, itd.)
- **Lista wszystkich filmów** - przeglądaj całą bazę danych

## Technologie

- Python 3.x
- pandas - przetwarzanie danych
- scikit-learn - TF-IDF i podobieństwo cosinusowe
- numpy - operacje numeryczne

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu

2. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

## Uruchomienie

Uruchom program w terminalu:
```bash
python main.py
```

## Użycie

Po uruchomieniu programu zobaczysz menu z opcjami:

1. **Pokaż rekomendacje dla filmu** - wpisz tytuł filmu (np. "Inception"), a system pokaże podobne filmy
2. **Pokaż najpopularniejsze filmy** - wyświetla filmy z najwyższymi ocenami
3. **Szukaj filmów według gatunku** - wpisz gatunek (Drama, Action, Sci-Fi, Crime, etc.)
4. **Wyświetl wszystkie filmy** - pokazuje całą bazę 30 filmów
5. **Wyjście** - zamyka program

## Przykład użycia

```
Podaj tytuł filmu: Inception
Ile rekomendacji? 5

Rekomendacje:
- Interstellar (Adventure|Drama|Sci-Fi)
- The Matrix (Action|Sci-Fi)
- The Prestige (Drama|Mystery|Sci-Fi)
```

## Struktura projektu

```
MovieRecomend/
├── main.py              # Główny plik z systemem rekomendacji
├── requirements.txt     # Zależności projektu
├── Readme.md           # Dokumentacja
└── data/
    └── movies.csv      # Baza danych filmów
```

## Jak działa algorytm?

1. **TF-IDF (Term Frequency-Inverse Document Frequency)** - przekształca gatunki i rok filmu w wektory numeryczne
2. **Cosine Similarity** - oblicza podobieństwo między filmami na podstawie tych wektorów
3. **Ranking** - sortuje filmy według podobieństwa i zwraca top N rekomendacji


