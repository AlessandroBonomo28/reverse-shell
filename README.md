# Reverse-shell
reverse shell in python. Un client master può eseguire comandi sui client slave collegati al server  

# Istruzioni d'uso:
1) avviare lo script bot-server
2) avviare lo script bot-master-client sullo stesso computer su cui gira il server
3) avviare lo script bot-client su un computer della rete locale e inserire l'indirizzo IP del server

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
   La sintassi del comando è la seguente: *shellexec -c '<comando shell>'*
   il parametro -c sta per command e prende come parametro il comando shell da eseguire sullo SLAVE selezionato
   #### ESEMPI CON COMANDI UNIX:
   shellexec -c 'cd' -> visualizza il path attuale
   shellexec -c 'dir' -> visualizza il contenuto della dir corrente
   shellexec -c 'dir -d C:\' -> visualizza il contenuto della dir C:\
   shellexec -c 'echo -hello> -file.txt' -> crea un file di nome '-file.txt' e scrive '-hello' all'interno
   shellexec -c 'type -file.txt' -> visualizza il contenuto di '-file.txt'
   #### NOTE: 
   alcuni output di shellexec sono troppo grandi e vengono troncati. Alcune volte capita che il comando
   shellexec -c 'dir' invia un output che satura il buffer di ricezione. Quando il buffer è saturo i comandi
   successivi ricevono come risposta il continuo dell'output precedente. Quando succede bisogna eseguire il
   comando 'flush' finchè il server non torna a rispondere normalmente.
   #### ESEMPI CON COMANDI LINUX:
   shellexec -c 'cd' -> visualizza il path attuale
   shellexec -c 'ls' -> visualizza il contenuto della dir corrente
   shellexec -c 'ls -l' -> visualizza il contenuto della dir corrente con dettagli
   shellexec -c 'echo -hello> -file.txt' -> crea un file di nome '-file.txt' e scrive '-hello' all'interno
   shellexec -c 'cat -file.txt' -> visualizza il contenuto di '-file.txt'

# Script bot-master-client:
Si collega alla socket 127.0.0.1:12000, invia comandi al server e stampa le risposte.
  
# Script bot-client:
Si collega all' indirizzo IP del server, inserito da tastiera. Riceve comandi dal server, li esegue e invia una risposta. 
