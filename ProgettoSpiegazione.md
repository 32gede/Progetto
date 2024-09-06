
### Python Flask Application Setup

Il codice fornito configura un'applicazione web Flask con varie estensioni come sessioni, autenticazione degli utenti e protezione contro attacchi CSRF. Ecco un'analisi dettagliata di ogni sezione.

```python
app = Flask(__name__, template_folder='templates')
app.jinja_env.autoescape = True
```
Un'istanza di Flask viene creata specificando la cartella dei template Jinja2. L'autoescape è abilitato per prevenire attacchi XSS.

```python
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```
Configura una cartella di caricamento per i file e verifica che la directory esista, creandola se necessario.

```python
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'
csrf = CSRFProtect(app)
Session(app)
```
La sessione è configurata per usare il filesystem, e viene impostata una chiave segreta per gestire le sessioni e proteggere le richieste tramite `CSRFProtect`.

---

#### Protezione contro CSRF (Cross-Site Request Forgery)
```python
app.config['SECRET_KEY'] = 'your_secret_key_here'
csrf = CSRFProtect(app)
```

##### Approfondimento: CSRFProtect
`CSRFProtect` è un'estensione di Flask utilizzata per proteggere le applicazioni da attacchi CSRF (Cross-Site Request Forgery). Gli attacchi CSRF avvengono quando un attaccante induce l'utente autenticato a inviare richieste non autorizzate a un'applicazione web in cui è loggato. L'estensione `CSRFProtect` genera e verifica un token di sicurezza unico per ogni sessione utente, che deve essere incluso in ogni richiesta POST, PUT, DELETE o PATCH. Questo token è invisibile all'utente finale, ma viene aggiunto automaticamente ai form HTML tramite `{{ csrf_token() }}` in Jinja2.

**Vantaggi:**
- Protezione automatica per tutte le route con metodi POST.
- Si integra facilmente con form e richieste AJAX.
- Prevenzione degli attacchi tramite richieste non intenzionali, garantendo che le richieste provengano da utenti legittimi.

---

L'estensione `Session` viene inizializzata per gestire le sessioni degli utenti.

```python
init_db()
```
La funzione `init_db()` viene chiamata per inizializzare il database e creare le tabelle necessarie.

```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'
```
`LoginManager` gestisce l'autenticazione degli utenti e reindirizza gli utenti non autenticati alla pagina di login, definita dalla route `'main.login'`.

```python
@login_manager.user_loader
def load_user(user_id):
    with get_db_session() as db_session:
        user = db_session.get(User, int(user_id))
        db_session.expunge(user)
        return user
```
La funzione `load_user` carica un utente dal database in base al suo ID, utilizzando una sessione del database e scollegando l'oggetto utente dopo il recupero.

```python
app.register_blueprint(main_routes)
```
Il blueprint delle route principali viene registrato, consentendo all'app di gestire le route definite nel modulo `main_routes`.
#### Utilizzo dei *Blueprint* in Flask
```python
app.register_blueprint(main_routes)
```

##### Approfondimento: Blueprint
In Flask, i *blueprint* sono un modo per organizzare e strutturare grandi applicazioni. Consentono di suddividere le funzionalità dell'applicazione in moduli logici e separati, come route, gestori di errori, filtri di template e altro ancora. Questo approccio rende il codice più modulare e facilmente manutenibile.

Un *blueprint* in Flask consente di definire componenti dell'applicazione che possono essere registrate successivamente sull'istanza principale di Flask. Ciò è utile per evitare di avere tutte le route e le logiche dell'applicazione in un unico file.

**Vantaggi dei *blueprint*:**
- Modularità: ogni parte dell'applicazione può essere separata e mantenuta indipendentemente.
- Riutilizzabilità: un *blueprint* può essere riutilizzato in più applicazioni Flask.
- Chiarezza: facilita la suddivisione di una grande applicazione in sottocomponenti logici come moduli di autenticazione, moduli di amministrazione, ecc.

