# Talk to Legends

**Talk to Legends** è un'applicazione web che ti permette di conversare con personaggi storici e leggende del passato. Utilizzando modelli linguistici avanzati (LLM), l'app simula le personalità, le conoscenze e gli stili comunicativi di figure iconiche per un'esperienza educativa e coinvolgente.

## 🚀 Funzionalità Principali

-   **Conversazioni con Leggende**: Scegli una figura storica (es. Einstein, Leonardo da Vinci) e inizia a chattare.
-   **Supporto Multilingua**: Interfaccia e conversazioni disponibili in diverse lingue (Italiano, Inglese, Francese, Tedesco).
-   **Configurazione LLM Flessibile**: Supporto per provider compatibili con l'API di OpenAI (Ollama, Regolo, OpenRouter).
-   **Formattazione Markdown**: Supporto completo per Markdown e GFM (GitHub Flavored Markdown) per messaggi ricchi di contenuto, tabelle e formattazione.
-   **Persistenza Sessione**: Le sessioni di chat sono identificate da UUID e possono essere riprese tramite URL dedicato.
-   **Interfaccia Personalizzabile**: Regolazione dinamica della dimensione del font per una lettura ottimale.


###  Docker e Docker Compose
Puoi avviare l'applicazione in due modi utilizzando i file di configurazione presenti nella root:

#### Con Docker Compose (Consigliato)
Questo comando builda e avvia l'intero stack (backend e frontend serviti tramite Caddy):
```bash
docker-compose up --build
```
L'app sarà disponibile all'indirizzo `http://localhost:8000`.

#### Con Docker (Manualmente)
Puoi buildare ed eseguire l'immagine direttamente:
```bash
# Build dell'immagine
docker build -t talk-to-legends .

# Avvio del container
docker run -p 8000:80 talk-to-legends
```

#### Da Docker Hub
L'immagine ufficiale è disponibile su Docker Hub. Puoi scaricarla ed eseguirla senza buildarla localmente:
```bash
# Pull dell'immagine da Docker Hub
docker pull fortyeightthousand/talk_to_legends:v1.0

# Avvio del container
docker run -p 8000:80 fortyeightthousand/talk_to_legends:v1.0
```

#### Con Docker Desktop
Se preferisci usare l'interfaccia grafica di **Docker Desktop** (disponibile per Windows, macOS e Linux), segui questi passaggi:

1. **Installa Docker Desktop**: scaricalo da [docker.com](https://www.docker.com/products/docker-desktop/) e avvialo.
2. **Cerca l'immagine**: nella barra di ricerca in alto seleziona la tab **Images** oppure **Docker Hub** e cerca `fortyeightthousand/talk_to_legends`.
3. **Pull dell'immagine**: clicca sul pulsante **Pull** in corrispondenza del tag `v1.0`.
4. **Avvia il container**:
   - Vai nella tab **Images** e individua `fortyeightthousand/talk_to_legends:v1.0`.
   - Clicca sul pulsante **Run** (icona ▶️).
   - Espandi la sezione **Optional settings** e configura:
     - **Container name**: `talk-to-legends` (opzionale).
     - **Host port**: `8000`.
     - **Container port**: `80`.
   - Clicca su **Run** per avviare il container.
5. **Verifica lo stato**: nella tab **Containers** vedrai il container in esecuzione. Da qui potrai avviarlo, fermarlo, visualizzare i log e accedere al terminale.

### 🌐 Avvio nel Browser
Una volta avviato il container (con uno qualsiasi dei metodi sopra descritti), apri il tuo browser e vai all'indirizzo:

```
http://localhost:8000
```

L'interfaccia di **Talk to Legends** sarà pronta per l'uso. Dalla barra laterale puoi configurare il provider LLM e iniziare a chattare con i personaggi storici.

---

## ⚙️ Configurazione LLM nell'App

Dall'interfaccia utente occorre configurare le impostazione dell'LLM tramite la barra laterale:
-   **LLM URL**: L'endpoint del servizio (es. `https://api.regolo.ai/v1`).
-   **LLM Model**: Il modello specifico da utilizzare (es. `gemma2-9b-it`).
-   **LLM API Key**: La chiave per l'autenticazione.

---

## 📄 Licenza

Questo progetto è distribuito sotto la licenza **Creative Commons Attribution-NonCommercial (CC BY-NC 4.0)**. 
Questa licenza permette l'uso, la condivisione e l'adattamento gratuito per scopi non commerciali, a condizione di attribuire correttamente la paternità all'autore originale.
