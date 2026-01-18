# 🎬 MovieRecommend - System Rekomendacji Filmów

System rekomendacji filmów z interfejsem webowym Flask i automatycznym pobieraniem danych z TMDb API.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Funkcje

- 🔍 **Inteligentne wyszukiwanie** - wyszukiwanie filmów w bazie danych
- 🎯 **Rekomendacje oparte na treści** - algorytm content-based filtering (TF-IDF + cosine similarity)
- 🧠 **Analiza semantyczna** - używa gatunków i opisów fabuły (overview) do lepszych rekomendacji
- 🎬 **Wybór z wielu wyników** - gdy jest kilka filmów o podobnym tytule, wybierasz w przeglądarce
- 🖼️ **Okładki filmów** - wysokiej jakości obrazy z TMDb
- 🎭 **Przeglądanie według gatunków** - Action, Comedy, Drama, Sci-Fi i więcej
- 📱 **Responsywny design** - działa na desktop i mobile
- ⭐ **Oceny i statystyki** - rating, rok produkcji, popularność

## 🎨 Technologie

- **Backend:** Python, Flask
- **ML:** scikit-learn (TF-IDF, cosine similarity)
- **Data:** pandas, numpy
- **API:** The Movie Database (TMDb)
- **Frontend:** HTML, CSS (responsywne)

## 🚀 Szybki Start

### 1. Wymagania
- Python 3.8 lub nowszy
- Klucz API z TMDb (darmowy)

### 2. Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/Erni0k/MovieRecommend.git
cd MovieRecommend

