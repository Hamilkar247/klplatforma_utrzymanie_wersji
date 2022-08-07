import os
from re import L
import sys
import shutil
import subprocess
from datetime import datetime
import traceback
import urllib.request
import zipfile
from dotenv import load_dotenv
import json
import signal

def nazwa_programu():
    return "update_projektu_skryptu_klraspi.py"

def data_i_godzina():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%y %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print(e)
        print(traceback.print_exc())

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

class ExceptionEnvProjektu(Exception):
    pass

class ExceptionWindows(Exception):
    pass

def file_istnienie(path_to_file, komunikat):
    if os.path.isdir(path_to_file):
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def folder_istnienie(path_to_folder, komunikat):
    if os.path.isdir(path_to_folder):
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def zmienna_env_file(tag_in_env, komunikat):
    path_to_file=os.getenv(tag_in_env)
    if os.path.exists(path_to_file) == False:
        drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_file}")#sprawdz czy plik .env istnieje")
        raise ExceptionEnvProjektu
    return path_to_file

def zmienna_env_folder(tag_in_env, komunikat):
    path_to_folder=os.getenv(tag_in_env)
    if os.path.isdir(path_to_folder) == False:
        drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_folder}")#sprawdz czy plik .env istnieje")
        raise ExceptionEnvProjektu
    return path_to_folder

def usun_flare(folder_do_sprawdzenia, flara_do_sprawdzenia):
    if os.path.isdir(folder_do_sprawdzenia):
        if os.path.exists(flara_do_sprawdzenia):
            os.remove(flara_do_sprawdzenia)
            drukuj("usuwam flare")

def stworz_flare_z_pid(flara_path):
    flara_file=open(flara_path, "w")
    flara_file.write(f"{str(os.getpid())}")
    flara_file.close()

###################################

def pobierz_z_outsystemu_date_wersji():
    drukuj("def: pobierz_z_outsystemu_date_wersji")
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
            if ustawienie["Name"] == "obecna_wersja_czasowa_oprogramowania_na_produkcji":
                data=ustawienie['Value']
    except Exception as e:
        drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
        drukuj(f"{e}")
        drukuj(f"sprawdz link: {url}")
        traceback.print_exc()
    print
    return data
    #return "03/08/22 12:07:09"

def pobierz_aktualna_wersje(spodziewana_data_wersji, basic_path_projektu, basic_path_ram):
    drukuj("def: pobierz_aktualna_wersje")
    url_zip_code_repo=os.getenv("url_zip_code_repo")
    urllib.request.urlretrieve(url_zip_code_repo, f"{basic_path_ram}/skrypty_klraspi.zip")
    with zipfile.ZipFile(f"{basic_path_ram}/skrypty_klraspi.zip", "r") as zip_ref:
        zip_ref.extractall(f"{basic_path_ram}/skrypty_klraspi_tymczasowy")
    
    path_commit_txt=f"{basic_path_ram}/skrypty_klraspi_tymczasowy/skrypty_klraspi-master/commit.txt"
    if os.path.exists(path_commit_txt):
        drukuj("jestem")
        file_commit=open(path_commit_txt, "r")
        commit_data=str(file_commit.read()).strip()
        if spodziewana_data_wersji==commit_data:
            return commit_data
        else:
            return ""
    return ""

def zwroc_stan_projektu(basic_path_skryptu_klraspi):
    drukuj("def: zwroc_stan_projektu")
    scieszka_do_pliku_commit=f"{basic_path_skryptu_klraspi}/commit.txt"
    if os.path.exists(scieszka_do_pliku_commit):
        file=open(scieszka_do_pliku_commit, "r")
        data=file.read().strip()
        drukuj(f"zwracam date z commit.txt: {data}")
    else:
        data="brak pliku"
    return data

def przekopiuj_stary_env(basic_path_skryptu_klraspi):
    drukuj("def: przekopiuj_stary_env")
    if os.path.exists(".env_skopiowany"):
        shutil.copyfile(".env_skopiowany", f"{basic_path_skryptu_klraspi}/.env")    

def tworzenie_virtualenv_dla_projektu(basic_path_skryptu_klraspi):
    drukuj("def: tworzenie_virtualenv_dla_projektu")
    bash_command=f"virtualenv {basic_path_skryptu_klraspi}/venv".split()
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    drukuj(f"stdout: {stdout}")
    drukuj(f"stderr: {stderr}")

def zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi):
    drukuj("def: zachomikuj_stary_env_i_usun_stary_projekt")
    if os.path.isdir(f"{basic_path_skryptu_klraspi}") == True:
        if os.path.exists(f"{basic_path_skryptu_klraspi}/.env"):
            shutil.copyfile(f"{basic_path_skryptu_klraspi}/.env", ".env_skopiowany")
        if os.path.isdir(basic_path_skryptu_klraspi):
            shutil.rmtree(f"{basic_path_skryptu_klraspi}") 
    path_to_tymczasowy_miejsce_pobranego_programu=f"{basic_path_ram}/skrypty_klraspi_tymczasowy/skrypty_klraspi-master"
    if os.path.isdir(path_to_tymczasowy_miejsce_pobranego_programu):
        shutil.move(path_to_tymczasowy_miejsce_pobranego_programu, f"{basic_path_skryptu_klraspi}")
        shutil.rmtree(f"{basic_path_ram}/skrypty_klraspi_tymczasowy")
        os.remove(f"{basic_path_ram}/skrypty_klraspi.zip")
        tworzenie_virtualenv_dla_projektu(basic_path_skryptu_klraspi)
        przekopiuj_stary_env(basic_path_skryptu_klraspi)
        drukuj("usunalem stary kod i zachomikowalem .env")
    else:
        drukuj("nie udalo sie przeniesc pliku - chyba kwestia - bo może nie ma")

def sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(basic_path_ram):
    skrypty_klraspi_path=f"{basic_path_ram}/uruchom_skrypt_o_godzinie.py.flara"
    if os.path.exists(skrypty_klraspi_path) == True:
        pass
        file=open(skrypty_klraspi_path, "r")
        numer_pid=file.read()
        if os.name == "posix":
            if int(numer_pid)>-1:
                os.kill(int(numer_pid), signal.SIGTERM)
                os.remove(skrypty_klraspi_path)
        else:
            raise ExceptionWindows

##################

def main():
    basic_path_ram=""
    basic_path_skryptu_klraspi=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        dotenv_path = "./.env_projektu"
        file_istnienie(dotenv_path, "dotenv_path - sprawdz .env_projektu")
        load_dotenv(dotenv_path)
        # pobierz_z_outsystemu_date_wersji()
        if os.name == "posix":
            drukuj("posix")
            basic_path_ram=zmienna_env_folder("basic_path_ram", ".env_projektu - problem z basic_path_ram")
            basic_path_skryptu_klraspi=os.getenv("basic_path_skryptu_klraspi")
            head, tail = os.path.split(basic_path_skryptu_klraspi)
            if os.path.isdir(head) == False:
                drukuj(f"basic_path_skryptu_klraspi - head: {head}")
                raise ExceptionEnvProjektu
            #pobierz_aktualna_wersje()
            obecny_projekt=zwroc_stan_projektu(basic_path_skryptu_klraspi)
            obecny_na_outsystem=pobierz_z_outsystemu_date_wersji()
            if obecny_projekt==obecny_na_outsystem:
                drukuj("mamy zbieznosc ;) - nic nie robie")
            elif obecny_projekt=="brak pliku":
                drukuj("brak pliku - pierwszy raz pobieram z repa")
                drukuj("rozpoczynam pobieranie z repa")
                text=pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                if text != "":
                    zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                drukuj("koniec elif")
            else:
                sprawdz_czy_skrypty_klraspi_dziala_i_ubij_jesli_dziala(basic_path_ram)
                drukuj("rozpoczynam pobieranie z repa")
                #zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                text=pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                if text != "":
                    zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                    przekopiuj_stary_env(basic_path_skryptu_klraspi)
                    drukuj("przekopiowalem stary env")
                drukuj("koniec elsa")  
            drukuj("proces zakonczony") 
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"czy napewno skopiowales .env_projektu.example na .env_projektu, i zmieniles tam scieszki zalezne? Tak tylko pytam...")
        traceback.print_exc()
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest menadzer zadan/crontab")
        traceback.print_exc()

if __name__ == "__main__":
    main()
