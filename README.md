- [Informazioni Generali](#informazioni-generali)
- [Descrizione dell'applicazione](#descrizione-dellapplicazione)
  - [Features implementate](#features-implementate)
- [Database](#database)
  - [Demo Accounts](#demo-accounts)
- [Istruzioni per l'installazione in locale](#istruzioni-per-linstallazione-in-locale)
- [Browser-based Testing](#browser-based-testing)
  - [Autenticazione](#autenticazione)
  - [Pagina profilo](#pagina-profilo)
  - [Home, Pagina Prodotti e Categorie](#home-pagina-prodotti-e-categorie)
  - [Modifica ed Eliminazione di Prodotti e Categorie](#modifica-ed-eliminazione-di-prodotti-e-categorie)
  - [Creazione di Prodotti e Categorie](#creazione-di-prodotti-e-categorie)
  - [Ordini e Carrello](#ordini-e-carrello)


# Informazioni Generali
| | |
|-|-|
| **Titolo del Progetto** | Progetto Back End Ecommerce |
| **Studente** | Matteo Sensi |
| **Progetto scelto** | Full Stack Web Ecommerce |
| **Framewok usato** | Django v5.2.14 |
| **Link di Deploy** | https://progetto-back-end-ecommerce.onrender.com |
 

# Descrizione dell'applicazione
L'applicazione in questione è un applicazione web che rappresenta un e-commerce di un negozio, questa quindi serve a permettere agli utenti di visualizzare i prodotti e successivamente acquistarli sul web.
## Features implementate
Nell'applicazione ci sono tre gruppi distinti che differenziano i tipi di utenti:
- **Customer**: Questo gruppo viene assegnato automaticamente quando un utente si registra al sito e come operazione principali può fare:
  - Modificare i le proprie informazioni, compresa la password (per visualizzare l'email sul terminale di django occore usare la stessa email usata per la registrazione dell'utente)
  - Aggiungere i prodotti al carrello
  - Visualizzare il proprio carrello
  - Modificare gli elementi nel carrello (aggiungerli, diminuirli, eliminarli)
  - Eseguire l'ordine
  - Visualizzare i propri ordini (può anche filtrarli in funzione di cosa preferisce visualizzare)
  - Fare il logout
- **Editor**:
  - Eredita tutti i permessi di un Customer
  - Modificare le informazioni sui prodotti
  - Modificare le informazioni sulle categorie
- **Manager**:
  - Eredita tutti i permessi di un Editor
  - Eliminare un prodotto
  - Creare un prodotto
  - Eliminare una categoria
  - Creare una Categoria
  - Gestire gli ordini, il che implica poter vedere gli ordini di tutti gli utenti e modificare lo stato di un ordine. Per la visualizzazione sono disponibili i filtri

Questi ultimi due gruppi devono essere assegnati da un superuser ad un utente dalla pagina admin dell'applicazione.
Le pagine 'I tuoi ordini', 'profilo' e l'operazione di logout sono disponibili nel menu a tendina che appare dopo che si è effettuato l'accesso
Inoltre, chiunque acceda al sito, anche se non è registrato, ha le seguenti funzionalità:
- Visualizzare i prodotti del catalogo, con annessi filtri
- Visualizzare i dettagli di un singolo prodotto
- Visualizzare le categorie
- Procedere con l'accesso o la registrazione

Gli utenti Manager nella navbar avranno una sezione in più chiamata 'Manager' dove possono gestire gli ordini, aggiungere le categorie e i prodotti. Per modificare ed eliminare i prodotti invece si può fare dalla pagina prodotti e dalla pagina del prodotto. Stessa cosa per le categorie nelle rispettive pagine.

# Database
Il database usato è quello di default di django ("db.sqlite3") e contiene le seguenti tabelle:

- **Cart**(id, user_id)
- **CartItem**(id, cart_id, product_id, quantity)
- **Order**(id, created_at, user_id, status, email_used, order_address)
- **Orderitem**(id, quantity, order_id, product_id, actual_price_per_unit)
- **Product**(id, name, description, price, stock, discount, slug)
- **product_categories**(id, product_id, tag_id)
- **Tag**(id, slug, name)
- **User**(id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, address, phone, email)

In tutte le tabelle sono state usate le PK autogenerate da django.
Della tabella User (derivata dal modello AbstractUser) non sono state usate tutte le informazioni, first_name e last_name non sono state usate.

Il database è già stato popolato con prodotti, categorie, utenti, ordini e carrelli:
Utenti (presi dalla pagina admin):


Prodotti:
-	Costruzioni Modulari (34.90€) costruzioni-modulari
-	Puzzle 1000 Pezzi (18.90€) puzzle-1000-pezzi
-	Gioco da Tavolo Strategico (29.90€) gioco-da-tavolo-strategico
-	Cappello Invernale (19.90€) cappello-invernale
-	Maglietta Tech (24.90€) maglietta-tech
-	Jeans Slim Fit (49.90€) jeans-slim-fit
-	Felpa con Cappuccio (39.99€) felpa-con-cappuccio
-	Corda per Saltare (14.90€) corda-per-saltare
-	Tappetino Yoga (19.90€) tappetino-yoga
-	Palla da Calcio (24.90€) palla-da-calcio
-	Zaino Sportivo (45.00€) zaino-sportivo
-	Asciugamani in Spugna (29.90€) asciugamani-in-spugna
-	Set di Posate (39.90€) set-di-posate
-	Frullatore da Cucina (59.90€) frullatore-da-cucina
-	Lampada da Tavolo (34.50€) lampada-da-tavolo
-	Speaker Bluetooth (79.90€) speaker-bluetooth
-	Tablet 10 pollici (249.00€) tablet-10-pollici
-	Smartwatch Active (199.90€) smartwatch-active
-	Cuffie Wireless (129.90€) cuffie-wireless
-	Smartphone X100 (500.00€) smartphone-x100

Categorie:
- Scuola
-	Sport
-	Giochi
-	Abbigliamento
-	Casa
-	Elettronica


Ordini:
- Order 4 - admin - 879.55€
-	Order 3 - admin - 110.42€
-	Order 2 - admin - 1104.20€
-	Order 1 - admin - 2208.40€
-	Order 9 - editor - 2156.30€
-	Order 8 - editor - 0€
-	Order 7 - editor - 0€
-	Order 14 - manager - 134.81€
-	Order 13 - manager - 220.84€
-	Order 12 - manager - 2500.00€
-	Order 10 - manager - 229.82€
-	Order 11 - test - 110.42€
-	Order 6 - test - 247.82€
-	Order 5 - test - 1000.00€

Carrelli:
- Cart of manager
- Cart of editor
-	Cart of admin
-	Cart of test


## Demo Accounts
Gli account già presenti nel database sono:

|Username | Password | email | Ruolo |
|-|-|-|-|
| admin | admin12345! | admin@admin.test | Manager + admin django |
| manager | man1234! | manager@manager.com| Manager |
| editor | edit1234! | editor@editor.com | Editor |
| test | test12345! | test@user.com | Customer |

# Istruzioni per l'installazione in locale
Installare l'applicazione in locale eseguire i seguenti script:
**È necessario aver installato python3**
Clona la repository in una cartella: 
```bash
git clone <repository-url>
cd <repository-folder>
```
Crea un virtual envirorment con Python:
```bash
python -m venv myenv
```
Attiva il virtual envirorment:
- Windows
```
myenv\Scripts\activate
```
- Linux/MacOs:
```
source myenv/bin/activate
```
Installa le dipendenze:
```
pip install -r requirements.txt
```

Applica le migrazioni nel caso fosse necessario. In questo caso non dovrebbe essere necessario in quanto il db è già stato creato ed è nella repository.
```
python manage.py makemigrations
python manage.py migrate
```

**Modifica la SECRET_KEY all'interno di settings.py della cartella /ecommerce impostandone una personale.**

Avvia il server:
```
python manage.py runserver
```
Apri l'applicazione su un browser all'indirizzo http://127.0.0.1:8000/

# Browser-based Testing
## Autenticazione
|Scenario | Azione | Risultato atteso |
|-|-|-|
| Accesso | L'utente inserisce credenziali valide e clicca su accedi | L'utente viene autenticato e reindirizzato alla homepage |
| Registrazione | L'utente inserisce credenziali valide e clicca su registrati | L'utente viene creato e reindirizzato alla pagina di accesso |
| Accesso non autorizzato | L'utente inserisce credenziali non valide e clicca su accedi | Viene mostrato un messaggio di errore nel form |
| Modifica della password | L'utente preme il link per il cambio password | L'utente viene reindirizzato ad un form dove viene chiesta l'email nella quale viene inserito il link per il cambio password, una volta inserita la nuova password l'utente sarà reindirizzato alla pagina di accesso |
| Log out | L'utente preme il pulsante per il log out | L'utente viene sloggato e verrà visualizzata la home page |

## Pagina profilo
Per poter accedere a questa pagina un utente deve essere registrato.

|Scenario | Azione | Risultato atteso |
|-|-|-|
| Visualizzazione | L'utente apre la pagina profilo | L'utente visualizza i suoi dati dentro ad un form per poterli modificare |
| Modifica |L'utente inserisce correttamente le modifiche e clicca il pulsante per la modifica | L'utente verrà reindirizzato alla stessa pagina e sarà notificato con un messaggio di corretta modifica |


## Home, Pagina Prodotti e Categorie
|Scenario | Azione | Risultato atteso |
|-|-|-|
| Visualizzazione Home| L'utente apre la home-page | Nella home page saranno visibili le categorie disponibili e i prodotti in sconto non esauriti **_(1)_** |
| Visualizzazione Prodotti - 1| L'utente apre la pagina prodotti | L'utente vedrà tutto il catalogo e i filtri per la ricerca, se i prodotti sono esauriti l'utente vedrà un badge con scritto esaurito al posto del prezzo **_(1)_** |
| Visualizzazione Prodotti - 1 - Filtri per la ricerca errati| L'utente inserisce dei filtri errati | L'utente verrà notificato dell'errore |
| Visualizzazione Prodotti - 2| Un utente **manager** apre la pagina prodotti | L'utente, oltre ai dettagli dei prodotti visualizzerà per ogni prodotto i bottoni per la modifica e per l'eliminazione del prodotto. Accade la stessa cosa nella pagina del prodotto |
| Visualizzazione Prodotti - 3| Un utente **editor** apre la pagina prodotti | L'utente visualizzarà solo i pulsanti di modifica. Stessa cosa nella pagina del prodotto 
| Visualizzazione Categorie - 1| L'utente apre la pagina delle categorie | L'utente vedrà i prodotti raggruppati per categoria, se una categoria non ha associato nessun prodotto viene visualizzato un messaggio **_(1)_** |
| Visualizzazione Categorie - 2| Un utente **manager** apre la pagina delle categorie | L'utente, oltre ai prodotti delle singole categorie visualizzerà a fianco al nome delle categore i bottoni per la modifica e per l'eliminazione di quest'ultime. Accade la stessa cosa nella pagina della categoria |
| Visualizzazione Categorie - 3| Un utente **editor** apre la pagina delle categorie | L'utente visualizzarà solo i pulsanti di modifica. Stessa cosa nella pagina della categoria |
| Pagina Prodotto | L'utente acceda alla pagina prodotto | Vengono mostrati immagine, nome, descrizione, prezzo, categorie del prodotto (cliccabili) e disponibilità. Viene mostrato anche il pulsante per aggiungere il prodotto al carrello con l'input per la quantità |
| Pagina Prodotto - Quantità errata | L'utente inserisce una quantità che supera la disponibilità o inferiore a uno | L'utente viene notificato dell'errore| 
| Pagina Prodotto - Aggiunta al carrello | L'utente clicca il pulsante aggiungi al carrello dopo aver inserito una quantità valida | L'utente viene notificato dell'evento e rimane nella pagina del prodotto **_(2)_** |

- **_(1)_** La card del prodotto contiene l'immagine, il titolo, descrizione e il prezzo, un bottone per essere reindirizzato alla pagina del prodotto e le categorie di cui fa parte (anche queste sono cliccabili e reindirizzano l'utente alla pagina della categoria).
- **_(2)_** Se vengono inserite più volte quantità inferiori alla disponibilità è possibile superare la disponibilità del prodotto nel carrello ma al momento del checkout verrà comunque individuato e notificato e l'ordine non sarà effettuato

## Modifica ed Eliminazione di Prodotti e Categorie

I pulsanti per la modifica e per l'eliminazione delle categorie e dei prodotti sono visibili solo agli utenti che hanno i permessi di farlo. Se un utente che non ha i permessi prova ad accederci tramite l'URL l'utente sarà reindirizzato alla home page.

|Scenario | Azione | Risultato atteso |
|-|-|-|
| Modifica Prodotto | Un utente con i permessi clicca sul pulsante di modifica di un prodotto  | Verrà visualizzato un form per modificare i dettagli del prodotto. Se i campi sono corretti l'utente verrà reindirizzato alla pagina del prodotto modificato e verrà notificata la corretta modifica. |
| Modifica Prodotto - Campi errati | L'utente inserisce dei campi errati nel form di modifica | L'utente verrà notificato degli errori |
| Modifica Categoria | Un utente con i permessi clicca sul pulsante di modifica di una categoria  | Verrà visualizzato un form per modificare i dettagli della categoria. Se i campi sono corretti l'utente verrà reindirizzato alla pagina delle categorie e verrà notificata la corretta modifica. |
| Modifica Categoria - Campi errati | L'utente inserisce dei campi errati nel form di modifica | L'utente verrà notificato degli errori (in particolare non possono esistere due categorie con lo stesso nome) |
| Eliminazione Prodotto | Un utente con i permessi clicca sul pulsante di eliminazione di un prodotto  | Verrà visualizzata una pagina di conferma. Se procediamo all'eliminazione del prodotto l'utente sarà reindirizzato alla pagina dei prodotti e verrà notificato della corretta eliminazione. |
| Eliminazione Categoria | Un utente con i permessi clicca sul pulsante di eliminazione di un prodotto  | Verrà visualizzata una pagina di conferma. Se procediamo all'eliminazione della categoria l'utente sarà reindirizzato alla pagina delle categorie e verrà notificato della corretta eliminazione. |

## Creazione di Prodotti e Categorie
Un utente manager visualizzerà queste opzioni nella pagina Manager, visibile solo agli utenti di questo gruppo. Se un utente senza i permessi provasse ad accedere alle pagine di creazione di Prodotti e Categorie verrà reindirizzato alla home page.

|Scenario | Azione | Risultato atteso |
|-|-|-|
| Creazioe Prodotto | Un utente con i permessi clicca sul pulsante di creazione di un prodotto  | Verrà visualizzato un form per definire i dettagli del prodotto. Se i campi sono corretti l'utente verrà reindirizzato alla pagina dei prodotti e verrà notificata la corretta creazione. |
| Creazione Prodotto - Campi errati | L'utente inserisce dei campi errati nel form di creazione | L'utente verrà notificato degli errori. |
| Creazioe Categoria | Un utente con i permessi clicca sul pulsante di creazione di una categoria | Verrà visualizzato un form per inserire il nome della categoria. Se i campi sono corretti l'utente verrà reindirizzato alla pagina delle categorie e verrà notificata la corretta creazione. |
| Creazione Categoria - Campi errati | L'utente inserisce dei campi errati nel form di creazione | L'utente verrà notificato degli errori |


## Ordini e Carrello
Per tutte queste azioni l'utente deve essere registrato o avere dei permessi, se così non fosse l'utente sarà reindirizzato alla home page o alla pagina di login

|Scenario | Azione | Risultato atteso |
|-|-|-|
| Visualizzazione Carrello | L'utente apre la pagina del carrello | L'utente visualizzerà tutti i prodotti aggiunti al carrello con la possibilità di eliminarli o modificarne la quantità e un riepilogo dell'ordine con il costo totale degli articoli. |
| Carrello - Modifica Quantità | L'utente inserisce una quantità valida | L'utente visualizzerà la pagina del carrello con un messaggio di avvenuta modifica |
| Carrello - Modifica Quantità - Errore Quantità | L'utente inserisce una quantità non valida | L'utente visualizzerà la pagina del carrello con un messaggio di errore |
| Carrello - Rimuovi Elemento | L'utente preme il pulsante per l'eliminazione dell'elemento dal carrello | L'utente visualizzerà la pagina del carrello con un messaggio avvenuta eliminazione |
| Visualizzazione Checkout | L'utente procede con il checkout **_(1)_** | L'utente visualizzerà tutti i prodotti del carrello con il riepilogo del totale e i dati di consegna, modificabili attraverso il form |
| Checkout | L'utente clicca il pulsante per fare l'ordine | L'utente visualizzerà una pagina di conferma dove potrà essere reindirizzato alla pagina degli ordini o a quella dei prodotti |
| Checkout - Dati non Validi | L'utente inserisce dei dati non validi e procede con l'ordine | L'utente sarà notificato degli errori |
| Visualizzazione Ordini | L'utente entra nella pagina degli ordini | L'utente visualizzarà tutti i sui ordini che potrà filtrare con l'apposito form |
| Visualizzazione Ordini - Filtri Errati | L'utente inserisce dei filtri errati | Verranno notificati gli errori |
| Visualizzazione Ordini - Manager | L'utente (manager) entra nella pagina degli ordini attraverso la pagina manager | L'utente visualizzarà tutti gli ordini di tutti gli utenti con la possibilità di filtrarli e di modificarne lo stato |
| Visualizzazione Ordini - Manager - Filtri Errati | L'utente inserisce dei filtri errati | Verranno notificati gli errori |
| Visualizzazione Ordini - Manager - Modifica Stato | Modifica lo stato dell'ordine | Verrà notificata la corretta modifica |

- **_(1)_** Se il carrello è vuoto il pulsante per procedere al checkout sarà disabilitato. Nel caso accedesse comunque con l'url alla pagina di checkout anche in quel caso il pulsante di invio form è disabilitato e nelle View ci sono i controlli per evitare di salvare ordini vuoti.

