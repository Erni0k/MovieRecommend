"""
Moduł zawierający klasę systemu rekomendacji filmów
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from tmdb_fetcher import TMDbFetcher, load_api_key_from_env, process_movies_to_dataframe


class MovieRecommender:
    """Prosty system rekomendacji filmów oparty na content-based filtering"""
    
    def __init__(self, data_path='data/movies.csv', tmdb_api_key=None):
        """Inicjalizacja systemu rekomendacji"""
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
        # Inicjalizacja TMDb API jeśli dostępny klucz
        self.tmdb_fetcher = None
        if tmdb_api_key or load_api_key_from_env():
            try:
                self.tmdb_fetcher = TMDbFetcher(tmdb_api_key or load_api_key_from_env())
                print("✓ Połączono z TMDb API - automatyczne wyszukiwanie włączone")
            except Exception as e:
                print(f"⚠️  TMDb API niedostępne: {e}")
        
        self._prepare_features()
        
    def _prepare_features(self):
        """Przygotowanie cech do analizy (gatunki + overview)"""
        # Podwójna waga dla gatunków + opis fabuły
        genres_doubled = self.df['genres'].str.replace('|', ' ') + ' ' + self.df['genres'].str.replace('|', ' ')
        
        if 'overview' in self.df.columns:
            # Użyj overview - opis fabuły zawiera motywy, klimat, słowa kluczowe
            self.df['features'] = genres_doubled + ' ' + self.df['overview'].fillna('')
        else:
            # Fallback: tylko gatunki
            self.df['features'] = genres_doubled
        
        # TF-IDF vectorization
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['features'])
        
        # Obliczenie macierzy podobieństwa
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
    
    def _search_and_add_movie(self, movie_title):
        """
        Wyszukuje film w TMDb API i dodaje do bazy danych
        Returns: (bool, movie_id) - czy sukces i ID znalezionego filmu
        """
        if not self.tmdb_fetcher:
            return False, None
        
        try:
            print(f"\n🔍 Wyszukiwanie '{movie_title}' w TMDb API...")
            results = self.tmdb_fetcher.search_movies(movie_title, pages=1)
            
            if not results:
                print(f"❌ Nie znaleziono filmu '{movie_title}' w TMDb")
                return False, None
            
            # Pokaż wyniki i pozwól wybrać
            if len(results) > 1:
                print(f"\n📋 Znaleziono {len(results)} wyników:")
                for i, movie in enumerate(results[:5], 1):
                    year = movie.get('release_date', '')[:4] or '?'
                    rating = movie.get('vote_average', 0)
                    print(f"  {i}. {movie['title']} ({year}) - Ocena: {rating}/10")
                
                choice = input("\nWybierz numer filmu (Enter = pierwszy): ").strip()
                idx = int(choice) - 1 if choice.isdigit() and 1 <= int(choice) <= 5 else 0
                selected_movie = results[idx]
            else:
                selected_movie = results[0]
                print(f"  Znaleziono: {selected_movie['title']}")
            
            # Pobierz ID filmu
            movie_id = selected_movie.get('id')
            
            # Sprawdź czy film już nie istnieje (po ID)
            if movie_id and movie_id in self.df['movieId'].values:
                print("ℹ️  Ten film już jest w bazie danych")
                return True, movie_id
            
            # Przetwórz i dodaj film
            print(f"\n➕ Dodawanie filmu: {selected_movie['title']}...")
            api_key = load_api_key_from_env()
            new_movie_df = process_movies_to_dataframe([selected_movie], fetch_keywords=True, api_key=api_key)
            
            # Dodaj do DataFrame
            if not new_movie_df.empty:
                self.df = pd.concat([self.df, new_movie_df], ignore_index=True)
                
                # Zapisz do CSV
                self.df.to_csv(self.data_path, index=False)
                
                # Przebuduj macierz podobieństwa
                self._prepare_features()
                
                print(f"✅ Dodano film do bazy danych ({len(self.df)} filmów)")
                return True, movie_id
            
            return False, None
            
        except Exception as e:
            print(f"❌ Błąd podczas wyszukiwania: {e}")
            import traceback
            traceback.print_exc()
            return False, None
    
    def get_recommendations(self, movie_title, n=5):
        """Generuje rekomendacje dla podanego filmu (wersja webowa - bez input())"""
        # Próba 1: Dokładne dopasowanie tytułu (case-insensitive)
        exact_match = self.df[self.df['title'].str.lower() == movie_title.lower()]
        
        if len(exact_match) > 0:
            # Znaleziono dokładne dopasowanie
            movie_id = exact_match.iloc[0]['movieId']
            return self._get_similar_movies(movie_id, n)
        
        # Próba 2: Częściowe dopasowanie (szukaj frazy w tytule)
        partial_match = self.df[self.df['title'].str.lower().str.contains(movie_title.lower(), regex=False, na=False)]
        
        if len(partial_match) > 1:
            # Wiele dopasowań - zwróć listę do wyboru w przeglądarce
            columns = ['movieId', 'title', 'genres', 'year', 'rating', 'poster_url'] if 'poster_url' in self.df.columns else ['movieId', 'title', 'genres', 'year', 'rating']
            return {
                'type': 'multiple_matches',
                'movies': partial_match[columns].to_dict('records')
            }
        elif len(partial_match) == 1:
            # Jeden film znaleziony
            movie_id = partial_match.iloc[0]['movieId']
            return self._get_similar_movies(movie_id, n)
        
        # Nie znaleziono - sprawdź TMDb API
        if self.tmdb_fetcher:
            success, movie_id = self._search_and_add_movie(movie_title)
            if success and movie_id:
                return self._get_similar_movies(movie_id, n)
            return f"Film '{movie_title}' nie został znaleziony w bazie danych ani w TMDb API."
        
        return f"Film '{movie_title}' nie został znaleziony w bazie danych. Aby włączyć automatyczne wyszukiwanie, ustaw TMDB_API_KEY."
    
    def get_recommendations_by_id(self, movie_id, n=5):
        """Generuje rekomendacje na podstawie ID filmu (po wyborze użytkownika)"""
        return self._get_similar_movies(movie_id, n)
    
    def _get_similar_movies(self, movie_id, n=5):
        """Wewnętrzna metoda do generowania podobnych filmów na podstawie ID"""
        # Znajdź indeks filmu po movieId
        try:
            idx = self.df[self.df['movieId'] == movie_id].index[0]
        except (IndexError, KeyError):
            return f"Film o ID {movie_id} nie został znaleziony w bazie."
        
        # Pobierz podobieństwa dla tego filmu
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sortuj po podobieństwie (malejąco)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Pobierz n najbardziej podobnych filmów (pomijając sam film)
        sim_scores = sim_scores[1:n+1]
        
        # Pobierz indeksy filmów
        movie_indices = [i[0] for i in sim_scores]
        
        # Zwróć rekomendacje
        columns = ['title', 'genres', 'year', 'rating', 'poster_url'] if 'poster_url' in self.df.columns else ['title', 'genres', 'year', 'rating']
        recommendations = self.df.iloc[movie_indices][columns].copy()
        recommendations['similarity_score'] = [round(score[1], 3) for score in sim_scores]
        
        return recommendations
    
    def get_top_rated(self, n=10):
        """Zwraca najpopularniejsze filmy według oceny"""
        columns = ['title', 'genres', 'year', 'rating', 'poster_url'] if 'poster_url' in self.df.columns else ['title', 'genres', 'year', 'rating']
        return self.df.nlargest(n, 'rating')[columns]
    
    def search_by_genre(self, genre, n=10):
        """Znajdź filmy według gatunku"""
        mask = self.df['genres'].str.contains(genre, case=False, na=False)
        columns = ['title', 'genres', 'year', 'rating', 'poster_url'] if 'poster_url' in self.df.columns else ['title', 'genres', 'year', 'rating']
        results = self.df[mask].nlargest(n, 'rating')[columns]
        return results if len(results) > 0 else f"Nie znaleziono filmów w gatunku '{genre}'"
    
    def list_all_movies(self):
        """Wyświetl wszystkie dostępne filmy"""
        columns = ['title', 'genres', 'year', 'rating', 'poster_url'] if 'poster_url' in self.df.columns else ['title', 'genres', 'year', 'rating']
        return self.df[columns]
