# funzione con cui leggo le righe del file che contiene le operazioni. Ritorna una lista i cui elementi sono le righe in cui sono specificate le operazioni.
def read_file(filename):

    operations = []

    with open(filename) as f:

        lines = f.readlines()

    for line in lines:

        if line[0] == 'u':

            if line[-1] == '\n':

                line = line[:-1]

            operations.append(line)

    return operations


# procedura con cui vado a "splittare" i vari pezzi che compongono l'operazione (node_id := gen1 +(o * o - o /) gen2). Inoltre, vengono ricavati i genitori di ogni nodo.
def split(operations):

    for i in range (len(operations)):

        chars_of_operation = len(operations[i]) # serve per sapere da quanti caratteri è composta la stringa, così so quando fermarmi nell'individuare gen2.

        u = ''
        stop = False
        character = 0

        # trovo il node_id
        while(stop == False):

            character += 1

            if (operations[i][character] == '0' or
                operations[i][character] == '1' or
                operations[i][character] == '2' or
                operations[i][character] == '3' or
                operations[i][character] == '4' or
                operations[i][character] == '5' or
                operations[i][character] == '6' or
                operations[i][character] == '7' or
                operations[i][character] == '8' or
                operations[i][character] == '9'):

                u = u + operations[i][character]

            if (operations[i][character] == '='):
                stop = True

        nodes_id[i] = u

        stop = False

        gen1 = ''

        # trovo gen1 e l'operatore
        while (stop == False):

            character += 1

            if (operations[i][character] != ' ' and
                operations[i][character] != 'u' and
                operations[i][character] != '+' and
                operations[i][character] != '-' and
                operations[i][character] != '*' and
                operations[i][character] != '/'):

                gen1 = gen1 + operations[i][character]

            if (operations[i][character] == '+' or
                operations[i][character] == '-' or
                operations[i][character] == '*' or
                operations[i][character] == '/'):

                stop = True

        nodes_operator[i] = operations[i][character]
        nodes_parents[i][0] = gen1

        gen2 = ''

        # trovo gen2
        while (character < chars_of_operation - 1):

            character += 1

            if (operations[i][character] != ' ' and
                operations[i][character] != 'u'):

                gen2 = gen2 + operations[i][character]

        nodes_parents[i][1] = gen2


# funzione che ritorna l'indice di un determinato elemento della lista nodes_id.
def find_index(ids, value):

    for index in range(NODE_NUMBER):

        if ids[index] == value:

            return index


# funzione che ritorna il critical path relativo ad un nodo.
def find_nodes_critical_path(id,sons, depth):

    index = find_index(nodes_id, id)

    if len(sons[index]) > 0 and len(sons[index]) < 2: #ho solo 1 nodo figlio.

        depth += 1

        if sons[index][0] != nodes_id[-1]: # se il nodo figlio NON è il nodo di uscita

            depth = find_nodes_critical_path(sons[index][0],sons, depth) #chiamo ricorsivamente la funzione, andando ad esplorare il figlio del nodo che ho appena analizzato.

    elif len(sons[index]) >= 2: # ho 2 o più nodi figli, quindi il critical path relativo al nodo in questione sarà dato dal numero di nodi del percorso più lungo che mi porta al nodo di uscita.

        depth += 1

        tmp = depth # questa variabile temporanea serve per memorizzare il valore del critical path relativo al nodo al momento del bivio.
        temp_depth = [] # in questa lista vado andrò a salvare i possibili critical path, sulla base del percorso che viene seguito per arrivare al nodo di uscita.

        for son in sons[index]:

            depth = find_nodes_critical_path(son, sons, depth)
            temp_depth.append(depth)
            depth = tmp

        depth = max(temp_depth) # il critical path relativo al nodo in questione sarà dato dal massimo dei critical paths che ho inserito nella lista.

    return depth


