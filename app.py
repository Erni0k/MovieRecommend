"""
Flask Web Application dla Systemu Rekomendacji Filmów
"""

from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender
import pandas as pd

app = Flask(__name__)

# Inicjalizacja systemu rekomendacji
try:
    recommender = MovieRecommender()
    print(f"✓ Załadowano {len(recommender.df)} filmów do bazy danych")
except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku data/movies.csv")
    print("Uruchom najpierw: python download_data.py")
    recommender = None


@app.route('/')
def index():
    """Strona główna"""
    if not recommender:
        return "Błąd: System rekomendacji nie został zainicjalizowany. Uruchom download_data.py", 500
    
    # Pobierz najpopularniejsze filmy do wyświetlenia na stronie głównej
    top_movies = recommender.get_top_rated(12)
    
    # Konwertuj DataFrame na listę słowników
    movies_list = top_movies.to_dict('records')
    
    return render_template('index.html', movies=movies_list)


@app.route('/search', methods=['POST'])
def search():
    """Wyszukiwanie filmu i generowanie rekomendacji"""
    if not recommender:
        return jsonify({'error': 'System rekomendacji niedostępny'}), 500
    
    movie_title = request.form.get('movie_title', '').strip()
    n_recommendations = int(request.form.get('n_recommendations', 6))
    
    if not movie_title:
        return jsonify({'error': 'Nie podano tytułu filmu'}), 400
    
    # Pobierz rekomendacje
    recommendations = recommender.get_recommendations(movie_title, n_recommendations)
    
    if isinstance(recommendations, str):
        # Błąd - film nie znaleziony
        return render_template('results.html', 
                             error=recommendations, 
                             search_query=movie_title)
    
    # Sukces - konwertuj DataFrame na listę słowników
    movies_list = recommendations.to_dict('records')
    
    return render_template('results.html', 
                         movies=movies_list, 
                         search_query=movie_title)


@app.route('/genre/<genre_name>')
def genre(genre_name):
    """Filmy według gatunku"""
    if not recommender:
        return "Błąd: System rekomendacji niedostępny", 500
    
    results = recommender.search_by_genre(genre_name, 12)
    
    if isinstance(results, str):
        return render_template('genre.html', error=results, genre=genre_name)
    
    movies_list = results.to_dict('records')
    return render_template('genre.html', movies=movies_list, genre=genre_name)


@app.route('/api/search')
def api_search():
    """API endpoint dla wyszukiwania (AJAX)"""
    if not recommender:
        return jsonify({'error': 'System niedostępny'}), 500
    
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'results': []})
    
    # Szukaj filmów zawierających frazę
    mask = recommender.df['title'].str.contains(query, case=False, na=False)
    results = recommender.df[mask].head(10)[['title', 'year', 'rating', 'poster_url']]
    
    return jsonify({'results': results.to_dict('records')})


@app.route('/all')
def all_movies():
    """Wszystkie filmy"""
    if not recommender:
        return "Błąd: System rekomendacji niedostępny", 500
    
    # Pobierz wszystkie filmy posortowane według popularności
    all_movies_df = recommender.df.sort_values('rating', ascending=False)
    movies_list = all_movies_df[['title', 'genres', 'year', 'rating', 'poster_url']].to_dict('records')
    
    return render_template('all_movies.html', movies=movies_list, total=len(movies_list))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
