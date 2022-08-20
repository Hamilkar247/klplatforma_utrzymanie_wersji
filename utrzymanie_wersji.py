from inspect import trace
import os
from re import L
import requests
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
from funkcje_pomocnicze import ExceptionVirtualenv, ExceptionRepository, FunkcjePomocnicze, ExceptionWindows, ExceptionNotExistFolder, ExceptionEnvProjektu
from getmac import get_mac_address as gma
import socket
from pytz import timezone
#####################

def nazwa_programu():
    return "utrzymanie_wersji.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

#######################
class UtrzymanieWersji():
    
    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()
        
        self.klplatforma_odbior_wysylka="klplatforma_odbior_wysylka"
        #self.klplatforma_odbior_wysylka_tymczasowy="klplatforma_odbior_wysylka_tymczasowy"
        self.nazwa_pliku_z_data_programu="commit.txt"

        self.url_wersji_programu=os.getenv("url_wersja_programu")
        self.docelowy_url_dla_logow=os.getenv("docelowy_url_dla_logow")
        self.url_zip_code_repo=os.getenv("url_zip_code_repo")
        self.basic_path_ram=os.getenv("basic_path_ram")

    def pobierz_z_outsystemu_date_wersji(self):
        self.fp.drukuj("def: pobierz_z_outsystemu_date_wersji")
        content_new=[]
        data=""
        #przykladowy docelowy url https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/ProgramSettings
        try:
            with urllib.request.urlopen(self.url_wersji_programu) as url:
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
            self.fp.drukuj(f"sprawdz link: {self.url_wersji_programu}")
            traceback.print_exc()
        return data
        #return "03/08/22 12:07:09"
    
    def pobierz_aktualna_wersje(self, spodziewana_data_wersji, basic_path_projektu, basic_path_ram):
        self.fp.drukuj("def: pobierz_aktualna_wersje")

        urllib.request.urlretrieve(self.url_zip_code_repo, f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}.zip")
        path_commit_txt=""
        try: 
            self.fp.drukuj("otwieranie zipa")
            with zipfile.ZipFile(f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}.zip", "r") as zip_ref:
                zip_ref.extractall(f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}_tymczasowy")
        
            path_commit_txt=f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}_tymczasowy/{self.klplatforma_odbior_wysylka}-master/{self.nazwa_pliku_z_data_programu}"
        except Exception as e:
            self.fp.drukuj(f"exception: {e}")
            self.fp.drukuj("program był pisany pod pobieranie zipów z githuba - w przypadku zmiany hostingu może być problem ")
            traceback.print_exc()
            
        if os.path.exists(path_commit_txt):
            self.fp.drukuj(f"plik z commitem z pobranej paczki istniej {path_commit_txt}")
            file_commit=open(path_commit_txt, "r")
            commit_data=str(file_commit.read()).strip()
            if spodziewana_data_wersji==commit_data:
                return commit_data
            else:
                self.fp.drukuj(f"spodziewana_data_wersji==commit_data: {spodziewana_data_wersji}=={commit_data} - a więc zwracam nic" )
                self.fp.drukuj("UWAGA czy napewno wypchnąłeś danem git push --force na repo? wyglada na niespojnosci daty settingsie programu na frontendzie z  ")
                raise ExceptionRepository
                return ""
        else:
            self.fp.drukuj(f"nie ma pliku w scieszce {path_commit_txt} - zwracam nic")
        return ""
    
    def zwroc_stan_projektu(self, basic_path_klplatforma_odbior_wysylka):
        self.fp.drukuj("def: zwroc_stan_projektu")
        scieszka_do_pliku_commit=f"{basic_path_klplatforma_odbior_wysylka}/{self.nazwa_pliku_z_data_programu}"
        if os.path.exists(scieszka_do_pliku_commit):
            file=open(scieszka_do_pliku_commit, "r")
            data=file.read().strip()
            self.fp.drukuj(f"zwracam date z {self.nazwa_pliku_z_data_programu}: {data}")
        else:
            data="brak pliku"
        return data

    def istnienie_virtualenv(self, basic_path_klplatforma_odbior_wysylka):
        self.fp.drukuj("def: istnienie_virtualenv")
        scieszka_do_virtualenvironment=f"{basic_path_klplatforma_odbior_wysylka}/venv"
        if os.path.isdir(scieszka_do_virtualenvironment):
            self.fp.drukuj("jest venv")
            return True
        else:
            self.fp.drukuj("nie ma venva - trzeba go stworzyc")
            return False

    def przekopiuj_stary_env(self, basic_path_klplatforma_odbior_wysylka):
        self.fp.drukuj("def: przekopiuj_stary_env - UWAGA to chwile trwa")
        if os.path.exists(".env_skopiowany"):
            shutil.copyfile(".env_skopiowany", f"{basic_path_klplatforma_odbior_wysylka}/.env")    

    def virtualenv_i_instalacja_libek(self):
        self.fp.drukuj("def: virtualenv_i_instalacja_libek")
        if os.name == "posix":
            self.fp.drukuj(f"aktualny folder roboczy {os.getcwd()}")
            plik_bash=f"{os.getcwd()}/linux_bash_do_instalacji_libek_w_venv.sh"
            if os.path.exists(plik_bash) == True:
                bash_command=f"{os.getcwd()}/linux_bash_do_instalacji_libek_w_venv.sh".split()
                process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                stdout=stdout.decode("utf-8")
                stderr=stderr.decode("utf-8")
                self.fp.drukuj(f"stdout:\n {stdout}")
                self.fp.drukuj(f"stderr:\n {stderr}")
            if os.path.isdir(f"../{self.klplatforma_odbior_wysylka}/venv") == False:
                self.fp.drukuj("no i nadal nie ma")
                raise ExceptionVirtualenv
        else:
            raise ExceptionWindows

    def zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(self, basic_path_ram, basic_path_klplatforma_odbior_wysylka):
        self.fp.drukuj("def: zachomikuj_stary_env_i_usun_stary_projekt")
        if os.path.isdir(f"{basic_path_klplatforma_odbior_wysylka}") == True:
            if os.path.exists(f"{basic_path_klplatforma_odbior_wysylka}/.env"):
                shutil.copyfile(f"{basic_path_klplatforma_odbior_wysylka}/.env", ".env_skopiowany")
            if os.path.isdir(basic_path_klplatforma_odbior_wysylka):
                shutil.rmtree(f"{basic_path_klplatforma_odbior_wysylka}") 
        path_to_tymczasowy_miejsce_pobranego_programu=f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}_tymczasowy/{self.klplatforma_odbior_wysylka}-master"
        if os.path.isdir(path_to_tymczasowy_miejsce_pobranego_programu):
            shutil.move(path_to_tymczasowy_miejsce_pobranego_programu, f"{basic_path_klplatforma_odbior_wysylka}")
            shutil.rmtree(f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}_tymczasowy") #usuwa juz pusty folder - zawartosc zostala juz przeniesiona
            os.remove(f"{basic_path_ram}/{self.klplatforma_odbior_wysylka}.zip")
            self.przekopiuj_stary_env(basic_path_klplatforma_odbior_wysylka)
            self.virtualenv_i_instalacja_libek()
            self.fp.drukuj("usunalem stary kod i zachomikowalem .env")
        else:
            self.fp.drukuj("nie udalo sie przeniesc pliku - chyba kwestia - bo może nie ma")
    
    def sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(self, basic_path_ram):
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
                raise ExceptionWindows

    def operacja_wyslania_loga_serwer(self, flaga_stworzenie_venv, flaga_pobranie_wersji_z_repo):
        self.flaga_stworzenie_venv=flaga_stworzenie_venv
        self.flaga_pobranie_wersji_z_repo=flaga_pobranie_wersji_z_repo
        self.wysylka_loga_na_serwer()

    def wylicz_status_platform(self):
        status=0
        if self.flaga_stworzenie_venv==True:
            status=status+262144 #2^18
        if self.flaga_pobranie_wersji_z_repo==True:
            status=status+524288 #2^19

    def wysylka_loga_na_serwer(self):
        json_data = {
            "wersja_json": "0.8",
            "sn_platform": self.get_mac_address(),#self.sn_platform,
            #nie potrzebne#"sn_device_mother": self.mother_serial_number,
            "status_platform": self.wylicz_status_platform(),
            "zasieg_platform_wifi": "-1",
            "bateria_platform": "-1",
            "local_ipv4": self.getIPV4(),
            "timezone": self.get_diff(datetime.now(), "Europe/Warsaw"),
            "data": []
        }
        json_object = json.dumps(json_data, indent = 4)
        slownik_response = self.wyslanie_obiektu_json_z_danymi(json_data)
        #dopisac ze zalezy od OK=200
        self.fp.drukuj(f"slownik_response: {slownik_response}")
        self.fp.drukuj(type(slownik_response['status_code'] ))
        self.fp.drukuj(type(slownik_response["sukces_zapisu"]))
        if slownik_response['status_code'] == "200" and slownik_response["sukces_zapisu"] == "True":
            with open(f"{self.basic_path_ram}/wysylka.log", "a") as logi:
                logi.write(f"log_klplatforma\n")
                logi.write(f"status_code:{slownik_response['status_code']}\n")
                logi.write(f"sukces_zapisu:{slownik_response['sukces_zapisu']}\n")
            with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                status_logi.write(f"------------------\n")
                status_logi.write(f"{self.fp.data_i_godzina()}\n")
                status_logi.write(f"{self.wylicz_status_platform()}\n")

    def wyslanie_obiektu_json_z_danymi(self, json_object):
        #shutil.copy2(self.path_plik_z_krotkami_do_wysylki_file, self.path_plik_z_krotkami_do_wysylki_file+".work")
        #print(json_object)
        dict_zwracany={"status_code":"0", "sukces_zapisu":"False", "error_text":"brak"}
        try:
            response = requests.post(
                self.docelowy_url_dla_logow,
                json=json_object,
            )
            self.fp.drukuj(f"response.txt: {response.text}")
            #mogę jeszcze sprawdzać Success
            print(f"response.status_code: {response.status_code}")
            if response.status_code == 200:
                self.fp.drukuj("poprawna odpowiedż serwera")
                json_response=json.loads(response.text)
                print(json_response)
                dict_zwracany['status_code']="200"
                try:
                    if json_response["Success"] is not None:
                        czy_sukces=json_response["Success"]
                        if czy_sukces == True:
                            pass
                            print("jest")
                        else:
                            self.fp.drukuj(f"Success:{czy_sukces}")
                        dict_zwracany["sukces_zapisu"]=str(f"{czy_sukces}")
                except KeyError as e:
                    self.fp.drukuj(f"Nie ma takiego parametru w odeslanym jsonie z outsystemu {e}")
                    dict_zwracany["sukces_zapisu"]=str(f"{False}")
            else:
                self.fp.drukuj("błędna odpowiedź serwera")
                self.fp.drukuj(f"response.status_code: {response.status_code}")
        except urllib.error.URLError as e:
            self.fp.drukuj(f"Problem z wyslaniem pakietu: {e}")
            traceback.print_exc()
        except Exception as e:
            self.fp.drukuj("zlapałem wyjatek: {e}")
            traceback.print_exc()
        self.fp.drukuj(f"dict_zwracany: {type(dict_zwracany)}")
        return dict_zwracany

    def get_mac_address(self):
        if os.name == "posix":
            self.fp.drukuj(f"mac_address:{gma()}")
            return gma()
        else:
            drukuj("brak oprogramowanego windowsa")
            raise ExceptionWindows

    #trzeba zastapic libka pythonowa by uniezaleźnić od basha
    def getIPV4(self):
        try:
            str_ip="nie wyznaczono"
            self.fp.drukuj("def: getIPV4")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print(s.getsockname()[0])
            str_ip=s.getsockname()[0]
            if str_ip is None:
                self.fp.drukuj("nie udało się wyznaczyć numeru ip w sieci lokalnej")
                str_ip=f"nie wyznaczono"
                
        except Exception as e:
            self.fp.drukuj(f"getIPV4: wystapil blad {e}")
            str_ip=f"nie wyznaczono"
            traceback.print_exc()
        return str_ip

    def get_diff(self, now, tzname):
        tz = timezone(tzname)
        utc = timezone('UTC')
        utc.localize(datetime.now())
        delta =  utc.localize(now) - tz.localize(now)
        print(delta)
        delta=str(delta).split(":")[0]
        delta="+"+delta
        print(delta)
        return delta

