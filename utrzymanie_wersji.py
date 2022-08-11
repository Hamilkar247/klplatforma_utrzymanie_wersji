import os
from re import L
import sys
import shutil
import subprocess
from datetime import datetime
import time
import traceback
import urllib.request
import zipfile
from dotenv import load_dotenv
import json
import signal
import psutil
from funkcje_pomocnicze import FunkcjePomocnicze

#####################

def nazwa_programu():
    return "update_projektu_skryptu_klraspi.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp


#######################
class UtrzymanieWersji():
    
    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()


    def pobierz_z_outsystemu_date_wersji(self):
        self.fp.drukuj("def: pobierz_z_outsystemu_date_wersji")
        url_wersji_programu=os.getenv("url_wersja_programu")
        content_new=[]
        data=""
        #przykladowy docelowy url https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/ProgramSettings
        try:
            with urllib.request.urlopen(url_wersji_programu) as url:
                content_new = json.loads(url.read()) #json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())
            print(content_new)
            #print(content_new[0])
            for ustawienie in content_new:
                print(ustawienie)
                if "Name" in ustawienie:
                    if ustawienie["Name"] == "obecna_wersja_czasowa_oprogramowania_na_produkcji":
                        data=ustawienie['Value']
        except Exception as e:
            self.fp.drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
            self.fp.drukuj(f"exception {e}")
            self.fp.drukuj(f"sprawdz link: {url_wersji_programu}")
            traceback.print_exc()
        return data
        #return "03/08/22 12:07:09"
    
    def pobierz_aktualna_wersje(self, spodziewana_data_wersji, basic_path_projektu, basic_path_ram):
        self.fp.drukuj("def: pobierz_aktualna_wersje")
        url_zip_code_repo=os.getenv("url_zip_code_repo")
        urllib.request.urlretrieve(url_zip_code_repo, f"{basic_path_ram}/skrypty_klraspi.zip")
        with zipfile.ZipFile(f"{basic_path_ram}/skrypty_klraspi.zip", "r") as zip_ref:
            zip_ref.extractall(f"{basic_path_ram}/skrypty_klraspi_tymczasowy")
        
        path_commit_txt=f"{basic_path_ram}/skrypty_klraspi_tymczasowy/skrypty_klraspi-master/commit.txt"
        if os.path.exists(path_commit_txt):
            self.fp.drukuj(f"plik z commitem z pobranej paczki istniej {path_commit_txt}")
            file_commit=open(path_commit_txt, "r")
            commit_data=str(file_commit.read()).strip()
            if spodziewana_data_wersji==commit_data:
                return commit_data
            else:
                self.fp.drukuj(f"spodziewana_data_wersji==commit_data: {spodziewana_data_wersji}=={commit_data} - a więc zwracam nic" )
                return ""
        else:
            self.fp.drukuj(f"nie ma pliku w scieszce {path_commit_txt} - zwracam nic")
        return ""
    
    def zwroc_stan_projektu(self, basic_path_skryptu_klraspi):
        self.fp.drukuj("def: zwroc_stan_projektu")
        scieszka_do_pliku_commit=f"{basic_path_skryptu_klraspi}/commit.txt"
        if os.path.exists(scieszka_do_pliku_commit):
            file=open(scieszka_do_pliku_commit, "r")
            data=file.read().strip()
            self.fp.drukuj(f"zwracam date z commit.txt: {data}")
        else:
            data="brak pliku"
        return data
    
    def przekopiuj_stary_env(self, basic_path_skryptu_klraspi):
        self.fp.drukuj("def: przekopiuj_stary_env - UWAGA to chwile trwa")
        if os.path.exists(".env_skopiowany"):
            shutil.copyfile(".env_skopiowany", f"{basic_path_skryptu_klraspi}/.env")    
    
    def virtualenv_i_instalacja_libek(self):
        self.fp.drukuj("def: virtualenv_i_instalacja_libek")
        if os.name == "posix":
            bash_command=f"{os.getcwd()}/linux_bash_do_instalacji_libek_w_venv.sh".split()
            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            self.fp.drukuj(f"stdout: {stdout}")
            self.fp.drukuj(f"stderr: {stderr}")
        else:
            raise self.fp.exceptionWindows
    
    def zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(self, basic_path_ram, basic_path_skryptu_klraspi):
        self.fp.drukuj("def: zachomikuj_stary_env_i_usun_stary_projekt")
        if os.path.isdir(f"{basic_path_skryptu_klraspi}") == True:
            if os.path.exists(f"{basic_path_skryptu_klraspi}/.env"):
                shutil.copyfile(f"{basic_path_skryptu_klraspi}/.env", ".env_skopiowany")
            if os.path.isdir(basic_path_skryptu_klraspi):
                shutil.rmtree(f"{basic_path_skryptu_klraspi}") 
        path_to_tymczasowy_miejsce_pobranego_programu=f"{basic_path_ram}/skrypty_klraspi_tymczasowy/skrypty_klraspi-master"
        if os.path.isdir(path_to_tymczasowy_miejsce_pobranego_programu):
            shutil.move(path_to_tymczasowy_miejsce_pobranego_programu, f"{basic_path_skryptu_klraspi}")
            shutil.rmtree(f"{basic_path_ram}/skrypty_klraspi_tymczasowy") #usuwa juz pusty folder - zawartosc zostala juz przeniesiona
            os.remove(f"{basic_path_ram}/skrypty_klraspi.zip")
            self.przekopiuj_stary_env(basic_path_skryptu_klraspi)
            self.virtualenv_i_instalacja_libek()
            self.fp.drukuj("usunalem stary kod i zachomikowalem .env")
        else:
            self.fp.drukuj("nie udalo sie przeniesc pliku - chyba kwestia - bo może nie ma")
    
    def sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(basic_path_ram):
        skrypty_klraspi_path=f"{basic_path_ram}/uruchom_skrypt_o_godzinie.py.flara"
        if os.path.exists(skrypty_klraspi_path) == True:
            with open(skrypty_klraspi_path, "r") as file:
                linie=file.readline()
            numer_pid=int(linie)
            if os.name == "posix":
                if int(numer_pid)>-1:
                    if psutil.pid_exists(numer_pid) == True:
                        os.kill(int(numer_pid), signal.SIGTERM)
                        os.remove(skrypty_klraspi_path)
            else:
                raise self.fp.ExceptionWindows

