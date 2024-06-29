# Rubik Accessibile, by Gabriele Battaglia
# Data concepimento: giovedi' 19 ottobre 2017
# Portato su Python3 l'11 ottobre 2022, grazie Gigi per avermi ricordato questo gioco.
# 29 giugno 2024, pubblicato su GitHub
import random, time, pickle
from GBUtils import key

#COSTANTI
VERSIONE = "0.9.0, del 13 novembre 2022, di Gabriele Battaglia"

#Funzioni
def Carica():
	'''Carica la partita in corso
	ritorna il dizionario con gli oggetti faccia
	ritorna partita vero, se ne trova una salvata, piu le mosse, il tempo e il nome del giocatore
	torna anche la percentuale di completamento cubo
	altrimenti torna partita falso, nome sconosciuto e tempo e mosse a 0'''
	try:
		rbk = open("rubik.dat","rb")
		sit = pickle.load(rbk)
		f = sit[0]
		mosse = sit[1]
		tempobase = sit[2]
		ng = sit[3]
		classifica = sit[4]
		pc = sit[5]
		rbk.close()
		print("\nBentornato " + ng + ", la tua partita e' stata caricata con successo.")
		key(msg="Premi un tasto quando sei pronto a far ripartire il tempo.")
		print("\t\tRipreso!")
		tempo = time.time()
		return f, True, mosse, tempo, tempobase, ng, classifica, pc
	except IOError:
		f = NuovoCubo()
		print("Nessuna partita salvata trovata sul disco.\nIl cubo e' stato inizializzato come nuovo, potrai cominciare una partita, con il comando N.\nBuon gioco!")
		return f, False, 0, 0, 0, "Sconosciuto", [], 100


def ConvertiInTempo(Secondi):
	S = Secondi % 60
	M = ((Secondi - S) % 3600) / 60
	O = (Secondi - S - M * 60) / 3600
	return (int(O), int(M), int(S))

def Istruzioni():
	'''Visualizza manuale'''
	print("\nManuale dell'App.")
	try:
		man = open("README.md", "r")
		rig = man.readlines()
		man.close()
		cr = 0; tasto = "."
		for l in rig:
			print(l,end="")
			cr += 1
			if cr % 15 == 0:
				tasto = key(900, "\nPremi spazio per proseguire o ESC per uscire dalla guida. Pagina "+str(int(cr/10)))
				if tasto == chr(27): break
		print("\nVersione App: " + VERSIONE + ", Fine manuale.")
	except IOError:
		print("Attenzione, file della guida, mancante.\n\tRichiedere il file all'autore dell'App.")
		return

def Inizia():
	print("\nBene! Pronto per una nuova partita con Rubik? Cominciamo!")
	print("Per prima cosa e' necessario rimescolare il cubo in una combinazione mai vista prima.")
	print("Per far cio', ti chiedero' di premere un tasto per fermare il rimescolio.")
	print("Potrai premerlo quando sullo schermo appare l'annuncio.\nVado, inizio a mescolare il cubo!")
	mesc = 0; tasto = ""
	while (mesc > 3500000 or tasto == ""):
		if mesc == 500000: print("Ora puoi premere un tasto per interrompere, oppure aspettare per mescolare di piu'")
		if mesc > 500000:
			tasto = key(0)
		f[5].Ruota(random.randint(3, 6), random.randint(0, 2))
		mesc += 1
	print("Ottimo, il cubo di Rubik e' pronto.\n\tE' stato mescolato ben " + str(mesc) + " volte.\nCome ti chiami? ", end="")
	ng = input()
	ng = ng[:12]
	key(msg="Ok " + ng + ", premi un tasto quando sei pronto.")
	print("Tempo partito!")
	tempo = time.time()
	return f, True, 0, tempo, 0, ng

def Menu():
	'''Visualizza il menu'''
	print("\n- Menu' del gioco.\n")
	print(" - ( 1 2 3 ) - seleziona la fila da spostare;")
	print(" - ( 4   5 ) - Ruotano la faccia anteriore;")
	print(" - ( 6   7 ) - Ruotano la faccia mediana;")
	print(" - ( 8   9 ) - Ruotano la faccia posteriore;")
	print(" - (   F   ) - vedi tutte le Facce del cubo;")
	print(" - \t\t( S ) - Sinistra;")
	print(" - \t\t( D ) - Destra;")
	print(" - \t\t( E ) - alto;")
	print(" - \t\t( X ) - basso;")
	print(" - \t\t( A ) - Anteriore;")
	print(" - \t\t( W ) - posteriore;")
	print(" - (   H   ) - Istruzioni del gioco;")
	print(" - (   M   ) - visualizza questo Menu';")
	print(" - (   N   ) - inizia una Nuova partita;")
	print(" - (   T   ) - Tempo trascorso;")
	print(" - (   B   ) - Visualizza il cubo sulla barra Braille;")
	print(" - (  ESC  ) - per uscire dal gioco.")
	return

