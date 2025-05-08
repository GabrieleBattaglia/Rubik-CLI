# Rubik Accessibile, by Gabriele Battaglia
# Data concepimento: giovedi' 19 ottobre 2017
# Portato su Python3 l'11 ottobre 2022
# 29 giugno 2024, pubblicato su GitHub

import random
import time
import pickle
import sys
from GBUtils import key
# COSTANTI
VERSIONE = "1.0.3, del 8 maggio 2025" 
NOME_FILE_SALVATAGGIO = "rubik.dat"
NOME_FILE_CLASSIFICA_TXT = "classifica.txt"
NOME_SCONOSCIUTO = "Sconosciuto"
MAX_CLASSIFICA_ENTRIES = 50
BIANCO, GIALLO, VERDE, BLU, ROSSO, ARANCIO = "Bianco", "Giallo", "Verde", "Blu", "Rosso", "Arancio"
FACCIA_ANTERIORE, FACCIA_POSTERIORE, FACCIA_SUPERIORE, FACCIA_INFERIORE, FACCIA_SINISTRA, FACCIA_DESTRA = 5, 0, 2, 8, 4, 6
RUOTA_FACCIA_ORARIO, RUOTA_FACCIA_ANTIORARIO = 1, 2
RUOTA_RIGA_DESTRA, RUOTA_RIGA_SINISTRA = 3, 4       # Per comandi K, J
RUOTA_COLONNA_SU, RUOTA_COLONNA_GIU = 5, 6          # Per comandi I, M
COLOR_TO_NUMBER = {
    BIANCO: "1", GIALLO: "2", VERDE: "3",
    BLU: "4", ROSSO: "5", ARANCIO: "6"
}
# Mappatura ID Faccia a Lettera per il prompt Braille
FACCIA_ID_TO_LETTERA = {
    FACCIA_ANTERIORE: "A", FACCIA_POSTERIORE: "W", FACCIA_SUPERIORE: "E",
    FACCIA_INFERIORE: "X", FACCIA_SINISTRA: "S", FACCIA_DESTRA: "D"
}
f_cubo = {} # Dizionario globale per le facce

