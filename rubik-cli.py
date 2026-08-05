# Rubik Accessibile, by Gabriele Battaglia
# Data concepimento: giovedi' 19 ottobre 2017
# Portato su Python3 l'11 ottobre 2022
# 29 giugno 2024, pubblicato su GitHub
# 5 agosto 2026, restyling motore 3D, JSON & Acusticator per accessibilita'

import json
import os
import pickle
import random
import time

from GBUtils import Acusticator, key

# COSTANTI
VERSIONE = "1.2.0, del 5 agosto 2026"
NOME_FILE_SALVATAGGIO_JSON = "rubik.json"
NOME_FILE_SALVATAGGIO_DAT = "rubik.dat"
NOME_FILE_CLASSIFICA_JSON = "classifica.json"
NOME_FILE_CLASSIFICA_TXT = "classifica.txt"
NOME_SCONOSCIUTO = "Sconosciuto"
MAX_CLASSIFICA_ENTRIES = 50

BIANCO, GIALLO, VERDE, BLU, ROSSO, ARANCIO = (
    "Bianco",
    "Giallo",
    "Verde",
    "Blu",
    "Rosso",
    "Arancio",
)
FACCIA_POSTERIORE = 0
FACCIA_SUPERIORE = 2
FACCIA_SINISTRA = 4
FACCIA_ANTERIORE = 5
FACCIA_DESTRA = 6
FACCIA_INFERIORE = 8

COLOR_TO_NUMBER = {
    BIANCO: "1",
    GIALLO: "2",
    VERDE: "3",
    BLU: "4",
    ROSSO: "5",
    ARANCIO: "6",
}
FACCIA_ID_TO_LETTERA = {
    FACCIA_ANTERIORE: "A",
    FACCIA_POSTERIORE: "W",
    FACCIA_SUPERIORE: "E",
    FACCIA_INFERIORE: "X",
    FACCIA_SINISTRA: "S",
    FACCIA_DESTRA: "D",
}
FACCIA_ID_TO_NOME = {
    FACCIA_ANTERIORE: "anteriore",
    FACCIA_POSTERIORE: "posteriore",
    FACCIA_SUPERIORE: "superiore",
    FACCIA_INFERIORE: "inferiore",
    FACCIA_SINISTRA: "sinistra",
    FACCIA_DESTRA: "destra",
}

audio_attivo = True


def riproduci_suono(evento):
    """Riproduce un effetto audio con Acusticator senza bloccare l'interfaccia."""
    if not audio_attivo:
        return
    try:
        if evento == "mossa_su":
            # Nota alta per aumento percentuale completamento
            Acusticator(["c5", 0.06, 0, 0.4], kind=1, sync=False)
        elif evento == "mossa_giu":
            # Nota piu' bassa per diminuzione percentuale completamento
            Acusticator(["e3", 0.08, 0, 0.4], kind=1, sync=False)
        elif evento == "mossa_neutra":
            # Click neutro per mossa che non varia la percentuale
            Acusticator(["g4", 0.04, 0, 0.3], kind=1, sync=False)
        elif evento == "vittoria":
            # Arpeggio ascendente di vittoria
            Acusticator(
                [
                    "c4",
                    0.08,
                    0,
                    0.5,
                    "e4",
                    0.08,
                    0,
                    0.5,
                    "g4",
                    0.08,
                    0,
                    0.5,
                    "c5",
                    0.3,
                    0,
                    0.6,
                ],
                kind=1,
                sync=False,
            )
        elif evento == "inizio":
            # Chime di inizio partita / rimescolamento completato
            Acusticator(
                ["g4", 0.08, 0, 0.4, "c5", 0.12, 0, 0.5],
                kind=1,
                sync=False,
            )
        elif evento == "click":
            # Feedback generico menu o selezione
            Acusticator(["a4", 0.03, 0, 0.2], kind=1, sync=False)
    except Exception:
        # Tolleranza se la scheda audio non risponde
        pass


class Faccia:

    def __init__(self, colore, id_faccia_numerico):
        self.colore_iniziale = colore
        self.id_faccia = id_faccia_numerico
        self.y = [[colore for _ in range(3)] for _ in range(3)]

    def __str__(self):
        return "\n".join([" ".join(riga) for riga in self.y]) + ".\n"

    def to_dict(self):
        return {
            "colore_iniziale": self.colore_iniziale,
            "id_faccia": self.id_faccia,
            "y": self.y,
        }

    @staticmethod
    def from_dict(d):
        f = Faccia(d["colore_iniziale"], d["id_faccia"])
        f.y = d["y"]
        return f