# questa funzione ritorna, ogni volta che viene chiamata, la riga della tabella associata al passo i, e contiene la lista dei nodi pronti e la lista dei nodi che verranno schedulati durante quel passo.
def table(ids,parents,operators,status,cpaths,maxmult,maxadd,maxsot,maxdiv):

    # setto a 0 (pronto) i nodi che:
    for i in range(NODE_NUMBER):

        if status[i] == -1: # non sono ancora pronti e

            if((parents[i][0] not in ids and parents[i][1] not in ids) or # non hanno altri nodi come genitori o
                (parents[i][0] in ids and parents[i][1] in ids and status[find_index(ids,parents[i][0])] == 1 and status[find_index(ids,parents[i][1])] == 1) or # hanno entrambi i genitori (che sono anch'essi nodi) già stati schedulati o 
                (parents[i][0] in ids and status[find_index(ids,parents[i][0])] == 1 and parents[i][1] not in ids) or # hanno un genitore che non è un nodo e l'altro che è un nodo già schedulato o
                (parents[i][0] not in ids and parents[i][1] in ids and status[find_index(ids,parents[i][1])] == 1)): # viceversa

                status[i] = 0

    ready_nodes = [] # lista in cui verranno messi i nodi pronti al passo i.
    ready_nodes_to_show = []

    nmult = 0 # inizializzo a 0 il numero di addizioni che avò tra i nodi pronti
    nadd = 0 # inizializzo a 0 il numero di moltiplicazioni che avò tra i nodi pronti
    nsot = 0 # inizializzo a 0 il numero di sottrazioni che avò tra i nodi pronti
    ndiv = 0 # inizializzo a 0 il numero di divisioni che avò tra i nodi pronti

    for j in range(NODE_NUMBER):
        if status[j] == 0: # se il nodo è pronto

            ready_nodes.append(ids[j]) # lo aggiungo alla lista dei nodi pronti.
            ready_nodes_to_show.append("u" + str(ids[j]) + " (" + str(operators[j]) + ")" + " (C. PATH = " + str(cpaths[j]) + ")")

            if operators[j] == '+':

                nadd += 1

            elif operators[j] == '*':

                nmult += 1

            elif operators[j] == '-':

                nsot += 1

            else:

                ndiv += 1

    nodes_to_schedule = [] # questa lista conterrà i nodi da schedulare al passo i

    mults_to_schedule = [] # questa lista conterrà i nodi (*) pronti al passo i (non è detto che verranno effettivamente schedulati tutti)
    adds_to_schedule = [] # questa lista conterrà i nodi (+) pronti al passo i (non è detto che verranno effettivamente schedulati tutti)
    sotts_to_schedule = [] # questa lista conterrà i nodi (-) pronti al passo i (non è detto che verranno effettivamente schedulati tutti)
    divs_to_schedule = [] # questa lista conterrà i nodi (/) pronti al passo i (non è detto che verranno effettivamente schedulati tutti)

    # considero i nodi (*) pronti.
    if nmult > 0 and nmult <= int(maxmult): #se i nodi (*) pronti sono almeno 1, e meno di N_MULT (cioè i mult disponibili)

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '*':

                nodes_to_schedule.append("u" + node + " (*)")
                nodes_status[find_index(ids,node)] = 1 # setto lo stato del nodo a 1 (schedulato) 

    elif nmult > int(maxmult): # altrimenti, se i nodi (*) pronti sono più di N_MULT

        for node in ready_nodes: # per ogni nodo pronto

            if operators[find_index(ids,node)] == '*': # se è un nodo (*)

                mults_to_schedule.append(node) # lo aggiungo alla lista dei nodi (*) pronti.

        for t in range(int(maxmult)): # per N_MULT volte vado a selezionare il nodo (*) con critical path relativo più alto (nel caso di più nodi con critical path relativo uguale, viene selezionato prima quello più a "sinistra")

            tmp_max = -1
            tmp_id = -1

            for mult in mults_to_schedule:

                if cpaths[find_index(ids,mult)] > tmp_max: # se il critical path relativo del nodo che sto analizzando è > di quelli trovati finora

                    tmp_max = cpaths[find_index(ids,mult)] # lo assegno alla variabile temporanea del max_critical_path
                    tmp_id = mult # e assegno a questa altra variabile temporanea l'id del nodo.

            nodes_to_schedule.append("u" + tmp_id + " (*)")
            nodes_status[find_index(ids, tmp_id)] = 1 # setto lo stato del nodo a 1 (schedulato)
            mults_to_schedule.remove(tmp_id) # rimuovo il nodo appena schedulato dalla lista di quelli ancora da schedulare

    # considero i nodi (+) pronti (procedimento analogo al caso dei nodi (*))
    if nadd > 0 and nadd <= int(maxadd):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '+':

                nodes_to_schedule.append("u" + node + " (+)")
                nodes_status[find_index(ids,node)] = 1  

    elif nadd > int(maxadd):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '+':

                adds_to_schedule.append(node)

        for t in range(int(maxadd)):

            tmp_max = -1
            tmp_id = -1

            for add in adds_to_schedule:

                if cpaths[find_index(ids,add)] > tmp_max:

                    tmp_max = cpaths[find_index(ids,add)]
                    tmp_id = add

            nodes_to_schedule.append("u" + tmp_id + " (+)")
            nodes_status[find_index(ids, tmp_id)] = 1 
            adds_to_schedule.remove(tmp_id)

    # considero i nodi (-) pronti (procedimento analogo al caso dei nodi (*))
    if nsot > 0 and nsot <= int(maxsot):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '-':

                nodes_to_schedule.append("u" + node + " (-)")
                nodes_status[find_index(ids,node)] = 1  

    elif nsot > int(maxsot):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '-':

                sotts_to_schedule.append(node)

        for t in range(int(maxsot)):

            tmp_max = -1
            tmp_id = -1

            for sott in sotts_to_schedule:

                if cpaths[find_index(ids,sott)] > tmp_max:

                    tmp_max = cpaths[find_index(ids,sott)]
                    tmp_id = sott

            nodes_to_schedule.append("u" + tmp_id + " (-)")
            nodes_status[find_index(ids, tmp_id)] = 1 
            sotts_to_schedule.remove(tmp_id)

    # considero i nodi (/) pronti (procedimento analogo al caso dei nodi (*))
    if ndiv > 0 and ndiv <= int(maxdiv):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '/':

                nodes_to_schedule.append("u" + node + " (/)")
                nodes_status[find_index(ids,node)] = 1  

    elif ndiv > int(maxdiv):

        for node in ready_nodes:

            if operators[find_index(ids,node)] == '/':

                divs_to_schedule.append(node)

        for t in range(int(maxdiv)):

            tmp_max = -1
            tmp_id = -1

            for div in divs_to_schedule:

                if cpaths[find_index(ids,div)] > tmp_max:

                    tmp_max = cpaths[find_index(ids,div)]
                    tmp_id = div

            nodes_to_schedule.append("u" + tmp_id + " (/)")
            nodes_status[find_index(ids, tmp_id)] = 1 
            divs_to_schedule.remove(tmp_id)

    return [ready_nodes_to_show, nodes_to_schedule]   


