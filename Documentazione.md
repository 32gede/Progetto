# Documentazione del Progetto

## Introduzione
L’obiettivo del progetto è lo sviluppo di una web application che si interfaccia con un database relazionale, consentendo agli utenti di interagire con prodotti, ordini e recensioni in un contesto di e-commerce. L'applicazione è stata sviluppata in Python, utilizzando il framework Flask per la gestione del backend e SQLAlchemy come ORM per l'interazione con il database. 

La scelta del DBMS è ricaduta su PostgreSQL per la sua robustezza e scalabilità, particolarmente adatta a gestire un'applicazione web con operazioni di lettura e scrittura frequenti. Inoltre, l'utilizzo di Flask, una delle librerie più leggere e flessibili per lo sviluppo web in Python, ha permesso un rapido sviluppo e iterazione dell'applicazione. 

Questa documentazione si propone di illustrare le principali funzionalità dell'applicazione, la progettazione concettuale e logica del database, le query SQL implementate, le scelte progettuali adottate, e altre informazioni tecniche rilevanti per comprendere il progetto. Nella sezione finale, verrà anche chiarito il contributo di ciascun membro del gruppo.

## Struttura del Progetto
Il progetto è organizzato secondo la seguente struttura:

- **`app.py`**: Contiene la configurazione dell'applicazione Flask, l'inizializzazione del database, e la gestione delle sessioni e dell'autenticazione.
- **`models.py`**: Definisce i modelli di dati utilizzati dall'applicazione, inclusi utenti, prodotti, ordini e recensioni. Implementa anche la logica di business correlata, come la gestione delle relazioni e la protezione delle password.
- **`routes.py`**: Gestisce le rotte dell'applicazione, definendo le operazioni che possono essere eseguite dagli utenti, come la visualizzazione dei prodotti, l'aggiunta di articoli al carrello, e la gestione degli ordini.
- **`database.py`**: Contiene la configurazione della connessione al database, inclusa l'inizializzazione e la gestione delle sessioni.
- **`forms.py`**: Definisce i form utilizzati nell'applicazione, validando i dati inseriti dagli utenti e garantendo la sicurezza tramite Flask-WTF.
- **`templates/`**: Contiene i file HTML utilizzati per la visualizzazione delle pagine web, inclusi layout, form e pagine specifiche per utenti autenticati e non autenticati.
- **`Google.py`**: Contiene il codice per l'autenticazione con Google.
- **`collegamento_google.py`**: Contiene il codice per il collegamento con Google.

## Funzionalità principali

L'applicazione fornisce diverse funzionalità per supportare un'esperienza di e-commerce completa. Di seguito sono descritte le principali funzionalità:

### Registrazione e autenticazione degli utenti

Gli utenti possono registrarsi fornendo un indirizzo email, una password e altre informazioni personali come nome e indirizzo. L'autenticazione viene gestita tramite email e password, con controlli di sicurezza per proteggere le credenziali.

### Gestione del profilo utente

Gli utenti possono visualizzare e aggiornare le loro informazioni personali, tra cui nome, indirizzo e città. Questa funzionalità è accessibile solo dopo l'autenticazione e garantisce che le informazioni siano mantenute aggiornate per facilitare gli acquisti e le spedizioni.

### Visualizzazione e ricerca di prodotti

Gli utenti possono navigare tra i prodotti disponibili e utilizzare la funzionalità di ricerca per trovare rapidamente i prodotti desiderati. I prodotti possono essere filtrati per categoria, prezzo o parole chiave specifiche.

### Aggiunta di prodotti al carrello

Gli utenti possono aggiungere prodotti al loro carrello per procedere con l'acquisto. Il carrello è persistente e gli utenti possono visualizzare, modificare o rimuovere articoli prima di procedere al checkout.

### Completamento degli ordini

Dopo aver aggiunto i prodotti al carrello, gli utenti possono completare l'acquisto tramite una procedura di checkout. Gli ordini vengono salvati nel database, e gli utenti possono successivamente monitorare lo stato del loro ordine.

### Gestione degli ordini per venditori e acquirenti