class RubikEngine:
    """Motore geometrico 3D per il Cubo di Rubik."""

    def __init__(self, f_cubo_dict=None):
        if f_cubo_dict:
            self.facce = f_cubo_dict
        else:
            self.inizializza_nuovo()

    def inizializza_nuovo(self):
        self.facce = {
            FACCIA_ANTERIORE: Faccia(BIANCO, FACCIA_ANTERIORE),
            FACCIA_POSTERIORE: Faccia(GIALLO, FACCIA_POSTERIORE),
            FACCIA_SUPERIORE: Faccia(VERDE, FACCIA_SUPERIORE),
            FACCIA_INFERIORE: Faccia(BLU, FACCIA_INFERIORE),
            FACCIA_SINISTRA: Faccia(ROSSO, FACCIA_SINISTRA),
            FACCIA_DESTRA: Faccia(ARANCIO, FACCIA_DESTRA),
        }
        return self.facce

    def calcola_percentuale(self):
        corretti = 0
        for faccia_obj in self.facce.values():
            centro = faccia_obj.y[1][1]
            for r in range(3):
                for c in range(3):
                    if r == 1 and c == 1:
                        continue
                    if faccia_obj.y[r][c] == centro:
                        corretti += 1
        if corretti == 48:
            return 100
        return int(corretti * 100 / 48)

    def _ruota_matrice_oraria(self, grid):
        return [
            [grid[2][0], grid[1][0], grid[0][0]],
            [grid[2][1], grid[1][1], grid[0][1]],
            [grid[2][2], grid[1][2], grid[0][2]],
        ]

    def rotazione_faccia_anteriore(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_ANTERIORE] = self._ruota_matrice_oraria(
                f[FACCIA_ANTERIORE]
            )
            tmp = f[FACCIA_SUPERIORE][2][:]
            f[FACCIA_SUPERIORE][2] = [
                f[FACCIA_SINISTRA][2][2],
                f[FACCIA_SINISTRA][1][2],
                f[FACCIA_SINISTRA][0][2],
            ]
            f[FACCIA_SINISTRA][0][2] = f[FACCIA_INFERIORE][0][0]
            f[FACCIA_SINISTRA][1][2] = f[FACCIA_INFERIORE][0][1]
            f[FACCIA_SINISTRA][2][2] = f[FACCIA_INFERIORE][0][2]
            f[FACCIA_INFERIORE][0] = [
                f[FACCIA_DESTRA][2][0],
                f[FACCIA_DESTRA][1][0],
                f[FACCIA_DESTRA][0][0],
            ]
            f[FACCIA_DESTRA][0][0] = tmp[0]
            f[FACCIA_DESTRA][1][0] = tmp[1]
            f[FACCIA_DESTRA][2][0] = tmp[2]
        else:
            for _ in range(3):
                self.rotazione_faccia_anteriore(oraria=True)

    def rotazione_faccia_posteriore(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_POSTERIORE] = self._ruota_matrice_oraria(
                f[FACCIA_POSTERIORE]
            )
            tmp = f[FACCIA_SUPERIORE][0][:]
            f[FACCIA_SUPERIORE][0] = [
                f[FACCIA_DESTRA][0][2],
                f[FACCIA_DESTRA][1][2],
                f[FACCIA_DESTRA][2][2],
            ]
            f[FACCIA_DESTRA][0][2] = f[FACCIA_INFERIORE][2][2]
            f[FACCIA_DESTRA][1][2] = f[FACCIA_INFERIORE][2][1]
            f[FACCIA_DESTRA][2][2] = f[FACCIA_INFERIORE][2][0]
            f[FACCIA_INFERIORE][2] = [
                f[FACCIA_SINISTRA][2][0],
                f[FACCIA_SINISTRA][1][0],
                f[FACCIA_SINISTRA][0][0],
            ]
            f[FACCIA_SINISTRA][0][0] = tmp[2]
            f[FACCIA_SINISTRA][1][0] = tmp[1]
            f[FACCIA_SINISTRA][2][0] = tmp[0]
        else:
            for _ in range(3):
                self.rotazione_faccia_posteriore(oraria=True)

    def rotazione_faccia_superiore(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_SUPERIORE] = self._ruota_matrice_oraria(
                f[FACCIA_SUPERIORE]
            )
            tmp = f[FACCIA_POSTERIORE][0][:]
            f[FACCIA_POSTERIORE][0] = f[FACCIA_SINISTRA][0][:]
            f[FACCIA_SINISTRA][0] = f[FACCIA_ANTERIORE][0][:]
            f[FACCIA_ANTERIORE][0] = f[FACCIA_DESTRA][0][:]
            f[FACCIA_DESTRA][0] = tmp
        else:
            for _ in range(3):
                self.rotazione_faccia_superiore(oraria=True)

    def rotazione_faccia_inferiore(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_INFERIORE] = self._ruota_matrice_oraria(
                f[FACCIA_INFERIORE]
            )
            tmp = f[FACCIA_ANTERIORE][2][:]
            f[FACCIA_ANTERIORE][2] = f[FACCIA_SINISTRA][2][:]
            f[FACCIA_SINISTRA][2] = f[FACCIA_POSTERIORE][2][:]
            f[FACCIA_POSTERIORE][2] = f[FACCIA_DESTRA][2][:]
            f[FACCIA_DESTRA][2] = tmp
        else:
            for _ in range(3):
                self.rotazione_faccia_inferiore(oraria=True)

    def rotazione_faccia_sinistra(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_SINISTRA] = self._ruota_matrice_oraria(f[FACCIA_SINISTRA])
            tmp_sup = [f[FACCIA_SUPERIORE][i][0] for i in range(3)]
            tmp_post = [f[FACCIA_POSTERIORE][i][2] for i in range(3)]
            for i in range(3):
                f[FACCIA_SUPERIORE][i][0] = tmp_post[2 - i]
            tmp_inf = [f[FACCIA_INFERIORE][i][0] for i in range(3)]
            for i in range(3):
                f[FACCIA_POSTERIORE][i][2] = tmp_inf[2 - i]
            for i in range(3):
                f[FACCIA_INFERIORE][i][0] = f[FACCIA_ANTERIORE][i][0]
            for i in range(3):
                f[FACCIA_ANTERIORE][i][0] = tmp_sup[i]
        else:
            for _ in range(3):
                self.rotazione_faccia_sinistra(oraria=True)

    def rotazione_faccia_destra(self, oraria=True):
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            f[FACCIA_DESTRA] = self._ruota_matrice_oraria(f[FACCIA_DESTRA])
            tmp_sup = [f[FACCIA_SUPERIORE][i][2] for i in range(3)]
            for i in range(3):
                f[FACCIA_SUPERIORE][i][2] = f[FACCIA_ANTERIORE][i][2]
            for i in range(3):
                f[FACCIA_ANTERIORE][i][2] = f[FACCIA_INFERIORE][i][2]
            tmp_post = [f[FACCIA_POSTERIORE][i][0] for i in range(3)]
            for i in range(3):
                f[FACCIA_INFERIORE][i][2] = tmp_post[2 - i]
            for i in range(3):
                f[FACCIA_POSTERIORE][i][0] = tmp_sup[2 - i]
        else:
            for _ in range(3):
                self.rotazione_faccia_destra(oraria=True)

    def rotazione_sezione_mediana_frontale(self, oraria=True):
        # S-slice (strato mediano tra Anteriore e Posteriore, vista da davanti)
        f = {fid: obj.y for fid, obj in self.facce.items()}
        if oraria:
            tmp = f[FACCIA_SUPERIORE][1][:]
            f[FACCIA_SUPERIORE][1] = [
                f[FACCIA_SINISTRA][2][1],
                f[FACCIA_SINISTRA][1][1],
                f[FACCIA_SINISTRA][0][1],
            ]
            f[FACCIA_SINISTRA][0][1] = f[FACCIA_INFERIORE][1][0]
            f[FACCIA_SINISTRA][1][1] = f[FACCIA_INFERIORE][1][1]
            f[FACCIA_SINISTRA][2][1] = f[FACCIA_INFERIORE][1][2]
            f[FACCIA_INFERIORE][1] = [
                f[FACCIA_DESTRA][2][1],
                f[FACCIA_DESTRA][1][1],
                f[FACCIA_DESTRA][0][1],
            ]
            f[FACCIA_DESTRA][0][1] = tmp[0]
            f[FACCIA_DESTRA][1][1] = tmp[1]
            f[FACCIA_DESTRA][2][1] = tmp[2]
        else:
            for _ in range(3):
                self.rotazione_sezione_mediana_frontale(oraria=True)

    def sposta_riga_orizzontale(self, idx_riga, verso_destra=True):
        if idx_riga == 0:
            self.rotazione_faccia_superiore(oraria=verso_destra)
        elif idx_riga == 2:
            self.rotazione_faccia_inferiore(oraria=not verso_destra)
        elif idx_riga == 1:
            f = {fid: obj.y for fid, obj in self.facce.items()}
            if verso_destra:
                tmp = f[FACCIA_POSTERIORE][1][:]
                f[FACCIA_POSTERIORE][1] = f[FACCIA_SINISTRA][1][:]
                f[FACCIA_SINISTRA][1] = f[FACCIA_ANTERIORE][1][:]
                f[FACCIA_ANTERIORE][1] = f[FACCIA_DESTRA][1][:]
                f[FACCIA_DESTRA][1] = tmp
            else:
                tmp = f[FACCIA_POSTERIORE][1][:]
                f[FACCIA_POSTERIORE][1] = f[FACCIA_DESTRA][1][:]
                f[FACCIA_DESTRA][1] = f[FACCIA_ANTERIORE][1][:]
                f[FACCIA_ANTERIORE][1] = f[FACCIA_SINISTRA][1][:]
                f[FACCIA_SINISTRA][1] = tmp

    def sposta_colonna_verticale(self, idx_col, verso_alto=True):
        if idx_col == 0:
            self.rotazione_faccia_sinistra(oraria=not verso_alto)
        elif idx_col == 2:
            self.rotazione_faccia_destra(oraria=verso_alto)
        elif idx_col == 1:
            f = {fid: obj.y for fid, obj in self.facce.items()}
            if verso_alto:
                tmp_sup = [f[FACCIA_SUPERIORE][i][1] for i in range(3)]
                tmp_post = [f[FACCIA_POSTERIORE][i][1] for i in range(3)]
                for i in range(3):
                    f[FACCIA_SUPERIORE][i][1] = f[FACCIA_ANTERIORE][i][1]
                    f[FACCIA_ANTERIORE][i][1] = f[FACCIA_INFERIORE][i][1]
                    f[FACCIA_INFERIORE][i][1] = tmp_post[2 - i]
                    f[FACCIA_POSTERIORE][i][1] = tmp_sup[2 - i]
            else:
                tmp_inf = [f[FACCIA_INFERIORE][i][1] for i in range(3)]
                tmp_post = [f[FACCIA_POSTERIORE][i][1] for i in range(3)]
                for i in range(3):
                    f[FACCIA_INFERIORE][i][1] = f[FACCIA_ANTERIORE][i][1]
                    f[FACCIA_ANTERIORE][i][1] = f[FACCIA_SUPERIORE][i][1]
                    f[FACCIA_SUPERIORE][i][1] = tmp_post[2 - i]
                    f[FACCIA_POSTERIORE][i][1] = tmp_inf[2 - i]


