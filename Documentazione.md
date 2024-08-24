# Documentazione del Progetto

#### Table of Contents

1. [Introduzione](#Introduzione)
2. [Struttura del Progetto](#Struttura-del-Progetto)
2. [Funzionalità principali](#Funzionalità-principali)
3. [Progettazione concettuale e logica della basi di dati](#Progettazione-concettuale-e-logica-della-basi-di-dati)
4. [Query principali](#Query-principali)
5. [Principali scelte progettuali](#Principali-scelte-progettuali)
6. [Sicurezza](#Sicurezza)
7. [Ulteriori informazioni](#Ulteriori-informazioni)
7. [Contributo al progetto (appendice)](#Contributo-al-progetto-(appendice))
8. [Considerazioni Finali e Miglioramenti Futuri](#Considerazioni-Finali-e-Miglioramenti-Futuri)

---

<a name="Introduzione" /></a>

## Introduzione
L’obiettivo del progetto è lo sviluppo di una web application che si interfaccia con un database relazionale, consentendo agli utenti di interagire con prodotti, ordini e recensioni in un contesto di e-commerce. L'applicazione è stata sviluppata in Python, utilizzando il framework Flask per la gestione del backend e SQLAlchemy come ORM per l'interazione con il database. 

La scelta del DBMS è ricaduta su PostgreSQL per la sua robustezza e scalabilità, particolarmente adatta a gestire un'applicazione web con operazioni di lettura e scrittura frequenti.

Questa documentazione si propone di illustrare le principali funzionalità dell'applicazione, la progettazione concettuale e logica del database, le query SQL implementate, le scelte progettuali adottate, e altre informazioni tecniche rilevanti. Nella sezione finale, verrà anche chiarito il contributo di ciascun membro del gruppo.

---

<a name="Struttura-del-Progetto" /></a>

## Struttura del Progetto
Il progetto è organizzato secondo la seguente struttura:

- **`app.py`**: Contiene la configurazione dell'applicazione Flask, l'inizializzazione del database, e la gestione delle sessioni e dell'autenticazione.
- **`models.py`**: Definisce i modelli di dati utilizzati dall'applicazione, inclusi utenti, prodotti, ordini e recensioni. Implementa anche la logica di business correlata, come la gestione delle relazioni e la protezione delle password.
- **`routes.py`**: Gestisce le rotte dell'applicazione, definendo le operazioni che possono essere eseguite dagli utenti, come la visualizzazione dei prodotti, l'aggiunta di articoli al carrello, e la gestione degli ordini.
- **`database.py`**: Contiene la configurazione della connessione al database, inclusa l'inizializzazione e la gestione delle sessioni.
- **`forms.py`**: Definisce i form utilizzati nell'applicazione, validando i dati inseriti dagli utenti e garantendo la sicurezza tramite Flask-WTF.
- **`templates/`**: Contiene i file HTML utilizzati per la visualizzazione delle pagine web, inclusi layout, form e pagine specifiche per utenti autenticati e non autenticati.

I seguenti file sono stati utilizzati per implementare l'uploads di immagini ai prodotti:
- **`Google.py`**: Contiene il codice per l'autenticazione con Google, inclusa la gestione del flusso OAuth 2.0, la richiesta di token di accesso e la verifica delle credenziali dell'utente.
- **`collegamento_google.py`**: Contiene il codice per il collegamento con Google, gestendo l'integrazione con i servizi di Google per operazioni come la sincronizzazione dei dati e l'accesso alle API di Google.

---

<a name="Funzionalità-principali" /></a>

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

---

<a name="Progettazione-concettuale-e-logica-della-basi-di-dati" /></a>

## Progettazione concettuale e logica della basi di dati

La progettazione del database è stata effettuata utilizzando la notazione ER e successivamente trasformata in uno schema logico che implementa le tabelle del database. La progettazione è stata guidata dai requisiti funzionali dell'applicazione, con particolare attenzione all'integrità referenziale e alla normalizzazione.

### Diagramma ER

Il diagramma ER rappresenta le entità principali, le loro relazioni e gli attributi associati. Le entità includono User, Product, Order, OrderItem e Review.

![Diagramma ER](https://github.com/32gede/Progetto/blob/main/Schema%20DB.png)

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

---

<a name="Query-principali" /></a>

## Query principali

Le query SQL utilizzate all'interno dell'applicazione sono progettate per soddisfare i requisiti funzionali e ottimizzare le prestazioni del database. Di seguito sono riportate alcune delle query più significative.

### Query per ottenere i prodotti di un venditore

```python
products = db_session.query(Product).filter_by(seller_id=current_user.id).all()
```
```sql
SELECT * FROM products WHERE seller_id = :seller_id;
```
Questa query è fondamentale per i venditori, poiché consente loro di visualizzare tutti i prodotti che hanno messo in vendita. È essenziale per la gestione dell'inventario e per monitorare le vendite.
### Query per ottenere gli ordini di un utente

```python
orders = db_session.query(Order).filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()```
```
```sql
SELECT * FROM orders WHERE user_id = :user_id;
```
Questa query permette agli utenti di visualizzare i loro ordini, fornendo una panoramica dello stato degli acquisti e delle consegne. È cruciale per migliorare l'esperienza utente e per il servizio clienti.
### Query per ottenere le recensioni di un prodotto

```python
reviews = sorted(product.reviews, key=lambda review: review.created_at, reverse=True)
```
```sql
SELECT * FROM reviews WHERE product_id = :product_id;
```
Le recensioni sono importanti per gli acquirenti per prendere decisioni informate. Questa query consente di raccogliere feedback sui prodotti, migliorando la trasparenza e la fiducia nel marketplace

### Query per cercare prodotti in base a criteri specifici

```python
products = search_products(
    db_session,
    form.name.data,
    form.description.data,
    form.min_price.data,
    form.max_price.data,
    form.brand_name.data,
    form.category_name.data
)
```
```sql
SELECT * FROM products
JOIN brands ON products.brand_id = brands.id
JOIN categories ON products.category_id = categories.id
WHERE (:name IS NULL OR products.name ILIKE '%' || :name || '%')
AND (:description IS NULL OR products.description ILIKE '%' || :description || '%')
AND (:min_price IS NULL OR products.price >= :min_price)
AND (:max_price IS NULL OR products.price <= :max_price)
AND (:brand_name IS NULL OR brands.name ILIKE '%' || :brand_name || '%')
AND (:category_name IS NULL OR categories.name ILIKE '%' || :category_name || '%');
```
Questa query complessa permette agli utenti di cercare prodotti in base a vari criteri come nome, descrizione, prezzo, marca e categoria. È essenziale per migliorare la funzionalità di ricerca e filtraggio dei prodotti.

---

<a name="Principali-scelte-progettuali" /></a>

## Principali scelte progettuali

### Politiche di integrità

La progettazione del database prevede l'uso di chiavi esterne per garantire l'integrità referenziale tra le tabelle. Inoltre, la validazione dei dati viene effettuata sia a livello di database che a livello di applicazione per assicurare la correttezza dei dati.

* ### **Chiavi esterne**
Le chiavi esterne collegano le tabelle users, products, orders, order_items e reviews per garantire che le relazioni tra le entità siano mantenute in modo coerente.
* ### **Validazione dei dati**
Viene implementata una validazione rigorosa dei dati, inclusi controlli sui campi obbligatori, vincoli di unicità e limiti sui valori numerici.  Questo viene effettuato sia a livello di database che a livello di applicazione per garantire la coerenza dei dati.
In particolare questo viene fatto tramite il modulo Flask-WTF, che fornisce un'interfaccia per la validazione dei dati inseriti dagli utenti nei form.   

Ad esempio, la validazione dell'email viene effettuata per garantire che l'utente inserisca un indirizzo email valido, mentre la validazione della password viene utilizzata per garantire che la password soddisfi i requisiti. Questo è un esempio preso dal codice di come vengono gestiti i dati:  
```python
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
    DataRequired(message='Email is required.'),
    Email(message='Invalid email address.'),
    Length(min=3, max=255, message='Email must be between 3 and 255 characters.')
])
password = PasswordField('Password', validators=[
    DataRequired(message='Password is required.'),
    Length(min=1, max=128, message='Password must be between 1 and 128 characters.')
])
# Altre validazioni per il nome, l'indirizzo, ecc.
```
* ### Transazioni nel Sistema

Le transazioni vengono utilizzate per garantire l'integrità dei dati durante le operazioni di aggiornamento o inserimento, assicurando che le modifiche siano eseguite in modo atomico e consistente. Nel contesto di un'applicazione web, una transazione consente di raggruppare più operazioni di database in un'unica unità di lavoro, assicurando che tutte le operazioni vengano completate con successo prima di confermare (commit) le modifiche nel database. Se una qualsiasi delle operazioni fallisce, tutte le modifiche vengono annullate (rollback), mantenendo il database in uno stato coerente.

#### Codice Python per la gestione delle transazioni

Ecco un esempio di gestione delle transazioni in Python, utilizzando SQLAlchemy all'interno di un'applicazione Flask:

```python
# in database.py 
# Funzione per ottenere una sessione del database
@contextmanager
def get_db_session():
    session = Session() # Crea una nuova sessione del database
    try:
        yield session # Restituisce la sessione del database all'applicazione per l'utilizzo
    finally:
        session.close()  # Chiude la sessione del database

# in routes.py
# Esempio di utilizzo delle transazioni per aggiungere un nuovo prodotto al database
@main_routes.route('/product/add', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_product():
    form = ProductForm()

    with get_db_session() as db_session: # Ottiene una sessione del database per l'operazione di aggiunta del prodotto 
        # Recupera i marchi e le categorie dal database

        if form.validate_on_submit():
            try:
            # Crea un nuovo prodotto con i dati del form
                session.commit()  # Conferma tutte le modifiche se nessuna eccezione viene sollevata
            except Exception as e:
                # Gestisce eventuali errori durante l'aggiunta del prodotto
                db_session.rollback()  # Rollback in caso di errore, annullando tutte le modifiche 
                flash(str(e), 'error')
                return redirect(url_for('main.add_product'))

            flash('Product added successfully!', 'success')
            return redirect(url_for('main.view_products_seller'))

    return render_template('add_product.html', form=form, brands=brands, categories=categories)
```
* ### **Trigger SQL nel Sistema**  
I trigger sono utilizzati nel database per garantire che l'integrità dei dati sia mantenuta durante le operazioni critiche come aggiornamenti, inserimenti e cancellazioni.   
Abbiamo optato per i seguetni trigger:
* **Assegnazione e Validazione del Ruolo**: Il trigger **trg_validate_and_assign_role** assegna automaticamente un ruolo predefinito agli utenti e impedisce l'assegnazione di ruoli non validi, garantendo che i dati degli utenti siano sempre corretti.
* **Gestione dell'Inventario**: Il trigger **trg_manage_inventory_on_order** gestisce automaticamente l'inventario, riducendo la quantità disponibile durante gli acquisti e ripristinandola in caso di cancellazione, prevenendo così vendite eccessive e garantendo la disponibilità corretta dei prodotti.
* **Aggiornamento Valutazione del Venditore**: Il trigger **trg_update_seller_rating** aggiorna automaticamente la valutazione media di un venditore in base alle recensioni dei suoi prodotti, aiutando a mantenere valutazioni accurate e aggiornate.
* **Aggiornamento Stato dell'Ordine**: Il trigger **trg_auto_update_order_status** aggiorna automaticamente lo stato degli ordini in base alle tempistiche, migliorando l'efficienza del flusso di lavoro degli ordini e riducendo la necessità di intervento manuale.
* **Prevenzione Cancellazione Prodotti**: Il trigger **trg_prevent_product_deletion_if_active_orders** impedisce la cancellazione di prodotti che hanno ordini attivi, proteggendo l'integrità dei dati e prevenendo errori di gestione dell'inventario.  

Di seguito viene illustrato illustrato il trigger **manage_inventory_on_order()**:

    
```sql
CREATE OR REPLACE FUNCTION manage_inventory_on_order() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.quantity > (SELECT quantity FROM products WHERE id = NEW.product_id) THEN
            RAISE EXCEPTION 'Insufficient inventory for product_id %', NEW.product_id;
        END IF;
        UPDATE products SET quantity = quantity - NEW.quantity WHERE id = NEW.product_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE products SET quantity = quantity + OLD.quantity WHERE id = OLD.product_id;
    ELSIF TG_OP = 'UPDATE' THEN
        IF NEW.quantity > OLD.quantity THEN
            IF (NEW.quantity - OLD.quantity) > (SELECT quantity FROM products WHERE id = NEW.product_id) THEN
                RAISE EXCEPTION 'Insufficient inventory for product_id %', NEW.product_id;
            END IF;
            UPDATE products SET quantity = quantity - (NEW.quantity - OLD.quantity) WHERE id = NEW.product_id;
        ELSIF NEW.quantity < OLD.quantity THEN
            UPDATE products SET quantity = quantity + (OLD.quantity - NEW.quantity) WHERE id = OLD.product_id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER manage_inventory_trigger
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION manage_inventory_on_order();
```
### Definizione di ruoli e politiche di autorizzazione

L'applicazione implementa un sistema di ruoli che distingue tra acquirenti, venditori e amministratori. Le politiche di autorizzazione sono definite per garantire che solo gli utenti con i permessi appropriati possano accedere a determinate funzionalità.

* **Acquirenti**: Possono visualizzare i prodotti, aggiungerli al carrello e completare gli acquisti.
* **Venditori**: Possono aggiungere, modificare e rimuovere i prodotti, nonché gestire gli ordini ricevuti.

### Uso di indici

L'applicazione utilizza indici su colonne frequentemente utilizzate, come `email` e `product_id`, per migliorare le prestazioni delle query.   
Ad esempio, la ricerca di prodotti o la verifica delle credenziali durante il login sono operazioni critiche che devono essere eseguite rapidamente, e l'uso di indici consente di ridurre significativamente i tempi di risposta.

* **Indice su email**: L'indice sull'email nella tabella users accelera le operazioni di autenticazione e recupero degli utenti.
* **Indice su seller_id**: Facilita la ricerca rapida dei prodotti per venditore, migliorando le prestazioni della gestione dell'inventario.

---

<a name="Sicurezza" /></a>

## Sicurezza

La sicurezza è una priorità fondamentale per l'applicazione, con diverse misure adottate per proteggere i dati e gli utenti da potenziali minacce.

- **Protezione delle Password**: Le password degli utenti sono crittografate utilizzando werkzeug.security, un algoritmo di hashing sicuro che protegge le credenziali degli utenti da attacchi di forza bruta.

- **Validazione dei Dati**: Tutti i dati inseriti dagli utenti sono validati per prevenire attacchi di tipo SQL injection e XSS. Inoltre, vengono utilizzati token CSRF per proteggere i form da attacchi CSRF.

- **Gestione delle Sessioni**: Le sessioni degli utenti sono gestite in modo sicuro utilizzando Flask-Login, che fornisce un sistema di autenticazione robusto e sicuro. Le sessioni vengono crittografate e firmate per prevenire attacchi di session hijacking.

- **Protezione da Sql Injection**: L'applicazione utilizza SQLAlchemy per interagire con il database, che offre una protezione integrata contro gli attacchi di SQL injection. Le query parametriche vengono utilizzate per evitare l'iniezione di codice SQL dannoso.

- **Protezione CSRF e Gestione dei Form**: Tutti i form dell'applicazione sono gestiti tramite Flask-WTF, che offre protezione contro attacchi CSRF. Questo è particolarmente importante in un'applicazione di e-commerce dove le transazioni devono essere sicure.

- **Sicurezza e Autenticazione**: L'applicazione utilizza Flask-Login per la gestione degli accessi in contemporanea con un sistema di ruoli che distingue tra acquirenti e venditori. Questo garantisce che solo gli utenti autorizzati possano accedere a determinate funzionalità.

---

<a name="Ulteriori-informazioni" /></a>

## Ulteriori informazioni

### Connessione al Database

Per la connessione al database, abbiamo utilizzato la seguente stringa di connessione:

```python
DATABASE_URL = 'postgresql://Progetto_owner:pQxVqHj8hG7R@ep-aged-snow-a24c6vx8.eu-central-1.aws.neon.tech/Progetto?sslmode=require'
```

Abbiamo optato per Neon Console, che ci ha permesso di avere un database  PostgreSQL online. Questo ha facilitato la collaborazione tra i membri del gruppo, consentendo a tutti e tre di lavorare insieme sullo stesso database in tempo reale.


---

<a name="Contributo-al-progetto-(appendice)"></a>

## Contributo al progetto (appendice)

Il progetto è stato sviluppato attraverso una collaborazione stretta e continua tra tutti i membri del team. Sebbene ciascuno di noi abbia avuto aree di responsabilità specifiche, spesso abbiamo lavorato insieme, supportandoci a vicenda nelle diverse fasi dello sviluppo.

* **Alessandro Sartori**: Ha avuto la responsabilità principale per il design del database, occupandosi della creazione dello schema logico e dell'implementazione delle query principali. Inoltre, ha curato gli aspetti legati alla sicurezza dell'applicazione, garantendo l'integrità e la protezione dei dati.
* **Federico Riato**: Ha guidato lo sviluppo del backend dell'applicazione, concentrandosi sull'implementazione delle API, sull'autenticazione e autorizzazione degli utenti, e sulla gestione dei prodotti all'interno del sistema.
* **Federico Vedovotto**: Ha svolto un ruolo chiave nello sviluppo del frontend, progettando e implementando le interfacce utente. È stato anche responsabile della gestione degli ordini e della procedura di checkout, assicurando un'esperienza utente fluida e intuitiva.

Abbiamo collaborato frequentemente, aiutandoci l'un l'altro nelle varie aree del progetto, lavorando insieme per superare le sfide e garantire la coerenza e l'efficacia complessiva dell'applicazione.

---

<a name="Considerazioni-Finali-e-Miglioramenti-Futuri"></a>

## Considerazioni Finali e Miglioramenti Futuri

Il progetto, pur essendo stato sviluppato con tecnologie robuste e ben integrate, potrebbe beneficiare di ulteriori miglioramenti, come l'implementazione di un sistema di caching per ridurre i tempi di caricamento delle pagine più pesanti. Un altro possibile miglioramento futuro è l'integrazione di sistemi di pagamento reali, utilizzando API come Stripe o PayPal, per rendere l'applicazione pronta per l'uso in ambienti di produzione. Inoltre, l'introduzione di un sistema di raccomandazione basato su machine learning potrebbe arricchire ulteriormente l'esperienza utente, offrendo suggerimenti personalizzati basati sulla cronologia degli acquisti e delle ricerche degli utenti.