# Creazione cubo.
class Faccia:
	def __init__(self, colore, f):
		'''f indica di che faccia si tratta e stabilisce le relazioni spaziali con le altre facce'''
		self.x = []; self.y = []; self.f = f
		if f == 5:
			self.u=2; self.d=8; self.l=4; self.r=6; self.b=0
		if f == 6:
			self.u=2; self.d=8; self.l=5; self.r=0; self.b=4
		if f == 0:
			self.u=2; self.d=8; self.l=6; self.r=4; self.b=5
		if f == 4:
			self.u=2; self.d=8; self.l=0; self.r=5; self.b=6
		if f == 2:
			self.u=0; self.d=5; self.l=4; self.r=6; self.b=8
		if f == 8:
			self.u=5; self.d=0; self.l=4; self.r=6; self.b=2
		for j in range(3):
			self.x.append(colore)
		for j in range(3):
			self.y.append(self.x); self.x = self.x [:]
		return
	def __str__(self):
		if self.f == 5 or self.f == 2 or self.f == 8 or self.f == 6 or self.f == 4 or self.f == 0:
			return str(self.y[0][0] + " " + self.y[0][1] + " " + self.y[0][2] + ", \n" + self.y[1][0] + " " + self.y[1][1] + " " + self.y[1][2] + ", \n" + self.y[2][0] + " " + self.y[2][1] + " " + self.y[2][2] + ".\n")
		return "Errore"
	def Ruota(self, c, q):
		'''Il metodo principale della classe che effettua la rotazione della faccia e di tutte le facce correlate
		riceve c (cosa) e q (quale).
		cosa, indica cosa fare: 1 ruota faccia orario, 2 ruota faccia antiorario, 3 riga a destra, 4 riga a sinistra, 5 colonna su e 6 colonna giu.
		in caso di c = a 3, 4, 5 e 6, q indica quale riga o quale colonna.
		'''
		if c == 5:
			tmp = [f[self.f].y[0][q],f[self.f].y[1][q],f[self.f].y[2][q]]
			for j in range(3):
				f[self.f].y[j][q] = f[self.d].y[j][q]
				f[self.f].y[j][q] = f[self.f].y[j][q]
			for j in range(3):
				f[self.d].y[j][q] = f[self.b].y[j][q]
				f[self.d].y[j][q] = f[self.d].y[j][q]
			for j in range(3):
				f[self.b].y[j][q] = f[self.u].y[j][q]
				f[self.b].y[j][q] = f[self.b].y[j][q]
			for j in range(3):
				f[self.u].y[j][q] = tmp[j]
				f[self.u].y[j][q] = f[self.u].y[j][q]
			# rotazioni correlate
			if q == 0: f[self.l].Ruota(2, 0)
			elif q == 2: f[self.r].Ruota(1, 0)
		elif c == 6:
			tmp = [f[self.f].y[0][q],f[self.f].y[1][q],f[self.f].y[2][q]]
			for j in range(3):
				f[self.f].y[j][q] = f[self.u].y[j][q]
				f[self.f].y[j][q] = f[self.f].y[j][q][:]
			for j in range(3):
				f[self.u].y[j][q] = f[self.b].y[j][q]
				f[self.u].y[j][q] = f[self.u].y[j][q][:]
			for j in range(3):
				f[self.b].y[j][q] = f[self.d].y[j][q]
				f[self.b].y[j][q] = f[self.b].y[j][q][:]
			for j in range(3):
				f[self.d].y[j][q] = tmp[j]
				f[self.d].y[j][q] = f[self.d].y[j][q][:]
			# rotazioni correlate
			if q == 0: f[self.l].Ruota(1, 0)
			elif q == 2: f[self.r].Ruota(2, 0)
		elif c == 3:
			tmp = f[self.f].y[q]; tmp = tmp[:]
			f[self.f].y[q] = f[self.l].y[q]; f[self.f].y[q] = f[self.f].y[q][:]
			f[self.l].y[q] = f[self.b].y[q]; f[self.l].y[q] = f[self.l].y[q][:]
			f[self.b].y[q] = f[self.r].y[q]; f[self.b].y[q] = f[self.b].y[q][:]
			f[self.r].y[q] = tmp; f[self.r].y[q] = f[self.r].y[q][:]
			# rotazioni correlate
			if q == 0: f[self.u].Ruota(2, 0)
			elif q == 2: f[self.d].Ruota(2, 0)
		elif c == 4:
			tmp = f[self.f].y[q]; tmp = tmp[:]
			f[self.f].y[q] = f[self.r].y[q]; f[self.f].y[q] = f[self.f].y[q][:]
			f[self.r].y[q] = f[self.b].y[q]; f[self.r].y[q] = f[self.r].y[q][:]
			f[self.b].y[q] = f[self.l].y[q]; f[self.b].y[q] = f[self.b].y[q][:]
			f[self.l].y[q] = tmp; f[self.l].y[q] = f[self.l].y[q][:]
			# rotazioni correlate
			if q == 0: f[self.u].Ruota(1, 0)
			elif q == 2: f[self.d].Ruota(1, 0)
		elif c == 1:
			# copio 123 in appunti
			tmp = f[self.f].y[0]; tmp = tmp[:]
			# copio 1 su 3, 4 su 2 e 7 su 1
			f[self.f].y[0] = [f[self.f].y[2][0],f[self.f].y[1][0],f[self.f].y[0][0]]; f[self.f].y[0] = f[self.f].y[0][:]
			# copio 9 su 7, 8 su 4.
			f[self.f].y[2][0] = f[self.f].y[2][2]; f[self.f].y[2][0] = f[self.f].y[2][0][:]
			f[self.f].y[1][0] = f[self.f].y[2][1]; f[self.f].y[1][0] = f[self.f].y[1][0][:]
			# copio 3 su 9, 6 su 8
			f[self.f].y[2][2] = f[self.f].y[0][2]; f[self.f].y[2][2] = f[self.f].y[2][2][:]
			f[self.f].y[2][1] = f[self.f].y[1][2]; f[self.f].y[2][1] = f[self.f].y[2][1][:]
			# copio tmp3 su 9, tmp2 su 6
			f[self.f].y[2][2] = tmp[2]; f[self.f].y[2][2] = f[self.f].y[2][2][:]
			f[self.f].y[1][2] = tmp[1]; f[self.f].y[1][2] = f[self.f].y[1][2][:]
		elif c == 2:
			# copio 123 in tmp
			tmp = f[self.f].y[0]; tmp = tmp[:]
			# copio 3 su 1, 6 su 2, 9 su 3
			f[self.f].y[0] = [f[self.f].y[0][2],f[self.f].y[1][2],f[self.f].y[2][2]]; f[self.f].y[0] = f[self.f].y[0][:]
			# copio 8 su 6, 7 su 9
			f[self.f].y[1][2] = f[self.f].y[2][1]; f[self.f].y[1][2] = f[self.f].y[1][2][:]
			f[self.f].y[2][2] = f[self.f].y[2][0]; f[self.f].y[2][2] = f[self.f].y[2][2][:]
			# copio 4 su 8, tmp1 su 7, tmp2 su 4.
			f[self.f].y[2][1] = f[self.f].y[1][0]; f[self.f].y[2][1] = f[self.f].y[2][1][:]
			f[self.f].y[2][0] = tmp[0]; f[self.f].y[2][0] = f[self.f].y[2][0][:]
			f[self.f].y[1][0] = tmp[1]; f[self.f].y[1][0] = f[self.f].y[1][0][:]
		return True        
	def Completa(self):
		'''Ritorna un valore fra 0 e 8 che indica quanti cubetti della faccia sono stati sistemati bene, cioe' del colore di quello centrale'''
		k = 0
		if f[self.f].y[0][0] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[0][1] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[0][2] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[1][0] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[1][2] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[2][0] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[2][1] == f[self.f].y[1][1]: k += 1
		if f[self.f].y[2][2] == f[self.f].y[1][1]: k += 1
		return k
	# qui metodi

