import os
import sys
import shutil
import subprocess
from datetime import datetime
import traceback
import urllib.request
import zipfile
from dotenv import load_dotenv
import json

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
        shutil.move(path_to_tymczasowy_miejsce_pobranego_programu, f"{basic_path_skryptu_klraspi}/skrypty_klraspi")
        shutil.rmtree(f"{basic_path_ram}/skrypty_klraspi_tymczasowy")
        os.remove(f"{basic_path_ram}/skrypty_klraspi.zip")
        tworzenie_virtualenv_dla_projektu(basic_path_skryptu_klraspi)
        przekopiuj_stary_env()
        drukuj("usunalem stary kod i zachomikowalem .env")
    else:
        drukuj("nie udalo sie przeniesc pliku - chyba kwestia - bo może nie ma")

class ExceptionEnvProjektu(Exception):
    pass

if __name__ == "__main__":
    basic_path_ram=""
    basic_path_skryptu_klraspi=""
    flara_skryptu=""
    try:
        if os.path.exists("./.env_projektu"):
            dotenv_path = "./.env_projektu"
            load_dotenv(dotenv_path)
            # pobierz_z_outsystemu_date_wersji()
            if os.name == "posix":
                drukuj("posix")
                basic_path_ram=os.getenv("basic_path_ram")
                if os.path.isdir(basic_path_ram) == False:
                    raise ExceptionEnvProjektu
                basic_path_skryptu_klraspi=os.getenv("basic_path_skryptu_klraspi")
                #ciekawostka podwojny isdir - powinnnniec dzialac to jak 
                head, tail = os.path.split(basic_path_skryptu_klraspi)
                if os.path.isdir(head) == False:
                    drukuj(f"head: {head}")
                    raise ExceptionEnvProjektu
                #pobierz_aktualna_wersje()
                obecny_projekt=zwroc_stan_projektu(basic_path_skryptu_klraspi)
                obecny_na_outsystem=pobierz_z_outsystemu_date_wersji()
                if obecny_projekt==obecny_na_outsystem:
                    drukuj("mamy zbieznosc ;) - nic nie robie")
                elif obecny_projekt=="brak pliku":
                    drukuj("brak pliku")
                    text=pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                    if text != "":
                        zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                    drukuj("sprawdz .env w nowo pobranym projekcie - nie bylo go pierwotnie")
                    drukuj("koniec elif")
                else:
                    drukuj("rozpoczynam pobieranie z repa")
                    #zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                    text=pobierz_aktualna_wersje(spodziewana_data_wersji=obecny_na_outsystem, basic_path_projektu=basic_path_skryptu_klraspi, basic_path_ram=basic_path_ram)
                    if text != "":
                        zachomikuj_stary_env_i_usun_stary_projekt(basic_path_ram, basic_path_skryptu_klraspi)
                        przekopiuj_stary_env(basic_path_ram, basic_path_skryptu_klraspi)
                        drukuj("przekopiowalem stary env")
                    drukuj("koniec elsa")
                #drukuj(f"pobierz_z_outsystem_hash: {pobierz_z_outsystemu_hash()}")
                #drukuj(f"pobierz_aktualna_wersje: {pobierz_aktualna_wersje()}")
                #if pobierz_z_outsystemu_hash() == pobierz_aktualna_wersje():
                #    drukuj("id pobranego kodu i wersji z outsystem sa zbiezne")
                #else:
                #    pass    
                drukuj("proces zakonczony")
        else:
            drukuj("No byniu - a .env_projektu to nie laska zrobic?!")
    
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"czy napewno skopiowales .env_projektu.example na .env_projektu, i zmieniles tam scieszki zalezne? Tak tylko pytam...")
        traceback.print_exc()
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest menadzer zadan/crontab")
        traceback.print_exc()
    

#    if sprawdz_hash() == True:
#        #os.chdir()
#        if os.path.isdir("../skrypty_klraspi") == True:
#            if os.path.exists("../skrypty_klraspi/.env"):
#                shutil.copyfile("../skrypty_klraspi/.env", ".env_skopiowany")
#            shutil.rmtree('../skrypty_klraspi')
#        os.chdir("..")
#        if os.path.isdir("../skrypty_klraspi") == False:
#            drukuj(f"{os.getcwd()}")
#            bash_command="git clone https://github.com/Hamilkar247/skrypty_klraspi".split()
#            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#            stdout, stderr = process.communicate()
#            drukuj(f"stdout: {stdout}") 
#            drukuj(f"stderr: {stderr}")
#            os.chdir("skrypty_klraspi")
#            file_data = open(f"data.txt", "w")
#            file_data.write(f"{data_i_godzina()}")
#            if os.path.exists("../update_projektu_skryptu_klraspi/.env_skopiowany") == True:
#                shutil.copyfile("../update_projektu_skryptu_klraspi/.env_skopiowany", ".env")
#            bash_command="virtualenv venv".split()
#            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#            stdout, stderr = process.communicate()
#            drukuj(f"stdout: {stdout}") 
#            drukuj(f"stderr: {stderr}")
#
#            #bash_command="git log -n 1 --oneline $(git branch -r)".split()
#            #process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#            #stdout, stderr = process.communicate()
#            #drukuj(f"stdout: {stdout}")
#            #drukuj(f"stderr: {stderr}")
#            #if stdout != "":
#            #    file_commit=open("commit.txt", "w")
#            #    file_commit.write(f"{stdout}")
#            #else:
#            #    drukuj("brak strumienia wyjściowego")

#https://stackoverflow.com/a/54636170/13231758
##     activate_this_file = "/path/to/virtualenv/bin/activate_this.py"
##
##exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))

            # if os.path.isdir("venv") == True:
            #     bash_command="source venv/bin/activate".split()
            #     process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #     stdout, stderr = process.communicate()
            #     drukuj(f"stdout: {stdout}") 
            #     drukuj(f"stderr: {stderr}")

            #     if os.path.exists("requirements.txt") == True:
            #         bash_command="pip3 install -r requirements.txt".split()
            #         process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #         stdout, stderr = process.communicate()
            #         drukuj(f"stdout: {stdout}") 
            #         drukuj(f"stderr: {stderr}")
   # else:
   #     drukuj("hash się nie zmienił")