# inizio    

file_to_read = input("Digitare il nome del file di configurazione desiderato (es. config1.txt)\n>>") # l'utente può decidere il file da usare, in cui sono specificate le operazioni.

operations_list = read_file(file_to_read) # leggo le operazioni dal file.

NODE_NUMBER = len(operations_list) # numero totale di operazioni/nodi u.
print("\nSono state lette", NODE_NUMBER, "operazioni.\n")

nodes_id = [-1 for i in range(NODE_NUMBER)] # inizializzo a -1 la lista contenente gli id dei nodi u.
nodes_parents = [[-1,-1] for i in range(NODE_NUMBER)] # inizializzo a -1 la lista di liste contenente i genitori dei rispettivi nodi.
nodes_sons = [[] for i in range(NODE_NUMBER)] # creo la lista di liste contenente i figli dei rispettivi nodi.
nodes_operator = [-1 for i in range(NODE_NUMBER)] # inizializzo a -1 la lista contenente gli operatori dei nodi.
nodes_status = [-1 for i in range(NODE_NUMBER)] # inizializzo a -1 la lista contenente gli stati dei nodi (-1 = non pronto; 0 = pronto; 1 = schedulato).
nodes_critical_paths = [0 for i in range(NODE_NUMBER)] # inizializzo a 0 la lista contenente i critical paths relativi dei nodi.

