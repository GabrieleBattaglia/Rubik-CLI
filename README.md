# Rubik-CLI
This is my attempt to make an accessible Rubik cube for blind players.

## Se esegui lo script Python, assicurati di avere GBUtils.py nella stessa cartella. Puoi scaricarlo dall'omonimo progetto su GitHub.

# Manuale d'uso di Rubik Accessibile, di Gabriele Battaglia.

Indice.

1. Introduzione.
2. Cos'e' il cubo di Rubik.
3. L'applicazione.
3.1. Il prompt dei comandi.
3.2. I menu' dell'applicazione.
4. Guida alla risoluzione del cubo di Rubik.

## 1. Introduzione.
Grazie per aver deciso di giocare con Rubik Accessibile!
Tranquilli, tranquilli: conosco l'avversione dei piu' per tutto cio' che anche
vagamente, assomiglia ad un manuale, ad una guida o ad un libretto delle
istruzioni. Percio' saro' clemente e mi impegnero' per scrivere
l'indispensabile, ma in maniera chiara e precisa. Se seguirai queste poche
indicazioni, non avrai problemi ad usare quest'app e sono certo che 
riuscirai a divertirti con Rubik, il primo cubo di Rubik, completamente 
accessibile ed in italiano.
Buon divertimento. Gabriele Battaglia.

Ti ricordo che questa guida puo'essere letta anche al di fuori
dell'applicazione aprendo, col tuo editor di testi preferito, il file
README.md che dovresti poter trovare assieme all'eseguibile. Se cosi'
non fosse, ti invito a scrivermi per riceverne una copia a: iz4apu@libero.it

## 2. Cos'e' il cubo di Rubik?
Inventato dal professor Erno Rubik alla fine degli anni 70, il cubo in 
oggetto, anche chiamato cubo magico e' uno dei rompicapi piu' famosi al mondo. 
Si tratta di una figura geometrica tridimensionale, di lati uguali, a 6 facce. 
Ogni faccia e' suddivisa in 9 quadratini colorati, disposti come i numeri di 
una tastiera telefonica: 3 file da 3 cubetti ciascuna. 
Queste file di cubetti sia in verticale che in orizzontale, possono ruotare 
cambiando cosi' faccia. All'inizio ogni faccia ha 9 cubetti tutti del medesimo 
colore, dopo che il cubo e' stato mescolato, i cubetti saranno di colori 
diversi; risolvere il cubo, significa riportare tutti i cubetti di colore 
uguale, su tutte le 6 facce del cubo. 
L'abilita' del risolutore sta, dapprima nel riuscirci, ed in secondo luogo, 
nel riuscirci in fretta. L'app che stai provando terra' per te i tempi di 
risoluzione e ti permettera' di entrare in una speciale Top Ten, quando avrai 
portato a termine il cubo. 
Esistono vari algoritmi di risoluzione. Piu' avanti in questa guida, te ne 
proporro' uno preso dal sito wikihow che spero possa esserti utile, ma ti 
ricordo che molto altro materiale e' reperibile in rete cercando con i motori 
di ricerca, oppure su Youtube. 

## 3. L'applicazione.
Questo programma e' strutturato per funzionare da terminale, o da console, un 
altro modo per dirlo e', da prompt dei comandi, o dalla Shell di Windows. 
La sua accessibilita' dovrebbe essere totale, nella misura in cui lo screen 
reader che stai usando e' in grado di leggere questo tipo di finestre a testo 
che scorre. Io ho testato personalmente NVDA 2017.3, Jaws e VoiceOver su MacOS 
10.13 e funzionano molto bene, con qualche problema in piu' per VoiceOver ma 
nulla di particolarmente serio. Il programma e' stato scritto interamente dal 
sottoscritto usando Python 2.7 e NotePad++, sotto Windows 10. 
Una premessa per chi, come te, si accinge a giocare per la prima volta. 
L'applicazione presenta un numero abbastanza importante di comandi da 
tastiera, le informazioni da considerare sono notevoli ed il cubo di Rubik, 
esso stesso, e' per sua natura... un rompicapo. Percio' fin da ora mi sento di 
poterti consigliare un po di pazienza. Dai il tempo a te stesso di 
famigliarizzare con i concetti del gioco e con i comandi dell'applicazione, 
non mollare subito, se all'inizio tutto ti sembra un po confuso. Il programma 
e' scritto secondo una logica pensata a lungo, provata, ripensata e corretta; 
ogni scelta che ho fatto ha un suo senso il quale, sebbene possa non essere 
chiaro subito, non manchera' di manifestarsi, se gli concederai la 
possibilita' 
Inoltre, per qualsiasi domanda, dubbio, richiesta o insulto, sono a tua 
disposizione via mail, trovi l'indirizzo qui sopra, nell'introduzione della 
presente guida. 

