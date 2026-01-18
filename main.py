"""
System rekomendacji filmów - interfejs użytkownika (CLI)
"""

import pandas as pd
from recommender import MovieRecommender


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
        print("Uruchom najpierw: python download_data.py")
        return
    
    while True:
        print("\nWybierz opcję:")
        print("1. Pokaż rekomendacje dla filmu")
        print("2. Pokaż najpopularniejsze filmy")
        print("3. Szukaj filmów według gatunku")
        print("4. Wyświetl wszystkie filmy")
        print("5. Wyjście")
        
        choice = input("\nTwój wybór (1-5): ").strip()
        
        # Normalizuj wybór - akceptuj zarówno numer jak i pierwsze znaki
        if choice and not choice.isdigit():
            # Spróbuj wyodrębnić numer z początku
            first_char = choice[0]
            if first_char.isdigit():
                choice = first_char
        
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
            elif isinstance(recommendations, dict) and recommendations.get('type') == 'multiple_matches':
                print(f"\n📋 Znaleziono {len(recommendations['movies'])} filmów o podobnym tytule:")
                for i, m in enumerate(recommendations['movies'][:10], 1):
                    year = m.get('year', '?')
                    rating = m.get('rating', 0)
                    print(f"  {i}. {m['title']} ({year}) - Ocena: {rating}/10")
                
                choice = input("\nWybierz numer filmu (Enter = anuluj): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(recommendations['movies']):
                    selected = recommendations['movies'][int(choice) - 1]
                    recs = recommender.get_recommendations_by_id(selected['movieId'], n)
                    if isinstance(recs, pd.DataFrame):
                        print(f"\n🎬 Rekomendacje dla filmu '{selected['title']}':\n")
                        print(recs.to_string(index=False))
                    else:
                        print(f"\n❌ {recs}")
            elif isinstance(recommendations, pd.DataFrame):
                print(f"\n🎬 Rekomendacje dla filmu '{movie}':\n")
                print(recommendations.to_string(index=False))
            else:
                print(f"\n❌ Nieoczekiwany format odpowiedzi")
            
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
