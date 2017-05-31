# tster

Prosta testerka napisana na potrzeby projektu na Bazy danych @ II UWr 2017

Funkcjonalności:
 - Zero zależności! Tylko czysty Python 3
 - Prosty w obsłudze i zmianie - kod testerki ma mniej niż 100 linii
 - Kolorowy output

Testy piszemy w pliku tests.py. Do pisania testów NIE jest wymagana znajomość języka.
Mała uwaga: w testach specjalnie nie podałem przykładowego sekretu ani hasła do bazy testowej. 

Uruchamienie komendą (pod Linuksem; na innych systemach powinno być podobnie):
```
python3 tster.py <ścieżka_do_programu>
```

Polecam też wykonać poniższą komendę, by zmiana wartości w `secrets.py` przypadkiem nie trafiła do repozytorium:
```
git update-index --skip-worktree secrets.py
```

Mile widziane pull requesty z testami ;)