# Zainstaluj zależności
pip install -r requirements.txt
```

### 3. Konfiguracja API

1. Zarejestruj się na https://www.themoviedb.org/
2. Przejdź do **Settings → API**
3. Wygeneruj klucz API (v3)
4. Utwórz plik `.env`:

```env
TMDB_API_KEY=twoj_klucz_api_tutaj
```

### 4. Pobierz bazę filmów

```bash
python download_data.py
```

Wybierz liczbę filmów:
- **Opcja 1:** ~400 filmów (szybkie, zalecane do testów)
- **Opcja 2:** ~1000 filmów (średnie)
- **Opcja 3:** ~2000 filmów (duże)

**Uwaga:** Pobieranie może trwać 5-10 minut.

### 5. Uruchom aplikację

```bash
# Interfejs webowy (zalecane)
python app.py
```

Otwórz: **http://localhost:5000**

```bash
# Lub interfejs CLI (przestarzały)
python main.py
```

### 6. Analiza parametrów (opcjonalnie)

```bash
python analyze_parameters.py
```

Skrypt wygeneruje szczegółową analizę:
- Parametry TF-IDF
- Wpływ wag gatunków
- Optymalna liczba rekomendacji
- Rozkład podobieństwa
- Korelacja ocen
- Wykresy: `similarity_distribution.png`, `genre_distribution.png`, `rating_correlation.png`

## 📁 Struktura Projektu

```
MovieRecommend/
├── app.py                    # Aplikacja Flask (główna)
├── main.py                   # Interfejs CLI (przestarzały)
├── recommender.py            # Logika rekomendacji (TF-IDF + cosine similarity)
├── tmdb_fetcher.py           # Komunikacja z TMDb API
├── download_data.py          # Pobieranie początkowej bazy danych
├── analyze_parameters.py    # Analiza parametrów systemu rekomendacji (NOWE)
│
├── templates/                # Szablony HTML
│   ├── base.html            # Szablon bazowy
│   ├── index.html           # Strona główna
│   ├── results.html         # Wyniki rekomendacji
│   ├── select_movie.html    # Wybór filmu z wielu wyników (NOWE)
│   ├── genre.html           # Filmy według gatunku
│   └── all_movies.html      # Wszystkie filmy
│
├── static/
│   └── style.css            # Style CSS (responsywne)
│
├── data/
│   └── movies.csv           # Baza danych filmów (gitignore)
│
├── requirements.txt          # Zależności Python
├── .env                      # Klucz API (NIE commituj!)
├── .gitignore               # Pliki ignorowane przez git
└── Readme.md                # Ten plik
```

## 🎮 Użycie

### Interfejs Webowy

1.# Analiza Parametrów

**analyze_parameters.py** - narzędzie do głębokiej analizy systemu:

```bash
python analyze_parameters.py
```

**Co analizuje:**
- ✅ **Parametry TF-IDF** - wpływ max_features na jakość (100, 500, 1000, 5000)
- ✅ **Wagi gatunków** - testowanie różnych wag dla genres vs overview
- ✅ **Liczba rekomendacji** - optymalne n dla różnych filmów
- ✅ **Rozkład podobieństwa** - statystyki macierzy cosine similarity
- ✅ **Wpływ gatunków** - popularność i znaczenie gatunków
- ✅ **Korelacja ocen** - relacja między oceną bazową a rekomendacjami
- ✅ **Ważność cech** - top 20 słów/fraz w TF-IDF

**Wyniki:**
- Raporty w konsoli z detalami każdej analizy
- 3 wykresy PNG: podobieństwo, gatunki, korelacja
- Pomaga w optymalizacji parametrów algorytmu

## **Wyszukiwanie filmu:**
   - Wpisz tytuł filmu (np. "Avatar", "Matrix")
   - Jeśli jest kilka filmów o podobnym tytule, zobaczysz listę do wyboru
   - Wybierz film z listy klikając "Wybierz ten film"
   - Otrzymasz personalizowane rekomendacje

2. **Przeglądanie według gatunku:**
   - Kliknij gatunek w nawigacji
   - Lub przejdź do `/genre/<nazwa>`

3. **Wszystkie filmy:**
   - Kliknij "Wszystkie filmy" w menu
   - Lub przejdź do `/all`

## 🔧 Jak to działa?

### Algorytm Rekomendacji

System używa **content-based filtering** z następującymi cechami:

1. **Cechy filmów:**
   - **Gatunki (podwójna waga)** - Action, Sci-Fi, Drama, etc.
   - **Overview (opis fabuły)** - wyłapuje motywy, klimat, słowa kluczowe
   
2. **TF-IDF Vectorization** - przekształca tekst na wektory numeryczne
   - Nadaje większą wagę rzadkim słowom (np. "dystopia" vs "film")
   - Uwzględnia kontekst semantyczny z opisów

3. **Cosine Similarity** - oblicza podobieństwo między filmami
   - Wartość 0-1 (1 = identyczne)
   - Sortuje filmy według najbardziej podobnych

**Przykład:**
```
Film: "Inception"
Cechy: "Action Sci-Fi Thriller Action Sci-Fi Thriller Dom Cobb is a skilled thief stealing secrets from dreams..."

System poleci:
- Inne filmy o snach, kradzieżach, umysłach
- Filmy Sci-Fi z podobnym klimatem
- Action/Thriller z podobną fabułą
```

### Multi-stage Search

1. **Dokładne dopasowanie** - "Avatar" → "Avatar (2009)"
2. **Częściowe dopasowanie** - "terrifier" → lista: "Terrifier", "Terrifier 2", "Terrifier 3"
3. **Wybór w przeglądarce** - użytkownik wybiera z listy (BRAK input() w konsoli!)
4. **Generowanie rekomendacji** - na podstawie wybranego filmu

### TMDb API

- Automatyczne pobieranie nowych filmów
- Okładki 500px (linki, nie pliki)
matplotlib>=3.5.0         # Do wykresów (analyze_parameters.py)
seaborn>=0.11.0          # Do wizualizacji (analyze_parameters.py)
- Metadane: oceny, opisy, gatunki, rok
- Rate limiting: pauza co 35 zapytań

### Okładki Filmów

**Automatyczne dodawanie** przy:
- Pobieraniu nowej bazy (`download_data.py`)
- Wyszukiwaniu nieznanych filmów (dodawane do CSV z `poster_url`)

URL format: `https://image.tmdb.org/t/p/w500/[poster_path].jpg`

## 📊 API Endpoints

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Strona główna z top 12 filmów |
| `/search` | POST | Wyszukiwanie i rekomendacje (obsługuje `movie_title` i `movie_id`) |
| `/genre/<nazwa>` | GET | Filmy według gatunku |
| `/all` | GET | Wszystkie filmy w bazie |
| `/api/search?q=<query>` | GET | AJAX wyszukiwanie (JSON) |

