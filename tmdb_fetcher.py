"""
Moduł do pobierania danych filmowych z The Movie Database (TMDb) API
"""

import requests
import pandas as pd
import os
import time
from typing import List, Dict, Optional


class TMDbFetcher:
    """Klasa do pobierania danych z TMDb API"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"  # URL bazowy dla okładek (w500 = szerokość 500px)
    
    def __init__(self, api_key: str):
        """
        Inicjalizacja fetcher'a TMDb
        
        Args:
            api_key: Klucz API z TMDb (możesz go uzyskać za darmo na https://www.themoviedb.org/settings/api)
        """
        self.api_key = api_key
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Wykonuje zapytanie do TMDb API
        
        Args:
            endpoint: Endpoint API (np. '/movie/popular')
            params: Dodatkowe parametry zapytania
            
        Returns:
            Dict z odpowiedzią JSON
        """
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        params['language'] = 'pl-PL'  # Można zmienić na 'en-US'
        
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Błąd podczas zapytania do API: {e}")
            raise
    
    def get_popular_movies(self, pages: int = 10) -> List[Dict]:
        """
        Pobiera popularne filmy
        
        Args:
            pages: Liczba stron do pobrania (1 strona = ~20 filmów)
            
        Returns:
            Lista filmów
        """
        movies = []
        
        print(f"📥 Pobieranie popularnych filmów ({pages} stron)...")
        
        for page in range(1, pages + 1):
            print(f"  Strona {page}/{pages}...", end='\r')
            data = self._make_request('/movie/popular', {'page': page})
            movies.extend(data.get('results', []))
            time.sleep(0.25)  # Aby nie przekroczyć limitu zapytań
        
        print(f"✅ Pobrano {len(movies)} popularnych filmów")
        return movies
    
    def get_top_rated_movies(self, pages: int = 10) -> List[Dict]:
        """
        Pobiera najlepiej oceniane filmy
        
        Args:
            pages: Liczba stron do pobrania
            
        Returns:
            Lista filmów
        """
        movies = []
        
        print(f"📥 Pobieranie najlepiej ocenianych filmów ({pages} stron)...")
        
        for page in range(1, pages + 1):
            print(f"  Strona {page}/{pages}...", end='\r')
            data = self._make_request('/movie/top_rated', {'page': page})
            movies.extend(data.get('results', []))
            time.sleep(0.25)
        
        print(f"✅ Pobrano {len(movies)} najlepiej ocenianych filmów")
        return movies
    
    def get_movie_keywords(self, movie_id: int) -> List[str]:
        """
        Pobiera słowa kluczowe (keywords) dla danego filmu
        
        Args:
            movie_id: ID filmu w TMDb
            
        Returns:
            Lista słów kluczowych
        """
        try:
            data = self._make_request(f'/movie/{movie_id}/keywords')
            keywords = data.get('keywords', [])
            return [kw.get('name', '') for kw in keywords]
        except Exception as e:
            return []
    
    def get_movies_by_genre(self, genre_id: int, pages: int = 5) -> List[Dict]:
        """
        Pobiera filmy według gatunku
        
        Args:
            genre_id: ID gatunku (28=Action, 35=Comedy, 18=Drama, etc.)
            pages: Liczba stron do pobrania
            
        Returns:
            Lista filmów
        """
        movies = []
        
        print(f"📥 Pobieranie filmów gatunku {genre_id} ({pages} stron)...")
        
        for page in range(1, pages + 1):
            print(f"  Strona {page}/{pages}...", end='\r')
            data = self._make_request('/discover/movie', {
                'page': page,
                'with_genres': genre_id,
                'sort_by': 'popularity.desc'
            })
            movies.extend(data.get('results', []))
            time.sleep(0.25)
        
        print(f"✅ Pobrano {len(movies)} filmów")
        return movies
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Pobiera szczegółowe informacje o filmie
        
        Args:
            movie_id: ID filmu w TMDb
            
        Returns:
            Szczegóły filmu
        """
        return self._make_request(f'/movie/{movie_id}')
    
    def get_genre_list(self) -> List[Dict]:
        """
        Pobiera listę dostępnych gatunków
        
        Returns:
            Lista gatunków z ID i nazwami
        """
        data = self._make_request('/genre/movie/list')
        return data.get('genres', [])
    
    def search_movies(self, query: str, pages: int = 3) -> List[Dict]:
        """
        Wyszukuje filmy po tytule
        
        Args:
            query: Fraza do wyszukania
            pages: Liczba stron wyników
            
        Returns:
            Lista znalezionych filmów
        """
        movies = []
        
        print(f"🔍 Wyszukiwanie: '{query}'...")
        
        for page in range(1, pages + 1):
            data = self._make_request('/search/movie', {
                'query': query,
                'page': page
            })
            movies.extend(data.get('results', []))
            time.sleep(0.25)
        
        print(f"✅ Znaleziono {len(movies)} filmów")
        return movies


def process_movies_to_dataframe(movies: List[Dict], fetch_keywords: bool = False, api_key: str = None) -> pd.DataFrame:
    """
    Przetwarza surowe dane filmów z API do DataFrame
    
    Args:
        movies: Lista filmów z API TMDb
        fetch_keywords: Czy pobierać słowa kluczowe (wolniejsze, wymaga dodatkowych zapytań API)
        api_key: Klucz API TMDb (wymagany jeśli fetch_keywords=True)
        
    Returns:
        DataFrame z przetworzonymi filmami
    """
    processed_movies = []
    
    # Inicjalizuj fetcher do pobierania keywords jeśli potrzebne
    fetcher = None
    if fetch_keywords and api_key:
        fetcher = TMDbFetcher(api_key)
    
    total = len(movies)
    for idx, movie in enumerate(movies, 1):
        if fetch_keywords and idx % 50 == 0:
            print(f"  Przetwarzanie z keywords: {idx}/{total}...", end='\r')
        # Pobierz gatunki (genre_ids to lista ID)
        genre_ids = movie.get('genre_ids', [])
        
        # Mapowanie podstawowych ID gatunków
        genre_map = {
            28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy',
            80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family',
            14: 'Fantasy', 36: 'History', 27: 'Horror', 10402: 'Music',
            9648: 'Mystery', 10749: 'Romance', 878: 'Sci-Fi', 10770: 'TV Movie',
            53: 'Thriller', 10752: 'War', 37: 'Western'
        }
        
        genres_list = [genre_map.get(gid, f'Genre{gid}') for gid in genre_ids]
        genres_str = '|'.join(genres_list) if genres_list else 'Unknown'
        
        # Wyodrębnij rok z daty premiery
        release_date = movie.get('release_date', '')
        year = int(release_date.split('-')[0]) if release_date else 0
        
        # Pobierz URL okładki
        poster_path = movie.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
        
        # Pobierz keywords jeśli włączone
        keywords_str = ''
        if fetcher:
            keywords_list = fetcher.get_movie_keywords(movie.get('id'))
            keywords_str = ' '.join(keywords_list) if keywords_list else ''
            time.sleep(0.1)  # Throttle API requests
        
        processed_movies.append({
            'movieId': movie.get('id'),
            'title': f"{movie.get('title', 'Unknown')} ({year})" if year else movie.get('title', 'Unknown'),
            'genres': genres_str,
            'year': year,
            'rating': round(movie.get('vote_average', 0), 2),
            'num_ratings': movie.get('vote_count', 0),
            'popularity': round(movie.get('popularity', 0), 2),
            'overview': movie.get('overview', ''),
            'poster_url': poster_url,
            'keywords': keywords_str
        })
    
    df = pd.DataFrame(processed_movies)
    
    # Usuń duplikaty (ten sam film może być w różnych kategoriach)
    df = df.drop_duplicates(subset=['movieId'], keep='first')
    
    return df


def download_tmdb_data(api_key: str, 
                       num_popular: int = 200,
                       num_top_rated: int = 200,
                       data_dir: str = 'data',
                       output_filename: str = 'movies.csv') -> str:
    """
    Pobiera dane filmów z TMDb i zapisuje do pliku CSV
    
    Args:
        api_key: Klucz API TMDb
        num_popular: Liczba popularnych filmów do pobrania
        num_top_rated: Liczba najlepiej ocenianych filmów
        data_dir: Katalog docelowy
        output_filename: Nazwa pliku wyjściowego
        
    Returns:
        Ścieżka do zapisanego pliku
    """
    print("=" * 70)
    print("POBIERANIE DANYCH Z THE MOVIE DATABASE (TMDb)")
    print("=" * 70)
    
    # Utwórz katalog jeśli nie istnieje
    os.makedirs(data_dir, exist_ok=True)
    
    # Inicjalizacja fetcher'a
    fetcher = TMDbFetcher(api_key)
    
    # Pobierz gatunki
    print("\n📋 Pobieranie listy gatunków...")
    genres = fetcher.get_genre_list()
    print(f"✅ Dostępne gatunki: {', '.join([g['name'] for g in genres[:5]])}...")
    
    all_movies = []
    
    # Pobierz popularne filmy
    pages_popular = (num_popular // 20) + 1
    popular = fetcher.get_popular_movies(pages=pages_popular)
    all_movies.extend(popular)
    
    # Pobierz najlepiej oceniane filmy
    pages_top = (num_top_rated // 20) + 1
    top_rated = fetcher.get_top_rated_movies(pages=pages_top)
    all_movies.extend(top_rated)
    
    # Przetwórz dane
    print("\n🔄 Przetwarzanie danych i pobieranie keywords...")
    df = process_movies_to_dataframe(all_movies, fetch_keywords=True, api_key=api_key)
    df = process_movies_to_dataframe(all_movies)
    
    # Sortuj według popularności
    df = df.sort_values('popularity', ascending=False).reset_index(drop=True)
    
    # Zapisz do pliku
    output_path = os.path.join(data_dir, output_filename)
    df.to_csv(output_path, index=False)
    
    print(f"\n{'=' * 70}")
    print(f"✅ Pobrano i przetworzono {len(df)} unikalnych filmów")
    print(f"✅ Zapisano do: {output_path}")
    print(f"📊 Średnia ocena: {df['rating'].mean():.2f}")
    print(f"📊 Zakres lat: {df['year'].min()}-{df['year'].max()}")
    print("=" * 70)
    
    return output_path


def get_poster_url(poster_path: str, size: str = 'w500') -> str:
    """
    Generuje pełny URL do okładki filmu
    
    Args:
        poster_path: Ścieżka do okładki z API TMDb
        size: Rozmiar okładki (w92, w154, w185, w342, w500, w780, original)
        
    Returns:
        Pełny URL do okładki lub pusty string jeśli brak
    """
    if not poster_path:
        return ''
    return f"https://image.tmdb.org/t/p/{size}{poster_path}"


def load_api_key_from_env() -> Optional[str]:
    """
    Ładuje klucz API z zmiennej środowiskowej TMDB_API_KEY lub pliku .env
    
    Returns:
        Klucz API lub None jeśli nie znaleziono
    """
    # Najpierw sprawdź zmienną środowiskową
    api_key = os.environ.get('TMDB_API_KEY')
    
    # Jeśli nie ma w zmiennej, spróbuj załadować z pliku .env
    if not api_key:
        env_path = '.env'
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('TMDB_API_KEY='):
                            api_key = line.split('=', 1)[1].strip()
                            # Usuń ewentualne cudzysłowy
                            api_key = api_key.strip('"').strip("'")
                            break
            except Exception as e:
                print(f"⚠️  Błąd podczas ładowania .env: {e}")
    
    return api_key