##################

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    basic_path_skryptu_klraspi=""
    path_preflara=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        dotenv_path = "./.env_projektu"
        fp.file_istnienie(dotenv_path, "dotenv_path - sprawdz .env_projektu")
        load_dotenv(dotenv_path)
        # pobierz_z_outsystemu_date_wersji()
        uw=UtrzymanieWersji()
        while True:
            if os.name == "posix":
                fp.drukuj("posix")
                basic_path_ram=fp.zmienna_env_folder("basic_path_ram", ".env_projektu - problem z basic_path_ram")
                basic_path_skryptu_klraspi=os.getenv("basic_path_skryptu_klraspi")
                head, tail = os.path.split(basic_path_skryptu_klraspi)
                if os.path.isdir(head) == False:
                    fp.drukuj(f"basic_path_skryptu_klraspi - head: {head}")
                    raise fp.exceptionEnvProjektu
                #pobierz_aktualna_wersje()
                obecny_projekt=uw.zwroc_stan_projektu(basic_path_skryptu_klraspi)
                obecny_na_outsystem=uw.pobierz_z_outsystemu_date_wersji()
                #preflara do umozliwienia uruchomienia sie skrypty_klraspi
                path_preflara=f"{basic_path_ram}/uruchom_skrypty_klraspi.preflara"
                if obecny_projekt==obecny_na_outsystem:
                    fp.drukuj("mamy zbieznosc ;) - nic nie robie")
                    if os.path.exists(path_preflara) == False:
                        file=open(path_preflara, "w")
                        file.write(f"{os.getpid()}")
                elif obecny_projekt=="brak pliku":
                    if os.path.exists(path_preflara):
                        os.remove(path_preflara)
                    fp.drukuj("brak pliku - pierwszy raz pobieram z repa")
                    fp.drukuj("rozpoczynam pobieranie z repa")
                    text=uw.pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                    if text != "":
                        uw.zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(basic_path_ram, basic_path_skryptu_klraspi)
                        file=open(path_preflara, "w")
                        file.write(f"{os.getpid()}")
                    fp.drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                    fp.drukuj("koniec elif")
                else:
                    if os.path.exists(path_preflara):
                        os.remove(path_preflara)
                    uw.sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(basic_path_ram)
                    fp.drukuj("rozpoczynam pobieranie z repa")
                    #zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                    wersja_na_outsystemie=uw.pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                    fp.drukuj(f"wersja_na_outsystemie: {wersja_na_outsystemie}")
                    if wersja_na_outsystemie != "":
                        fp.drukuj("akcja w else")
                        uw.zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(basic_path_ram, basic_path_skryptu_klraspi)
                        uw.przekopiuj_stary_env(basic_path_skryptu_klraspi)
                        fp.drukuj("przekopiowalem stary env")
                        fp.drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                        file=open(path_preflara, "w")
                        file.write(f"{os.getpid()}")
                    else:
                        fp.drukuj("brak akcji w else")
                    fp.drukuj("koniec elsa")
                fp.drukuj("proces zakonczony") 
                time.sleep(5*60)
            fp.usun_flare(basic_path_ram, path_preflara)
    except TypeError as e:
        fp.drukuj(f"exception: {e}")
        raise fp.exceptionEnvProjektu
    except fp.exceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"czy napewno skopiowales .env_projektu.example na .env_projektu, i zmieniles tam scieszki zalezne? Tak tylko pytam...")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except fp.ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy .env_projektu widziany jest menadzer zadan/crontab")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)

if __name__ == "__main__":
    main()
