## Trigger

1. [ ] **Aggiornamento del livello di inventario**:
   - Quando viene effettuato un ordine, ridurre la quantità del prodotto ordinato dal livello di inventario.
   - Se un ordine viene annullato, ripristinare la quantità del prodotto nel livello di inventario.
   - Se un ordine viene rimborsato, ripristinare la quantità del prodotto nel livello di inventario.
   - Se un ordine viene cancellato, ripristinare la quantità del prodotto nel livello di inventario.

2. [ ] **Verifica del ruolo utente alla registrazione**:
   - Assicurarsi che il ruolo assegnato a un utente sia valido (es. 'buyer' o 'seller').
   - Assegnare automaticamente il ruolo di 'buyer' a un nuovo utente.
   - Assegnare automaticamente il ruolo di 'seller' a un nuovo utente che ha completato la registrazione come venditore.
   - Impedire agli utenti di registrarsi con ruoli non validi.
   - Impedire agli utenti di modificare il proprio ruolo.
   - Impedire agli utenti di eliminare il proprio account se ci sono ordini in corso.
   - Impedire agli utenti di eliminare il proprio account se ci sono prodotti in vendita.
   - Impedire agli utenti di eliminare il proprio account se ci sono pagamenti in sospeso.
   
3. [ ] **Aggiornamento della valutazione del venditore**:
   - Quando viene aggiunta una recensione per un prodotto, aggiornare la valutazione media del venditore.

4. [ ] **Aggiornamento della valutazione dell'acquirente**:
   - Quando un venditore lascia una valutazione per un acquirente (es. comportamento durante la transazione), aggiornare la valutazione media dell'acquirente.

5. [ ] **Notifiche sugli ordini**:
   - Inviare una notifica all'utente quando lo stato di un ordine viene aggiornato (es. da 'in lavorazione' a 'spedito').
   - Inviare una notifica all'utente quando un ordine viene consegnato.
   - Inviare una notifica all'utente quando un ordine viene annullato.
   - Inviare una notifica all'utente quando un ordine viene rimborsato.
   - Inviare una notifica all'utente quando un ordine viene cancellato.
   - Inviare una notifica all'utente quando un ordine viene completato.
   - Inviare una notifica all'utente quando un ordine viene pagato.
   - Inviare una notifica all'utente quando un ordine viene spedito.

6. [ ] **Rimozione di prodotti**:
   - Prima di eliminare un prodotto, verificare che non ci siano ordini in corso per quel prodotto. In caso affermativo, impedire la rimozione.
   - Prima di eliminare un prodotto, verificare che non ci siano recensioni associate a quel prodotto. In caso affermativo, impedire la rimozione.
   - Prima di eliminare un prodotto, verificare che non ci siano pagamenti in sospeso per quel prodotto. In caso affermativo, impedire la rimozione.
   - Prima di eliminare un prodotto, verificare che non ci siano prodotti in vendita associati a quel prodotto. In caso affermativo, impedire la rimozione.

7. [ ] **Verifica della disponibilità del prodotto**:
   - Prima di aggiungere un prodotto al carrello, verificare che il prodotto sia ancora disponibile in quantità sufficiente.
   - Prima di effettuare un ordine, verificare che tutti i prodotti siano ancora disponibili in quantità sufficiente.
   - Prima di effettuare un pagamento, verificare che tutti i prodotti siano ancora disponibili in quantità sufficiente.
   - Prima di effettuare un pagamento, verificare che il prezzo totale dell'ordine sia corretto.
   - Prima di effettuare un pagamento, verificare che l'indirizzo di fatturazione dell'utente sia valido.
   - Prima di effettuare un pagamento, verificare che l'indirizzo di spedizione dell'utente sia valido.
   - Prima di effettuare un pagamento, verificare che il metodo di pagamento dell'utente sia valido.
   - Prima di effettuare un pagamento, verificare che la valuta dell'importo totale dell'ordine sia corretta.
   - Prima di effettuare un pagamento, verificare che l'utente abbia abbastanza fondi per coprire l'importo totale dell'ordine.
   - Prima di effettuare un pagamento, verificare che l'utente abbia un credito sufficiente per coprire l'importo totale dell'ordine.

