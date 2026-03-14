⋆˚꩜｡ Bämätehdas

Nettisivu meikkilookkien jakamiseen ja arvosteluun.

♡ Sovelluksessa käyttäjät pystyvät jakamaan meikkilookkejansa. Lookeilla on otsikko, kuvaus, kuva tai kuvia, sekä mahdollisuus lisätä siihen vaikeusaste ja kategoria.
♡ Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
♡ Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lookkeja.
♡ Käyttäjä näkee kaikki sovellukseen lisätyt lookit.
♡ Käyttäjä pystyy etsimään lookkeja hakusanoilla (myöhemmin myös kategorioiden avulla).
♡ Käyttäjäsivu näyttää, montako lookkia käyttäjä on luonut ja listan käyttäjän luomista lookeista.
♡ Käyttäjä pystyy valitsemaan lookille yhden tai useamman luokittelun (esim. arkimeikki tai juhlameikki ja lookin vaikeusateen.)
♡ Käyttäjä pystyy antaa toisille lookeille kommentteja ja oman arvion vaikeusasteesta. Lookeissa näytetään kommentit sekä vaikeusasteet. (Ei vielä toteutettu)
    
Tässä pääasiallinen tietokohde on meikkilookit ja toissijainen tietokohde on komentti lookkeihin.

⋆˚꩜｡ Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