**Esempio di utilizzo di un *blueprint*:**
Supponiamo di avere un modulo separato chiamato `main_routes.py` per gestire le route principali dell'applicazione:
```python
from flask import Blueprint

main_routes = Blueprint('main', __name__)

@main_routes.route('/login')
def login():
    return "Login Page"
```
Quindi, questo *blueprint* può essere registrato nell'applicazione principale:
```python
app.register_blueprint(main_routes, url_prefix='/main')
```
In questo esempio, tutte le route del *blueprint* `main_routes` saranno accessibili con il prefisso `/main`, quindi la pagina di login sarà accessibile tramite `/main/login`.

---

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```
Se il file viene eseguito direttamente, avvia il server Flask in modalità debug sull'host `0.0.0.0` e porta `5000`.

### Connessione al Database con SQLAlchemy

Il seguente codice imposta una connessione al database PostgreSQL usando SQLAlchemy.

```python
DATABASE_URL = 'postgresql://Progetto_owner:pQxVqHj8hG7R@ep-aged-snow-a24c6vx8.eu-central-1.aws.neon.tech/Progetto?sslmode=require'
```
Viene definita la URL di connessione al database PostgreSQL, includendo le credenziali e la modalità SSL.

```python
engine = sa.create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5
)
```
Viene creato un motore SQLAlchemy, con una dimensione massima della pool di connessioni pari a 10, con un overflow massimo di 5.

```python
Session = sessionmaker(bind=engine)
```
Viene configurata la classe `Session`, legata al motore creato in precedenza.

```python
@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
```
Questa funzione definisce un gestore di contesto per la gestione delle sessioni di database, che assicura che la sessione venga chiusa una volta completata l'operazione.

```python
def init_db():
    Base.metadata.create_all(engine)
