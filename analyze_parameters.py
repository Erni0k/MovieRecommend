"""
Narzędzie do analizy parametrów zarządzających systemem rekomendacji
"""

import pandas as pd
import numpy as np
from recommender import MovieRecommender
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
import os

class ParameterAnalyzer:
    """Analiza parametrów systemu rekomendacji"""
    
    def __init__(self):
        # Zmień katalog roboczy na katalog skryptu
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        self.recommender = MovieRecommender()
        self.df = self.recommender.df
        
    def analyze_tfidf_parameters(self):
        """Analiza parametrów TF-IDF"""
        print("\n=== ANALIZA PARAMETRÓW TF-IDF ===\n")
        
        # Test różnych konfiguracji max_features
        max_features_options = [100, 500, 1000, 5000, None]
        
        for max_feat in max_features_options:
            features = self.df['genres'].fillna('') + ' ' + self.df['genres'].fillna('')
            
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=max_feat
            )
            
            tfidf_matrix = vectorizer.fit_transform(features)
            
            print(f"Max features: {max_feat}")
            print(f"  - Wymiar macierzy: {tfidf_matrix.shape}")
            print(f"  - Liczba unikalnych cech: {len(vectorizer.get_feature_names_out())}")
            print(f"  - Gęstość macierzy: {tfidf_matrix.nnz / (tfidf_matrix.shape[0] * tfidf_matrix.shape[1]):.4f}")
            print()
    
    def analyze_genre_weights(self):
        """Analiza wpływu wag gatunków"""
        print("\n=== ANALIZA WAG GATUNKÓW ===\n")
        
        # Spróbuj znaleźć film testowy, jeśli nie istnieje - użyj pierwszego z bazy
        test_movie_candidates = ["Toy Story", "The Matrix", "Inception"]
        test_movie = None
        
        for candidate in test_movie_candidates:
            if not self.df[self.df['title'] == candidate].empty:
                test_movie = candidate
                break
        
        if test_movie is None:
            # Użyj pierwszego filmu z bazy
            test_movie = self.df.iloc[0]['title']
        
        weight_options = [1, 2, 3, 5, 10]
        
        for weight in weight_options:
            # Symulacja różnych wag
            features = (self.df['genres'].fillna('') + ' ') * weight + \
                       self.df['overview'].fillna('')
            
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(features)
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
            
            # Znajdź film testowy
            idx = self.df[self.df['title'] == test_movie].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
            
            print(f"Waga gatunków: {weight}")
            print(f"  Rekomendacje dla '{test_movie}':")
            for i, (movie_idx, score) in enumerate(sim_scores, 1):
                print(f"    {i}. {self.df.iloc[movie_idx]['title']} (podobieństwo: {score:.4f})")
            print()
    
    def analyze_recommendation_count(self):
        """Analiza optymalnej liczby rekomendacji"""
        print("\n=== ANALIZA LICZBY REKOMENDACJI ===\n")
        
        # Znajdź filmy testowe, które faktycznie istnieją w bazie
        test_movies_candidates = ["Toy Story", "The Matrix", "Inception", "Avatar", "Titanic"]
        test_movies = []
        
        for candidate in test_movies_candidates:
            if not self.df[self.df['title'] == candidate].empty:
                test_movies.append(candidate)
                if len(test_movies) >= 3:
                    break
        
        # Jeśli nie znaleziono żadnego z kandydatów, użyj pierwszych 3 z bazy
        if len(test_movies) == 0:
            test_movies = self.df['title'].head(3).tolist()
        
        n_options = [3, 5, 10, 15, 20]
        
        for movie in test_movies:
            print(f"\nFilm: {movie}")
            for n in n_options:
                recommendations = self.recommender.get_recommendations(movie, n)
                if isinstance(recommendations, pd.DataFrame):
                    avg_rating = recommendations['rating'].mean()
                    print(f"  n={n:2d}: Średnia ocena rekomendacji: {avg_rating:.2f}")
    
    def analyze_similarity_distribution(self):
        """Analiza rozkładu podobieństwa"""
        print("\n=== ANALIZA ROZKŁADU PODOBIEŃSTWA ===\n")
        
        # Pobierz macierz podobieństwa
        cosine_sim = self.recommender.cosine_sim
        
        # Statystyki
        upper_triangle = cosine_sim[np.triu_indices_from(cosine_sim, k=1)]
        
        print(f"Średnie podobieństwo: {upper_triangle.mean():.4f}")
        print(f"Mediana podobieństwa: {np.median(upper_triangle):.4f}")
        print(f"Odchylenie standardowe: {upper_triangle.std():.4f}")
        print(f"Min podobieństwo: {upper_triangle.min():.4f}")
        print(f"Max podobieństwo: {upper_triangle.max():.4f}")
        
        # Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(upper_triangle, bins=50, edgecolor='black')
        plt.title('Rozkład wartości podobieństwa między filmami')
        plt.xlabel('Cosine Similarity')
        plt.ylabel('Liczba par filmów')
        plt.grid(True, alpha=0.3)
        plt.savefig('similarity_distribution.png', dpi=300, bbox_inches='tight')
        print("\n✓ Wykres zapisany jako 'similarity_distribution.png'")
    
    def analyze_genre_impact(self):
        """Analiza wpływu gatunków na rekomendacje"""
        print("\n=== ANALIZA WPŁYWU GATUNKÓW ===\n")
        
        # Zlicz gatunki
        all_genres = []
        for genres in self.df['genres'].dropna():
            all_genres.extend(genres.split('|'))
        
        genre_counts = pd.Series(all_genres).value_counts()
        
        print("Top 10 najpopularniejszych gatunków:")
        for i, (genre, count) in enumerate(genre_counts.head(10).items(), 1):
            print(f"  {i:2d}. {genre:20s}: {count:4d} filmów")
        
        # Wykres
        plt.figure(figsize=(12, 6))
        genre_counts.head(15).plot(kind='bar')
        plt.title('15 najpopularniejszych gatunków filmowych')
        plt.xlabel('Gatunek')
        plt.ylabel('Liczba filmów')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('genre_distribution.png', dpi=300, bbox_inches='tight')
        print("\n✓ Wykres zapisany jako 'genre_distribution.png'")
    
    def analyze_rating_correlation(self):
        """Analiza korelacji między oceną a liczbą rekomendacji"""
        print("\n=== ANALIZA KORELACJI OCEN ===\n")
        
        # Dla każdego filmu, sprawdź średnią ocenę jego top 10 rekomendacji
        correlations = []
        
        for idx in range(min(100, len(self.df))):  # Testuj na 100 filmach
            movie_rating = self.df.iloc[idx]['rating']
            
            sim_scores = list(enumerate(self.recommender.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
            
            recommended_ratings = [self.df.iloc[i[0]]['rating'] for i in sim_scores]
            avg_recommended_rating = np.mean(recommended_ratings)
            
            correlations.append({
                'movie_rating': movie_rating,
                'avg_recommended_rating': avg_recommended_rating
            })
        
        corr_df = pd.DataFrame(correlations)
        correlation = corr_df['movie_rating'].corr(corr_df['avg_recommended_rating'])
        
        print(f"Korelacja między oceną filmu a średnią oceną rekomendacji: {correlation:.4f}")
        
        # Wykres
        plt.figure(figsize=(10, 6))
        plt.scatter(corr_df['movie_rating'], corr_df['avg_recommended_rating'], alpha=0.5)
        plt.xlabel('Ocena filmu bazowego')
        plt.ylabel('Średnia ocena rekomendowanych filmów')
        plt.title(f'Korelacja ocen (r={correlation:.4f})')
        plt.grid(True, alpha=0.3)
        plt.savefig('rating_correlation.png', dpi=300, bbox_inches='tight')
        print("✓ Wykres zapisany jako 'rating_correlation.png'\n")
    
    def analyze_feature_importance(self):
        """Analiza ważności cech w TF-IDF"""
        print("\n=== ANALIZA WAŻNOŚCI CECH ===\n")
        
        # Pobierz nazwy cech
        feature_names = self.recommender.tfidf_vectorizer.get_feature_names_out()
        
        # Oblicz średnią wagę każdej cechy
        feature_scores = np.asarray(self.recommender.tfidf_matrix.mean(axis=0)).flatten()
        
        # Top cechy
        top_indices = feature_scores.argsort()[-20:][::-1]
        
        print("Top 20 najważniejszych cech (słów/fraz):")
        for i, idx in enumerate(top_indices, 1):
            print(f"  {i:2d}. {feature_names[idx]:20s}: {feature_scores[idx]:.4f}")
    
    def run_full_analysis(self):
        """Uruchom pełną analizę"""
        print("="*60)
        print("ANALIZA PARAMETRÓW SYSTEMU REKOMENDACJI FILMÓW")
        print("="*60)
        
        self.analyze_tfidf_parameters()
        self.analyze_genre_weights()
        self.analyze_recommendation_count()
        self.analyze_similarity_distribution()
        self.analyze_genre_impact()
        self.analyze_rating_correlation()
        self.analyze_feature_importance()
        
        print("\n" + "="*60)
        print("ANALIZA ZAKOŃCZONA")
        print("="*60)
        print("\nWygenerowane wykresy:")
        print("  - similarity_distribution.png")
        print("  - genre_distribution.png")
        print("  - rating_correlation.png")


if __name__ == '__main__':
    analyzer = ParameterAnalyzer()
    analyzer.run_full_analysis()