8. [ ] **Aggiornamento del prezzo del prodotto**: 
   - Quando il prezzo di un prodotto viene aggiornato, aggiornare il prezzo di tutti gli ordini che contengono quel prodotto.
   - Quando il prezzo di un prodotto viene aggiornato, aggiornare il prezzo di tutti i prodotti in vendita che corrispondono a quel prodotto.
   - Quando il prezzo di un prodotto viene aggiornato, aggiornare il prezzo di tutti i prodotti nel carrello che corrispondono a quel prodotto.
   - Quando il prezzo di un prodotto viene aggiornato, aggiornare il prezzo di tutti i prodotti nei pagamenti in sospeso che corrispondono a quel prodotto.

9. [ ] **Calcolo del totale ordine**:
   - Calcolare automaticamente l'importo totale di un ordine in base ai prodotti aggiunti al carrello.

10. [ ] **Notifiche di rimborso**:
    - Inviare una notifica all'utente quando viene emesso un rimborso per un ordine.
    - Inviare una notifica all'utente quando un ordine viene rimborsato.
    - Inviare una notifica all'utente quando un ordine viene annullato.
    - Inviare una notifica all'utente quando un ordine viene cancellato.
    - Inviare una notifica all'utente quando un ordine viene completato.
    - Inviare una notifica all'utente quando un ordine viene pagato.
    - Inviare una notifica all'utente quando un ordine viene spedito.
    - Inviare una notifica all'utente quando un ordine viene consegnato.

11. [ ] **Aggiornamento dello stato dell'ordine**:
    - Quando viene effettuato un pagamento, aggiornare lo stato dell'ordine da 'in attesa' a 'pagato'.
    - Quando un ordine viene spedito, aggiornare lo stato dell'ordine da 'pagato' a 'spedito'.
    - Quando un ordine viene consegnato, aggiornare lo stato dell'ordine da 'spedito' a 'consegnato'.
    - Quando un ordine viene rimborsato, aggiornare lo stato dell'ordine da 'pagato' a 'rimborsato'.
    - Quando un ordine viene annullato, aggiornare lo stato dell'ordine da 'pagato' a 'annullato'.
    - Quando un ordine viene cancellato, aggiornare lo stato dell'ordine da 'pagato' a 'cancellato'.
    - Quando un ordine viene completato, aggiornare lo stato dell'ordine da 'consegnato' a 'completato'.

12. [ ] **Controllo del limite di credito**:
    - Impedire agli utenti di effettuare ordini se superano il loro limite di credito.
    - Impedire agli utenti di effettuare pagamenti se superano il loro limite di credito.
    - Impedire agli utenti di effettuare ordini se superano il loro limite di credito.

13. [ ] **Calcolo del totale speso**:
    - Calcolare automaticamente l'importo totale speso da un utente in base ai suoi ordini.

14. [ ] **Aggiornamento dello stato del pagamento**:
    - Quando un ordine viene spedito, aggiornare lo stato del pagamento da 'in attesa' a 'completato'.
    - Se un ordine viene annullato, aggiornare lo stato del pagamento da 'in attesa' a 'annullato'.
    - Se un ordine viene consegnato, aggiornare lo stato del pagamento da 'completato' a 'consegnato'.
    - Se un ordine viene rimborsato, aggiornare lo stato del pagamento da 'completato' a 'rimborsato'.
    - Se un ordine viene cancellato, aggiornare lo stato del pagamento da 'completato' a 'cancellato'.

