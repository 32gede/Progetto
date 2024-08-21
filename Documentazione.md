# Documentazione del Progetto

## Introduzione
Questa applicazione è stata sviluppata come parte del progetto del corso di Basi di Dati. L'applicazione è una piattaforma di e-commerce che permette agli utenti di acquistare e vendere prodotti. La documentazione è strutturata come segue:
1. Introduzione
2. Funzionalità principali
3. Progettazione concettuale e logica della basi di dati
4. Query principali
5. Principali scelte progettuali
6. Ulteriori informazioni
7. Contributo al progetto (appendice)

## Funzionalità principali
L'applicazione fornisce le seguenti funzionalità principali:
- **Registrazione e autenticazione degli utenti**: Gli utenti possono registrarsi fornendo email, password e altre informazioni personali. Dopo la registrazione, possono autenticarsi utilizzando le loro credenziali.
- **Gestione del profilo utente**: Gli utenti possono aggiornare le loro informazioni personali, come nome, indirizzo e città.
- **Visualizzazione e ricerca di prodotti**: Gli utenti possono visualizzare i prodotti disponibili e cercare prodotti specifici utilizzando parole chiave.
- **Aggiunta di prodotti al carrello**: Gli utenti possono aggiungere prodotti al loro carrello per un acquisto successivo.
- **Completamento degli ordini**: Gli utenti possono completare l'acquisto dei prodotti nel loro carrello, generando un ordine.
- **Gestione degli ordini per venditori e acquirenti**: I venditori possono gestire gli ordini ricevuti e gli acquirenti possono visualizzare lo stato dei loro ordini.
- **Sistema di recensioni per i prodotti**: Gli utenti possono lasciare recensioni e valutazioni sui prodotti acquistati.

## Progettazione concettuale e logica della basi di dati
La progettazione della base di dati segue la notazione grafica introdotta nel Modulo 1 del corso. La base di dati è composta dalle seguenti tabelle principali:
- `users`: contiene le informazioni degli utenti
- `products`: contiene le informazioni dei prodotti
- `orders`: contiene le informazioni degli ordini
- `order_items`: contiene i dettagli degli articoli degli ordini
- `reviews`: contiene le recensioni dei prodotti

### Diagramma ER
![Diagramma ER](path/to/er_diagram.png)

### Schema Logico
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
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Query principali
Di seguito sono riportate alcune delle query più interessanti implementate nell'applicazione:

### Query per ottenere i prodotti di un venditore
```sql
SELECT * FROM products WHERE seller_id = :seller_id;
```

### Query per ottenere gli ordini di un utente
```sql
SELECT * FROM orders WHERE user_id = :user_id;
```

### Query per ottenere le recensioni di un prodotto
```sql
SELECT * FROM reviews WHERE product_id = :product_id;
```

## Principali scelte progettuali
### Politiche di integrità
- **Utilizzo di chiavi esterne**: Le chiavi esterne sono utilizzate per garantire l'integrità referenziale tra le tabelle. Ad esempio, `seller_id` in `products` è una chiave esterna che fa riferimento a `id` in `users`.
- **Validazione dei dati**: La validazione dei dati viene effettuata a livello di applicazione per garantire che i dati inseriti siano coerenti e validi. Ad esempio, la validazione dell'email e della password durante la registrazione.

### Definizione di ruoli e politiche di autorizzazione
- **Ruoli utente**: Sono stati definiti due ruoli principali: acquirente e venditore. Gli acquirenti possono cercare e acquistare prodotti, mentre i venditori possono aggiungere e gestire i loro prodotti.
- **Politiche di autorizzazione**: Le politiche di autorizzazione sono implementate per garantire che solo gli utenti autorizzati possano accedere a determinate funzionalità. Ad esempio, solo i venditori possono aggiungere nuovi prodotti.

### Uso di indici
- **Indici sulle colonne**: Sono stati creati indici sulle colonne frequentemente utilizzate nelle query per migliorare le prestazioni. Ad esempio, è stato creato un indice sulla colonna `email` della tabella `users` per velocizzare le ricerche degli utenti per email.

## Ulteriori informazioni
### Scelte tecnologiche
- **Linguaggio di programmazione**: Python
- **Framework web**: Flask
- **ORM**: SQLAlchemy
- **Database**: SQLite (per sviluppo e testing)

## Contributo al progetto (appendice)
- **Membro 1**: Design del database, implementazione delle query principali, documentazione.
- **Membro 2**: Sviluppo del backend, gestione dell'autenticazione e autorizzazione.
- **Membro 3**: Sviluppo del frontend, integrazione con il backend, test e debug.

Il codice del progetto è strutturato in modo da favorire la manutenzione e la leggibilità, con commenti appropriati e una chiara separazione delle responsabilità tra i vari moduli.
