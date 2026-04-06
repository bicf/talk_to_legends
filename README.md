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
