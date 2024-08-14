## Trigger

1. [ ] **Aggiornamento del livello di inventario**:
   - Quando viene effettuato un ordine, ridurre la quantità del prodotto ordinato dal livello di inventario.
   - Se un ordine viene annullato, ripristinare la quantità del prodotto nel livello di inventario.

2. [ ] **Verifica del ruolo utente alla registrazione**:
   - Assicurarsi che il ruolo assegnato a un utente sia valido (es. 'buyer' o 'seller').

3. [ ] **Aggiornamento della valutazione del venditore**:
   - Quando viene aggiunta una recensione per un prodotto, aggiornare la valutazione media del venditore.

4. [ ] **Aggiornamento della valutazione dell'acquirente**:
   - Quando un venditore lascia una valutazione per un acquirente (es. comportamento durante la transazione), aggiornare la valutazione media dell'acquirente.

5. [ ] **Notifiche sugli ordini**:
   - Inviare una notifica all'utente quando lo stato di un ordine viene aggiornato (es. da 'in lavorazione' a 'spedito').

6. [ ] **Rimozione di prodotti**:
   - Prima di eliminare un prodotto, verificare che non ci siano ordini in corso per quel prodotto. In caso affermativo, impedire la rimozione.

7. [ ] **Verifica della disponibilità del prodotto**:
   - Prima di aggiungere un prodotto al carrello, verificare che il prodotto sia ancora disponibile in quantità sufficiente.

8. [ ] **Aggiornamento del prezzo del prodotto**: 
   - Quando il prezzo di un prodotto viene aggiornato, aggiornare il prezzo di tutti gli ordini che contengono quel prodotto.

9. [ ] **Blocco di utenti inattivi**:
   - Disattivare automaticamente gli account utente che non sono stati utilizzati per un certo periodo di tempo.

10. [ ] **Calcolo del totale ordine**:
    - Calcolare automaticamente l'importo totale di un ordine in base ai prodotti aggiunti al carrello.

11. [ ] **Notifiche di rimborso**:
    - Inviare una notifica all'utente quando viene emesso un rimborso per un ordine.

12. [ ] **Aggiornamento dello stato dell'ordine**:
    - Quando viene effettuato un pagamento, aggiornare lo stato dell'ordine da 'in attesa' a 'pagato'.

13. [ ] **Controllo del limite di credito**:
    - Impedire agli utenti di effettuare ordini se superano il loro limite di credito.

14. [ ] **Calcolo del totale speso**:
    - Calcolare automaticamente l'importo totale speso da un utente in base ai suoi ordini.

15. [ ] 

## Check Constraint

1. [ ] **Vincolo sul prezzo del prodotto**:
   - Il prezzo di un prodotto deve essere maggiore di 0.

2. [ ] **Vincolo sulla quantità del prodotto**:
   - La quantità di un prodotto deve essere maggiore o uguale a 0.

3. [ ] **Vincolo sull'indirizzo email dell'utente**:
   - Assicurarsi che l'indirizzo email degli utenti sia univoco e rispetti il formato corretto.

4. [ ] **Vincolo sul ruolo dell'utente**:
   - Il ruolo dell'utente deve essere uno tra 'buyer' e 'seller'.

5. [ ] **Vincolo sulla valutazione del prodotto**:
   - La valutazione di un prodotto deve essere compresa tra 1 e 5.

6. [ ] **Vincolo sull'inventario**:
   - Il livello di inventario di un prodotto non può essere negativo.

7. [ ] **Vincolo sull'importo dell'ordine**:
   - L'importo totale di un ordine deve essere maggiore di 0.

8. [ ] **Vincolo sulla lunghezza della descrizione del prodotto**:
   - La descrizione del prodotto non può superare una certa lunghezza (es. 500 caratteri).

9. [ ] **Vincolo sulla data dell'ordine**:
   - La data di un ordine non può essere nel futuro.

10. [ ] **Vincolo sulla categoria del prodotto**:
    - La categoria del prodotto deve esistere nella tabella delle categorie.

11. [ ] **Vincolo sullo stato dell'ordine**:
    - Lo stato di un ordine deve essere uno tra 'in attesa', 'in lavorazione', 'spedito', 'consegnato' o 'cancellato'.

12. [ ] **Vincolo sulle credenziali utente**:
    - Le credenziali degli utenti (es. password) devono rispettare determinati criteri di sicurezza (es. lunghezza minima, caratteri speciali).

13. [ ] **Vincolo sulla valuta del prezzo**:
    - Il prezzo di un prodotto deve essere espresso nella stessa valuta (es. USD, EUR).

14. [ ] **Vincolo sulle recensioni**:
    - Le recensioni devono essere accompagnate da una valutazione e non possono essere lasciate dagli acquirenti per i propri prodotti.