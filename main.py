import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


class MovieRecommender:
    """Prosty system rekomendacji filmów oparty na content-based filtering"""
    
    def __init__(self, data_path='data/movies.csv'):
        """Inicjalizacja systemu rekomendacji"""
        self.df = pd.read_csv(data_path)
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self._prepare_features()
        
    def _prepare_features(self):
        """Przygotowanie cech do analizy (gatunki + rok)"""
        # Łączenie gatunków i roku w jeden ciąg tekstowy
        self.df['features'] = self.df['genres'].str.replace('|', ' ') + ' ' + self.df['year'].astype(str)
        
        # TF-IDF vectorization
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['features'])
        
        # Obliczenie macierzy podobieństwa
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
    
    def get_recommendations(self, movie_title, n=5):
        # Znajdź indeks filmu
        try:
            idx = self.df[self.df['title'].str.lower() == movie_title.lower()].index[0]
        except IndexError:
            return f"Film '{movie_title}' nie został znaleziony w bazie danych."
        
        # Pobierz podobieństwa dla tego filmu
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sortuj po podobieństwie (malejąco)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Pobierz n najbardziej podobnych filmów (pomijając sam film)
        sim_scores = sim_scores[1:n+1]
        
        # Pobierz indeksy filmów
        movie_indices = [i[0] for i in sim_scores]
        
        # Zwróć rekomendacje
        recommendations = self.df.iloc[movie_indices][['title', 'genres', 'year', 'rating']].copy()
        recommendations['similarity_score'] = [round(score[1], 3) for score in sim_scores]
        
        return recommendations
    
    def get_top_rated(self, n=10):
        """Zwraca najpopularniejsze filmy według oceny"""
        return self.df.nlargest(n, 'rating')[['title', 'genres', 'year', 'rating']]
    
    def search_by_genre(self, genre, n=10):
        """Znajdź filmy według gatunku"""
        mask = self.df['genres'].str.contains(genre, case=False, na=False)
        results = self.df[mask].nlargest(n, 'rating')[['title', 'genres', 'year', 'rating']]
        return results if len(results) > 0 else f"Nie znaleziono filmów w gatunku '{genre}'"
    
    def list_all_movies(self):
        """Wyświetl wszystkie dostępne filmy"""
        return self.df[['title', 'genres', 'year', 'rating']]


def main():
    """Funkcja główna - prosty interfejs CLI"""
    print("=" * 70)
    print("SYSTEM REKOMENDACJI FILMÓW")
    print("=" * 70)
    
    # Inicjalizacja systemu
    try:
        recommender = MovieRecommender()
        print(f"\n✓ Załadowano {len(recommender.df)} filmów do bazy danych\n")
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku data/movies.csv")
        return
    
    while True:
        print("\nWybierz opcję:")
        print("1. Pokaż rekomendacje dla filmu")
        print("2. Pokaż najpopularniejsze filmy")
        print("3. Szukaj filmów według gatunku")
        print("4. Wyświetl wszystkie filmy")
        print("5. Wyjście")
        
        choice = input("\nTwój wybór (1-5): ").strip()
        
        if choice == '1':
            print("\n--- Rekomendacje dla filmu ---")
            movie = input("Podaj tytuł filmu: ").strip()
            
            if not movie:
                print("\n❌ Błąd: Nie podano tytułu filmu.")
                continue
            
            n_input = input("Ile rekomendacji? (domyślnie 5): ").strip()
            
            if n_input == "":
                n = 5
            elif n_input.isdigit() and int(n_input) > 0:
                n = int(n_input)
            else:
                print(f"\n❌ Błąd: '{n_input}' nie jest prawidłową liczbą. Używam wartości domyślnej (5).")
                n = 5
            
            recommendations = recommender.get_recommendations(movie, n)
            
            if isinstance(recommendations, str):
                print(f"\n❌ {recommendations}")
            else:
                print(f"\n🎬 Rekomendacje dla filmu '{movie}':\n")
                print(recommendations.to_string(index=False))
            
        elif choice == '2':
            print("\n--- Najpopularniejsze filmy ---")
            n_input = input("Ile filmów wyświetlić? (domyślnie 10): ").strip()
            
            if n_input == "":
                n = 10
            elif n_input.isdigit() and int(n_input) > 0:
                n = int(n_input)
            else:
                print(f"\n❌ Błąd: '{n_input}' nie jest prawidłową liczbą. Używam wartości domyślnej (10).")
                n = 10
            
            top_movies = recommender.get_top_rated(n)
            print(f"\n🏆 Top {n} filmów:\n")
            print(top_movies.to_string(index=False))
            
        elif choice == '3':
            print("\n--- Szukaj według gatunku ---")
            genre = input("Podaj gatunek (np. Drama, Action, Sci-Fi): ").strip()
            
            if not genre:
                print("\n❌ Błąd: Nie podano gatunku.")
                continue
            
            n_input = input("Ile filmów wyświetlić? (domyślnie 10): ").strip()
            
            if n_input == "":
                n = 10
            elif n_input.isdigit() and int(n_input) > 0:
                n = int(n_input)
            else:
                print(f"\n❌ Błąd: '{n_input}' nie jest prawidłową liczbą. Używam wartości domyślnej (10).")
                n = 10
            
            results = recommender.search_by_genre(genre, n)
            print(f"\n🎭 Filmy w gatunku '{genre}':\n")
            print(results.to_string(index=False) if isinstance(results, pd.DataFrame) else results)
            
        elif choice == '4':
            print("\n--- Wszystkie filmy w bazie ---")
            all_movies = recommender.list_all_movies()
            print(f"\n📚 Lista wszystkich filmów ({len(all_movies)}):\n")
            print(all_movies.to_string(index=False))
            
        elif choice == '5':
            print("\nDo widzenia! 👋")
            break
            
        else:
            print("\n❌ Nieprawidłowy wybór. Wybierz liczbę od 1 do 5.")


if __name__ == "__main__":
    main()
