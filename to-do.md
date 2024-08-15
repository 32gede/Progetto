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
   1. [ ] **Permettere di modificare email**: Implementare la funzionalità per modificare l'email degli utenti.
   2. [ ] **Permettere di modificare ruolo**: Implementare la funzionalità per modificare il ruolo degli utenti.
   3. [ ] **Permettere di modificare nome**: Implementare la funzionalità per modificare il nome degli utenti.
   4. [ ] **Permettere di modificare cognome**: Implementare la funzionalità per modificare il cognome degli utenti.
   5. [ ] **Permettere di modificare indirizzo**: Implementare la funzionalità per modificare l'indirizzo degli utenti.
   6. [ ] **Permettere di modificare città**: Implementare la funzionalità per modificare la città degli utenti.
   7. [ ] **Permettere di modificare CAP**: Implementare la funzionalità per modificare il CAP degli utenti.
   8. [ ] **Permettere di modificare provincia**: Implementare la funzionalità per modificare la provincia degli utenti.
   9. [ ] **Permettere di modificare telefono**: Implementare la funzionalità per modificare il telefono degli utenti.
   10. [ ] **Permettere di modificare data di nascita**: Implementare la funzionalità per modificare la data di nascita degli utenti.
   11. [ ] **Permettere di modificare sesso**: Implementare la funzionalità per modificare il sesso degli utenti.
   12. [ ] **Permettere di modificare codice fiscale**: Implementare la funzionalità per modificare il codice fiscale degli utenti.
   13. [ ] **Permettere di modificare partita IVA**: Implementare la funzionalità per modificare la partita IVA degli utenti.
   14. [ ] **Permettere di modificare descrizione**: Implementare la funzionalità per modificare la descrizione degli utenti.
   15. [ ] **Permettere di modificare immagine profilo**: Implementare la funzionalità per modificare l'immagine profilo degli utenti.
4. [ ] **Reset della password**: Implementare la funzionalità di reset della password per consentire agli utenti di recuperare l'accesso al proprio account.
5. [ ] **Permettere di eliminare account**: Implementare la funzionalità per eliminare l'account degli utenti.

## Gestione dei prodotti

1. [x] **Aggiungere prodotti**: Consentire ai venditori di aggiungere nuovi prodotti con tutte le informazioni necessarie (nome, descrizione, prezzo, quantità, brand, categoria).
2. [x] **Modificare prodotti**: Consentire ai venditori di modificare le informazioni dei prodotti esistenti.
3. [x] **Eliminare prodotti**: Consentire ai venditori di eliminare i propri prodotti.
4. [x] **Visualizzare prodotti**: Consentire a tutti gli utenti di visualizzare l'elenco dei prodotti disponibili.
5. [x] **Filtrare e ordinare prodotti**: Implementare la funzionalità di filtro e ordinamento dei prodotti per facilitare la ricerca agli utenti.
6. [x] **Immagine Prodotto**: Consentire ai venditori di aggiungere un'immagine per ciascun prodotto.
7. [ ] **Gestione delle categorie**: Implementare un sistema di categorie per organizzare i prodotti e facilitare la navigazione.
8. [ ] **Prodotti in offerta**: Consentire ai venditori di contrassegnare i prodotti in offerta e visualizzarli in un'apposita sezione.
9. [ ] **Prodotti più venduti**: Implementare un sistema per tracciare i prodotti più venduti e visualizzarli in un'apposita sezione.
10. [ ] **Prodotti consigliati**: Implementare un sistema per suggerire prodotti in base agli acquisti precedenti o alle preferenze dell'utente.

## Ricerca e Filtri

1. [x] **Ricerca per parole chiave**: Implementare la ricerca dei prodotti basata su parole chiave che cercano nel nome e nella descrizione dei prodotti.
2. [x] **Filtri per attributi**: Implementare filtri basati su attributi come prezzo, brand, categoria, ecc.
3. [x] **Interfaccia di ricerca avanzata**: Creare un'interfaccia utente per la ricerca avanzata che consenta agli utenti di combinare vari criteri di ricerca e filtro
4. [ ] **Ricerca per recensioni**: Consentire agli utenti di cercare prodotti in base alle recensioni e alle valutazioni.
5. [ ] **Ricerca per venditori**: Implementare la ricerca di prodotti in base al venditore che li ha inseriti.
6. [ ] **Ricerca per località**: Consentire agli utenti di cercare prodotti in base alla loro posizione geografica.
7. [ ] **Ricerca fuzzy**: Implementare la ricerca fuzzy per correggere gli errori di battitura e restituire risultati simili.

## Carrello della spesa