Vediamo percio' di conoscere quest'applicazione da vicino, vediamo cosa fa e 
cosa le si puo' chiedere. Secondo me, il modo migliore di spiegarla e' quello 
di partire dal suo menu'. I dettagli, dove necessario, saranno aggiunti via 
via che li si incontra. 

L'applicazione puo' essere lanciata scrivendo rubik.py dal prompt dei comandi, 
se sei in possesso dei sorgenti, oppure rubik.exe, se hai l'eseguibile. 
Rubik Accessibile, come prima cosa, controllera' nella propria cartella: se 
trovera' il file rubik.dat, lo carichera' e ti consentira' di riprendere la 
partita in corso, in caso contrario invece, inizializzera' un cubo tutto nuovo 
fiammante e presentera' a schermo il prompt di attesa comandi. Direi che 
questo e' il tuo caso, se non hai mai lanciato l'app, prima. 
Ricordati che, qual'ora volessi tornare a questa condizione iniziale, ti 
bastera' cancellare dalla cartella di Rubik, il file con estensione ".dat". 

### 3.1. Il prompt dei comandi.
Il prompt dei comandi e' una riga di testo, generalmente una frase, una 
parola, un codice che l'applicazione mostra all'utente come ultima riga dello 
schermo, solitamente seguita dal cursore. Il suo significato e' sono qui, sono 
pronta per te, dimmi cosa fare. 
Anche Rubik accessibile ha il suo prompt. All'inizio probabilmente esso 
apparira' cosi': 

PC 100% M0>

PC significa percentuale completata, e siccome il cubo e' nuovo fiammante, 
indica completato! Chissa' se riuscirai a rivedere questo magico numero... 
dopo averlo mescolato! 
M0 invece, indica che sei alla mossa 0, cioe' che ancora non hai toccato 
nulla. Questo indicatore salira' di una unita', ogni volta che sposterai una 
fila di cubetti o che ruoterai una faccia del cubo. 
Concludendo, quando vedi il prompt in attesa di comandi, vuol dire che va 
tutto bene, che l'applicazione e' li', in tuo potere, pronta a scattare ad 
ogni tuo minimo comando. 
Quale sara' allora il tuo primo comando? Niente di piu' utile del chiederle: 
"Cosa sai fare?" 

### 3.2. I menu' dell'applicazione.
E chiediamoglielo quindi, facciamolo tramite il comando m di menu'. Ti ricordo 
che in Rubik accessibile, la pressione dei tasti ha un effetto immediato, non 
e' necessario premere invio, dopo aver digitato un comando. 

M percio', mostra questo menu':

 (" - ( 1 2 3 ) - seleziona la fila da spostare;")
Questi sono gli unici comandi che danno accesso ad un sottomenu': cioe' la cui 
azione non si esaurisce con la scelta di 1 2 o 3, ma viene richiesta un'azione 
ulteriore che potrai leggere fra un attimo. 
Dicevamo che la faccia del cubo e' composta da 9 quadratini, o cubetti, 
giusto? Bene, 1, 2 o 3 ti permettono di indicare quale fila o colonna vuoi 
spostare. Le file sono orizzontali, 1 per quella in alto, 2 la mediana e 3 
quella in basso, le colonne sono verticali, 1 sara' la colonna a sinistra, 2 
quella in mezzo, 3 indichera' quella a destra. 
Fatta questa scelta, ecco apparire il sotto menu' seguente:

("Sposta fila selezionata in: (I) alto, (M) basso, (J) sinistra, (K) destra?")

Percio' dovrai immaginare che la "I", la "J", la "K" e la "M" siano 4 tasti 
freccia e indichino dove muovere i cubetti selezionati. 
Un esempio: premendo prima il 3, poi la "I", sposterai la colonna di cubetti a 
destra, tanto per intenderci i numeri del telefono 3, 6 e 9, dalla faccia che 
stai guardando, alla faccia superiore del cubo. Al posto dei cubetti spostati, 
ne arriveranno 3 nuovi dalla faccia inferiore del cubo. Questo movimento 
equivale a ruotare in senso orario, la faccia destra. 

 (" - ( 4 5 ) - Ruotano la faccia anteriore;")
Il 4 infatti ruota verso sinistra la faccia anteriore, quella che stai 
guardando che e' di colore bianco, di 90 gradi in senso antiorario, mentre il 
5 la ruota verso destra, o in senso orario. Naturalmente avendo solo cubetti 
bianchi, anche dopo averla ruotata, essa rimarra' sempre uguale ma saranno 
invece cambiate le faccie laterali, quella superiore e quella inferiore. 

 (" - ( 6 7 ) - Ruotano la faccia mediana;")