class Faccia:
    def __init__(self, colore, id_faccia_numerico):
        self.colore_iniziale = colore
        self.id_faccia = id_faccia_numerico
        self.y = [[colore for _ in range(3)] for _ in range(3)]

        # Mappatura delle facce adiacenti
        if self.id_faccia == FACCIA_ANTERIORE:      #5
            self.u, self.d, self.l, self.r, self.b = FACCIA_SUPERIORE, FACCIA_INFERIORE, FACCIA_SINISTRA, FACCIA_DESTRA, FACCIA_POSTERIORE
        elif self.id_faccia == FACCIA_DESTRA:       #6
            self.u, self.d, self.l, self.r, self.b = FACCIA_SUPERIORE, FACCIA_INFERIORE, FACCIA_ANTERIORE, FACCIA_POSTERIORE, FACCIA_SINISTRA
        elif self.id_faccia == FACCIA_POSTERIORE:   #0
            self.u, self.d, self.l, self.r, self.b = FACCIA_SUPERIORE, FACCIA_INFERIORE, FACCIA_DESTRA, FACCIA_SINISTRA, FACCIA_ANTERIORE
        elif self.id_faccia == FACCIA_SINISTRA:     #4
            self.u, self.d, self.l, self.r, self.b = FACCIA_SUPERIORE, FACCIA_INFERIORE, FACCIA_POSTERIORE, FACCIA_ANTERIORE, FACCIA_DESTRA
        elif self.id_faccia == FACCIA_SUPERIORE:    #2
            self.u, self.d, self.l, self.r, self.b = FACCIA_POSTERIORE, FACCIA_ANTERIORE, FACCIA_SINISTRA, FACCIA_DESTRA, FACCIA_INFERIORE
        elif self.id_faccia == FACCIA_INFERIORE:    #8
            self.u, self.d, self.l, self.r, self.b = FACCIA_ANTERIORE, FACCIA_POSTERIORE, FACCIA_SINISTRA, FACCIA_DESTRA, FACCIA_SUPERIORE

    def __str__(self):
        return "\n".join([" ".join(riga) for riga in self.y]) + ".\n"

    def Ruota(self, tipo_rotazione, indice_rc):
        # print(f"DEBUG: Faccia {self.id_faccia} Ruota(tipo={tipo_rotazione}, indice_rc={indice_rc})") # DEBUG
        global f_cubo
        original_y_faccia_corrente = [riga[:] for riga in self.y] # Copia profonda della faccia corrente

        # Rotazione della faccia stessa (senza coinvolgere altre facce direttamente qui, solo i suoi quadratini)
        if tipo_rotazione == RUOTA_FACCIA_ORARIO:
            self.y[0][0]=original_y_faccia_corrente[2][0]; self.y[0][1]=original_y_faccia_corrente[1][0]; self.y[0][2]=original_y_faccia_corrente[0][0]
            self.y[1][0]=original_y_faccia_corrente[2][1];                                                 self.y[1][2]=original_y_faccia_corrente[0][1]
            self.y[2][0]=original_y_faccia_corrente[2][2]; self.y[2][1]=original_y_faccia_corrente[1][2]; self.y[2][2]=original_y_faccia_corrente[0][2]
        elif tipo_rotazione == RUOTA_FACCIA_ANTIORARIO:
            self.y[0][0]=original_y_faccia_corrente[0][2]; self.y[0][1]=original_y_faccia_corrente[1][2]; self.y[0][2]=original_y_faccia_corrente[2][2]
            self.y[1][0]=original_y_faccia_corrente[0][1];                                                 self.y[1][2]=original_y_faccia_corrente[2][1]
            self.y[2][0]=original_y_faccia_corrente[0][0]; self.y[2][1]=original_y_faccia_corrente[1][0]; self.y[2][2]=original_y_faccia_corrente[2][0]
        
        # Rotazioni di strato (slice moves) - queste modificano self.id_faccia e le sue adiacenti
        elif tipo_rotazione == RUOTA_RIGA_DESTRA: # Riga orizzontale si sposta a destra (comando K)
            # self.id_faccia è la faccia di riferimento (Anteriore per comandi 123)
            # Le righe coinvolte sono quelle di Anteriore, Sinistra, Posteriore, Destra
            temp_riga = f_cubo[self.id_faccia].y[indice_rc][:] # Salva riga originale della faccia di riferimento
            f_cubo[self.id_faccia].y[indice_rc] = f_cubo[self.l].y[indice_rc][:] # Anteriore <- Sinistra
            f_cubo[self.l].y[indice_rc] = f_cubo[self.b].y[indice_rc][:]         # Sinistra <- Posteriore
            f_cubo[self.b].y[indice_rc] = f_cubo[self.r].y[indice_rc][:]         # Posteriore <- Destra
            f_cubo[self.r].y[indice_rc] = temp_riga                              # Destra <- Anteriore (originale)
            # Rotazioni correlate delle facce intere Superiore/Inferiore se la slice è adiacente
            if indice_rc == 0: f_cubo[self.u].Ruota(RUOTA_FACCIA_ANTIORARIO, 0) 
            elif indice_rc == 2: f_cubo[self.d].Ruota(RUOTA_FACCIA_ANTIORARIO, 0) 
        elif tipo_rotazione == RUOTA_RIGA_SINISTRA: # Riga orizzontale si sposta a sinistra (comando J)
            temp_riga = f_cubo[self.id_faccia].y[indice_rc][:]
            f_cubo[self.id_faccia].y[indice_rc] = f_cubo[self.r].y[indice_rc][:] # Anteriore <- Destra
            f_cubo[self.r].y[indice_rc] = f_cubo[self.b].y[indice_rc][:]         # Destra <- Posteriore
            f_cubo[self.b].y[indice_rc] = f_cubo[self.l].y[indice_rc][:]         # Posteriore <- Sinistra
            f_cubo[self.l].y[indice_rc] = temp_riga                              # Sinistra <- Anteriore (originale)
            if indice_rc == 0: f_cubo[self.u].Ruota(RUOTA_FACCIA_ORARIO, 0) 
            elif indice_rc == 2: f_cubo[self.d].Ruota(RUOTA_FACCIA_ORARIO, 0) 
        elif tipo_rotazione == RUOTA_COLONNA_SU: # Colonna verticale si sposta in su (comando I)
            # Le colonne coinvolte sono quelle di Anteriore, Inferiore, Posteriore, Superiore
            temp_col_elementi = [f_cubo[self.id_faccia].y[j][indice_rc] for j in range(3)] # Salva colonna originale Anteriore
            for j in range(3): f_cubo[self.id_faccia].y[j][indice_rc] = f_cubo[self.d].y[j][indice_rc] # Anteriore <- Inferiore
            for j in range(3): f_cubo[self.d].y[j][indice_rc] = f_cubo[self.b].y[j][indice_rc]          # Inferiore <- Posteriore
            for j in range(3): f_cubo[self.b].y[j][indice_rc] = f_cubo[self.u].y[j][indice_rc]          # Posteriore <- Superiore
            for j in range(3): f_cubo[self.u].y[j][indice_rc] = temp_col_elementi[j]                   # Superiore <- Anteriore (originale)
            # Rotazioni correlate delle facce intere Sinistra/Destra se la slice è adiacente
            if indice_rc == 0: f_cubo[self.l].Ruota(RUOTA_FACCIA_ANTIORARIO, 0)
            elif indice_rc == 2: f_cubo[self.r].Ruota(RUOTA_FACCIA_ORARIO, 0)
        elif tipo_rotazione == RUOTA_COLONNA_GIU: # Colonna verticale si sposta in giu (comando M)
            temp_col_elementi = [f_cubo[self.id_faccia].y[j][indice_rc] for j in range(3)]
            for j in range(3): f_cubo[self.id_faccia].y[j][indice_rc] = f_cubo[self.u].y[j][indice_rc] # Anteriore <- Superiore
            for j in range(3): f_cubo[self.u].y[j][indice_rc] = f_cubo[self.b].y[j][indice_rc]          # Superiore <- Posteriore
            for j in range(3): f_cubo[self.b].y[j][indice_rc] = f_cubo[self.d].y[j][indice_rc]          # Posteriore <- Inferiore
            for j in range(3): f_cubo[self.d].y[j][indice_rc] = temp_col_elementi[j]                   # Inferiore <- Anteriore (originale)
            if indice_rc == 0: f_cubo[self.l].Ruota(RUOTA_FACCIA_ORARIO, 0)
            elif indice_rc == 2: f_cubo[self.r].Ruota(RUOTA_FACCIA_ANTIORARIO, 0)
        return True

    def Completa(self):
        colore_centro = self.y[1][1]
        corretti = 0
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1: continue # Salta il quadratino centrale
                if self.y[i][j] == colore_centro: corretti += 1
        return corretti

