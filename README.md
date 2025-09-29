# Meikkisovellus

Nettisivu meikkilookkien jakamiseen ja arvosteluun.

- Sovelluksessa käyttäjät pystyvät jakamaan meikkilookkejansa. Lookeissa kerrotaan mitä meikkejä siihen on käytetty.
- Käyttäjä pystyy luomaan tuunuksen ja kirjautumaan sisään soellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lookkeja.
- Käyttäjä näkee sovellukseen lisätyt lookit.
- Käyttäjä pystyy etsimään lookkeja hakusanoilla.
- Käyttäjäsivu näyttää, montako lookkia käyttäjä on lisännyt ja listan käyttäjän lisäämistä lookeista.
- Käyttäjä pystyy valitsemaan lookille yhden tai useamman luokittelun (esim. arkimeikki, juhlameikki, tietty tyyli, yms.)
- Käyttäjä pystyy antaa lookeille kommentteja ja vaikeusasteen.  Lookeissa näytetään kommentit sekä vaikeusaste.
    
Tässä pääasiallinen tietokohde on meikkilookit ja toissijainen tietokohde on komentti lookkeihin.


## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