def CaricaClassifica():
    classifica = []
    if os.path.exists(NOME_FILE_CLASSIFICA_JSON):
        try:
            with open(
                NOME_FILE_CLASSIFICA_JSON, "r", encoding="utf-8"
            ) as f_json:
                classifica = json.load(f_json)
            return classifica
        except Exception as e:
            print(f"Errore lettura {NOME_FILE_CLASSIFICA_JSON}: {e}")

    # Fallback se la classifica e' presente solo in rubik.dat o rubik.json
    return classifica


def AggiornaSalvaClassifica(classifica, nome, mosse_gioco, tempo_gioco_sec):
    classifica.append(
        {"nome": nome, "mosse": mosse_gioco, "tempo": tempo_gioco_sec}
    )
    classifica.sort(key=lambda x: (x["tempo"], x["mosse"]))
    classifica = classifica[:MAX_CLASSIFICA_ENTRIES]

    # Salvataggio JSON
    try:
        with open(
            NOME_FILE_CLASSIFICA_JSON, "w", encoding="utf-8"
        ) as f_json:
            json.dump(classifica, f_json, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Errore salvataggio {NOME_FILE_CLASSIFICA_JSON}: {e}")

    # Salvataggio TXT visuale
    try:
        with open(NOME_FILE_CLASSIFICA_TXT, "w", encoding="utf-8") as f_txt:
            f_txt.write("--- Classifica Rubik Accessibile ---\n")
            f_txt.write(
                f"{'Pos.':<4} {'Nome':<12} {'Mosse':>6} {'Tempo (H:M:S)':>15}\n"
                + "-" * 40
                + "\n"
            )
            for i, entry in enumerate(classifica):
                h, m, s = ConvertiInTempo(entry["tempo"])
                f_txt.write(
                    f"{i+1:<4} {entry['nome']:<12} {entry['mosse']:>6} {f'{h:02d}:{m:02d}:{s:02d}':>15}\n"
                )
            f_txt.write("-" * 40 + "\n")
        print(f"Classifica aggiornata e salvata in {NOME_FILE_CLASSIFICA_TXT}")
    except Exception as e:
        print(f"Errore nel salvare la classifica TXT: {e}")

    return classifica


def CaricaPartita(engine):
    global audio_attivo
    classifica = CaricaClassifica()
    braille_prompt = True

    # 1. Tenta prima la ricarica da JSON
    if os.path.exists(NOME_FILE_SALVATAGGIO_JSON):
        try:
            with open(
                NOME_FILE_SALVATAGGIO_JSON, "r", encoding="utf-8"
            ) as f_json:
                data = json.load(f_json)

            facce_dict = {}
            for k, v in data.get("facce", {}).items():
                facce_dict[int(k)] = Faccia.from_dict(v)

            engine.facce = facce_dict
            mosse = data.get("mosse", 0)
            tempo_base = data.get("tempo_base", 0)
            nome_giocatore = data.get("nome_giocatore", NOME_SCONOSCIUTO)
            braille_prompt = data.get("braille_prompt", True)
            audio_attivo = data.get("audio_attivo", True)
            if not classifica:
                classifica = data.get("classifica", [])

            perc_comp = engine.calcola_percentuale()
            print(
                f"\nBentornato {nome_giocatore}, la tua partita e' stata caricata da JSON."
            )
            key(
                prompt="\rPremi un tasto per ripartire\r"
            )
            print("\t\tRipreso!")
            return (
                True,
                mosse,
                time.time(),
                tempo_base,
                nome_giocatore,
                classifica,
                perc_comp,
                braille_prompt,
            )
        except Exception as e:
            print(f"Errore durante il caricamento da JSON: {e}")

    # 2. Migrazione / Fallback da Pickle (rubik.dat)
    if os.path.exists(NOME_FILE_SALVATAGGIO_DAT):
        try:
            with open(NOME_FILE_SALVATAGGIO_DAT, "rb") as rbk_file:
                dati_salvati = pickle.load(rbk_file)
            (
                f_cubo_caricato,
                mosse,
                tempo_base,
                nome_giocatore,
                classifica_pickle,
                _,
            ) = dati_salvati
            engine.facce = f_cubo_caricato
            if not classifica:
                classifica = classifica_pickle
            perc_comp = engine.calcola_percentuale()
            print(
                f"\nBentornato {nome_giocatore}, la partita e' stata convertita dal precedente file .dat."
            )
            key(
                prompt="\rPremi un tasto per ripartire\r"
            )
            print("\t\tRipreso!")
            return (
                True,
                mosse,
                time.time(),
                tempo_base,
                nome_giocatore,
                classifica,
                perc_comp,
                braille_prompt,
            )
        except Exception as e:
            print(f"Errore caricamento file legacy .dat: {e}")

    # 3. Nuovo Cubo se non esiste alcun salvataggio
    engine.inizializza_nuovo()
    print("Nessuna partita salvata trovata sul disco.")
    print(
        "Il cubo e' stato inizializzato come nuovo. Puoi iniziare una partita con il comando N."
    )
    return (
        False,
        0,
        0,
        0,
        NOME_SCONOSCIUTO,
        classifica,
        engine.calcola_percentuale(),
        True,
    )


def SalvaPartita(
    engine,
    mosse,
    tempo_trascorso_totale,
    nome_giocatore,
    classifica,
    perc_comp,
    braille_prompt,
    messaggio=True,
):
    try:
        data = {
            "facce": {
                fid: obj.to_dict() for fid, obj in engine.facce.items()
            },
            "mosse": mosse,
            "tempo_base": tempo_trascorso_totale,
            "nome_giocatore": nome_giocatore,
            "classifica": classifica,
            "percentuale_comp": perc_comp,
            "braille_prompt": braille_prompt,
            "audio_attivo": audio_attivo,
        }
        with open(
            NOME_FILE_SALVATAGGIO_JSON, "w", encoding="utf-8"
        ) as f_json:
            json.dump(data, f_json, indent=2, ensure_ascii=False)
        if messaggio:
            print("Perfetto, partita e configurazioni salvate sul disco!")
    except Exception as e:
        print(f"Errore durante il salvataggio della partita: {e}")


def ConvertiInTempo(secondi_totali):
    secondi_totali = int(secondi_totali)
    s = secondi_totali % 60
    m = (secondi_totali // 60) % 60
    h = secondi_totali // 3600
    return h, m, s


def Istruzioni():
    print("\nManuale dell'App.")
    try:
        with open("README.md", "r", encoding="utf-8") as man_file:
            righe = man_file.readlines()
        righe_stampate, pagina = 0, 1
        for i, riga_testo in enumerate(righe):
            print(riga_testo, end="")
            righe_stampate += 1
            if righe_stampate % 15 == 0 and i < len(righe) - 1:
                tasto_utente = key(
                    prompt=f"\rPagina {pagina}\r",
                    attesa=300,
                )
                if tasto_utente in (chr(27), "esc"):
                    break
                pagina += 1
                righe_stampate = 0
        print(f"\nVersione App: {VERSIONE}, Fine manuale.")
    except FileNotFoundError:
        print("Attenzione, file README.md mancante.")
    except Exception as e:
        print(f"Errore leggendo il file della guida: {e}")


def IniziaNuovaPartita(engine):
    engine.inizializza_nuovo()
    print("\nBene! Pronto per una nuova partita con Rubik? Cominciamo!")
    print("Rimescolamento automatico in corso...")

    target_mescolamenti = random.randint(40, 2000)

    mosse_disponibili = [
        lambda: engine.rotazione_faccia_anteriore(True),
        lambda: engine.rotazione_faccia_anteriore(False),
        lambda: engine.rotazione_faccia_posteriore(True),
        lambda: engine.rotazione_faccia_posteriore(False),
        lambda: engine.rotazione_faccia_superiore(True),
        lambda: engine.rotazione_faccia_superiore(False),
        lambda: engine.rotazione_faccia_inferiore(True),
        lambda: engine.rotazione_faccia_inferiore(False),
        lambda: engine.rotazione_faccia_sinistra(True),
        lambda: engine.rotazione_faccia_sinistra(False),
        lambda: engine.rotazione_faccia_destra(True),
        lambda: engine.rotazione_faccia_destra(False),
        lambda: engine.rotazione_sezione_mediana_frontale(True),
        lambda: engine.rotazione_sezione_mediana_frontale(False),
        lambda: engine.sposta_riga_orizzontale(1, True),
        lambda: engine.sposta_riga_orizzontale(1, False),
        lambda: engine.sposta_colonna_verticale(1, True),
        lambda: engine.sposta_colonna_verticale(1, False),
    ]

    for _ in range(target_mescolamenti):
        mossa_rand = random.choice(mosse_disponibili)
        mossa_rand()

    print(
        f"Ottimo, il cubo di Rubik e' pronto.\n\tE' stato mescolato ben {target_mescolamenti} volte."
    )
    riproduci_suono("inizio")
    nome_giocatore_nuovo = ""
    while not nome_giocatore_nuovo:
        nome_giocatore_nuovo = input("Come ti chiami? ").strip()[:12]
    key(prompt=f"\rOk {nome_giocatore_nuovo}, premi un tasto per iniziare\r")
    print("Tempo partito!")
    return (
        True,
        0,
        time.time(),
        0,
        nome_giocatore_nuovo,
        engine.calcola_percentuale(),
    )


def Menu():
    print("\n- Menu' del gioco.\n")
    print(" - (1 2 3) - Seleziona fila/colonna (poi I J K M per direzione).")
    print("             I: Alto (colonna su), M: Basso (colonna giu)")
    print("             J: Sinistra (riga sx), K: Destra (riga dx)")
    print(" - (4) Ruota Faccia Anteriore Antiorario.")
    print(" - (5) Ruota Faccia Anteriore Orario.")
    print(" - (6) Ruota Sezione Mediana Antiorario (S-slice).")
    print(" - (7) Ruota Sezione Mediana Orario (S-slice).")
    print(" - (8) Ruota Faccia Posteriore Antiorario.")
    print(" - (9) Ruota Faccia Posteriore Orario.")
    print(
        " - (F) Faccia Anteriore. (S)inistra, (D)estra, (E)alto, (X)basso, (W)posteriore."
    )
    print(
        " - (H) Istruzioni. (M) Menu. (N) Nuova partita. (T) Tempo/Mosse. (C) Classifica."
    )
    print(
        " - (B) Prompt Braille ON/OFF. (A) Effetti Audio ON/OFF. (ESC) Esci (con salvataggio)."
    )


def MostraClassifica(classifica):
    if not classifica:
        print("\nLa classifica e' vuota.")
        return
    print("\n--- Classifica Rubik Accessibile ---")
    print(f"{'Pos.':<4} {'Nome':<12} {'Mosse':>6} {'Tempo (H:M:S)':>15}")
    print("-" * 40)
    for i, entry in enumerate(classifica):
        h, m, s = ConvertiInTempo(entry["tempo"])
        print(
            f"{i+1:<4} {entry['nome']:<12} {entry['mosse']:>6} {f'{h:02d}:{m:02d}:{s:02d}':>15}"
        )
    print("-" * 40)


if __name__ == "__main__":
    engine = RubikEngine()
    print(f"\nBenvenuti in Rubik Accessibile. Versione: {VERSIONE}")
    print("Digita (M) per il Menu.")

    (
        partita_in_corso,
        mosse_partita,
        t_inizio_session,
        t_base_partita,
        nome_giocatore,
        classifica,
        perc_comp,
        braille_prompt,
    ) = CaricaPartita(engine)
    ultima_faccia_visualizzata_id = FACCIA_ANTERIORE

    while True:
        t_sessione = (
            (time.time() - t_inizio_session)
            if partita_in_corso and t_inizio_session > 0
            else 0
        )
        t_totale = t_base_partita + t_sessione

        if braille_prompt:
            faccia_attuale_prompt = engine.facce.get(
                ultima_faccia_visualizzata_id
            )
            if faccia_attuale_prompt:
                riga1_num = "".join(
                    [
                        COLOR_TO_NUMBER.get(colore, "0")
                        for colore in faccia_attuale_prompt.y[0]
                    ]
                )
                riga2_num = "".join(
                    [
                        COLOR_TO_NUMBER.get(colore, "0")
                        for colore in faccia_attuale_prompt.y[1]
                    ]
                )
                riga3_num = "".join(
                    [
                        COLOR_TO_NUMBER.get(colore, "0")
                        for colore in faccia_attuale_prompt.y[2]
                    ]
                )
                faccia_lettera_prompt = FACCIA_ID_TO_LETTERA.get(
                    ultima_faccia_visualizzata_id, "?"
                )
                prompt_str = f"\rPC{perc_comp:d}%.M{mosse_partita:d} F:{faccia_lettera_prompt}({riga1_num}.{riga2_num}.{riga3_num})>\r"
            else:
                prompt_str = f"\rPC{perc_comp:d}%.M{mosse_partita:d}>\r"
        else:
            prompt_str = f"\rPC {perc_comp:3d}% Mosse {mosse_partita:d}>\r"

        tasto_cmd = key(prompt=prompt_str, attesa=900).lower()

        if (
            not partita_in_corso
            and tasto_cmd
            and tasto_cmd not in "nmhcqab"
            and tasto_cmd not in (chr(27), "esc")
        ):
            print(
                "Nessuna partita in corso. (N)uova partita, (H)elp, (C)lassifica o (ESC) per uscire."
            )
            continue

        if tasto_cmd:
            azione_compiuta = False
            perc_precedente = perc_comp

            if tasto_cmd == "m":
                Menu()
            elif tasto_cmd == "b":
                braille_prompt = not braille_prompt
                print(
                    f"Prompt Braille: {'ON' if braille_prompt else 'OFF'}."
                )
                riproduci_suono("click")
                SalvaPartita(
                    engine,
                    mosse_partita,
                    t_totale if partita_in_corso else 0,
                    nome_giocatore,
                    classifica,
                    perc_comp,
                    braille_prompt,
                    messaggio=False,
                )
            elif tasto_cmd == "a":
                audio_attivo = not audio_attivo
                print(f"Effetti Audio: {'ON' if audio_attivo else 'OFF'}.")
                if audio_attivo:
                    riproduci_suono("click")
                SalvaPartita(
                    engine,
                    mosse_partita,
                    t_totale if partita_in_corso else 0,
                    nome_giocatore,
                    classifica,
                    perc_comp,
                    braille_prompt,
                    messaggio=False,
                )
            elif tasto_cmd in (chr(27), "esc"):
                break

            elif tasto_cmd in "123":
                if not partita_in_corso:
                    print("Nessuna partita in corso.")
                    continue
                idx_rc = int(tasto_cmd) - 1
                direzione_tasto_scelta = ""
                prompt_dir = f"\rSposta {idx_rc+1}>\r"
                while True:
                    temp_input_dir = key(
                        prompt=prompt_dir, attesa=99999
                    ).lower()
                    if temp_input_dir in "ijkm" or temp_input_dir in (
                        chr(27),
                        "esc",
                    ):
                        direzione_tasto_scelta = temp_input_dir
                        break
                if direzione_tasto_scelta in (chr(27), "esc"):
                    continue

                if direzione_tasto_scelta == "i":
                    engine.sposta_colonna_verticale(idx_rc, verso_alto=True)
                    azione_compiuta = True
                elif direzione_tasto_scelta == "m":
                    engine.sposta_colonna_verticale(idx_rc, verso_alto=False)
                    azione_compiuta = True
                elif direzione_tasto_scelta == "k":
                    engine.sposta_riga_orizzontale(idx_rc, verso_destra=True)
                    azione_compiuta = True
                elif direzione_tasto_scelta == "j":
                    engine.sposta_riga_orizzontale(idx_rc, verso_destra=False)
                    azione_compiuta = True

            # Comandi 4-9 per rotazioni di Faccia Anteriore, Mediana, Posteriore
            elif tasto_cmd == "4":
                engine.rotazione_faccia_anteriore(oraria=False)
                print("Faccia anteriore ruotata antioraria.")
                azione_compiuta = True
            elif tasto_cmd == "5":
                engine.rotazione_faccia_anteriore(oraria=True)
                print("Faccia anteriore ruotata oraria.")
                azione_compiuta = True
            elif tasto_cmd == "6":
                engine.rotazione_sezione_mediana_frontale(oraria=False)
                print("Sezione mediana ruotata antioraria.")
                azione_compiuta = True
            elif tasto_cmd == "7":
                engine.rotazione_sezione_mediana_frontale(oraria=True)
                print("Sezione mediana ruotata oraria.")
                azione_compiuta = True
            elif tasto_cmd == "8":
                engine.rotazione_faccia_posteriore(oraria=False)
                print("Faccia posteriore ruotata antioraria.")
                azione_compiuta = True
            elif tasto_cmd == "9":
                engine.rotazione_faccia_posteriore(oraria=True)
                print("Faccia posteriore ruotata oraria.")
                azione_compiuta = True

            elif tasto_cmd == "h":
                Istruzioni()
            elif tasto_cmd == "c":
                MostraClassifica(classifica)
            elif tasto_cmd == "t":
                if partita_in_corso:
                    h, m, s = ConvertiInTempo(t_totale)
                    print(
                        f"\nTempo: {h:02d} ore, {m:02d} minuti, {s:02d} secondi. Mosse: {mosse_partita}."
                    )
                else:
                    print("\nNessuna partita avviata.")
            elif tasto_cmd == "n":
                if (
                    partita_in_corso
                    and key(
                        prompt="\rPerderai la partita in corso. Proseguire? (S/N)\r"
                    ).lower()
                    != "s"
                ):
                    print("\nOk, continua pure.")
                    continue
                (
                    partita_in_corso,
                    mosse_partita,
                    t_inizio_session,
                    t_base_partita,
                    nome_giocatore,
                    perc_comp,
                ) = IniziaNuovaPartita(engine)

            elif tasto_cmd in "sdexwf":
                map_tasti_faccia = {
                    "s": FACCIA_SINISTRA,
                    "d": FACCIA_DESTRA,
                    "e": FACCIA_SUPERIORE,
                    "x": FACCIA_INFERIORE,
                    "f": FACCIA_ANTERIORE,
                    "w": FACCIA_POSTERIORE,
                }
                fid = map_tasti_faccia[tasto_cmd]
                ultima_faccia_visualizzata_id = fid
                faccia_obj = engine.facce[fid]
                nome_faccia_display = FACCIA_ID_TO_NOME[fid]

                if braille_prompt:
                    print(f"\nFaccia {nome_faccia_display}:")
                    for riga in faccia_obj.y:
                        print(
                            "".join(
                                [
                                    COLOR_TO_NUMBER.get(colore, "0")
                                    for colore in riga
                                ]
                            )
                        )
                else:
                    print(
                        f"\nFaccia {nome_faccia_display}:\n{faccia_obj!s}"
                    )

            if mossa_eseguita := azione_compiuta:
                mosse_partita += 1
                perc_comp = engine.calcola_percentuale()

                # Feedback audio differenziato per la percentuale
                if perc_comp > perc_precedente:
                    riproduci_suono("mossa_su")
                elif perc_comp < perc_precedente:
                    riproduci_suono("mossa_giu")
                else:
                    riproduci_suono("mossa_neutra")

                if perc_comp == 100:
                    t_finale = t_base_partita + (
                        time.time() - t_inizio_session
                        if t_inizio_session > 0
                        else 0
                    )
                    h, m, s = ConvertiInTempo(t_finale)
                    riproduci_suono("vittoria")
                    print(f"\nCONGRATULAZIONI {nome_giocatore}!")
                    print(
                        f"Cubo risolto in {mosse_partita} mosse. Tempo: {h:02d} ore, {m:02d} minuti, {s:02d} secondi."
                    )
                    if nome_giocatore == NOME_SCONOSCIUTO:
                        nome_class = ""
                        while not nome_class:
                            nome_class = (
                                input("Nome per classifica (max 12 caratteri): ")
                                .strip()[:12]
                            )
                        nome_giocatore = (
                            nome_class if nome_class else NOME_SCONOSCIUTO
                        )

                    classifica = AggiornaSalvaClassifica(
                        classifica, nome_giocatore, mosse_partita, t_finale
                    )
                    MostraClassifica(classifica)

                    partita_in_corso = False
                    mosse_partita = 0
                    t_base_partita = 0
                    t_inizio_session = 0
                    SalvaPartita(
                        engine,
                        mosse_partita,
                        t_base_partita,
                        nome_giocatore,
                        classifica,
                        perc_comp,
                        braille_prompt,
                    )
                    print("\nPremi N per una nuova partita, o ESC per uscire.")

    # Uscita dal gioco (dopo ESC)
    if partita_in_corso:
        if (
            key(prompt="\rVuoi salvare il lavoro svolto? (S/N)\r").lower()
            == "s"
        ):
            t_da_salvare = t_base_partita + (
                time.time() - t_inizio_session if t_inizio_session > 0 else 0
            )
            SalvaPartita(
                engine,
                mosse_partita,
                t_da_salvare,
                nome_giocatore,
                classifica,
                perc_comp,
                braille_prompt,
            )
        else:
            print("\nBene, non salvo lo stato della partita.")
            # Salva comunque le impostazioni audio e braille aggiornate
            SalvaPartita(
                engine,
                0,
                0,
                nome_giocatore,
                classifica,
                perc_comp,
                braille_prompt,
                messaggio=False,
            )
    else:
        # Nessuna partita attiva: salva comunque la configurazione impostazioni
        SalvaPartita(
            engine,
            0,
            0,
            nome_giocatore,
            classifica,
            perc_comp,
            braille_prompt,
            messaggio=False,
        )

    print("\nChiusura di Rubik Accessibile.\nArrivederci!")