##################

def tworze_flare_na_znak_ze_mozna_uruchamiac_program(path_preflara):
    file=open(path_preflara, "w")
    file.write(f"{os.getpid()}")

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    basic_path_klplatforma_odbior_wysylka=""
    path_preflara=""
    flaga_pobranie_wersji_z_repo=False
    flaga_stworzenie_venv=False
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        dotenv_path = "./.env_projektu"
        fp.file_istnienie(dotenv_path, "dotenv_path - sprawdz .env_projektu")
        load_dotenv(dotenv_path)
        # pobierz_z_outsystemu_date_wersji()
        uw=UtrzymanieWersji()
        sekund=120
        while True:
            if os.name == "posix":
                fp.drukuj("posix")
                basic_path_ram=os.getenv("basic_path_ram")
                if basic_path_ram == "":
                    raise ExceptionEnvProjektu
                fp.drukuj(f"ahjo - basic_path_ram {basic_path_ram}")
                head, tail = os.path.split(basic_path_ram)
                if os.path.isdir(head) == True:
                    if os.path.isdir(basic_path_ram) == False:
                        os.mkdir(basic_path_ram)
                        fp.drukuj(f"stworzylem folder {basic_path_ram}")
                else:
                    fp.drukuj("sprawdz basic_path_ram")
                    raise ExceptionEnvProjektu
                basic_path_klplatforma_odbior_wysylka=os.getenv("basic_path_klplatforma_odbior_wysylka")
                head, tail = os.path.split(basic_path_klplatforma_odbior_wysylka)
                if os.path.isdir(head) == False:
                    fp.drukuj(f"basic_path_klplatforma_odbior_wysylka - head: {head}")
                    raise ExceptionEnvProjektu
                #pobierz_aktualna_wersje()
                obecny_projekt=uw.zwroc_stan_projektu(basic_path_klplatforma_odbior_wysylka)
                obecny_na_outsystem=uw.pobierz_z_outsystemu_date_wersji()
                #preflara do umozliwienia uruchomienia sie skrypty_klraspi
                fp.drukuj(f"obecny_na_outsystem: {obecny_na_outsystem}")
                path_preflara=f"{basic_path_ram}/{nazwa_programu()}.preflara"
                if obecny_projekt == obecny_na_outsystem:
                    fp.drukuj("mamy zbieznosc ;) - nic nie robie")
                    if uw.istnienie_virtualenv(basic_path_klplatforma_odbior_wysylka) == False:
                        uw.virtualenv_i_instalacja_libek()
                        flaga_stworzenie_venv=True
                    flaga_pobranie_wersji_z_repo=False
                    tworze_flare_na_znak_ze_mozna_uruchamiac_program(path_preflara)
                    
                elif obecny_projekt == "brak pliku":
                    if os.path.exists(path_preflara):
                        os.remove(path_preflara)
                    fp.drukuj("brak pliku - pierwszy raz pobieram z repa")
                    fp.drukuj("rozpoczynam pobieranie z repa")
                    text=uw.pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_klplatforma_odbior_wysylka, basic_path_ram=basic_path_ram)
                    if text != "":
                        uw.zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(basic_path_ram, basic_path_klplatforma_odbior_wysylka)
                        flaga_stworzenie_venv=True
                        flaga_pobranie_wersji_z_repo=True
                        tworze_flare_na_znak_ze_mozna_uruchamiac_program(path_preflara)
                    fp.drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                    fp.drukuj("koniec elif")
                else:
                    if os.path.exists(path_preflara):
                        os.remove(path_preflara)
                    uw.sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(basic_path_ram)
                    fp.drukuj("rozpoczynam pobieranie z repa")
                    #zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                    wersja_na_outsystemie=uw.pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_klplatforma_odbior_wysylka, basic_path_ram=basic_path_ram)
                    fp.drukuj(f"wersja_na_outsystemie: {wersja_na_outsystemie}")
                    if wersja_na_outsystemie != "":
                        fp.drukuj("akcja w else")
                        uw.zachomikuj_stary_env_i_usun_stary_projekt_przenies_nowy_w_jego_miejsce(basic_path_ram, basic_path_klplatforma_odbior_wysylka)
                        uw.przekopiuj_stary_env(basic_path_klplatforma_odbior_wysylka)
                        fp.drukuj("przekopiowalem stary env")
                        fp.drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                        tworze_flare_na_znak_ze_mozna_uruchamiac_program(path_preflara)
                        flaga_stworzenie_venv=True
                        flaga_pobranie_wersji_z_repo=True
                    else:
                        fp.drukuj("brak akcji w else")
                    fp.drukuj("koniec elsa")
                with open(f"{basic_path_ram}/sprawdzanie_repa.log", "a") as spr_repa_logi:
                    spr_repa_logi.write(f"------------------\n")
                    spr_repa_logi.write(f"{fp.data_i_godzina()}\n")
                    spr_repa_logi.write(f"flaga_stworzenie_venv: {flaga_stworzenie_venv}\n")
                    spr_repa_logi.write(f"flaga_pobranie_wersji_z_repa: {flaga_pobranie_wersji_z_repo}\n")
                uw.operacja_wyslania_loga_serwer(flaga_stworzenie_venv, flaga_pobranie_wersji_z_repo)
                fp.drukuj(f"proces zakonczony - czekamy {sekund} sekund") 
            time.sleep(sekund)
        #już poza pętlą - a więc zamykając program warto usunąć preflare programu
    except TypeError as e:
        fp.drukuj(f"exception: {e}")
        raise ExceptionEnvProjektu
    except ExceptionRepository as e:
        fp.drukuj(f"exception: ExceptionRepository")
        fp.drukuj("Wyglada na to że niespójna jest data programu miedzy repozytorium a frontend - sprawdz czy zrobiles git push --force w ostatnich zmianach")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except ExceptionVirtualenv as e:
        fp.drukuj(f"exception:  ExceptionVirtualenv ")
        fp.drukuj("Problem z stworzeniem virtualenv venv niestety")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception ExceptionEnvProjektu")
        fp.drukuj(f"czy napewno skopiowales .env_projektu.example na .env_projektu, i zmieniles tam scieszki zalezne? Tak tylko pytam...")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except ExceptionWindows as e:
        fp.drukuj(f"exception ExceptionWindows")
        fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy .env_projektu widziany jest menadzer zadan/crontab")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, path_preflara)
    fp.drukuj("koniec_programu")

if __name__ == "__main__":
    main()