Stessa cosa: 6 per una rotazione a sinistra, 7 per la rotazione contraria, ma 
della faccia di mezzo, del cubo. 

 (" - ( 8 9 ) - Ruotano la faccia posteriore;")
E' quest'ultima coppia di comandi, agisce invece sulla faccia Gialla, quella 
posteriore. Anche qui il numero piu' basso ruota verso sinistra, il piu' alto 
verso destra. 

(" - ( F ) - vedi tutte le Facce del cubo;")
Un comando molto semplice che si spiega da solo: "F" indica all'app di fornire 
una panoramica di tutte le facce. Verranno letti i colori su ogni faccia. 
Importante notare che "F" e' un comando di consultazione, non di movimento, 
quindi non verra' conteggiato come una mossa. I comandi di consultazione sono 
assolutamente liberi e se ne possono impartire quanti se ne desidera. 

Eccone altri. Quelli che seguono sono comandi utili a visualizzare le 
singole facce del cubo e sono tutti comandi di consultazione. 
 (" - ( S ) - Sinistra;")
 (" - ( D ) - Destra;")
 (" - ( E ) - alto;")
 (" - ( X ) - basso;")
 (" - ( A ) - Anteriore;")
 (" - ( W ) - posteriore;")

Il prossimo invece, porta alla visualizzazione del presente documento.
 (" - ( H ) - Istruzioni del gioco;")

Ed ecco il comando per visualizzare il menu' che stiamo guardando ora.
 (" - ( M ) - visualizza questo Menu';")
 
Uno dei comandi piu' importanti e':
 (" - ( N ) - inizia una Nuova partita;")
Se esiste gia' una partita in corso, il programma ti chiedera' se vuoi 
sostituirla con una nuova e perderla definitivamente. Se non c'e' nulla in 
corso invece, parte la procedura di mescolamento del cubo. Questa procedura 
non puo' essere interrotta finche' l'app non arriva a mezzo milione di 
movimenti casuali, poi, un messaggio a video ti informa che premendo un tasto 
puoi interrompere. Per ottenere un... caso ancora piu' casuale, potrai 
aspettare per un tempo a tua scelta, prima di procedere; il programma 
interrompera' comunque, arrivato ai 3 milioni e mezzo di movimenti casuali. 
Nota, il tempo utile per rimescolare il cubo per mezzo milione di volte 
variera' un pochino a seconda della velocita' del tuo processore ma dovrebbe 
comunque essere un tempo ragionevole, non piu' di una ventina di secondi 
circa. 
Terminata questa fase, sei pronto ad iniziare. La pressione di un tasto fara' 
scattare il cronometro e la tua partita avra' inizio. 

 (" - ( T ) - Tempo trascorso;")
Un comando utile per la consultazione del tempo totale della partita. Quando 
vuoi interrompere il gioco, assieme al cubo, anche il tempo viene salvato, se 
decidi di salvarlo, quindi il tempo letto con il tasto "T" rappresenta non 
solo quello trascorso durante la presente sessione di gioco, ma tutto quello 
trascorso da quando hai iniziato la partita. Ovviamente il programma conteggia 
solo il tempo in cui il programma e' aperto con la partita caricata. 

 (" - ( ESC ) - per uscire dal gioco.")
Con la pressione di Escape, ti verra' chiesto se vuoi salvare, tasto "S", 
oppure chiudere senza lasciar traccia del tuo lavoro. Dopo di che, il 
programma si chiudera' e tornerai al prompt dei comandi. 
Ti ricordo che per chiudere la shell di windows, dovrai digitare il comando 
exit, seguito da invio. 

## 4. Il metodo a strati, guida alla risoluzione del cubo.
Fonte: WikiHow.
Questa guida e' rivolta ai principianti che vogliano imparare a risolvere un 
cubo di Rubik utilizzando il metodo a strati. Comparato con altre soluzioni, 
questo algoritmo e' relativamente semplice da capire; inoltre, minimizza la 
necessita' di memorizzare lunghe sequenze di movimenti. Allenandoti a metterlo 
in pratica ti preparerai al passo successivo che prevede l'uso del metodo 
Fridrich, molto piu' rapido e utilizzato dai professionisti nelle 
competizioni, dato che consente di risolvere un cubo di Rubik in meno di 20 
secondi. Con una sufficiente dose di pazienza e determinazione, riuscirai a 
padroneggiare uno dei puzzle game piu' famosi nel mondo: il cubo di Erno 
Rubik. Buona lettura e soprattutto buon divertimento! 

