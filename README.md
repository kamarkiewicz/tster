# tster

Prosta testerka napisana na potrzeby projektu na Bazy danych @ II UWr 2017

Funkcjonalności:
 - Zero zależności! Tylko czysty Python 3
 - Prosty w obsłudze i zmianie - kod testerki ma mniej niż 100 linii
 - Kolorowy output

Testy piszemy w pliku `tests.py`. Do pisania testów NIE jest wymagana znajomość języka.

Polecam też wykonać poniższą komendę, by zmiana wartości w `secrets.py` przypadkiem nie trafiła do repozytorium:
```
git update-index --skip-worktree secrets.py
```

## proces testowania

Wpierw należy pozmieniać credentiale w pliku `secrets.py`.

Uruchamienie komendą (pod Linuksem; na innych systemach powinno być podobnie):
```
cd <ścieżka_z_tsterem>
python3 tster.py <ścieżka_do_programu> [<label>]
```

Przykładowo, jeśli chcemy przetestować swój program przy użyciu oficjalnych testów, wykonujemy:
```
cd /home/me/tster
python3 tster.py /home/me/projekt_bazy/program public_test
```

## FAQ

_Q_ Mi tster nie działa! Piszę:
```
python3 tster.py ~/Projekt\ na\ bazy/rozwiazanie.py api_open
```
a dostaję dziwne errory.

_A_ tster jako drugi argument przyjmuje dokładnie to, co normalnie podałbyś w shellu. Ponadto
musisz podawać pełną ścieżkę zamiast względnej. Więc jeśli normalnie uruchamiasz swój program:
```
cd /home/me/Projekt\ na\ bazy/ && python3 rozwiazanie.py
```
to do tstera musisz podać (będąc w katalogu tstera):
```
python3 tster.py "cd /home/me/Projekt\ na\ bazy/ && python3 rozwiazanie.py" api_open
```

_Q_ Jak mogę wyświetlić informacje do debugowania?

_A_ tster traktuje stdout jak prawdę objawioną i porównuje go z stdoutem przypadku testowego.
stderr nie jest w ogóle sprawdzany, więc to jego powinieneś używać do pisania po konsoli
w trakcie działania testu.



Mile widziane pull requesty z testami ;)