split(operations_list) # suddivido le operazioni nei vari campi.

# queste variabili mi indicheranno se durante l'algoritmo NON verranno eseguite determinate operazioni (se rimangono a 0, quell'operatore NON verrà utilizzato).
ad = 0
mu = 0
sot = 0
div = 0

if "*" in nodes_operator:

    mu = 1

if "+" in nodes_operator:

    ad = 1

if "-" in nodes_operator:

    sot = 1

if "/" in nodes_operator:

    div = 1


if mu == 0: #

    print("(Non sono eseguite moltiplicazioni durante l'algoritmo -> MULT = 0)\n") # avviso l'utente se non sono previste moltiplicazioni tra le operazioni.
    N_MULT = 0

else:

    N_MULT = input("Digitare il numero di MULT disponibili\n>>") # l'utente può decidere il numero massimo di moltiplicatori da usare.

if ad == 0:

    print("(Non sono eseguite addizioni durante l'algoritmo -> ADD = 0)") # avviso l'utente se non sono previste addizioni tra le operazioni.
    N_ADD = 0

else:

    N_ADD = input("Digitare il numero di ADD disponibili\n>>") # l'utente può decidere il numero massimo di adder da usare.

if sot == 0:

    print("(Non sono eseguite sottrazioni durante l'algoritmo -> SOTT = 0)") # avviso l'utente se non sono previste sottrazioni tra le operazioni.
    N_SOT = 0

else:

    N_SOT = input("Digitare il numero di SOTT disponibili\n>>") # l'utente può decidere il numero massimo di sottrattori da usare.

if div == 0:

    print("(Non sono eseguite divisioni durante l'algoritmo -> DIV = 0)") # avviso l'utente se non sono previste divisioni tra le operazioni.
    N_DIV = 0

else:

    N_DIV = input("Digitare il numero di DIV disponibili\n>>") # l'utente può decidere il numero massimo di divisori da usare.

print("\n\n")

for element in nodes_id:
    element = int(element)

print("NODES_ID =",nodes_id)
print("NODES_OPERATORS =""",nodes_operator)
print("NODES_STATUS =",nodes_status)
print("NODES_PARENTS =",nodes_parents)

# riempio la lista di liste che conterrà i figli di ogni nodo
for u in range(NODE_NUMBER):

    for couple in range(NODE_NUMBER):

        if nodes_id[u] in nodes_parents[couple]:

            nodes_sons[u].append(nodes_id[couple])


for list in nodes_sons:

    for element in list:

        element = int(element)
        
print("NODES_SONS =",nodes_sons)

i = 0

for node in nodes_id:

    d = 0
    nodes_critical_paths[i] = find_nodes_critical_path(node,nodes_sons,d)    
    i += 1

print("NODES__CRITICAL_PATHS =",nodes_critical_paths)

passo = 0

print("\n\nPASSO - LISTA NODI PRONTI - SCHEDULING\n")

while (nodes_status[-1] != 1):

    passo += 1
    
    print(passo,table(nodes_id,nodes_parents,nodes_operator,nodes_status,nodes_critical_paths,N_MULT,N_ADD,N_SOT,N_DIV))
    print("\n")

print("\nList Based Scheduling concluso.\n")
print("Sono necessari", passo, "cicli. (utilizzando",N_MULT,"MULT;",N_ADD,"ADD;",N_SOT,"SOTT;",N_DIV,"DIV)\n")