### Nowe w wersji 2.0:
- `select_movie.html` - szablon do wyboru filmu z wielu wyników
- `get_recommendations_by_id()` - rekomendacje na podstawie ID filmu
- Brak blokowania przez `input()` w konsoli

## ⚙️ Konfiguracja

### requirements.txt

```txt
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
requests>=2.28.0
Flask>=2.3.0
python-dotenv>=1.0.0
matplotlib>=3.5.0         # Do wykresów (analyze_parameters.py)
seaborn>=0.11.0          # Do wizualizacji (analyze_parameters.py)
```

### Zmiana rozmiaru okładek

W `tmdb_fetcher.py`, funkcja `get_poster_url`:

```python
def get_poster_url(poster_path: str, size: str = 'w500') -> str:
    # Dostępne rozmiary: w92, w154, w185, w342, w500, w780, original
```

## 🎨 Personalizacja

### Kolory CSS

W `static/style.css`:

```css
/* Gradient tła */
background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);

/* Akcent */
color: #4ecdc4;

/* Przyciski */
background: linear-gradient(45deg, #ff6b6b, #ff8e53);
```

### Dodanie gatunków do menu

W `templates/base.html`:

```html
<li><a href="/genre/Horror">Horror</a></li>
<li><a href="/genre/Romance">Romans</a></li>
```

## 🔒 Bezpieczeństwo

- ✅ Klucz API w `.env` (nie w kodzie)
- ✅ `.gitignore` chroni `.env`
- ⚠️ **NIGDY** nie commituj `.env` na GitHub

### .gitignore

```
.env
__pycache__/
*.pyc
.venv/
venv/
*.log
```

## 🐛 Rozwiązywanie Problemów

### Brak modułu
```bash
pip install -r requirements.txt
```

### Brak klucza API
```
Ustaw TMDB_API_KEY w pliku .env
```

### Brak pliku movies.csv
```bash
python download_data.py
## 🔬 Dla Zaawansowanych

### Analiza i Optymalizacja

System zawiera narzędzie analityczne **analyze_parameters.py** które pozwala:

1. **Testować różne konfiguracje TF-IDF:**
   ```python
   max_features_options = [100, 500, 1000, 5000, None]
   ```

2. **Eksperymentować z wagami:**
   ```python
   # W recommender.py, metoda _prepare_features()
   genres_doubled = genres + ' ' + genres  # Podwójna waga
   ```

3. **Mierzyć jakość rekomendacji:**
   - Średnia ocena rekomendacji
   - Rozkład podobieństwa
   - Korelacja z filmem bazowym

4. **Wizualizować dane:**
   - Histogramy podobieństwa
   - Rozkład gatunków
   - Scatter plots korelacji

### Przykładowe wyniki analizy:

```
=== ANALIZA PARAMETRÓW TF-IDF ===
Max features: 1000
  - Wymiar macierzy: (1755, 1000)
  - Liczba unikalnych cech: 1000
  - Gęstość macierzy: 0.0523

=== ANALIZA WAG GATUNKÓW ===
Waga gatunków: 2
  Rekomendacje dla 'The Matrix':
    1. The Matrix Reloaded (podobieństwo: 0.8642)
    2. The Matrix Revolutions (podobieństwo: 0.8401)
    ...
```

---



## 📝 Licencja

MIT License - możesz swobodnie używać i modyfikować projekt.

## 👨‍💻 Autor

Stworzony z ❤️ przez [Erni0k](https://github.com/Erni0k)

---

**Enjoy discovering new movies! 🎬🍿**
Skrypty automatycznie ustawiają UTF-8.

## 📈 Wydajność

- **Baza danych:** CSV (~1755+ filmów)
- **Wyszukiwanie:** <100ms
- **Rekomendacje:** <200ms
- **Dodanie filmu z API:** ~0.3s

---

**Wersja:** 1.0.0  
**Ostatnia aktualizacja:** Styczeń 2026