15. [ ] **Aggiornamento dello stato del prodotto**:
    - Quando un ordine viene spedito, aggiornare lo stato del prodotto da 'disponibile' a 'in transito'.
    - Quando un ordine viene consegnato, aggiornare lo stato del prodotto da 'in transito' a 'consegnato'.
    - Se un ordine viene cancellato, aggiornare lo stato del prodotto da 'in transito' a 'disponibile'.
    - Se un ordine viene rimborsato, aggiornare lo stato del prodotto da 'in transito' a 'disponibile'.
    - Se un ordine viene annullato, aggiornare lo stato del prodotto da 'in transito' a 'disponibile'.
    - Se un prodotto viene eliminato, aggiornare lo stato di tutti gli ordini che contengono quel prodotto a 'prodotto non disponibile'.

## Check Constraint

1. [ ] **Vincolo sul prezzo del prodotto**:
   1. [ ] Il prezzo di un prodotto deve essere maggiore di 0.
   2. [ ] Il prezzo di un prodotto non può superare un certo importo massimo.
   3. [ ] Il prezzo di un prodotto deve essere inferiore al prezzo di sconto.
   4. [ ] Il prezzo di un prodotto deve essere inferiore al prezzo di acquisto.
   5. [ ] Il prezzo di un prodotto deve essere inferiore al prezzo di spedizione.
   
2. [ ] **Vincolo sulla quantità del prodotto**:
   1. [ ] La quantità di un prodotto deve essere maggiore o uguale a 0.
   2. [ ] La quantità di un prodotto non può superare un certo limite massimo.

3. [ ] **Vincolo sull'indirizzo email dell'utente**:
   1. [ ] Assicurarsi che l'indirizzo email degli utenti sia univoco e rispetti il formato corretto.
   2. [ ] Assicurarsi che l'indirizzo email degli utenti sia associato a un dominio valido (es. gmail.com, yahoo.com).

4. [ ] **Vincolo sul ruolo dell'utente**:
   1. [ ] Il ruolo dell'utente deve essere uno tra 'buyer' e 'seller'.
   2. [ ] Gli utenti con ruolo 'buyer' devono avere un indirizzo di fatturazione valido.
   3. [ ] Gli utenti con ruolo 'seller' devono avere un indirizzo di spedizione valido.
   4. [ ] Gli utenti con ruolo 'buyer' devono avere un metodo di pagamento valido.
   5. [ ] Gli utenti con ruolo 'seller' devono avere un metodo di pagamento valido.

5. [ ] **Vincolo sulla valutazione del prodotto**:
   1. [ ] La valutazione di un prodotto deve essere compresa tra 1 e 5.
   2. [ ] La valutazione di un prodotto deve essere lasciata solo da acquirenti che hanno effettuato un ordine per quel prodotto.
   3. [ ] La valutazione di un prodotto deve essere accompagnata da una recensione.
   4. [ ] La valutazione di un prodotto deve essere unica per ogni acquirente.

6. [ ] **Vincolo sull'inventario**:
   - Il livello di inventario di un prodotto non può essere negativo.
   - Il livello di inventario di un prodotto non può superare un certo limite massimo.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono effettuati ordini.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono annullati ordini.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono rimborsati ordini.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono cancellati ordini.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono aggiunti prodotti in vendita.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono rimossi prodotti in vendita.
   - Il livello di inventario di un prodotto deve essere aggiornato automaticamente quando vengono eliminati i prodotti.

7. [ ] **Vincolo sull'importo dell'ordine**:
   - L'importo totale di un ordine deve essere maggiore di 0.
   - L'importo totale di un ordine deve corrispondere alla somma dei prezzi dei prodotti nel carrello.
   - L'importo totale di un ordine deve corrispondere alla somma dei prezzi dei prodotti nel carrello meno eventuali sconti più eventuali costi di spedizione meno eventuali tasse più eventuali commissioni meno eventuali crediti meno eventuali rimborsi.