def NuovoCubo():
    global f_cubo
    f_cubo.clear()
    f_cubo.update({
        FACCIA_ANTERIORE: Faccia(BIANCO, FACCIA_ANTERIORE), FACCIA_POSTERIORE: Faccia(GIALLO, FACCIA_POSTERIORE),
        FACCIA_SUPERIORE: Faccia(VERDE, FACCIA_SUPERIORE), FACCIA_INFERIORE: Faccia(BLU, FACCIA_INFERIORE),
        FACCIA_SINISTRA: Faccia(ROSSO, FACCIA_SINISTRA), FACCIA_DESTRA: Faccia(ARANCIO, FACCIA_DESTRA)
    })
    return f_cubo

def CalcolaPercentualeCompletamento(current_f_cubo):
    if not current_f_cubo: return 100 # Se il cubo non esiste, consideralo risolto per evitare errori
    quadratini_corretti_totali = 0
    for faccia_id in current_f_cubo:
        quadratini_corretti_totali += current_f_cubo[faccia_id].Completa()
    # 6 facce * 8 quadratini non centrali per faccia = 48 quadratini totali da sistemare.
    if quadratini_corretti_totali == 48: return 100
    return int(quadratini_corretti_totali * 100 / 48)

def CaricaPartita():
    global f_cubo
    try:
        with open(NOME_FILE_SALVATAGGIO, "rb") as rbk_file: dati_salvati = pickle.load(rbk_file)
        # Assicurati che l'ordine di unpack sia lo stesso di SalvaPartita
        f_cubo_caricato, mosse, tempo_base, nome_giocatore, classifica, percentuale_comp_salvata = dati_salvati
        f_cubo.update(f_cubo_caricato) # Aggiorna il dizionario globale
        percentuale_comp = CalcolaPercentualeCompletamento(f_cubo) # Ricalcola sempre per coerenza
        print(f"\nBentornato {nome_giocatore}, la tua partita e' stata caricata con successo.")
        key(prompt="Premi un tasto quando sei pronto a far ripartire il tempo.") # Usa attesa di default
        print("\t\tRipreso!")
        return True, mosse, time.time(), tempo_base, nome_giocatore, classifica, percentuale_comp
    except FileNotFoundError: print("Nessuna partita salvata trovata sul disco.")
    except Exception as e: print(f"Errore durante il caricamento della partita: {e}. Sara' creato un nuovo cubo.")
    
    NuovoCubo() # Inizializza f_cubo globale
    print("Il cubo e' stato inizializzato come nuovo. Puoi iniziare una partita con il comando N.")
    return False, 0, 0, 0, NOME_SCONOSCIUTO, [], CalcolaPercentualeCompletamento(f_cubo)


