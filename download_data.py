#!/usr/bin/env python3
"""
Skrypt do pobierania danych filmowych z The Movie Database (TMDb)
"""

from tmdb_fetcher import download_tmdb_data, load_api_key_from_env
import os


def main():
    print("=" * 70)
    print("POBIERANIE DANYCH Z THE MOVIE DATABASE (TMDb)")
    print("=" * 70)
    
    # Sprawdź klucz API
    api_key = load_api_key_from_env()
    
    if not api_key:
        print("\n⚠️  Brak klucza API TMDb!")
        print("\nAby pobrać dane z TMDb, musisz uzyskać klucz API:")
        print("1. Zarejestruj się na https://www.themoviedb.org/")
        print("2. Przejdź do Settings -> API")
        print("3. Wygeneruj klucz API (v3)")
        print("\nMożesz podać klucz na dwa sposoby:")
        print("A) Ustaw zmienną środowiskową: set TMDB_API_KEY=twoj_klucz")
        print("B) Wpisz klucz teraz:")
        
        api_key = input("\nTwój klucz API TMDb (lub Enter aby anulować): ").strip()
        
        if not api_key:
            print("\n❌ Anulowano. Brak klucza API.")
            return 1
    
    print(f"\n✅ Klucz API znaleziony (długość: {len(api_key)} znaków)")
    
    # Wybór liczby filmów
    print("\n" + "=" * 70)
    print("\nIle filmów chcesz pobrać?")
    print("1. ~400 filmów (szybkie, zalecane do testów)")
    print("2. ~1000 filmów (średnie)")
    print("3. ~2000 filmów (duże)")
    print("4. Niestandardowa ilość")
    
    choice = input("\nWybierz opcję (1-4) [domyślnie 1]: ").strip()
    
    if choice == '2':
        num_popular = 500
        num_top_rated = 500
    elif choice == '3':
        num_popular = 1000
        num_top_rated = 1000
    elif choice == '4':
        try:
            num_popular = int(input("Liczba popularnych filmów: "))
            num_top_rated = int(input("Liczba najlepiej ocenianych filmów: "))
        except ValueError:
            print("❌ Nieprawidłowa wartość, używam domyślnych ustawień.")
            num_popular = 200
            num_top_rated = 200
    else:
        num_popular = 200
        num_top_rated = 200
    
    print(f"\n📋 Konfiguracja:")
    print(f"  - Popularne filmy: {num_popular}")
    print(f"  - Najlepiej oceniane: {num_top_rated}")
    print(f"  - Szacowana liczba unikalnych filmów: ~{num_popular + num_top_rated}")
    
    try:
        output_path = download_tmdb_data(
            api_key=api_key,
            num_popular=num_popular,
            num_top_rated=num_top_rated
        )
        
        print(f"\n{'=' * 70}")
        print("✅ SUKCES! Dataset został pobrany z TMDb.")
        print(f"Plik: {output_path}")
        print("\nMożesz teraz uruchomić main.py aby korzystać z systemu rekomendacji.")
        print("=" * 70)
        
        # Zapisz klucz do pliku .env dla przyszłych użyć
        if not load_api_key_from_env():
            save_key = input("\nCzy zapisać klucz API do pliku .env? (t/n): ").strip().lower()
            if save_key == 't':
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f"TMDB_API_KEY={api_key}\n")
                print("✅ Klucz zapisany do .env")
                print("💡 Dodaj .env do .gitignore aby nie udostępniać klucza publicznie!")
                
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
