Projekt gry Flappy Janusz - Studia/Obiektówka

Żeby odpalić tą gierke potrzebujecie zrobić klika rzeczy:

# Wymagania:
* Python 3.10+
* Pygame (Nie tylko zaimportowane ale też pobrane)
* Ruff (opcjonalne):
  - Jest to wtyczka do wskazywania błędów

# --- Jak pobrać i uruchomić projekt? --- #

1. Sklonuj repozytorium z GitHub'a (w terminalu)
   - Wpisz: git clone "https://github.com/grejniaadam/flappyprojekt.git"

2. Wejdź do pliku. Stwórz  i odpal wirtualne środowisko.
   - Odpal terminal (w Pycharm alt+F12, w VS Code CTRL + delta(to po ESC))
   - Wpisz: cd flappyprojekt
            python -m venv .venv
            .\.venv\Scripts\activate

3. Zainstaluj wymagane biblioteki.
   - Wpisz: pip install -r requirements.txt

4. Uruchom grę:
   - Uruchamiamy ją z pomoca terminalu. Jeżeli macie aktywne środowisko 
     wpisujecie w terminalu: python main.py

# --- Warto skonfigurować sobie gita i githuba --- # Tak, Git i GitHub to oddziele rzeczy

Żeby git działało poprawnie i by wszystko było "legancko tego" potrzebujecie 
ustawić te dane. 

* Wykonujcię kolejno punkty.
   - Ustawienie nazwy Użytkownika: git config --global user.name "Imię i Nazwisko"
   - Ustawienie adresu e-mail: git config --global user.email "twój@email"
   - Ustawienie domyślnej nazwy gałęzi: git config --global init.defaultBranch main

* Obsługa Git'a w terminalu (podstawowe rzeczy):
   - Pobranie repo: git clone "link"

   - Dodanie repo (lokalnie): git add "nazwa_pliku" lub . wtedy doda wszystkie zmienione

   - Dodanie commitu (opisu): git commit -m "Tutaj opis wprowadzonych zmian"

   - Wypchnięcie repo na GitHub: git push

   - Pobranie zmian od innych programistów: git pull

   - Sprawdznie plików między nami a Gitem: git status



