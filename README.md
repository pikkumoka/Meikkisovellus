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

Asennusohje: Luo virtuaaliympäristö:

python3 -m venv venv
Aktivoi virtuaaliympäristö:

Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
Asenna tarvittavat Python-kirjastot:

pip install flask
Luo tietokannan taulut, sovelluksessa käytetään SQLite-tietokantaa. Luo tietokannan taulut ajamalla seuraava komento:

python app.py
Suorita sovellus. Kun kaikki on asetettu, voit käynnistää sovelluksen seuraavalla komennolla:

flask run