Parte 1.1: Apprendere le Basi
Per Risolvere il Cubo di Rubik, utilizza la denominazione corretta per 
indicare le 3 tipologie di pezzi. Il cubo di Rubik e' composto da tre pezzi 
fondamentali, che assumono il relativo nome in base alla loro posizione: 
• Pezzo centrale: sono i pezzi (chiamati anche facce o faccette) che si 
trovano al centro di ogni singola faccia principale del cubo e sono circondati 
dagli altri 8 elementi che la completano. Si tratta di pezzi che espongono un 
solo lato alla vista e che non possono essere spostati. 
• Angolo: sono i pezzi che occupano gli angoli del cubo e sono 
caratterizzati da 3 faccette visibili. 
• Spigolo: sono i pezzi compresi fra 2 angoli. Ognuno di questi elementi e' 
caratterizzato da 2 faccette visibili. 
• Nota: i singoli pezzi che compongono un cubo di Rubik non possono mai 
assumere una tipologia differente da quella iniziale. Questo significa che un 
angolo rimarra' sempre un angolo. 
 
Parte 1.2: Impara a fare riferimento alle sei facce principali del cubo con la 
terminologia corretta. Il cubo di Rubik originale e' composto da 6 facce, 
ognuna delle quali e' caratterizzata da un colore specifico indicato dal 
relativo pezzo centrale. Ad esempio, la "faccia rossa" e' la faccia 
principale, il cui pezzo centrale e' di colore rosso indipendentemente dal 
fatto che su altre facce principali ci siano dei pezzi di colore rosso. 
Spesso, risulta tuttavia molto piu' utile fare riferimento alle facce 
principali in base al punto di vista dell'utente, cioe' in base alla faccia 
che si sta osservando. Ecco l'elenco dei termini che vengono utilizzati dal 
presente articolo: 
• F (dall'inglese "Front" cioe' faccia frontale): impugna il cubo 
all'altezza degli occhi. La faccia principale che stai osservando e' la faccia 
frontale. 
• B (dall'inglese "Back" cioe' faccia retrostante): si tratta della faccia 
principale direttamente opposta (quindi non visibile) a quella che si sta 
osservando. 
• U (dall'inglese "Upper" cioe' faccia superiore): si tratta della faccia 
principale del cubo rivolta verso il soffitto (o il cielo se ti trovi 
all'aperto). 
• D (dall'inglese "Down" cioe' faccia inferiore): e' la faccia principale 
del cubo rivolta verso il pavimento o il terreno. 
• R (dall'inglese "Right" cioe' faccia destra): e' la faccia principale del 
cubo rivolta verso destra. 
• L (dall'inglese "Left" cioe' faccia sinistra): e' la faccia principale del 
cubo rivolta verso sinistra. 
 
Parte 1.3: Impara il significato di rotazione in senso orario e antiorario.
I termini "orario" e "antiorario" si applicano sempre in base alla faccia 
principale che si sta osservando. Avendo questo concetto ben chiaro in mente, 
un'istruzione composta solamente con la lettera che identifica una delle facce 
principali del cubo (ad esempio il comando L), indica di compiere una 
rotazione della faccia in oggetto di 90° in senso orario. L'istruzione 
caratterizzata da una lettera piu' l'apostrofo, come ad esempio L', indica di 
ruotare la faccia in oggetto di 90° in senso antiorario. Ecco alcuni esempi 
di istruzioni che ti aiuteranno a fare capire meglio: 
• F': indica di ruotare la faccia frontale in senso antiorario di 90°.
• R: indica di ruotare la faccia destra in senso orario di 90°. Questo 
significa che la faccia destra diventera' la faccia opposta a quella che si 
trova di fronte ai tuoi occhi (per verificare come funziona in pratica questo 
movimento, inizia a muovere la faccia principale frontale del cubo in senso 
orario finche' non diventa la faccia principale destra). 
• L: indica di ruotare la faccia principale sinistra in senso orario di 
90°. Questo significa portare la faccia principale sinistra di fronte ai tuoi 
occhi. 
• U': indica di ruotare la faccia superiore in senso antiorario di 90° 
sull'asse orizzontale. Questo significa che la faccia superiore diventera' la 
faccia principale opposta a quella che stai osservando. 
• B: indica di ruotare la faccia principale opposta a quella che stai 
osservando di 90° in senso orario rispetto a se stessa. Fai attenzione a non 
confonderti in questo passaggio; in altre parole significa ruotare la faccia 
frontale di 90° in senso antiorario. 
 
Parte 1.4: Se il passaggio va ripetuto due volte, la relativa istruzione 
comprendera' anche il numero 2. Il numero "2" posto dopo un'istruzione indica 
che dovrai ruotare la faccia principale indicata di 180° anziche' di 90°. Ad 
esempio, l'istruzione D2 indica di ruotare la faccia principale inferiore di 
180° (o di 2/4). 
• In questo caso non c'e' la necessita' di specificare il senso della 
rotazione (orario o antiorario) dato che ruotando una faccia principale di 
180° in senso orario o antiorario il risultato sara' identico. 
 
Parte 1.5: Fai riferimento a un pezzo specifico (o faccetta) di un cubo. Le 
istruzioni relative ai passaggi da compiere possono anche fare riferimento a 
un singolo pezzo di una faccia principale del cubo di Rubik. Questo tipo di 
istruzioni indicano la faccia principale in cui si trova il pezzo da muovere. 
Ecco alcuni esempi di istruzioni di questo tipo: 
• BD: indica lo spigolo che delimita la faccia principale retrostante e 
inferiore del cubo. 
• UFR: indica l'angolo del cubo di Rubik le cui faccette occupano la faccia 
principale superiore, frontale e destra. 
• Nota: se le istruzioni fanno riferimento a un singolo pezzo o faccetta 
(quindi a una singola faccia colorata che fa parte di una faccia principale 
del cubo), la prima lettera indica la faccia principale del cubo in cui si 
trova il pezzo. Ad esempio: 
• Individua la faccetta o il pezzo LFD: parti individuando l'angolo che fa 
parte della faccia principale sinistra, frontale e inferiore. Partendo da 
questo pezzo fai riferimento alla faccetta quadrata posta sulla faccia 
principale sinistra (dato che la prima lettera dell'istruzione indica questa 
faccia del cubo). 

Parte 2. Risolvere la Faccia Principale Superiore
Ruota il cubo finche' la faccia principale di colore bianco non occupa la 
faccia U (superiore). Dovrai mantenere il cubo in questa posizione finche' non 
incontrerai un'istruzione che indichi il contrario. L'obiettivo di questa 
sezione dell'articolo consiste nel posizionare tutti gli spigoli bianchi 
intorno al pezzo centrale di appartenenza, in modo da formare una croce o il 
segno "+" sulla faccia principale bianca del cubo. 
• Le istruzioni di questa sezione relative ai movimenti da eseguire fanno 
riferimento a un cubo di Rubik standard, in cui la faccia principale di colore 
bianco e' opposta a quella di colore giallo. Se possiedi una versione un po' 
datata del cubo di Rubik, seguire le istruzioni riportate in questa sezione 
potrebbe risultare difficile. 
• Ricorda che, fino a prova contraria, il pezzo centrale bianco deve 
occupare la faccia superiore del cubo. Modificare questa configurazione e' 
l'errore piu' comune che viene commesso durante questa parte del procedimento. 
Sposta gli spigoli bianchi verso la faccia principale superiore per formare la 
croce. Dato che le possibili configurazioni iniziali del cubo sono moltissime, 
non e' possibile dare una sequenza precisa di istruzioni per risolvere questa 
prima parte del rompicapo, ma i passaggi elencati di seguito dovrebbero 
esserti di aiuto: 
• Se nell'ultimo strato della faccia principale L o B c'e' uno spigolo 
bianco, ruotala una volta in modo da portare il pezzo bianco nello strato 
centrale. Procedi leggendo il prossimo punto. 
• Se c'e' uno spigolo bianco nello strato centrale della faccia principale R 
o L, ruota la faccia F o B in base a quella che si trova in prossimita' del 
pezzo bianco. Prosegui la rotazione finche' la faccia quadrata bianca non si 
trova sulla faccia principale inferiore. Procedi leggendo il prossimo punto. 
• Se sulla faccia principale inferiore e' presente uno spigolo bianco, 
ruotala finche' il pezzo in oggetto non occupa uno spigolo vuoto (cioe' che 
non sia gia' occupato da un pezzo bianco) della faccia superiore. Ruota 
l'intero cubo in modo che lo "spazio vuoto" in oggetto si sposti nella 
posizione UF (spigolo condiviso dalla faccia principale superiore e da quella 
frontale). Esegui una rotazione F2 (ruota la faccia frontale di 180° in senso 
orario) per portare la faccia quadrata bianca nella posizione UF. 
• Ripeti la sequenza di passaggi per ogni spigolo bianco, finche' tutti non 
occupano la faccia principale superiore. 
Completa la croce bianca in modo che gli spigoli combacino con i colori delle 
facce principali adiacenti. Osserva gli spigoli dello strato superiore (quelli 
in comune con la faccia principale superiore) delle facce principali F, R, B e 
L. L'obiettivo e' che ognuno di essi combaci con il colore del rispettivo 
pezzo centrale. Ad esempio, se la faccetta quadrata FU (lo spigolo della 
faccia principale frontale adiacente a quello superiore) e' di colore 
arancione, anche il pezzo centrale della faccia F dovrebbe essere arancione. 
Ecco come risolvere questo passaggio per ognuna delle facce principali 
coinvolte: 
• Ruota la faccia U finche' almeno 2 delle facce principali elencate non 
hanno lo spigolo superiore dello stesso colore del loro pezzo centrale (se 
tutte e quattro le facce principali combaciano, puoi passare direttamente al 
passaggio successivo). 
• Ruota l'intero cubo in modo che uno degli spigoli non ancora nella 
posizione corretta si trovi sulla faccia F (mantenendo la croce bianca sulla 
faccia U). 
• Ruota F2 e controlla che uno degli spigoli bianchi si sia spostato sulla 
faccia D. Controlla gli altri colori del pezzo in oggetto (in posizione FD). 
Nel nostro esempio la faccia quadrata in esame e' di colore rosso. 
• Ruota la faccia D finche' la faccia quadrata rossa non si trova 
direttamente al di sotto del pezzo centrale rosso. 
• Ruota la faccia rossa di 180°. A questo punto lo spigolo bianco dovrebbe 
essere ritornato nella sua posizione corretta della faccia U. 
• Controlla la presenza di un nuovo spigolo bianco sulla faccia D. Anche in 
questo caso controlla i colori delle altre faccette del pezzo in esame. Nel 
nostro esempio il colore e' il verde. 
• Ruota la faccia D finche' la faccetta verde non e' allineata direttamente 
sotto al pezzo centrale verde. 
• Ruota la faccia verde di 180°. Adesso, la croce bianca dovrebbe avere 
ripreso il suo posto sulla faccia U. Le facce F, R, B e L dovrebbero avere 
tutte il pezzo centrale e lo spigolo superiore dello stesso colore. 
Completa la faccia bianca con i rispettivi angoli. Questo passaggio e' 
complesso, quindi leggi le istruzioni con molta attenzione. Al termine di 
questo passaggio, la faccia bianca del cubo che adesso presenta solo la croce 
centrale dovrebbe completarsi con l'aggiunta dei 4 angoli. 
• Individua l'angolo della faccia D che presenta un pezzo bianco. L'angolo 
in esame e' caratterizzato da tre faccette di diversi colori. In questo 
articolo li chiameremo bianco, X e Y (arrivati a questo punto la faccetta 
bianca potrebbe non essere sulla faccia principale D). 
• Ruota la faccia D finche' l'angolo bianco/X/Y non si trova fra la faccia 
di colore X e quella di colore Y (ricorda che la faccia "X" e' quella il cui 
pezzo centrale e' di colore X). 
• Ruota l'intero cubo in modo che l'angolo bianco/X/Y si trovi nella 
posizione DFR, senza tuttavia preoccuparti della posizione esatta di ogni 
colore di questo pezzo. I pezzi centrali della faccia F e R dovrebbero 
corrispondere ai colori X e Y. Nota che la faccia superiore deve sempre essere 
quella di colore bianco. 
• Arrivati a questo punto, l'angolo in esame puo' avere assunto una di 
queste 3 configurazioni: 
• Se la faccetta bianca e' sulla faccia principale frontale (in posizione 
FRD), esegui i movimenti F D F'. 
• Se la faccetta bianca e' sulla faccia principale destra (in posizione 
RFD), esegui i movimenti R' D' R. 
• Se la faccetta bianca e' sulla faccia principale inferiore (in posizione 
DFR), esegui i movimenti F D2 F' D' F D F'. 
Ripeti la procedura per gli angoli rimasti. Utilizza la stessa sequenza di 
passaggi per portare i 3 angoli rimanenti al posto corretto all'interno della 
faccia principale bianca. Al termine di questo passaggio, dovresti aver 
completato con successo la faccia principale superiore bianca. Le facce F, R, 
B e L dovrebbero avere tutti i pezzi dello strato superiore dello stesso 
colore di quello del rispettivo pezzo centrale. 
• A volte puo' accadere che un angolo bianco occupi gia' la faccia U, ma in 
una posizione sbagliata, tale per cui i colori delle altre due faccette che li 
compongono non combacino con quello della faccia a cui fanno riferimento. Se 
questo e' il tuo caso, ruota il cubo in modo che l'angolo in esame occupi la 
posizione UFR, quindi applica i movimenti F D F'. Adesso la faccetta bianca 
dell'angolo dovrebbe trovarsi sulla faccia D, quindi sei in grado di spostarla 
nella posizione corretta seguendo le istruzioni descritte in precedenza. 

