# Lista di cose da fare

Come segnare qualcosa di fatto:  
+ `1. [ ] **buyers**: possono leggere e guardare i vari prodotti e aggiungerli alla loro lista/carrello della spesa.` 
    1. [ ] **buyers**: possono leggere e guardare i vari prodotti e aggiungerli alla loro lista/carrello della spesa.
+ `1. [x] **buyers**: possono leggere e guardare i vari prodotti e aggiungerli alla loro lista/carrello della spesa.` 
    1. [x] **buyers**: possono leggere e guardare i vari prodotti e aggiungerli alla loro lista/carrello della spesa.


## Permessi

1. [x] **buyers**: possono leggere e guardare i vari prodotti e aggiungerli alla loro lista/carrello della spesa.
2. [x] **sellers**: stessi permessi dei buyers, però possono modificare i prodotti che vendono.
3. [x] **Implementare controlli di autorizzazione nei route**: Utilizzare decorator per controllare i permessi degli utenti e assicurarsi che solo gli utenti autorizzati possano accedere a certe funzionalità.

## Sicurezza

1. [x] **Protezione contro SQL Injection**: SQLAlchemy utilizza query parametrizzate per prevenire SQL Injection. Verifica che tutte le query utilizzino correttamente i binding dei parametri.
2. [x] **Protezione contro XSS (Cross-Site Scripting)**:
   1. [x] Sanitizzare l'input dell'utente e eseguire l'escape dei dati prima di renderizzarli sul client.
   2. [x] Utilizzare flask.escape per evitare che il contenuto potenzialmente pericoloso venga eseguito come codice HTML o JavaScript.
   3. [x] Verificare che tutti i template utilizzino correttamente l'escaping di Jinja2.
3. [x] **Autenticazione e Autorizzazione**:
   1. [x] Utilizzare password hash con werkzeug.security.
   2. [x] Implementare la gestione dei ruoli utente (buyer, seller) e controlli di accesso basati sui ruoli.
   3. [x] Creare decorator per login_required e role_required per proteggere le route.
4. [ ] **Protezione CSRF (Cross-Site Request Forgery)**:
   1. [ ] Utilizzare Flask-WTF per proteggere i form dalle attacchi CSRF.
   2. [ ] Includere i token CSRF in tutti i form HTML.
5. [ ] **Politiche di Sicurezza per Sessioni**:
   1. [ ] Configurare correttamente le opzioni delle sessioni in Flask: `SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=True, SESSION_COOKIE_SAMESITE='Lax'`.
6. [ ] **Utilizzo di HTTPS**:
   1. [ ] Assicurarsi che la tua applicazione sia servita tramite HTTPS per proteggere i dati in transito tra il client e il server.

## Gestione degli utenti

1. [x] **Registrazione degli utenti**: Implementare la funzionalità di registrazione che consente agli utenti di creare un account scegliendo tra i ruoli di buyer e seller.
2. [x] **Autenticazione degli utenti**: Implementare la funzionalità di login che consente agli utenti di accedere al proprio account.
3. [ ] **Gestione dei profili**: Consentire agli utenti di aggiornare le informazioni del proprio profilo.
4. [ ] **Reset della password**: Implementare la funzionalità di reset della password per consentire agli utenti di recuperare l'accesso al proprio account.

## Gestione dei prodotti

1. [x] **Aggiungere prodotti**: Consentire ai venditori di aggiungere nuovi prodotti con tutte le informazioni necessarie (nome, descrizione, prezzo, quantità, brand, categoria).
2. [x] **Modificare prodotti**: Consentire ai venditori di modificare le informazioni dei prodotti esistenti.
3. [x] **Eliminare prodotti**: Consentire ai venditori di eliminare i propri prodotti.
4. [x] **Visualizzare prodotti**: Consentire a tutti gli utenti di visualizzare l'elenco dei prodotti disponibili.
5. [x] **Filtrare e ordinare prodotti**: Implementare la funzionalità di filtro e ordinamento dei prodotti per facilitare la ricerca agli utenti.
6. [ ] **Immagine Prodotto**: Consentire ai venditori di aggiungere un'immagine per ciascun prodotto.