def NuovoCubo():
	'''Inizializza un nuovo cubo'''
	# Le facce sono disposte come i numeri del telefono: 2 su, 8 giu, 4 sx, 6 dx, 5 davanti, 0 dietro
	# f e' Il dizionario che contiene i 6 oggetti facce.
	f = {5:Faccia("Bianco",5), \
		 0:Faccia("Giallo",0), \
		 2:Faccia("Verde",2), \
		 8:Faccia("Blu",8), \
		 4:Faccia("Rosso",4), \
		 6:Faccia("Arancio",6)}
	return f

#Main
print ("\nBenvenuti in Rubik Accessibile.\n\tUn gioco di logica che mettera' alla prova la tua mente!\n\n\tVersione: " + VERSIONE)
print ("\nDigita ( M ) - Per visualizzare il Menu'.")
f, partita, mosse, tempo, tempobase, ng, classifica, pc = Carica()
braille = False

while True:
	if braille:
		prompt=f"PC{pc:3d%%} M{mosse:d%}>"
	else:
		prompt=f"PC{pc:%3d%%} M{mosse:%d}>"
	tasto = key(900,msg=prompt)
	if tasto != "":
		if tasto == "m": Menu()
		elif tasto=="b":
			if braille:
				print("Visualizzazione del cubo su display Braille: disattivato.")
				braille=False
			else:
				print("Visualizzazione del cubo su display Braille: attivato.")
				braille=True
		elif tasto == chr(27): break
		elif tasto in "123":
			q = int(tasto) - 1; tasto = " "
			while tasto not in "jikm":
				print("\nSposta fila %d in: (I) alto, (M) basso, (J) sinistra, (K) destra?" % (q+1))
				tasto = key()
				if tasto == "i":
					f[5].Ruota(5, q)
				if tasto == "m":
					f[5].Ruota(6, q)
				if tasto == "k":
					f[5].Ruota(3, q)
				if tasto == "j":
					f[5].Ruota(4, q)
			mosse += 1
		elif tasto == "4":
			f[2].Ruota(4, 2)
			print("Faccia anteriore ruotata antioraria.")
			mosse += 1
		elif tasto == "5":
			f[2].Ruota(3, 2)
			print("Faccia anteriore ruotata oraria.")
			mosse += 1
		elif tasto == "6":
			f[2].Ruota(4, 1)
			print("Sezione mediana ruotata antioraria.")
			mosse += 1
		elif tasto == "7":
			f[2].Ruota(3, 1)
			print("Sezione mediana ruotata oraria.")
			mosse += 1
		elif tasto == "8":
			f[2].Ruota(4, 0)
			print("Faccia posteriore ruotata antioraria.")
			mosse += 1
		elif tasto == "9":
			f[2].Ruota(3, 0)
			print("Faccia posteriore ruotata oraria.")
			mosse += 1
		elif tasto == "h":
			Istruzioni()
		elif tasto == "t":
			if partita:
				orologio = ConvertiInTempo(tempobase + (time.time() - tempo))
				print("\nTempo partita: %2d ore, %2d minuti, %2d secondi." % orologio)
			else: print("\nLa partita non e' stata avviata. Usa il comando N.")
		elif tasto == "n":
			if partita:
				print("\nAttenzione, con questa azione perderai la partita in corso. Vuoi proseguire? Si' o No")
				tasto1 = key()
				if tasto1 == "s": f, partita, mosse, tempo, tempobase, ng = Inizia()
				else: print("\nOk, nessun problema, buona continuazione.")
			else: f, partita, mosse, tempo, tempobase, ng = Inizia()
		elif tasto == "f":
			print ("\nFaccia anteriore:\n" + str(f[5]))
			print ("\nFaccia posteriore:\n" + str(f[0]))
			print ("\nFaccia in basso:\n" + str(f[8]))
			print ("\nFaccia in alto:\n" + str(f[2]))
			print ("\nFaccia a sinistra:\n" + str(f[4]))
			print ("\nFaccia a destra:\n" + str(f[6]))
		elif tasto == "s":
			print ("\nFaccia a sinistra:\n" + str(f[4]))
		elif tasto == "d":
			print ("\nFaccia a destra:\n" + str(f[6]))
		elif tasto == "e":
			print ("\nFaccia in alto:\n" + str(f[2]))
		elif tasto == "x":
			print ("\nFaccia in basso:\n" + str(f[8]))
		elif tasto == "a":
			print ("\nFaccia anteriore:\n" + str(f[5]))
		elif tasto == "w":
			print ("\nFaccia posteriore:\n" + str(f[0]))
	pc = 0
	for j in (5, 4, 6, 2, 8, 0):
		pc += f[j].Completa()
	pc = int(pc * 100 / 48)
print("\nVuoi salvare il lavoro svolto fin qui? Si' o No")
tasto = key()
if tasto == "s":
	rbk = open("rubik.dat","wb")
	sit = [f, mosse, tempobase + (time.time() - tempo), ng, classifica, pc]
	pickle.dump(sit, rbk, pickle.HIGHEST_PROTOCOL)
	rbk.close()
	print("Perfetto, tutto al sicuro sul disco!")
else: print("\nBene, non salvo nulla.")
print("\nChiusura di Rubik Accessibile in corso.\nArrivederci!")
quit()