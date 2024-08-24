## Trigger

1. [x] **Trigger per la validazione e assegnazione del ruolo**:
    - **Descrizione**: Questo trigger assegna automaticamente il ruolo di 'buyer' agli utenti che non specificano un ruolo durante l'inserimento o l'aggiornamento. Inoltre, verifica che il ruolo assegnato sia valido (deve essere uno tra 'buyer', 'seller', 'admin').
2. [x] **Trigger per la gestione dell'inventario sugli ordini**:
    - **Descrizione**: Questo trigger gestisce automaticamente l'inventario dei prodotti quando viene effettuato un ordine, annullato o modificato. Riduce la quantità disponibile del prodotto in caso di ordine, e la ripristina se l'ordine viene cancellato o modificato.
3. [x] **Trigger per aggiornare la valutazione del venditore**:
    - **Descrizione**: Questo trigger aggiorna la valutazione media del venditore ogni volta che viene inserita, aggiornata o eliminata una recensione relativa a uno dei prodotti del venditore.
4. [x] **Trigger per aggiornare automaticamente lo stato degli ordini**:
    - **Descrizione**: Questo trigger aggiorna automaticamente lo stato di un ordine da 'confirmed' a 'shipped' o 'delivered' in base alla data di conferma e al tempo trascorso.
5. [x] **Trigger per impedire la cancellazione dei prodotti con ordini attivi**:
    - **Descrizione**: Questo trigger impedisce la cancellazione di un prodotto se esistono ordini attivi associati a quel prodotto.

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