Parte 3. Completare lo Strato Centrale
Individua uno spigolo della faccia D le cui faccette non presentino il colore 
giallo. La faccia principale di colore bianco continua a occupare la faccia 
superiore U, mentre la faccia di colore giallo, ancora incompleta, occupa la 
faccia inferiore D. Controlla la faccia D per individuare uno spigolo che non 
contenga il colore giallo. Prendi nota del colore delle 2 faccette dello 
spigolo in esame: 
• Il colore della faccia D lo chiamiamo X.
• Il colore dell'altra faccetta dello spigolo lo chiamiamo Y.
• Ricorda che il pezzo deve obbligatoriamente essere uno spigolo. Non 
partire da un pezzo d'angolo. 
Ruota l'intero cubo finche' il pezzo centrale di colore X non e' sulla faccia 
frontale F. Ruota il cubo intero sul suo asse verticale (come se dovessi far 
ruotare un globo). Interrompi il movimento quando il pezzo centrale di colore 
X occupa la faccia frontale F. 
• Durante la rotazione, le facce U e D dovrebbero mantenere le loro 
posizioni originarie. 
Ruota la faccia D. Ruotala in senso orario o antiorario finche' lo spigolo con 
i colori X/Y non assume la posizione DB. La faccetta di colore X dovrebbe 
trovarsi sulla faccia principale D, mentre quella di colore Y dovrebbe 
occupare la faccia B. 
Modifica il cubo in base alla posizione occupata dalla faccia principale di 
colore Y. La sequenza di movimenti da compiere varia in base alla posizione 
assunta dal pezzo centrale di colore Y: 
• Se la faccetta Y coincide con il colore del pezzo centrale della faccia R, 
esegui la sequenza di movimenti: F D F' D' R' D' R. 
• Se la faccetta Y coincide con il colore del pezzo centrale della faccia L, 
esegui la sequenza di movimenti: F' D' F D L D L'. 
Ripeti questo passaggio finche' i due strati superiori del cubo non sono 
completi. Individua un nuovo spigolo sulla faccia D le cui faccette non sono 
di colore giallo (se nessuno degli spigoli ha queste caratteristiche passa 
direttamente al passaggio successivo). Ripeti i passaggi di questa sezione 
descritti in precedenza per spostare lo spigolo in esame nella sua posizione 
corretta. Al termine, lo strato centrale e quello superiore delle facce F, R, 
B e L dovrebbero essere completi. 
Se tutti gli spigoli della faccia D presentano delle faccette di colore 
giallo, esegui le modifiche necessarie. Assicurati di avere controllato con 
cura tutti e 4 gli spigoli della faccia D. Ognuno e' composto da 2 faccette 
colorate. Perche' le istruzioni presenti in questo passaggio funzionino 
nessuna delle faccette degli spigoli deve essere di colore giallo. Se nel tuo 
caso tutti i requisiti descritti sono rispettati (e i due strati superiori non 
sono ancora completi), esegui le seguenti modifiche: 
• Scegli uno spigolo che contiene una faccetta di colore giallo.
• Ruota l'intero cubo in modo che lo spigolo scelto si trovi in posizione 
FR. La faccia di colore bianco deve sempre occupare la faccia superiore U (non 
ruotare nessuna delle singole facce, limitati a ruotare l'intero cubo). 
• Esegui i seguenti movimenti: F D F' D' R' D' R.
• Adesso uno spigolo privo di faccette di colore giallo dovrebbe trovarsi 
sulla faccia D. A questo punto, puoi ritornare all'inizio di questa sezione e 
ripetere la procedura decritta. 

Parte 4. Completare la Faccia di Colore Giallo
Ruota l'intero cubo in modo che il pezzo centrale di colore giallo occupi la 
faccia U. Da adesso in poi, questa sara' la nuova posizione assunta dal cubo 
fino ad arrivare al suo completamento. 
Crea la croce o il segno "+" sulla faccia U di colore giallo. Prendi nota del 
numero di spigoli di colore giallo presenti sulla faccia superiore U (ricorda 
che gli angoli non sono degli spigoli). A partire da questo punto, puoi avere 
4 possibili configurazioni: 
• Se 2 degli spigoli opposti della faccia superiore U sono gialli, esegui 
questi movimenti: ruota la faccia U finche' i 2 spigoli in esame occupano la 
posizione UL e UR. A questo punto, applica la seguente sequenza di movimenti: 
B L U L' U' B'. 
• Se le posizioni UF e UR della faccia U sono occupate da 2 pezzi gialli 
adiacenti e in posizione corretta (come se disegnassero una freccia che punta 
verso l'angolo posteriore sinistro del cubo), esegui questa sequenza di 
movimenti: B U L U' L' B'. 
• Se non ci sono spigoli di colore giallo, puoi scegliere di applicare una 
delle due sequenze di movimenti appena elencate. In questo modo sposterai 2 
spigoli gialli sulla faccia superiore U. Adesso ripeti il passaggio e, in base 
alla posizione occupata dagli spigoli gialli, applica la relativa sequenza di 
movimenti. 
• Se sono presenti tutti e 4 gli spigoli di colore giallo, significa che hai 
terminato questa fase del lavoro e puoi passare al passaggio successivo. 
Sposta un angolo giallo sulla faccia superiore U. Ruota l'intero cubo finche' 
la faccia di colore blu non occupa la faccia frontale F mentre la faccia di 
colore giallo permane nella posizione superiore U. Sposta gli angoli gialli 
nella loro posizione seguendo queste istruzioni: 
• Ruota la faccia U finche' l'angolo UFR non presenta il colore giallo sulla 
faccetta superiore. 
• Adesso il pezzo d'angolo in esame puo' assumere due configurazioni: 
• Se l'angolo presenta la faccetta gialla sulla faccia principale frontale 
F, esegui questa sequenza di movimenti: F D F' D' F D F' D'. 
• Se il pezzo presenta la faccetta gialla sulla faccia principale destra R, 
esegui questa sequenza di movimenti: D F D' F' D F D' F'. 
• Nota: arrivato a questo punto, il cubo ti sembrera' un po' sconclusionato. 
Non ti preoccupare, fra poco tutto andra' a posto come per magia. 
Ripeti i passaggi precedenti con gli angoli di colore giallo rimasti. Ricorda 
di mantenere la faccia di colore blu come faccia frontale F del cubo e di 
ruotare la faccia superiore U per portare un altro angolo nella pozione UFR. 
Adesso puoi ripetere i passaggi descritti in precedenza per spostare l'angolo 
giallo sulla faccia superiore U. Ripeti la procedura finche' non hai 
completato la faccia superiore U con il colore giallo. 

Parte 5. Completare il Cubo di Rubik
Ruota la faccia superiore U finche' il colore della faccetta frontale di uno 
spigolo non coincide con il colore del pezzo centrale adiacente. Ad esempio, 
se la faccia frontale F ha il pezzo centrale di colore blu, devi ruotare la 
faccia superiore U finche' la faccetta che si trova sopra al pezzo centrale 
blu non sara' dello stesso colore. A questo punto devi avere un solo spigolo 
che si trova nella posizione corretta, cioe' il cui colore e' uguale a quello 
del pezzo centrale adiacente, e non due o tre. 
• Se e' possibile allineare correttamente tutti e quattro gli spigoli con il 
pezzo centrale dello stesso colore, fallo e procedi direttamente all'ultimo 
passaggio di questa sezione. 
• Se cio' non e' possibile esegui questa sequenza di movimenti R2 D' R' L F2 
L' R U2 D R2, quindi prova di nuovo. 
Posiziona gli ultimi spigoli rimasti. Dopo aver allineato correttamente uno 
dei 4 spigoli, modifica il cubo nel seguente modo: 
• Ruotalo in modo che lo spigolo in posizione corretta occupi la faccia 
principale sinistra L. 
• Controlla che la faccetta in posizione FU abbia lo stesso colore del pezzo 
centrale della faccia principale destra R: 
• Se cosi' fosse, esegui la sequenza di movimenti R2 D' R' L F2 L' R U2 D 
R2, quindi passa direttamente al passaggio successivo. A questo punto il cubo 
dovrebbe essere quasi finito, ad esclusione degli angoli. 
• Se cosi' non fosse, esegui il movimento U2, quindi ruota l'intero cubo 
come se fosse un globo, in modo che la faccia principale frontale F diventi la 
faccia destra R. A questo punto, esegui la sequenza di movimenti R2 D' R' L F2 
L' R U2 D R2. 
Completa il cubo. Adesso rimangono da posizionare soltanto gli angoli: 
• Se un angolo e' in posizione corretta, passa direttamente al prossimo 
punto. Se nessuno degli angoli si trova nella posizione corretta, esegui la 
sequenza di movimenti L2 B2 L' F' L B2 L' F L'. Ripetila finche' un angolo non 
si trova nella sua posizione corretta. 
• Ruota l'intero cubo in modo che l'angolo al posto giusto non occupi la 
posizione FUR e la faccetta in posizione FUR sia dello stesso colore del pezzo 
centrale della faccia principale frontale F. 
• Esegui la sequenza di movimenti L2 B2 L' F' L B2 L' F L' .
• Se a questo punto il cubo non risulta ancora completo, esegui la sequenza 
di movimenti L2 B2 L' F' L B2 L' F L' una seconda volta. Congratulazioni hai 
completato con successo il famoso cubo di Rubik!