## Ricerca e Filtri

1. [x] **Ricerca per parole chiave**: Implementare la ricerca dei prodotti basata su parole chiave che cercano nel nome e nella descrizione dei prodotti.
2. [x] **Filtri per attributi**: Implementare filtri basati su attributi come prezzo, brand, categoria, ecc.
3. [x] **Interfaccia di ricerca avanzata**: Creare un'interfaccia utente per la ricerca avanzata che consenta agli utenti di combinare vari criteri di ricerca e filtro

## Carrello della spesa

1. [x] **Aggiungere al carrello**: Consentire agli utenti di aggiungere prodotti al carrello della spesa.
2. [x] **Aggiornare quantità**: Consentire agli utenti di aggiornare la quantità dei prodotti nel carrello.
3. [x] **Rimuovere dal carrello**: Consentire agli utenti di rimuovere prodotti dal carrello.
4. [x] **Visualizzare il carrello**: Creare una pagina del carrello dove gli utenti possono vedere i prodotti aggiunti e il totale dell'ordine.
5. [x] **Procedere al pagamento**: Implementare la funzionalità di checkout per permettere agli utenti di finalizzare l'acquisto.

## Gestione degli ordini

1. [X] **Creare ordini**: Implementare la funzionalità di creazione dell'ordine durante il checkout.
2. [x] **Visualizzare cronologia ordini**: Consentire agli utenti di visualizzare la cronologia dei propri ordini.
3. [ ] **Aggiornare stato dell'ordine**: Consentire ai venditori di aggiornare lo stato degli ordini dei prodotti che hanno venduto.
4. [ ] **Notifiche ordini**: Implementare un sistema di notifiche che informi gli utenti degli aggiornamenti sugli ordini (es. ordine spedito, ordine consegnato).

## Recensioni e Valutazioni

1. [x] **Aggiungere recensioni**: Consentire agli utenti di lasciare recensioni e valutazioni per i prodotti acquistati.
2. [x] **Moderare recensioni**: Consentire ai venditori di visualizzare e moderare le recensioni sui propri prodotti.
3. [ ] **Visualizzare valutazioni**: Visualizzare le valutazioni medie dei prodotti e consentire l'ordinamento dei prodotti in base alle valutazioni.

## Design del Database

1. [x] **Schema del database**: Progettare lo schema del database con tutte le tabelle necessarie (utenti, prodotti, carrelli, ordini, recensioni, ecc.).
2. [ ] **Vincoli e chiavi esterne**: Definire vincoli di integrità e chiavi esterne per garantire la consistenza dei dati.
3. [ ] **Trigger e transazioni**: Implementare trigger e transazioni per garantire l'integrità dei dati e automatizzare alcune operazioni (es. aggiornare le date di modifica).

## Front-end

1. [ ] **Design responsivo**: Creare un design responsivo che funzioni bene su dispositivi desktop e mobili.
2. [ ] **Framework CSS**: Utilizzare un framework CSS come Bootstrap per accelerare lo sviluppo del front-end.
3. [ ] **JavaScript**: Utilizzare JavaScript per migliorare l'esperienza utente (es. aggiornamenti dinamici del carrello, conferme di azioni, ecc.).

## Performance

2. [ ] **Indici**: Creare indici sulle colonne utilizzate più frequentemente nelle query per migliorare le prestazioni.
3. [ ] **Caching**: Implementare meccanismi di caching per ridurre il carico sul database e migliorare i tempi di risposta.

## Documentazione

1. [ ] **Documentazione** del codice: Commentare il codice in modo chiaro e dettagliato.
2. [ ] **Guide utente**: Creare guide utente per spiegare come utilizzare le funzionalità dell'applicazione.
3. [ ] **Guide per sviluppatori**: Creare documentazione per gli sviluppatori per facilitare la manutenzione e l'espansione del progetto.