8. [ ] **Vincolo sulla lunghezza della descrizione del prodotto**:
   - La descrizione del prodotto non può superare una certa lunghezza (es. 500 caratteri).
   - La descrizione del prodotto deve essere unica per ogni prodotto.
   - La descrizione del prodotto deve essere obbligatoria.
   - La descrizione del prodotto deve essere valida (es. non contenere caratteri speciali).
   - La descrizione del prodotto deve essere in un formato specifico (es. testo, HTML).
   - La descrizione del prodotto deve essere aggiornata automaticamente quando viene modificata la descrizione del prodotto.
   - La descrizione del prodotto deve essere aggiornata automaticamente quando viene eliminato il prodotto.
   - La descrizione del prodotto deve essere aggiornata automaticamente quando viene eliminata la categoria del prodotto.
   - La descrizione del prodotto deve essere aggiornata automaticamente quando viene aggiunta la categoria del prodotto.

9. [ ] **Vincolo sulla data dell'ordine**:
   - La data di un ordine non può essere nel futuro.
   - La data di un ordine deve essere inferiore alla data attuale.
   - La data di un ordine deve essere aggiornata automaticamente quando viene effettuato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene spedito un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene consegnato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene rimborsato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene annullato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene cancellato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene completato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene pagato un ordine.
   - La data di un ordine deve essere aggiornata automaticamente quando viene eliminato un ordine.

10. [ ] **Vincolo sulla categoria del prodotto**:
    - La categoria del prodotto deve esistere nella tabella delle categorie.
    - La categoria del prodotto deve essere obbligatoria.
    - La categoria del prodotto deve essere univoca per ogni prodotto.
    - La categoria del prodotto deve essere aggiornata automaticamente quando viene modificata la categoria del prodotto.
    - La categoria del prodotto deve essere aggiornata automaticamente quando viene eliminato il prodotto.
    - La categoria del prodotto deve essere aggiornata automaticamente quando viene eliminata la categoria del prodotto.
    - La categoria del prodotto deve essere aggiornata automaticamente quando viene aggiunta la categoria del prodotto.
    - La categoria del prodotto deve essere aggiornata automaticamente quando viene aggiunto il prodotto in vendita.

11. [ ] **Vincolo sullo stato dell'ordine**:
    - Lo stato di un ordine deve essere uno tra 'in attesa', 'in lavorazione', 'spedito', 'consegnato' o 'cancellato'.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene effettuato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene spedito un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene consegnato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene rimborsato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene annullato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene cancellato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene completato un ordine.
    - Lo stato di un ordine deve essere aggiornato automaticamente quando viene pagato un ordine.

12. [ ] **Vincolo sulle credenziali utente**:
    - Le credenziali degli utenti (es. password) devono rispettare determinati criteri di sicurezza (es. lunghezza minima, caratteri speciali).

13. [ ] **Vincolo sulla valuta del prezzo**:
    - Il prezzo di un prodotto deve essere espresso nella stessa valuta (es. USD, EUR).
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene modificata la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene eliminato il prodotto.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene eliminata la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiunta la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiunto il prodotto in vendita.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiornata la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiornato il prodotto in vendita.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiornata la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiornata la valuta del prezzo.
    - Il prezzo di un prodotto deve essere aggiornato automaticamente quando viene aggiornata la valuta del prezzo.

14. [ ] **Vincolo sulle recensioni**:
    - Le recensioni devono essere accompagnate da una valutazione e non possono essere lasciate dagli acquirenti per i propri prodotti.
    - Le recensioni devono essere aggiornate automaticamente quando viene aggiunta una recensione.
    - Le recensioni devono essere aggiornate automaticamente quando viene eliminata una recensione.
    - Le recensioni devono essere aggiornate automaticamente quando viene eliminato un prodotto.
    - Le recensioni devono essere aggiornate automaticamente quando viene eliminata la categoria del prodotto.
    - Le recensioni devono essere aggiornate automaticamente quando viene aggiunta la categoria del prodotto.
    - Le recensioni devono essere aggiornate automaticamente quando viene aggiunto il prodotto in vendita.