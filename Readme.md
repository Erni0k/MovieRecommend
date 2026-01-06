# System Rekomendacji Filmów 🎬

Prosty system rekomendacji filmów wykorzystujący content-based filtering (filtrowanie oparte na treści) z danymi z The Movie Database (TMDb).

## Opis projektu

System analizuje gatunki filmów i rok produkcji, aby rekomendować filmy podobne do wybranego tytułu. Wykorzystuje algorytm TF-IDF oraz miarę podobieństwa cosinusowego do znajdowania filmów o podobnych cechach.

Dane filmowe pobierane są z **The Movie Database (TMDb)** - największej społecznościowej bazy filmów z aktualnymi informacjami o milionach filmów i seriali.

## Funkcjonalności

- **Rekomendacje dla filmu** - znajdź filmy podobne do wybranego tytułu
  - 🆕 **Automatyczne wyszukiwanie** - jeśli filmu nie ma w bazie, system automatycznie wyszuka go w TMDb API i doda do bazy
- **Najpopularniejsze filmy** - wyświetl top filmy według ocen
- **Wyszukiwanie według gatunku** - filtruj filmy po gatunku (Drama, Action, Sci-Fi, itd.)
- **Lista wszystkich filmów** - przeglądaj całą bazę danych
- **Automatyczne pobieranie danych** - pobierz najnowsze dane z TMDb API
- **Dynamiczne rozszerzanie bazy** - baza rośnie wraz z użytkowaniem systemu

## Technologie

- Python 3.x
- pandas - przetwarzanie danych
- scikit-learn - TF-IDF i podobieństwo cosinusowe
- requests - komunikacja z TMDb API
- The Movie Database (TMDb) API - źródło danych
- numpy - operacje numeryczne

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu

2. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

3. **Pobierz dane z The Movie Database (TMDb):**

   **Krok 1: Uzyskaj klucz API TMDb (darmowy)**
   - Zarejestruj się na https://www.themoviedb.org/
   - Przejdź do Settings -> API
   - Wygeneruj klucz API (API Key v3)
   
   **Krok 2: Ustaw klucz API**
   ```bash
   # Windows PowerShell
   $env:TMDB_API_KEY="twoj_klucz_api"
   
   # Windows CMD
   set TMDB_API_KEY=twoj_klucz_api
   
   # Linux/Mac
   export TMDB_API_KEY="twoj_klucz_api"
   ```
   
   **Krok 3: Pobierz dane**
   ```bash
   python download_data.py
   ```
   
   Skrypt pobierze najnowsze dane filmowe z TMDb API i automatycznie przetworzy je.
   Dostępne opcje:
   - ~400 filmów (szybkie, zalecane do testów)
   - ~1000 filmów (średnie)
   - ~2000 filmów (duże)
   - Niestandardowa ilość

## Uruchomienie

Uruchom program w terminalu:
```bash
python main.py
```

## Użycie

Po uruchomieniu programu zobaczysz menu z opcjami:

1. **Pokaż rekomendacje dla filmu** - wpisz tytuł filmu (np. "Inception"), a system pokaże podobne filmy
   - 🔥 **NOWOŚĆ**: Jeśli filmu nie ma w lokalnej bazie, system automatycznie wyszuka go w TMDb API i doda do bazy!
   - Wymaga ustawionej zmiennej środowiskowej `TMDB_API_KEY`
2. **Pokaż najpopularniejsze filmy** - wyświetla filmy z najwyższymi ocenami
3. **Szukaj filmów według gatunku** - wpisz gatunek (Drama, Action, Sci-Fi, Crime, etc.)
4. **Wyświetl wszystkie filmy** - pokazuje całą bazę 30 filmów
5. **Wyjście** - zamyka program

## Przykład użycia

### Podstawowe wyszukiwanie
```
Podaj tytuł filmu: Inception
Ile rekomendacji? 5

Rekomendacje:
- Interstellar (Adventure|Drama|Sci-Fi)
- The Matrix (Action|Sci-Fi)
- The Prestige (Drama|Mystery|Sci-Fi)
```

### Automatyczne wyszukiwanie w TMDb API
```
Podaj tytuł filmu: Dune 2024

ℹ️  Film 'Dune 2024' nie został znaleziony w lokalnej bazie.
🔍 Wyszukiwanie 'Dune 2024' w TMDb API...
✅ Znaleziono 15 filmów

📋 Znaleziono wyniki:
  1. Dune: Part Two (2024) - Ocena: 8.2/10
  2. Dune (2021) - Ocena: 7.8/10
  3. Dune (1984) - Ocena: 6.2/10

Wybierz numer filmu (Enter = pierwszy): 1

➕ Dodawanie filmu: Dune: Part Two...
✅ Dodano film do bazy danych (401 filmów)

Rekomendacje dla 'Dune: Part Two':
- Blade Runner 2049 (Sci-Fi|Thriller)
- Arrival (Drama|Sci-Fi)
- Interstellar (Adventure|Drama|Sci-Fi)
```

## Struktura projektu

```
MovieRecomend/
├── main.py              # Główny plik z systemem rekomendacji
├── tmdb_fetcher.py      # Moduł do pobierania danych z TMDb API
├── download_data.py     # Skrypt do pobierania początkowej bazy
├── test_api.py          # Skrypt testowy API
├── requirements.txt     # Zależności projektu
├── Readme.md           # Dokumentacja
├── .env.example        # Szablon konfiguracji
├── .gitignore          # Pliki ignorowane przez git
└── data/
    └── movies.csv      # Baza danych filmów (auto-rozszerzająca się)
```

## Jak działa algorytm?

1. **TF-IDF (Term Frequency-Inverse Document Frequency)** - przekształca gatunki i rok filmu w wektory numeryczne
2. **Cosine Similarity** - oblicza podobieństwo między filmami na podstawie tych wektorów
3. **Ranking** - sortuje filmy według podobieństwa i zwraca top N rekomendacji