I venditori possono visualizzare e gestire gli ordini ricevuti, mentre gli acquirenti possono monitorare lo stato dei loro ordini, inclusi eventuali aggiornamenti di spedizione e consegna.

### Sistema di recensioni per i prodotti

Gli utenti possono lasciare recensioni e valutazioni sui prodotti acquistati. Questo sistema aiuta altri utenti a prendere decisioni informate sugli acquisti, basandosi su esperienze reali.

## Progettazione concettuale e logica della basi di dati

La progettazione del database è stata effettuata utilizzando la notazione ER e successivamente trasformata in uno schema logico che implementa le tabelle del database. La progettazione è stata guidata dai requisiti funzionali dell'applicazione, con particolare attenzione all'integrità referenziale e alla normalizzazione.

### Diagramma ER

Il diagramma ER rappresenta le entità principali, le loro relazioni e gli attributi associati. Le entità includono User, Product, Order, OrderItem e Review.

![Diagramma ER](https://github.com/32gede/Progetto/blob/main/Schema%20ER.png)

### Schema Logico

Lo schema logico del database è composto da diverse tabelle che rappresentano le entità e le loro relazioni. Di seguito è riportato un estratto dello schema SQL utilizzato per creare le tabelle principali:

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    address VARCHAR(255),
    city VARCHAR(255)
);

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    seller_id INT,
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    total DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    confirmed_at DATETIME,
    status VARCHAR(50) DEFAULT 'In attesa',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE reviews (
    id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Query principali

Le query SQL utilizzate all'interno dell'applicazione sono progettate per soddisfare i requisiti funzionali e ottimizzare le prestazioni del database. Di seguito sono riportate alcune delle query più significative.

### Query per ottenere i prodotti di un venditore

```sql
SELECT * FROM products WHERE seller_id = :seller_id;
```
Questa query consente ai venditori di visualizzare tutti i prodotti che hanno inserito nel sistema, fornendo una panoramica completa del loro inventario.

### Query per ottenere gli ordini di un utente

```sql
SELECT * FROM orders WHERE user_id = :user_id;
```
Questa query recupera tutti gli ordini effettuati da un utente specifico, permettendo agli acquirenti di visualizzare la cronologia dei loro acquisti.

### Query per ottenere le recensioni di un prodotto

```sql
SELECT * FROM reviews WHERE product_id = :product_id;
```
Questa query recupera tutte le recensioni associate a un determinato prodotto, fornendo un feedback prezioso per i potenziali acquirenti.

## Principali scelte progettuali

### Politiche di integrità

La progettazione del database prevede l'uso di chiavi esterne per garantire l'integrità referenziale tra le tabelle. Inoltre, la validazione dei dati viene effettuata sia a livello di database che a livello di applicazione per assicurare la correttezza dei dati.

* **Chiavi esterne**: Le chiavi esterne collegano le tabelle users, products, orders, order_items e reviews per garantire che le relazioni tra le entità siano mantenute in modo coerente.
* **Validazione dei dati**: Viene implementata una validazione rigorosa dei dati, inclusi controlli sui campi obbligatori, vincoli di unicità e limiti sui valori numerici.

### Definizione di ruoli e politiche di autorizzazione

L'applicazione implementa un sistema di ruoli che distingue tra acquirenti, venditori e amministratori. Le politiche di autorizzazione sono definite per garantire che solo gli utenti con i permessi appropriati possano accedere a determinate funzionalità.

* **Acquirenti**: Possono visualizzare i prodotti, aggiungerli al carrello e completare gli acquisti.
* **Venditori**: Possono aggiungere, modificare e rimuovere i prodotti, nonché gestire gli ordini ricevuti.
* **Amministratori**: Hanno accesso completo a tutte le funzionalità dell'applicazione, inclusa la gestione degli utenti e dei ruoli.

### Uso di indici

L'applicazione utilizza indici su colonne frequentemente utilizzate, come `email` e `product_id`, per migliorare le prestazioni delle query.. Ad esempio, la ricerca di prodotti o la verifica delle credenziali durante il login sono operazioni critiche che devono essere eseguite rapidamente, e l'uso di indici consente di ridurre significativamente i tempi di risposta.

* **Indice su email**: L'indice sull'email nella tabella users accelera le operazioni di autenticazione e recupero degli utenti.
* **Indice su seller_id**: Facilita la ricerca rapida dei prodotti per venditore, migliorando le prestazioni della gestione dell'inventario.

## Sicurezza

La sicurezza è una priorità fondamentale per l'applicazione, con diverse misure adottate per proteggere i dati e gli utenti da potenziali minacce.

- **Protezione delle Password**: Le password degli utenti sono crittografate utilizzando werkzeug.security, un algoritmo di hashing sicuro che protegge le credenziali degli utenti da attacchi di forza bruta.

- **Validazione dei Dati**: Tutti i dati inseriti dagli utenti sono validati per prevenire attacchi di tipo SQL injection e XSS. Inoltre, vengono utilizzati token CSRF per proteggere i form da attacchi CSRF.

- **Protezione CSRF e Gestione dei Form**: Tutti i form dell'applicazione sono gestiti tramite Flask-WTF, che offre protezione contro attacchi CSRF. Questo è particolarmente importante in un'applicazione di e-commerce dove le transazioni devono essere sicure.

- **Sicurezza e Autenticazione**: L'applicazione utilizza Flask-Login per la gestione degli accessi, con un sistema di ruoli che distingue tra acquirenti e venditori. Questo garantisce che solo gli utenti autorizzati possano accedere a determinate funzionalità.

- **Utilizzo di Talisman per la Sicurezza**: Sebbene non abilitato di default, l'applicazione è predisposta per l'uso di Flask-Talisman per aggiungere ulteriori livelli di sicurezza, come le Content Security Policy (CSP) che proteggono contro attacchi XSS.


## Ulteriori informazioni

### Scelte tecnologiche

L'applicazione è stata sviluppata utilizzando un insieme di tecnologie moderne, che sono state scelte per la loro robustezza e facilità di utilizzo.

* **Linguaggio di programmazione**: Python, scelto per la sua sintassi chiara e l'ampia disponibilità di librerie.
* **Framework web**: Flask, un microframework leggero che consente una rapida prototipazione e sviluppo.
* **ORM**: SQLAlchemy, utilizzato per l'interazione con il database e la gestione delle relazioni tra le tabelle.
* **Database**: SQLite è stato utilizzato per lo sviluppo e il testing, grazie alla sua semplicità e portabilità.

### Deployment e gestione delle dipendenze

* **Gestione delle dipendenze**: Viene utilizzato pip e venv per gestire le dipendenze del progetto, garantendo che l'ambiente di sviluppo sia isolato e riproducibile.
* **Deployment**: L'applicazione è stata progettata per essere facilmente distribuita su server come Heroku o AWS, con supporto per configurazioni specifiche come file .env per le variabili di ambiente.

## Contributo al progetto (appendice)

Il progetto è stato sviluppato collaborativamente dai membri del team, con ogni membro che ha contribuito in modo significativo alle varie fasi del progetto.

* **Membro 1**: Ha guidato il design del database, creando lo schema logico e implementando le query principali. Inoltre, ha documentato l'intero processo di progettazione e scelte implementative.
* **Membro 2**: Ha sviluppato il backend dell'applicazione, implementando le API, gestendo l'autenticazione, l'autorizzazione e la gestione degli ordini.
* **Membro 3**: Ha sviluppato il frontend, implementando le interfacce utente, integrando il design con il backend e eseguendo i test e il debug per assicurare che l'applicazione funzionasse correttamente su diverse piattaforme e dispositivi.

## Considerazioni Finali e Miglioramenti Futuri

Il progetto, pur essendo stato sviluppato con tecnologie robuste e ben integrate, potrebbe beneficiare di ulteriori miglioramenti, come l'implementazione di un sistema di caching per ridurre i tempi di caricamento delle pagine più pesanti, e l'integrazione di sistemi di pagamento reali per rendere l'applicazione pronta per l'uso in ambienti di produzione.