# Analisi di Social Network Analysis (SNA) sui Trasferimenti di Giocatori di Calcio - Dataset Transfermarkt

## Introduzione

Questa repository contiene un'analisi dei trasferimenti di giocatori di calcio utilizzando tecniche di Social Network Analysis (SNA). L'obiettivo di queste analisi è studiare le dinamiche tra i club calcistici e comprendere meglio i flussi di giocatori tra di essi, identificando potenziali pattern di interconnessione, centralità e previsioni di nuovi trasferimenti.

## Principali analisi effettuate

1. **Costruzione del grafo dei trasferimenti**:
   Il grafo dei trasferimenti è stato costruito rappresentando ogni club calcistico come un nodo e ogni trasferimento di giocatore come un arco che collega due nodi. In particolare, i club italiani e "Svincolati" sono stati analizzati separatamente, per comprendere le dinamiche all'interno di specifici gruppi di club.

2. **Centralità dei nodi**:
   È stata calcolata la centralità di grado, la centralità di betweenness, la centralità di closeness e la centralità di eigenvector per ciascun club nel grafo. Queste misure ci aiutano a capire:
   - **Centralità di Grado**: I club più attivi nei trasferimenti, ovvero quelli con il maggior numero di connessioni (trasferimenti).
   - **Centralità di Betweenness**: I club che fungono da intermediari tra altri club, giocando un ruolo cruciale nei trasferimenti attraverso diverse reti.
   - **Centralità di Closeness**: I club che sono più vicini a tutti gli altri nel grafo, indicando quelli che possono influenzare maggiormente il flusso di trasferimenti.
   - **Centralità di Eigenvector**: I club con una forte connessione ai club più importanti e centralizzati, che potrebbero essere quelli che facilitano i trasferimenti di valore elevato.

3. **Analisi delle Clique**:
   Sono state individuate le *clique* nel grafo, cioè gruppi di club che sono altamente interconnessi tra loro tramite trasferimenti. L'individuazione delle clique ci permette di comprendere meglio le alleanze o i gruppi di club che collaborano più frequentemente tra di loro nei trasferimenti di giocatori.

4. **Previsione di nuovi trasferimenti**:
   Utilizzando le tecniche di similarità coseno sugli embedding dei club, sono stati identificati i club che potrebbero essere destinati a scambi di giocatori. L'analisi di similarità coseno tra i club ha aiutato a evidenziare i collegamenti potenziali non ancora avvenuti, ma che potrebbero verificarsi in futuro in base ai trasferimenti passati.

5. **Ego-Networks**:
   Sono state analizzate le ego-network, ovvero le reti di club che ruotano attorno a un nodo specifico (club). L'analisi delle ego-network fornisce una panoramica di come un club interagisce con i suoi vicini (altri club con cui ha effettuato trasferimenti), evidenziando la posizione e l'influenza di un club nel contesto dei trasferimenti.

6. **Visualizzazione dei trasferimenti più costosi**:
   È stata effettuata una visualizzazione dei trasferimenti più costosi, con l'aggiunta dei nomi dei giocatori sugli archi, per studiare i flussi finanziari tra i club e le tendenze nei trasferimenti di valore elevato. L'analisi si concentra su come i trasferimenti di alto valore influenzano la struttura della rete e i club coinvolti.

7. **Soglie di similarità per nuovi collegamenti**:
   Utilizzando una soglia di similarità predefinita, sono stati identificati i trasferimenti predetti tra club che non erano ancora avvenuti, ma che presentano una forte probabilità di essere realizzati in base ai dati storici dei trasferimenti e alle similarità tra i club.

## Come usare questo progetto

1. Clona il repository:
   ```bash
   git clone https://github.com/Andreavisi1/Trasfermarkt-Social-Network-Analysis
   ```
   
2. Installa le dipendenze necessarie:
   ```bash
   pip install -r requirements.txt
   ```

 3.	Esegui gli script per l’analisi dei trasferimenti. Gli script calcolano le metriche di centralità, le clique, le ego-network, e predicono i trasferimenti basandosi sulla similarità coseno tra i club.


## Conclusioni

Queste analisi di Social Network Analysis (SNA) sui trasferimenti di giocatori di calcio offrono una visione approfondita delle dinamiche tra club e dei flussi di giocatori all’interno e tra le reti calcistiche. Le informazioni derivanti da questa analisi possono essere utilizzate per migliorare la previsione dei trasferimenti futuri, ottimizzare le strategie di mercato dei club e capire meglio i collegamenti tra le squadre a livello globale.