def SalvaPartita(in_f_cubo, mosse, tempo_trascorso_totale, nome_giocatore, classifica, percentuale_comp):
    try:
        with open(NOME_FILE_SALVATAGGIO, "wb") as rbk_file:
            # L'ordine deve corrispondere a CaricaPartita
            dati_da_salvare = [in_f_cubo, mosse, tempo_trascorso_totale, nome_giocatore, classifica, percentuale_comp]
            pickle.dump(dati_da_salvare, rbk_file, pickle.HIGHEST_PROTOCOL)
        print("Perfetto, tutto al sicuro sul disco!")
    except Exception as e: print(f"Errore durante il salvataggio della partita: {e}")

def ConvertiInTempo(secondi_totali):
    secondi_totali = int(secondi_totali)
    s = secondi_totali % 60
    m = (secondi_totali // 60) % 60
    h = secondi_totali // 3600
    return h, m, s

def Istruzioni():
    print("\nManuale dell'App.")
    try:
        with open("README.md", "r", encoding="utf-8") as man_file: righe = man_file.readlines()
        righe_stampate, pagina = 0, 1
        for i, riga_testo in enumerate(righe):
            print(riga_testo, end="")
            righe_stampate += 1
            if righe_stampate % 15 == 0 and i < len(righe) - 1:
                # Assumendo che 'attesa' nella tua key sia in secondi
                tasto_utente = key(prompt=f"\nPremi spazio per proseguire o ESC per uscire. Pagina {pagina}", attesa=300) 
                if tasto_utente == chr(27): break
                pagina +=1; righe_stampate = 0
        print(f"\nVersione App: {VERSIONE}, Fine manuale.")
    except FileNotFoundError: print("Attenzione, file README.md mancante.")
    except Exception as e: print(f"Errore leggendo il file della guida: {e}")

def IniziaNuovaPartita():
    global f_cubo
    NuovoCubo() 
    print("\nBene! Pronto per una nuova partita con Rubik? Cominciamo!")
    print("Per prima cosa e' necessario rimescolare il cubo.")
    print("Premi un tasto per fermare il rimescolio quando appare l'annuncio.")
    mosse_mesc, tasto_utente = 0, ""
    min_mesc, max_mesc = 20, 30 # Valori bassi per test. Originale: 500000, 3500000
    
    tipi_rotazione_slice = [RUOTA_RIGA_DESTRA, RUOTA_RIGA_SINISTRA, RUOTA_COLONNA_SU, RUOTA_COLONNA_GIU]
    # Mescola applicando rotazioni di slice a facce diverse per un migliore rimescolamento
    facce_da_ruotare_per_slice = [FACCIA_ANTERIORE, FACCIA_SUPERIORE, FACCIA_SINISTRA, FACCIA_DESTRA, FACCIA_INFERIORE, FACCIA_POSTERIORE] 

    while True:
        faccia_target_id = random.choice(facce_da_ruotare_per_slice)
        tipo_rot = random.choice(tipi_rotazione_slice)
        indice_rc_rand = random.randint(0,2)
        # La rotazione di slice è sempre relativa alla faccia su cui è chiamata
        f_cubo[faccia_target_id].Ruota(tipo_rot, indice_rc_rand)
        mosse_mesc += 1

        if mosse_mesc == min_mesc: print(f"Ora puoi premere un tasto (min {min_mesc} mescolamenti), o attendere (max {max_mesc}).")
        if mosse_mesc >= min_mesc:
            tasto_utente = key(attesa=0) # Chiamata non bloccante
            if tasto_utente != "": break
        if mosse_mesc >= max_mesc: print("Mescolamento massimo raggiunto."); break
            
    print(f"Ottimo, il cubo di Rubik e' pronto.\n\tE' stato mescolato ben {mosse_mesc} volte.")
    nome_giocatore_nuovo = ""
    while not nome_giocatore_nuovo: nome_giocatore_nuovo = input("Come ti chiami? ").strip()[:12]
    key(prompt=f"Ok {nome_giocatore_nuovo}, premi un tasto quando sei pronto.") # Attesa di default
    print("Tempo partito!")
    return True, 0, time.time(), 0, nome_giocatore_nuovo, CalcolaPercentualeCompletamento(f_cubo)

def Menu():
    print("\n- Menu' del gioco.\n")
    print(" - (1 2 3) - Seleziona fila/colonna (poi I J K M per direzione).")
    print("             I: Alto (colonna su), M: Basso (colonna giu)")
    print("             J: Sinistra (riga sx), K: Destra (riga dx)")
    print(" - (4) Ruota Faccia Anteriore Antiorario.")
    print(" - (5) Ruota Faccia Anteriore Orario.")
    print(" - (6) Ruota Sezione Mediana Antiorario (slice orizzontale).")
    print(" - (7) Ruota Sezione Mediana Orario (slice orizzontale).")
    print(" - (8) Ruota Faccia Posteriore Antiorario.")
    print(" - (9) Ruota Faccia Posteriore Orario.")
    print(" - (F) Vedi tutte le Facce. Singole: (S)inistra, (D)estra, (E)alto, (X)basso, (A)nteriore, (W)posteriore.")
    print(" - (H) Istruzioni. (M) Menu. (N) Nuova partita. (T) Tempo/Mosse. (C) Classifica.")
    print(" - (B) Prompt Braille ON/OFF. (ESC) Esci (con salvataggio).")

def MostraClassifica(classifica):
    if not classifica: print("\nLa classifica e' vuota."); return
    print("\n--- Classifica Rubik Accessibile ---")
    print(f"{'Pos.':<4} {'Nome':<12} {'Mosse':>6} {'Tempo (H:M:S)':>15}")
    print("-" * 40)
    for i, entry in enumerate(classifica):
        h, m, s = ConvertiInTempo(entry['tempo'])
        print(f"{i+1:<4} {entry['nome']:<12} {entry['mosse']:>6} {f'{h:02d}:{m:02d}:{s:02d}':>15}")
    print("-" * 40)

def AggiornaSalvaClassifica(classifica, nome, mosse_gioco, tempo_gioco_sec):
    classifica.append({'nome': nome, 'mosse': mosse_gioco, 'tempo': tempo_gioco_sec})
    classifica.sort(key=lambda x: (x['tempo'], x['mosse'])) # Ordina per tempo, poi per mosse
    classifica = classifica[:MAX_CLASSIFICA_ENTRIES] # Mantieni solo i migliori
    try:
        with open(NOME_FILE_CLASSIFICA_TXT, "w", encoding="utf-8") as f_txt:
            f_txt.write("--- Classifica Rubik Accessibile ---\n")
            f_txt.write(f"{'Pos.':<4} {'Nome':<12} {'Mosse':>6} {'Tempo (H:M:S)':>15}\n" + "-" * 40 + "\n")
            for i, entry in enumerate(classifica):
                h, m, s = ConvertiInTempo(entry['tempo'])
                f_txt.write(f"{i+1:<4} {entry['nome']:<12} {entry['mosse']:>6} {f'{h:02d}:{m:02d}:{s:02d}':>15}\n")
            f_txt.write("-" * 40 + "\n")
        print(f"Classifica aggiornata e salvata in {NOME_FILE_CLASSIFICA_TXT}")
    except Exception as e: print(f"Errore nel salvare la classifica TXT: {e}")
    return classifica

if __name__ == "__main__":
    print(f"\nBenvenuti in Rubik Accessibile. Versione: {VERSIONE}")
    print("Digita (M) per il Menu.")
    partita_in_corso, mosse_partita, t_inizio_session, t_base_partita, \
    nome_giocatore, classifica, perc_comp = CaricaPartita()
    if not f_cubo: # Assicura che f_cubo sia popolato se CaricaPartita fallisce catastroficamente
        NuovoCubo()
        perc_comp = CalcolaPercentualeCompletamento(f_cubo)
    braille_prompt = True
    ultima_faccia_visualizzata_id = FACCIA_ANTERIORE # Default all'avvio

    while True:
        t_sessione = (time.time() - t_inizio_session) if partita_in_corso and t_inizio_session > 0 else 0
        t_totale = t_base_partita + t_sessione
        if braille_prompt:
            faccia_attuale_prompt = f_cubo.get(ultima_faccia_visualizzata_id)
            if faccia_attuale_prompt:
                riga1_num = "".join([COLOR_TO_NUMBER.get(colore, "0") for colore in faccia_attuale_prompt.y[0]])
                riga2_num = "".join([COLOR_TO_NUMBER.get(colore, "0") for colore in faccia_attuale_prompt.y[1]])
                riga3_num = "".join([COLOR_TO_NUMBER.get(colore, "0") for colore in faccia_attuale_prompt.y[2]])
                faccia_lettera_prompt = FACCIA_ID_TO_LETTERA.get(ultima_faccia_visualizzata_id, "?")
                prompt_str = f"PC{perc_comp:d}%.M{mosse_partita:d} F:{faccia_lettera_prompt}({riga1_num}.{riga2_num}.{riga3_num})>"
            else: # Fallback se ultima_faccia_visualizzata_id non è valida (non dovrebbe succedere)
                prompt_str = f"PC{perc_comp:d}%.M{mosse_partita:d}>"

        else: # Braille OFF
            prompt_str = f"PC {perc_comp:3d}% Mosse {mosse_partita:d}> "
        tasto_cmd = key(prompt=prompt_str, attesa=900).lower()

        if not partita_in_corso and tasto_cmd and tasto_cmd not in "nmhcq" + chr(27):
            print("Nessuna partita in corso. (N)uova partita, (H)elp, (C)lassifica o (ESC) per uscire."); continue

        if tasto_cmd: # Solo se un tasto e' stato premuto (key non ha fatto timeout ritornando stringa vuota)
            # print(f"DEBUG: Tasto premuto: '{tasto_cmd}'") # DEBUG
            azione_compiuta = False # Flag per incrementare le mosse solo se una mossa del cubo è fatta

            if tasto_cmd == "m": Menu()
            elif tasto_cmd == "b": braille_prompt = not braille_prompt; print(f"Prompt Braille: {'ON' if braille_prompt else 'OFF'}.")
            elif tasto_cmd == chr(27): break # ESC per uscire dal loop principale
            
            elif tasto_cmd in "123":
                if not partita_in_corso: print("Nessuna partita in corso."); continue
                idx_rc = int(tasto_cmd) - 1
                direzione_tasto_scelta = "" # Nome variabile diverso per chiarezza
                prompt_dir = f"\nSposta fila/colonna {idx_rc+1}: (I)Alto (M)Basso (J)Sinistra (K)Destra? (ESC annulla)"
                while True:
                    temp_input_dir = key(prompt=prompt_dir, attesa=99999).lower() # Forza attesa bloccante
                    if temp_input_dir in "ijkm" + chr(27):
                        direzione_tasto_scelta = temp_input_dir
                        break
                if direzione_tasto_scelta == chr(27): 
                    continue 
                
                map_direzioni_rotazioni = { 
                    "i": RUOTA_COLONNA_SU, "m": RUOTA_COLONNA_GIU, 
                    "k": RUOTA_RIGA_DESTRA, "j": RUOTA_RIGA_SINISTRA 
                }
                if direzione_tasto_scelta in map_direzioni_rotazioni:
                    tipo_rot_scelta = map_direzioni_rotazioni[direzione_tasto_scelta]
                    f_cubo[FACCIA_ANTERIORE].Ruota(tipo_rot_scelta, idx_rc)
                    azione_compiuta = True
            # Comandi 4-9 per rotazioni di Faccia Anteriore, Mediana, Posteriore
            # Queste sono implementate ruotando strati della FACCIA_SUPERIORE
            elif tasto_cmd == "4": # Faccia Anteriore Antiorario
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_DESTRA, 2); print("Faccia anteriore ruotata antioraria."); azione_compiuta = True
            elif tasto_cmd == "5": # Faccia Anteriore Orario
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_SINISTRA, 2); print("Faccia anteriore ruotata oraria."); azione_compiuta = True
            elif tasto_cmd == "6": # Sezione Mediana Antiorario (slice orizzontale)
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_DESTRA, 1); print("Sezione mediana ruotata antioraria."); azione_compiuta = True
            elif tasto_cmd == "7": # Sezione Mediana Orario (slice orizzontale)
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_SINISTRA, 1); print("Sezione mediana ruotata oraria."); azione_compiuta = True
            elif tasto_cmd == "8": # Faccia Posteriore Antiorario
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_DESTRA, 0); print("Faccia posteriore ruotata antioraria."); azione_compiuta = True
            elif tasto_cmd == "9": # Faccia Posteriore Orario
                f_cubo[FACCIA_SUPERIORE].Ruota(RUOTA_RIGA_SINISTRA, 0); print("Faccia posteriore ruotata oraria."); azione_compiuta = True

            elif tasto_cmd == "h": Istruzioni()
            elif tasto_cmd == "c": MostraClassifica(classifica)
            elif tasto_cmd == "t":
                if partita_in_corso:
                    h,m,s = ConvertiInTempo(t_totale); print(f"\nTempo: {h:02d} ore, {m:02d} minuti, {s:02d} secondi. Mosse: {mosse_partita}.")
                else: print("\nNessuna partita avviata.")
            elif tasto_cmd == "n":
                if partita_in_corso and key(prompt="\nPerderai la partita in corso. Proseguire? (S/N) ").lower() != "s":
                    print("\nOk, continua pure."); continue
                partita_in_corso, mosse_partita, t_inizio_session, t_base_partita, nome_giocatore, perc_comp = IniziaNuovaPartita()
            
            # ... (altri comandi)
            elif tasto_cmd == "f": # Visualizza tutte le facce
                if not f_cubo: print ("\nCubo non inizializzato."); continue
                print() # Riga vuota per spaziatura
                for nome_faccia_str, id_f in [("anteriore",FACCIA_ANTERIORE),("posteriore",FACCIA_POSTERIORE),
                                           ("superiore",FACCIA_SUPERIORE), ("inferiore",FACCIA_INFERIORE),
                                           ("sinistra",FACCIA_SINISTRA),("destra",FACCIA_DESTRA)]:
                    faccia_obj = f_cubo[id_f]
                    if braille_prompt:
                        print(f"Faccia {nome_faccia_str}:")
                        for riga in faccia_obj.y:
                            print("".join([COLOR_TO_NUMBER.get(colore, "0") for colore in riga]))
                        print() # Spaziatura dopo ogni faccia
                    else: # Braille OFF
                        print(f"Faccia {nome_faccia_str} ({faccia_obj.colore_iniziale}):\n{str(faccia_obj)}") # str(faccia_obj) include già un "." e "\n"
                ultima_faccia_visualizzata_id = FACCIA_ANTERIORE # Dopo 'f', il prompt potrebbe mostrare l'anteriore o l'ultima effettivamente "guardata"

            elif tasto_cmd in "sdexaw": # Visualizza singola faccia
                if not f_cubo: print ("\nCubo non inizializzato."); continue
                map_tasti_faccia = {'s':FACCIA_SINISTRA, 'd':FACCIA_DESTRA, 'e':FACCIA_SUPERIORE, 
                                    'x':FACCIA_INFERIORE, 'a':FACCIA_ANTERIORE, 'w':FACCIA_POSTERIORE}
                fid = map_tasti_faccia[tasto_cmd]
                ultima_faccia_visualizzata_id = fid # Aggiorna l'ultima faccia visualizzata
                
                faccia_obj = f_cubo[fid]
                nome_faccia_str_singola = [k for k,v in FACCIA_ID_TO_LETTERA.items() if v == FACCIA_ID_TO_LETTERA[fid]][0] 
                # Trovare il nome testuale della faccia per il print
                # Questo è un po' goffo, sarebbe meglio avere una mappa ID -> nome testuale
                # Per ora usiamo il colore iniziale come identificativo se braille off
                
                if braille_prompt:
                    # Trova il nome testuale per il print braille
                    nome_faccia_display = ""
                    for nome_lookup, id_lookup in [("anteriore",FACCIA_ANTERIORE),("posteriore",FACCIA_POSTERIORE),
                                           ("superiore",FACCIA_SUPERIORE), ("inferiore",FACCIA_INFERIORE),
                                           ("sinistra",FACCIA_SINISTRA),("destra",FACCIA_DESTRA)]:
                        if id_lookup == fid:
                            nome_faccia_display = nome_lookup
                            break
                    print(f"\nFaccia {nome_faccia_display}:")
                    for riga in faccia_obj.y:
                        print("".join([COLOR_TO_NUMBER.get(colore, "0") for colore in riga]))
                else: # Braille OFF
                    print(f"\nFaccia {faccia_obj.colore_iniziale}:\n{str(faccia_obj)}")            
            if azione_compiuta:
                mosse_partita += 1
                perc_comp = CalcolaPercentualeCompletamento(f_cubo) # Ricalcola solo se una mossa è stata fatta
                if perc_comp == 100:
                    t_finale = t_base_partita + (time.time() - t_inizio_session if t_inizio_session > 0 else 0)
                    h,m,s = ConvertiInTempo(t_finale)
                    print(f"\nCONGRATULAZIONI {nome_giocatore}!")
                    print(f"Cubo risolto in {mosse_partita} mosse. Tempo: {h:02d} ore, {m:02d} minuti, {s:02d} secondi.")
                    if nome_giocatore == NOME_SCONOSCIUTO:
                        nome_class = ""
                        while not nome_class: nome_class = input("Nome per classifica (max 12 caratteri): ").strip()[:12]
                        nome_giocatore = nome_class if nome_class else NOME_SCONOSCIUTO
                    
                    classifica = AggiornaSalvaClassifica(classifica, nome_giocatore, mosse_partita, t_finale)
                    MostraClassifica(classifica)
                    
                    partita_in_corso = False
                    mosse_partita = 0
                    t_base_partita = 0 
                    t_inizio_session = 0 # Resetta anche questo
                    # Salva lo stato "risolto" e la classifica aggiornata
                    SalvaPartita(f_cubo, mosse_partita, t_base_partita, nome_giocatore, classifica, perc_comp)
                    print("\nPremi N per una nuova partita, o ESC per uscire.")
        # else: # tasto_cmd era vuoto (timeout di key)
            # print("DEBUG: Timeout di key, nessun tasto premuto.") # DEBUG -> Questo non dovrebbe apparire se key non ritorna "" su timeout

    # Uscita dal gioco (dopo ESC)
    if partita_in_corso: # Chiedi di salvare solo se c'è una partita attiva non risolta
        if key(prompt="\nVuoi salvare il lavoro svolto? (S/N) ").lower() == "s":
            t_da_salvare = t_base_partita + (time.time() - t_inizio_session if t_inizio_session > 0 else 0)
            SalvaPartita(f_cubo, mosse_partita, t_da_salvare, nome_giocatore, classifica, perc_comp)
        else: print("\nBene, non salvo nulla.")
    else: # Se la partita non è in corso (es. appena risolta o mai iniziata)
        # Potresti voler salvare comunque la classifica se è stata modificata e non ancora salvata
        # ma SalvaPartita viene già chiamata dopo la vittoria.
        print("\nNessuna partita attiva da salvare.")

    print("\nChiusura di Rubik Accessibile.\nArrivederci!")