1. [x] **Aggiungere al carrello**: Consentire agli utenti di aggiungere prodotti al carrello della spesa.
2. [x] **Aggiornare quantità**: Consentire agli utenti di aggiornare la quantità dei prodotti nel carrello.
3. [x] **Rimuovere dal carrello**: Consentire agli utenti di rimuovere prodotti dal carrello.
4. [x] **Visualizzare il carrello**: Creare una pagina del carrello dove gli utenti possono vedere i prodotti aggiunti e il totale dell'ordine.
5. [x] **Procedere al pagamento**: Implementare la funzionalità di checkout per permettere agli utenti di finalizzare l'acquisto.
6. [ ] **Coupon e sconti**: Consentire agli utenti di applicare coupon e sconti durante il checkout.
7. [ ] **Spedizione e tasse**: Calcolare automaticamente le spese di spedizione e le tasse durante il checkout.
8. [ ] **Salvare il carrello**: Consentire agli utenti di salvare il carrello per completare l'acquisto in un secondo momento.
9. [ ] **Pagamenti multipli**: Implementare la possibilità di effettuare pagamenti multipli (es. carta di credito, PayPal, bonifico bancario).
10. [ ] **Indirizzi di spedizione**: Consentire agli utenti di aggiungere e gestire diversi indirizzi di spedizione per gli ordini.
11. [ ] **Conferma dell'ordine**: Invia una conferma dell'ordine via email all'utente dopo il checkout.
12. [ ] **Notifiche di rimborso**: Invia notifiche agli utenti quando un ordine viene rimborsato o annullato.
13. [ ] **Ordini salvati**: Consentire agli utenti di visualizzare e ripetere gli ordini salvati in precedenza.
14. [ ] **Lista dei desideri**: Implementare una lista dei desideri per consentire agli utenti di salvare i prodotti per un acquisto futuro.

## Gestione degli ordini

1. [X] **Creare ordini**: Implementare la funzionalità di creazione dell'ordine durante il checkout.
2. [x] **Visualizzare cronologia ordini**: Consentire agli utenti di visualizzare la cronologia dei propri ordini.
3. [X] **Aggiornare stato dell'ordine**: Consentire ai venditori di aggiornare lo stato degli ordini dei prodotti che hanno venduto.
4. [X] **Notifiche ordini**: Implementare un sistema di notifiche che informi gli utenti degli aggiornamenti sugli ordini (es. ordine spedito, ordine consegnato).

## Recensioni e Valutazioni

1. [x] **Aggiungere recensioni**: Consentire agli utenti di lasciare recensioni e valutazioni per i prodotti acquistati.
2. [x] **Moderare recensioni**: Consentire ai venditori di visualizzare e moderare le recensioni sui propri prodotti.
3. [ ] **Visualizzare valutazioni**: Visualizzare le valutazioni medie dei prodotti e consentire l'ordinamento dei prodotti in base alle valutazioni.
4. [ ] **Risposte alle recensioni**: Consentire ai venditori di rispondere alle recensioni dei clienti per fornire feedback o risolvere eventuali problemi.
5. [ ] **Recensioni anonime**: Implementare la possibilità per gli utenti di lasciare recensioni in forma anonima.
6. [ ] **Segnalare recensioni**: Consentire agli utenti di segnalare recensioni inappropriate o fuorvianti.
7. [ ] **Recensioni verificate**: Implementare un sistema per verificare che le recensioni siano state effettivamente scritte da clienti che hanno acquistato il prodotto.
8. [ ] **Valutazioni per venditori**: Consentire agli acquirenti di valutare i venditori e lasciare feedback sulla loro esperienza complessiva.
9. [ ] **Recensioni più utili**: Implementare un sistema per votare le recensioni più utili e visualizzare le recensioni più votate in cima all'elenco.
10. [ ] **Recensioni con immagini**: Consentire agli utenti di aggiungere immagini alle recensioni per mostrare il prodotto in uso.
11. [ ] **Problema rimozione recensioni**: Problema quando c'è solo una recensione, divisione per 0.

## Design del Database

1. [x] **Schema del database**: Progettare lo schema del database con tutte le tabelle necessarie (utenti, prodotti, carrelli, ordini, recensioni, ecc.).
2. [ ] **Vincoli e chiavi esterne**: Definire vincoli di integrità e chiavi esterne per garantire la consistenza dei dati.
3. [ ] **Trigger e transazioni**: Implementare trigger e transazioni per garantire l'integrità dei dati e automatizzare alcune operazioni (es. aggiornare le date di modifica).
4. [ ] **Ottimizzazione delle query**: Ottimizzare le query del database per migliorare le prestazioni e ridurre i tempi di risposta.
   1. [ ] Utilizzare EXPLAIN per analizzare le query e identificare le aree di miglioramento.
   2. [ ] Utilizzare indici per velocizzare le query che coinvolgono colonne comuni.
   3. [ ] Evitare le query nidificate e le query complesse che coinvolgono molte tabelle.
   4. [ ] Utilizzare le transazioni per garantire la coerenza dei dati e prevenire problemi di concorrenza.
   5. [ ] Limitare il numero di record restituiti dalle query per ridurre il carico sul database.
   6. [ ] Utilizzare cache per memorizzare i risultati delle query frequenti e ridurre i tempi di risposta.
5. [ ] **Backup e ripristino**: Implementare un sistema di backup e ripristino per proteggere i dati da perdite accidentali o danni.

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