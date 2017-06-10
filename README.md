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


Mile widziane pull requesty z testami ;)

