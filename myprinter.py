class Printer():
    """Formatta e stampa tipi di dati"""
    def __init__(self):
        pass
    def print_bytes(self, stdout:IO[bytes]) -> None:
        """Stampa uno stream di bytes riga per riga
        
        Args:
        -------
            stdout : IO[bytes]       
        """
        while True:
            line = stdout.readline()
            if not line:
                break
            
            print((str(line.rstrip())[2:-1]))