```
La funzione `init_db` crea tutte le tabelle definite nel modello del database, assicurandosi che esistano nel database.

### Modelli SQLAlchemy

Il codice seguente definisce vari modelli SQLAlchemy che rappresentano entità nel sistema, come utenti, indirizzi, prodotti e ordini.

#### Modello `User`
Il modello `User` rappresenta un utente, con attributi come email, password e ruoli. Include metodi per la gestione delle password e la generazione di URL Gravatar.

```python
class User(UserMixin, Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
```
#### Gestione degli Utenti e Autenticazione con `UserMixin`
```python
class User(UserMixin, Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
```

##### Approfondimento: `UserMixin`
`UserMixin` è una classe di utilità fornita da Flask-Login per semplificare l'integrazione della gestione degli utenti nei modelli. Questa classe implementa quattro metodi fondamentali che Flask-Login si aspetta che il modello utente fornisca:
- `is_authenticated`: verifica se l'utente è autenticato.
- `is_active`: verifica se l'account dell'utente è attivo.
- `is_anonymous`: verifica se l'utente è anonimo.
- `get_id`: restituisce l'identificatore univoco dell'utente (ad esempio, il suo ID nel database).

Grazie a `UserMixin`, il modello `User` può utilizzare automaticamente questi metodi senza doverli implementare manualmente.

**Vantaggi:**
- Riduce il codice boilerplate per l'implementazione di sistemi di autenticazione.
- Semplifica la gestione dello stato degli utenti (ad esempio, se sono autenticati o meno).
- Si integra perfettamente con Flask-Login per la gestione delle sessioni degli utenti e il caricamento dinamico degli utenti tramite la funzione `@login_manager.user_loader`.

**Esempio di utilizzo:**
Con `UserMixin`, puoi facilmente verificare lo stato di un utente:
```python
if current_user.is_authenticated:
    # Azioni riservate agli utenti autenticati
```

---

#### Modello `Address`
Il modello `Address` rappresenta un indirizzo con campi come `address` e `city`. È collegato a utenti e ordini.

```python
class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
```

#### Modello `UserSeller`
Questo modello rappresenta il profilo di un venditore. Definisce relazioni tra il venditore, i prodotti e l'utente.

```python
class UserSeller(Base):
    __tablename__ = 'user_sellers'
    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    seller_rating: Mapped[int] = mapped_column(Integer, nullable=False)
```

#### Modello `Product`
Il modello `Product` rappresenta un prodotto nel sistema, con relazioni verso brand, categorie e recensioni.

```python
class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

#### Modello `Brand`
Il modello `Brand` rappresenta un marchio con una relazione ai prodotti.

```python
class Brand(Base):
    __tablename__ = 'brands'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

#### Modello `Category`
Il modello `Category` rappresenta una categoria, collegata ai prodotti.

```python
class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

#### Modello `Review`
Il modello `Review` rappresenta una recensione di un prodotto, con collegamenti agli utenti e ai prodotti.

```python
class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
```

#### Modello `CartItem`
Questo modello rappresenta un elemento nel carrello di un utente, collegato a prodotti e utenti.

```python
class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
```

#### Modello `Order`
Il modello `Order` rappresenta un ordine con dettagli come l'ID utente, il totale e lo stato. Include un metodo per aggiornare lo stato dell'ordine.

```python
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    
    def update_status_based_on_time(self):
        if self.status == 'Confermato' and self.confirmed_at:
            # Logica per aggiornare lo stato
```

#### Modello `OrderItem`
Rappresenta un articolo in un ordine, con relazioni al prodotto e all'ordine.

```python
class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
```

---

### Flask-WTF Forms: Analisi e Approfondimenti

Il codice presentato utilizza **Flask-WTF**, un'estensione che integra **WTForms** con **Flask**, per definire diversi moduli per una web application. Questi moduli gestiscono funzionalità come aggiunta di prodotti, autenticazione utente, registrazione, aggiornamento del profilo, gestione del carrello, conferma di ordini e ricerca di prodotti. Ecco un approfondimento delle varie classi di moduli.

---

### `ProductForm`: Modulo per Gestione Prodotti

```python
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=255)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=255)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01, max=1000000)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=1000000)])
    brand_id = StringField('Brand', validators=[DataRequired()])
    category_id = StringField('Category', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Add Product')
```

##### Approfondimento
Il modulo `ProductForm` è utilizzato per l'aggiunta o modifica di prodotti. Ogni campo ha dei **validatori** che assicurano l'inserimento corretto dei dati:
- `StringField` per nome e descrizione, con un **validator** di lunghezza per evitare nomi o descrizioni troppo brevi o lunghi.
- `DecimalField` per il prezzo, che deve essere un numero decimale tra un valore minimo e massimo.
- `IntegerField` per la quantità, che deve essere un numero intero positivo.
- `FileField` per l'immagine del prodotto, che limita i file accettati ai formati `.jpg`, `.jpeg`, e `.png` utilizzando `FileAllowed`.

---

### `LoginForm`: Modulo di Autenticazione Utente

```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=128)])
    submit = SubmitField('Sign in')
```

##### Approfondimento
Il modulo `LoginForm` gestisce l'autenticazione dell'utente. I validatori verificano:
- La presenza e la validità del formato dell'email (`Email()`).
- La presenza e la lunghezza minima della password (`DataRequired()`).

Questo modulo si integra con **Flask-Login** per la gestione delle sessioni di autenticazione.

---

### `RegistrationForm`: Modulo di Registrazione Utente

```python
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('seller', 'Seller'), ('buyer', 'Buyer')], validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=255)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=255)])
    city = StringField('City', validators=[Optional(), Length(min=2, max=255)])
    address = StringField('Address', validators=[Optional(), Length(min=2, max=255)])
    avatar_choice = SelectField('Avatar', choices=[('1yOOHEp8xJx7S_vbZmRe5K3nbia1XMVL6', 'Avatar 1'), ('1A8BXdiu2XE7FaAz8NmtYTYL4zYyIRsD7', 'Avatar 2')])
    submit = SubmitField('Register')
```

##### Approfondimento
Il modulo `RegistrationForm` include campi per registrare un nuovo utente. I campi principali includono:
- `Email` e `Password` con **validatori** che verificano la validità e assicurano che la password venga confermata correttamente con `EqualTo()`.
- Un campo di **ruolo** (`SelectField`) che permette all'utente di scegliere tra "venditore" o "compratore".
- I campi facoltativi `city` e `address` utilizzano `Optional()`, rendendo la loro compilazione non obbligatoria.

---

### `ProfileForm`: Modulo di Aggiornamento Profilo

```python
class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[Optional(), Length(min=2, max=255)])
    address = StringField('Address', validators=[Optional(), Length(min=2, max=255)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update Profile')
```

##### Approfondimento
Il modulo `ProfileForm` permette agli utenti di aggiornare il proprio profilo, compreso l'aggiornamento di informazioni come nome, username, avatar, città e indirizzo. Questo modulo utilizza **FileAllowed** per limitare il tipo di file accettato come avatar.

---

### `ReviewForm`: Modulo per le Recensioni

```python
class ReviewForm(FlaskForm):
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=3000)])
    submit = SubmitField('Submit')
```

##### Approfondimento
Il modulo `ReviewForm` permette agli utenti di lasciare una recensione di un prodotto. Viene utilizzato `NumberRange` per assicurare che la valutazione (`rating`) sia compresa tra 0 e 5, e `Length()` per limitare la lunghezza dei commenti.

---

### Moduli per il Carrello e Ordini

- **`AddToCartForm`**: consente di aggiungere prodotti al carrello, verificando che la quantità sia un numero intero positivo.
  
    ```python
    class AddToCartForm(FlaskForm):
        quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=1000000)])
        submit = SubmitField('Add to Cart')
    ```

- **`EditCartForm`**: consente di modificare la quantità dei prodotti nel carrello, con gli stessi vincoli di quantità validi.

    ```python
    class EditCartForm(FlaskForm):
        new_quantity = IntegerField('New Quantity', validators=[DataRequired(), NumberRange(min=1, max=1000000)])
        submit = SubmitField('Update')
    ```

- **`RemoveFromCartForm`**: permette di rimuovere un prodotto dal carrello con un semplice pulsante.

    ```python
    class RemoveFromCartForm(FlaskForm):
        submit = SubmitField('Remove')
    ```

---

### Altri Moduli Importanti

- **`ConfirmOrderForm`**: viene utilizzato per confermare un ordine.
  
    ```python
    class ConfirmOrderForm(FlaskForm):
        submit = SubmitField('Confirm Order')
    ```

- **`CheckoutForm`**: gestisce l'input di indirizzo e città durante il checkout.
  
    ```python
    class CheckoutForm(FlaskForm):
        address = StringField('Address', validators=[DataRequired()])
        city = StringField('City', validators=[DataRequired()])
        submit = SubmitField('Complete Order')
    ```

---

### Considerazioni sui Form in Flask-WTF
- **Validazione**: La validazione dei dati di input è fondamentale per garantire la correttezza delle informazioni inserite dagli utenti. Flask-WTF semplifica questo processo fornendo validatori predefiniti come `DataRequired`, `Length`, `Email`, e `NumberRange`.
- **Gestione dei File**: Con `FileAllowed` si possono limitare i formati di file che possono essere caricati, migliorando la sicurezza e l'affidabilità dell'applicazione.
- **Estensione**: Flask-WTF si integra perfettamente con WTForms, che consente di estendere la funzionalità dei moduli in modo flessibile e modulare.

Se hai bisogno di ulteriori chiarimenti o vuoi approfondire altre parti, fammi sapere!


### Analisi del Codice: `google.py` e `collegamento_google.py`

Il codice presentato contiene script Python che facilitano l'integrazione con le API di Google, specificamente Google Drive. Ecco un'analisi dettagliata e un approfondimento sulle principali funzionalità presenti in ciascun file.

---

### `google.py`: Creazione del Servizio Google API, Conversione di Date e Test di Connessione

#### 1. Funzione `Create_Service`: Creazione del Servizio API Google
La funzione `Create_Service` viene utilizzata per autenticarsi e interagire con le API di Google (ad esempio, Google Drive o Google Calendar).

##### Dettagli:
- **Parametri**: `client_secret_file`, `api_name`, `api_version`, e un elenco variabile di *scopes* (permettendo all'app di specificare i permessi necessari).
- **Processo**: 
  1. Controlla se esistono credenziali salvate in un file pickle (che memorizza dati serializzati).
  2. Se le credenziali non sono valide o non esistono, utilizza `InstalledAppFlow` per generare nuove credenziali.
  3. Salva le nuove credenziali in un file pickle.
  4. Restituisce un oggetto di servizio Google API per interagire con l'API specificata.

##### Esempio di Utilizzo:
Se vuoi creare un servizio per Google Drive, la funzione potrebbe essere chiamata come segue:
```python
service = Create_Service('credentials.json', 'drive', 'v3', ['https://www.googleapis.com/auth/drive'])
```

---

#### 2. Funzione `convert_to_RFC_datetime`: Conversione delle Date al Formato RFC 3339

Questa funzione è utile quando si interagisce con API di Google che richiedono le date nel formato RFC 3339 (ad esempio, Google Calendar).

##### Dettagli:
- **Parametri**: `year`, `month`, `day`, `hour`, e `minute`.
- **Processo**: Converte i valori della data forniti in una stringa conforme allo standard RFC 3339, che include data, ora e fuso orario.

##### Utilizzo:
Questo è particolarmente utile per garantire che le date siano sempre nel formato corretto quando si inviano richieste API. Ad esempio:
```python
rfc_datetime = convert_to_RFC_datetime(2023, 9, 6, 12, 30)
# Restituisce: "2023-09-06T12:30:00Z"
```

---

#### 3. Funzione `test_socket_connection`: Test della Connessione di Rete

Questa funzione verifica se è possibile stabilire una connessione socket al dominio `www.google.com` sulla porta 80 (HTTP).

##### Dettagli:
- **Processo**:
  1. Crea un socket e tenta di connettersi a `www.google.com`.
  2. Se la connessione riesce, stampa "Connection successful".
  3. Se fallisce, stampa l'errore della connessione.

##### Utilizzo:
Utile per testare rapidamente la connettività di rete prima di interagire con le API di Google. Ad esempio:
```python
test_socket_connection()
# Output: "Connection successful" oppure l'errore se la connessione fallisce.
```

---

### `collegamento_google.py`: Caricamento di Immagini su Google Drive

La funzione `carica_imm` è progettata per caricare un file su Google Drive e impostare i permessi per consentire a chiunque di visualizzarlo.

#### Processo Dettagliato:

1. **Impostazione dei Parametri**: 
   - `file_path`: il percorso del file da caricare.
   - `file_name`: il nome con cui il file sarà salvato su Google Drive.

2. **Autenticazione e Creazione del Servizio API**:
   - Utilizza la funzione `Create_Service` (definita nel file `google.py`) per creare un servizio Google Drive utilizzando le credenziali specificate nel file `credentials.json`.
   - Gli *scopes* richiesti includono `https://www.googleapis.com/auth/drive`, che consente l'accesso in scrittura su Google Drive.

3. **Caricamento del File**:
   - Viene determinato il tipo MIME (ad esempio, `image/png` o `image/jpeg`) in base all'estensione del file.
   - Viene creato un oggetto `MediaFileUpload` che rappresenta il file da caricare.
   - Il file viene caricato su Google Drive utilizzando il metodo `files().create`.

4. **Impostazione dei Permessi**:
   - Una volta caricato il file, vengono impostati i permessi affinché chiunque possa accedere e visualizzare il file (`role: 'reader'`, `type: 'anyone'`).

5. **Recupero del Link al File**:
   - Dopo l'upload, viene restituito il link per la visualizzazione del file su Google Drive.

##### Esempio di Utilizzo:
```python
file_id = carica_imm('/path/to/image.png', 'uploaded_image.png')
# Output: ID del file caricato su Google Drive
```

---

### Funzionamento Completo del Caricamento su Google Drive

1. **Esecuzione della funzione**:
   Quando chiami `carica_imm()`, l'immagine viene caricata su Google Drive nella cartella specificata da `folder_id`.

2. **Permessi del File**:
   Dopo aver caricato il file, il codice imposta i permessi di lettura pubblica. Questo è utile per scenari in cui vuoi condividere immagini o documenti pubblicamente senza dover gestire l'accesso manualmente su Google Drive.

---

### Esempio Completo: Caricamento di un'Immagine

Ecco un esempio completo del processo di caricamento di un'immagine su Google Drive:

```python
def carica_imm(file_path, file_name):
    print(f"Starting upload for {file_name} located at {file_path}")
    
    # Configurazione dell'API Google Drive
    CLIENT_SECRET_FILE = 'credential.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    if service is not None:
        folder_id = '1Hv34hUD0h4XOi74ETwjRFkiFIuJA-RJz'
        mime_type = 'image/png' if file_name.endswith('.png') else 'image/jpeg'
        
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_path, mimetype=mime_type)
        
        # Caricamento del file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        
        # Impostazione permessi
        permissions = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file_id,
            body=permissions
        ).execute()
        
        # Recupero del link
        file = service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()
        
        return file_id
    else:
        print("Failed to create Google API service.")
        return None
```

### Conclusione

Il codice fornito mostra come autenticarsi con le API di Google, caricare file su Google Drive e gestire le autorizzazioni. Le funzioni modulari per creare il servizio API e convertire date sono utili per diverse applicazioni, mentre `test_socket_connection` è una funzione rapida per verificare la connessione di rete.


### Flask Routes: Approfondimento e Analisi

Il codice presentato definisce le route per un'applicazione Flask. Viene utilizzata una combinazione di librerie per gestire varie funzionalità come autenticazione utenti, gestione dei prodotti e processi di acquisto. Le route sono organizzate tramite un `Blueprint` chiamato `main_routes`, che facilita la separazione del codice in moduli, migliorando la modularità e la manutenibilità.

---

### Blueprint e Organizzazione delle Route

```python
main_routes = Blueprint('main', __name__)
UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
```

#### Approfondimento: `Blueprint`
Un **Blueprint** in Flask consente di organizzare le route in moduli separati, utile per gestire applicazioni di grandi dimensioni. In questo caso, il blueprint `main_routes` viene utilizzato per definire le route principali dell'applicazione. Ogni route registrata nel blueprint può essere associata a una determinata parte del sito, come ad esempio la gestione utenti o prodotti.

**Vantaggi**:
- Facilita la suddivisione logica delle route.
- Rende il codice più modulare e scalabile.
- Permette di registrare lo stesso blueprint più volte con diversi prefissi URL, se necessario.

---

### Funzioni di Supporto per le Route

```python
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
```

#### Funzioni di gestione dei file:
- **`allowed_file()`**: verifica se il file caricato ha un'estensione tra quelle permesse.
- **`ensure_upload_folder()`**: assicura che la cartella di upload per gli avatar esista, creandola se necessario.

---

### Decoratore `role_required`: Controllo dell'Accesso Basato sui Ruoli

```python
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id' not in session:
                return redirect(url_for('main.login'))
            with get_db_session() as db_session:
                user = db_session.query(User).filter_by(id=session['id']).first()
                if user.role not in roles:
                    return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

#### Approfondimento: Controllo dell'accesso
Il decoratore `role_required` impone restrizioni di accesso alle route in base al ruolo dell'utente (ad esempio, "seller" o "buyer"). Utilizza un contesto di sessione per verificare il ruolo dell'utente e, se l'utente non ha il ruolo richiesto, lo reindirizza alla pagina principale.

**Vantaggi**:
- Controllo granulare dell'accesso alle funzionalità.
- Semplice integrazione con Flask-Login per la gestione delle sessioni e dei ruoli.

---

### Route Principali

#### Route per la Home e il Login
```python
@main_routes.route('/')
def index():
    update_order_status()
    if current_user.is_authenticated:
        ...
    return render_template('index.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        ...
    return render_template('login.html', form=form)
```

- **`index()`**: Aggiorna lo stato degli ordini e rende la pagina principale.
- **`login()`**: Gestisce il login dell'utente tramite il modulo `LoginForm`. Se il form viene validato correttamente, procede con l'autenticazione.

---

### Route per la Gestione dei Prodotti

#### Seller: Visualizzazione e Gestione Prodotti
```python
@main_routes.route('/seller/products')
@login_required
@role_required('seller')
def view_products_seller():
    form = ProductForm()
    with get_db_session() as db_session:
        products = db_session.query(Product).filter_by(seller_id=current_user.id).all()
    if not products:
        return render_template('products_seller.html', error="No products found.", form=form)
    return render_template('products_seller.html', products=products, form=form)
```

Questa route permette ai venditori di visualizzare i prodotti che hanno inserito:
- Usa il decoratore `@login_required` per assicurarsi che l'utente sia autenticato.
- Usa `@role_required('seller')` per permettere solo agli utenti con ruolo "seller" di accedere.

---

#### Buyer: Visualizzazione e Ricerca Prodotti
```python
@main_routes.route('/buyer/products')
@login_required
@role_required('buyer')
def view_products_buyer():
    form = SearchProductForm(request.args)
    with get_db_session() as db_session:
        products = db_session.query(Product).all()
        return render_template('products_buyer.html', products=products, form=form)
```

Questa route permette agli acquirenti di visualizzare e cercare prodotti:
- Implementa un modulo di ricerca (`SearchProductForm`) per filtrare i prodotti in base a diversi parametri.

---

### Route per le Recensioni

```python
@main_routes.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def view_reviews(product_id):
    form = ReviewForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if form.validate_on_submit():
            # Aggiungi la recensione
            ...
        reviews = sorted(product.reviews, key=lambda review: review.created_at, reverse=True)
        return render_template('view_reviews.html', product=product, reviews=reviews, form=form)
```

Questa route consente la visualizzazione e l'aggiunta di recensioni sui prodotti. Solo utenti autenticati con ruoli "buyer" o "seller" possono accedervi. Le recensioni vengono ordinate in base alla data di creazione.

---

### Route per il Carrello e gli Ordini

#### Visualizzazione del Carrello e Checkout
```python
@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    form = EditCartForm()
    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total, form=form)

@main_routes.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def checkout():
    form = CheckoutForm()
    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        if form.validate_on_submit():
            # Completa l'ordine
            ...
        user_buyer = db_session.query(User).filter_by(id=current_user.id).first()
    return render_template('checkout.html', cart_items=cart_items, user_buyer=user_buyer, form=form)
```

- **`cart()`**: Visualizza i prodotti nel carrello dell'utente.
- **`checkout()`**: Gestisce il processo di checkout, raccogliendo indirizzo e città dell'utente e finalizzando l'ordine.

---

### Route per la Ricerca e il Filtro di Prodotti

#### Filtro per Brand e Categorie
```python
@main_routes.route('/filter_brands', methods=['GET'])
@login_required
@role_required('buyer')
def filter_brands():
    form = FilterBrandsForm(request.args)
    if form.validate():
        # Logica di filtro per i brand
        ...
    else:
        return jsonify({'error': 'Invalid search term'}), 400

@main_routes.route('/filter_categories', methods=['GET'])
@login_required
@role_required('buyer')
def filter_categories():
    form = FilterCategoriesForm(request.args)
    if form.validate():
        # Logica di filtro per le categorie
        ...
    else:
        return jsonify({'error': 'Invalid search term'}), 400
```

Queste route permettono agli acquirenti di filtrare prodotti per marca o categoria, restituendo i risultati in formato JSON. Il modulo `FilterBrandsForm` e `FilterCategoriesForm` viene utilizzato per validare i termini di ricerca.

---

### Conclusione
Questo sistema di route utilizza una combinazione di **Blueprint**, decoratori come `login_required` e `role_required`, e Flask-WTF per gestire in modo efficiente l'accesso e la gestione delle funzionalità all'interno dell'applicazione. La modularità e l'organizzazione del codice tramite blueprint e decoratori garantiscono un'applicazione estensibile, sicura e facile da mantenere.
