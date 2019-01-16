# Projectvoorstel
## Samenvatting
Het idee is om een website te maken die recepten bij elkaar verzamelt op basis van ingrediënten die mensen aanklikken in de zoekbalk. De website geeft in eerste instantie alleen de keuze uit verse producten (vlees, zuivel, vis, groente, fruit). Dit is gericht op het tegengaan van voedselverspilling. Als de verse ingrediënten zijn aangeklikt krijgt de gebruiker recepten terug en een lijst met ingrediënten die worden gecombineerd met het gekozen ingrediënt. De lijst aan ingrediënten die de gebruiker terugkrijgt bestaat uit zowel verse als houdbare producten. De gebruiker kan kijken welke ingrediënten hij/zij verder in huis heeft en kan op de ingrediënten in de lijst klikken om recepten terug te krijgen met de gekozen combinatie.

## Schetsen
Schetsen van website in powerpoint. De volgende pagina's zijn nodig:
-   homepage.html
-   login.html
-   register.html
-   results.html
-   recipe.html
-   mypage.html
### Databases
![](https://github.com/taliafawzy/16/blob/master/databases.PNG)

## Features
1. Gebruiker kunnen inloggen
2. Gebruikers kunnen registreren
3. Er wordt voor iedere geregistreerde gebruiker een cookbook en portfolio aangemaakt
4. Gebruikers kunnen uitloggen
5. Gebruikers kunnen uit een uitvouwmenu recepten aanklikken
6. Gebruikers krijgen recepten met dit/deze ingrediënt(en) terug
7. Gebruikers krijgen (naast de recepten) ook andere ingrediënten te zien die vaak gecombineerd worden met het/de gekozen ingrediënt(en)
8. Gebruikers kunnen deze andere ingrediënten aanklikken en krijgen dan een niewue lijst van recepten terug
9. Gebruikers kunnen de gegeven recepten aanklikken
10. Gebruiker kunnen, mits ingelogd, een recept opslaan in hun cookbook
11. Gebruikers kunnen, mits ingelogd, een recept op de receptpagina waarderen
12. Gebruikers kunnen op hun profielpagina aangeven of een recept is geprobeerd
13. Gebruikers kunnen op hun profielpagina een persoonlijke rating aan een recept geven
14. Opgeslagen recepten worden met naam, link, 'tried' button of 'YES' en wel/geen rating in een tabel op de profielpagina getoond
15. Op de profielpagina wordt de gebruikersnaam van de gebruiker getoond en wordt bijgehouden hoeveel recepten zijn geprobeerd, gereviewd en opgeslagen
16. Gebruikers krijgen bij een aangeklikt recept te zien welke recepten ook zijn opgeslagen door gebruikers die getoonde recept ook in hun cookbook hebben


## Minimum viable product
Gebruikers kunnen via de website zoeken naar recepten met de specifieke ingrediënten die zij aanklikken. Het product laat gebruikers hun favoriete recepten opslaan die zij op hun persoonlijke pagina kunnen bekijken. Ze kunnen daar aangeven of ze het recept hebben geprobeerd en ze kunnen het recept waarderen door middel van het geven van sterren. Ook kunnen ze het recept op de receptpagina een rating geven.

## Afhankelijkheden
### Databronnen
- **Edamam recipe finder**
https://developer.edamam.com/edamam-recipe-api

### Externe Componenten
- **Bootstrap**
https://getbootstrap.com/
- **phpLiteAdmin**
https://www.phpliteadmin.org/
- **Flask**
http://flask.pocoo.org/
- **SQLite Databases**
https://www.sqlite.org/index.html


### Concurrerende bestaande websites
- http://myfridgefood.com/
Handig aan deze website is dat je ingrediënten aan kunt klikken in de quick search en zelf recepten kunt toevoegen.
- https://emptythefridge.be/
Naast recepten heeft de website ook een blog. Dit is misschien voor een bepaald publiek interessant. Zo geeft de auteur tips & tricks om eten te bewaren. Daarnaast heeft de wesite ook een seizoenstabel met ingredïenten, welke aangeeft wat wanneer vaak te verkrijgen is.
- https://www.keukenliefde.nl/kook-koelkast-leeg/
Deze website geeft de mogelijkheid om te sorten op menugang, soort gerecht en thema. Er staan ook knoppen bij het recept die het de gebruiker mogelijk maken om het recept te kopiëren of een printversie te openen.
- https://www.supercook.com/#/recipes
Mooie gebruiksvriendelijke layout.

### Moeilijke delen
- HTML en CSS layout er mooi en overzichtelijk uit laten zien.
- Het zoeken van recepten