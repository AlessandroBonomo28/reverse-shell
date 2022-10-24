# Reverse-shell
Reverse shell in python. Un client master può eseguire comandi sui client slave collegati al server  

# Istruzioni d'uso:
1) Avviare lo script bot-server
2) Avviare lo script bot-master-client sullo stesso computer su cui gira il server
3) Avviare lo script bot-client su un computer della rete locale e inserire l'indirizzo IP del server

# Script bot-server:
Ascolta sulla porta 12000. Quando riceve una connessione, se il client ha IP 127.0.0.1 (localhost), allora lo identifica
come MASTER, altrimenti, lo identifica come SLAVE e lo conserva in una lista. Il server mette a disposizione una serie di
comandi per il client MASTER:
- 'help': lista i comandi eseguibili su server 
- 'clients': stampa il numero di SLAVES connessi
- 'selnext': seleziona il prossimo client SLAVE nella lista
- 'sysinfo': richiede al client SLAVE selezionato di inviare informazioni sull'hardware
- 'closeslave': chiude la connessione con il client SLAVE selezionato e lo rimuove dalla lista
- 'exit': chiude la connessione con il client MASTER
## Il comando 'shellexec':
   shellexec è l'equivalente di una reverse shell: esegue un comando shell sul client SLAVE selezionato e stampa l'output. 
   #### SINTASSI
   La sintassi del comando è la seguente: 
   **shellexec -c '\<comando shell\>' \[-f\]** <br/>
   il parametro **-c** sta per command e prende come parametro il comando shell da eseguire sullo SLAVE selezionato
   il parametro **-f** è opzionale e permette di eseguire il fork del comando
   #### ESEMPI CON COMANDI UNIX:
   - shellexec -c 'cd' -> visualizza il path attuale
   - shellexec -c 'dir' -> visualizza il contenuto della dir corrente
   - shellexec -c 'dir C:\\' -> visualizza il contenuto della dir C:\\
   - shellexec -c 'mkdir folder1' -> crea una cartella di nome 'folder1'
   - shellexec -c 'echo hello > file.txt' -> crea un file di nome 'file.txt' e scrive 'hello' all'interno
   - shellexec -c 'type file.txt' -> visualizza il contenuto di 'file.txt'
   - shellexec -c 'shutdown -s -t 2' -> spegne il computer
   - shellexec -c 'shutdown /r' -> riavvia il computer
   - shellexec -c 'type NUL > out' -> crea un file vuoto di nome 'out'
   ###### Scrivere ed eseguire file bat
   1) shellexec -c 'echo riga 1 > file.bat' -> creo file bat e scrivo 'riga 1'
   2) shellexec -c 'echo riga 2 >> file.bat' -> scrivo in coda al file 'riga 2'
   3) shellexec -c 'echo riga 3 >> file.bat' -> scrivo in coda al file 'riga 3'
   4) shellexec -c 'file' -> eseguo file bat
   ###### Eseguire il fork di un programma
   - shellexec -c 'start /B notepad out' -f -> fork di notepad
   ###### Eseguire il fork di una finestra notepad con un messaggio all'interno
   1) shellexec -c 'echo SCRIVI QUI IL MESSAGGIO DEL NOTEPAD > out | start /B notepad out' -f
   2) shellexec -c 'del out' -> cancella il file temporaneo 'out'
   #### ESEMPI CON COMANDI LINUX:
   - shellexec -c 'cd' -> visualizza il path attuale
   - shellexec -c 'ls' -> visualizza il contenuto della dir corrente
   - shellexec -c 'ls -l' -> visualizza il contenuto della dir corrente con dettagli
   - shellexec -c 'echo hello > file.txt' -> crea un file di nome 'file.txt' e scrive 'hello' all'interno
   - shellexec -c 'cat file.txt' -> visualizza il contenuto di 'file.txt'

# Script bot-master-client:
Si collega alla socket 127.0.0.1:12000, invia comandi al server e stampa le risposte.
  
# Script bot-client:
Si collega all' indirizzo IP del server inserito da tastiera. Riceve comandi dal server, li esegue e invia una risposta. 
