import os
import sys
import shutil
import subprocess
from datetime import datetime
import traceback
import urllib.request
import zipfile

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

def pobierz_z_outsystemu_hash():
    return "2236feb"

def sprawdz_hash():
    #if open()
    return True

def pobierz_aktualna_wersje():
    urllib.request.urlretrieve("https://github.com/Hamilkar247/skrypty_klraspi/archive/refs/heads/master.zip", "skrypty_klraspi.zip")
    with zipfile.ZipFile("skrypty_klraspi.zip", "r") as zip_ref:
        zip_ref.extractall("skrypty_klraspi_tymczasowy")
    
    path_commit_txt="skrypty_klraspi_tymczasowy/skrypty_klraspi-master/commit.txt"
    if os.path.exists(path_commit_txt):
        print("jestem")
        file_commit=open(path_commit_txt, "r")
        commit=file_commit.read().split(" ")[0]
        return commit
    return ""

if __name__ == "__main__":
    pobierz_aktualna_wersje()
    print(f"pobierz_z_outsystem_hash: {pobierz_z_outsystemu_hash()}")
    print(f"pobierz_aktualna_wersje: {pobierz_aktualna_wersje()}")
    if pobierz_z_outsystemu_hash() == pobierz_aktualna_wersje():
        print("sa zbiezne")

##    
##    if sprawdz_hash() == True:
##        #os.chdir()
##        if os.path.isdir("../skrypty_klraspi") == True:
##            if os.path.exists("../skrypty_klraspi/.env"):
##                shutil.copyfile("../skrypty_klraspi/.env", ".env_skopiowany")
##            shutil.rmtree('../skrypty_klraspi')
##        os.chdir("..")
##        if os.path.isdir("../skrypty_klraspi") == False:
##            drukuj(f"{os.getcwd()}")
##            bash_command="git clone https://github.com/Hamilkar247/skrypty_klraspi".split()
##            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##            stdout, stderr = process.communicate()
##            drukuj(f"stdout: {stdout}") 
##            drukuj(f"stderr: {stderr}")
##            os.chdir("skrypty_klraspi")
##            file_data = open(f"data.txt", "w")
##            file_data.write(f"{data_i_godzina()}")
##            if os.path.exists("../update_projektu_skryptu_klraspi/.env_skopiowany") == True:
##                shutil.copyfile("../update_projektu_skryptu_klraspi/.env_skopiowany", ".env")
##            bash_command="virtualenv venv".split()
##            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##            stdout, stderr = process.communicate()
##            drukuj(f"stdout: {stdout}") 
##            drukuj(f"stderr: {stderr}")
##
            #bash_command="git log -n 1 --oneline $(git branch -r)".split()
            #process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #stdout, stderr = process.communicate()
            #drukuj(f"stdout: {stdout}")
            #drukuj(f"stderr: {stderr}")
            #if stdout != "":
            #    file_commit=open("commit.txt", "w")
            #    file_commit.write(f"{stdout}")
            #else:
            #    drukuj("brak strumienia wyjściowego")

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


