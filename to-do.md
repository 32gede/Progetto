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
4. [x] **Protezione CSRF (Cross-Site Request Forgery)**:
   1. [x] Utilizzare Flask-WTF per proteggere i form dalle attacchi CSRF.
   2. [x] Includere i token CSRF in tutti i form HTML.

## Gestione degli utenti

1. [x] **Registrazione degli utenti**: Implementare la funzionalità di registrazione che consente agli utenti di creare un account scegliendo tra i ruoli di buyer e seller.
2. [x] **Autenticazione degli utenti**: Implementare la funzionalità di login che consente agli utenti di accedere al proprio account.
3. [x] **Gestione dei profili**: Consentire agli utenti di aggiornare le informazioni del proprio profilo.
   2. [x] **Permettere di modificare nome**: Implementare la funzionalità per modificare il nome degli utenti.
   3. [ ] **Permettere di modificare cognome**: Implementare la funzionalità per modificare il cognome degli utenti.
   4. [x] **Permettere di modificare indirizzo**: Implementare la funzionalità per modificare l'indirizzo degli utenti.
   5. [x] **Permettere di modificare città**: Implementare la funzionalità per modificare la città degli utenti.
   14. [x] **Permettere di modificare immagine profilo**: Implementare la funzionalità per modificare l'immagine profilo degli utenti.
4. [ ] **Reset della password**: Implementare la funzionalità di reset della password per consentire agli utenti di recuperare l'accesso al proprio account.
5. [ ] **Permettere di eliminare account**: Implementare la funzionalità per eliminare l'account degli utenti.

## Gestione dei prodotti

1. [x] **Aggiungere prodotti**: Consentire ai venditori di aggiungere nuovi prodotti con tutte le informazioni necessarie (nome, descrizione, prezzo, quantità, brand, categoria).
2. [x] **Modificare prodotti**: Consentire ai venditori di modificare le informazioni dei prodotti esistenti.
3. [x] **Eliminare prodotti**: Consentire ai venditori di eliminare i propri prodotti.
4. [x] **Visualizzare prodotti**: Consentire a tutti gli utenti di visualizzare l'elenco dei prodotti disponibili.
5. [x] **Filtrare e ordinare prodotti**: Implementare la funzionalità di filtro e ordinamento dei prodotti per facilitare la ricerca agli utenti.
6. [x] **Immagine Prodotto**: Consentire ai venditori di aggiungere un'immagine per ciascun prodotto.
7. [x] **Gestione delle categorie**: Implementare un sistema di categorie per organizzare i prodotti e facilitare la navigazione.
8. [ ] **Prodotti in offerta**: Consentire ai venditori di contrassegnare i prodotti in offerta e visualizzarli in un'apposita sezione.
9. [ ] **Prodotti più venduti**: Implementare un sistema per tracciare i prodotti più venduti e visualizzarli in un'apposita sezione.
10. [ ] **Prodotti consigliati**: Implementare un sistema per suggerire prodotti in base agli acquisti precedenti o alle preferenze dell'utente.

## Ricerca e Filtri

1. [x] **Ricerca per parole chiave**: Implementare la ricerca dei prodotti basata su parole chiave che cercano nel nome e nella descrizione dei prodotti.
2. [x] **Filtri per attributi**: Implementare filtri basati su attributi come prezzo, brand, categoria, ecc.
3. [x] **Interfaccia di ricerca avanzata**: Creare un'interfaccia utente per la ricerca avanzata che consenta agli utenti di combinare vari criteri di ricerca e filtro
4. [ ] **Ricerca per recensioni**: Consentire agli utenti di cercare prodotti in base alle recensioni e alle valutazioni.
5. [ ] **Ricerca per venditori**: Implementare la ricerca di prodotti in base al venditore che li ha inseriti.

## Carrello della spesa

1. [x] **Aggiungere al carrello**: Consentire agli utenti di aggiungere prodotti al carrello della spesa.
2. [x] **Aggiornare quantità**: Consentire agli utenti di aggiornare la quantità dei prodotti nel carrello.
3. [x] **Rimuovere dal carrello**: Consentire agli utenti di rimuovere prodotti dal carrello.
4. [x] **Visualizzare il carrello**: Creare una pagina del carrello dove gli utenti possono vedere i prodotti aggiunti e il totale dell'ordine.
5. [x] **Procedere al pagamento**: Implementare la funzionalità di checkout per permettere agli utenti di finalizzare l'acquisto.
6. [ ] **Coupon e sconti**: Consentire agli utenti di applicare coupon e sconti durante il checkout.
7. [ ] **Spedizione e tasse**: Calcolare automaticamente le spese di spedizione e le tasse durante il checkout.
8. [x] **Salvare il carrello**: Consentire agli utenti di salvare il carrello per completare l'acquisto in un secondo momento.
10. [x] **Indirizzi di spedizione**: Consentire agli utenti di aggiungere e gestire diversi indirizzi di spedizione per gli ordini.
11. [ ] **Conferma dell'ordine**: Invia una conferma dell'ordine via email all'utente dopo il checkout.
13. [x] **Ordini salvati**: Consentire agli utenti di visualizzare e ripetere gli ordini salvati in precedenza.
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
5. [ ] **Recensioni con immagini**: Consentire agli utenti di aggiungere immagini alle recensioni per mostrare il prodotto in uso.

## Design del Database

1. [x] **Schema del database**: Progettare lo schema del database con tutte le tabelle necessarie (utenti, prodotti, carrelli, ordini, recensioni, ecc.).
2. [x] **Vincoli e chiavi esterne**: Definire vincoli di integrità e chiavi esterne per garantire la consistenza dei dati.
3. [x] **Trigger e transazioni**: Implementare trigger e transazioni per garantire l'integrità dei dati e automatizzare alcune operazioni (es. aggiornare le date di modifica).
4. [ ] **Ottimizzazione delle query**: Ottimizzare le query del database per migliorare le prestazioni e ridurre i tempi di risposta.
   1. [x] Utilizzare indici per velocizzare le query che coinvolgono colonne comuni.
   2. [x] Evitare le query nidificate e le query complesse che coinvolgono molte tabelle.
   3. [x] Utilizzare le transazioni per garantire la coerenza dei dati e prevenire problemi di concorrenza.
   4. [ ] Limitare il numero di record restituiti dalle query per ridurre il carico sul database.
   5. [ ] Utilizzare cache per memorizzare i risultati delle query frequenti e ridurre i tempi di risposta.
5. [x] **Backup e ripristino**: Implementare un sistema di backup e ripristino per proteggere i dati da perdite accidentali o danni.

## Front-end

1. [x] **Design responsivo**: Creare un design responsivo che funzioni bene su dispositivi desktop e mobili.
2. [x] **Framework CSS**: Utilizzare un framework CSS come Bootstrap per accelerare lo sviluppo del front-end.
3. [x] **JavaScript**: Utilizzare JavaScript per migliorare l'esperienza utente (es. aggiornamenti dinamici del carrello, conferme di azioni, ecc.).

## Performance

2. [x] **Indici**: Creare indici sulle colonne utilizzate più frequentemente nelle query per migliorare le prestazioni.
3. [ ] **Caching**: Implementare meccanismi di caching per ridurre il carico sul database e migliorare i tempi di risposta.

## Documentazione

1. [x] **Documentazione** del codice: Commentare il codice in modo chiaro e dettagliato.
