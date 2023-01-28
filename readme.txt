SEGUIRE QUESTE REGOLE E ISTRUZIONI NEL CASO SI VOGLIA CREARE UN NUOVO FILE DI CONFIGURAZIONE PERSONALIZZATO.


E' necessario che, all'interno del file di configurazione, i vari nodi abbiano un nome che inizia per 'u', e che questa sia seguita da un numero (senza spazi).
Inoltre, è richiesto che non ci siano spazi tra l'inizio della riga e la 'u'.

Esempi:

u1 := ... OK
u := ... NON OK
 u6 := ... NON OK

Dopo il secondo genitore, non è necessaria la punteggiatura.

Esempi:

... := a + b OK
... := a + b; da evitare

Le operazioni devono essere scritte ordinatamente in base alle dipendenze.

Esempi:

u1 := a * b 
u2 := u1 + c  OK

u1 := u2 + d
u2 := a * c  NON OK

L'ultimo nodo specificato deve essere il nodo di uscita (ossia il suo "node critical path" deve essere uguale a 0)