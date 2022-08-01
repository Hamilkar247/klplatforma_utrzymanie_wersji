import os
import sys
import shutil
import subprocess
from datetime import datetime
import traceback

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

def sprawdz_hash():
    return True

if __name__ == "__main__":
    if sprawdz_hash() == True:
        #os.chdir()
        if os.path.isdir("../skrypty_klraspi") == True:
            if os.path.exists("../skrypty_klraspi/.env"):
                shutil.copyfile("../skrypty_klraspi/.env", ".env_skopiowany")
            shutil.rmtree('../skrypty_klraspi')
        os.chdir("..")
        if os.path.isdir("../skrypty_klraspi") == False:
            drukuj(f"{os.getcwd()}")
            bash_command="git clone https://github.com/Hamilkar247/skrypty_klraspi".split()
            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            drukuj(f"stdout: {stdout}") 
            drukuj(f"stderr: {stderr}")
            os.chdir("skrypty_klraspi")
            file_data = open(f"data.txt", "w")
            file_data.write(f"{data_i_godzina()}")
            if os.path.exists("../update_projektu_skryptu_klraspi/.env_skopiowany") == True:
                shutil.copyfile("../update_projektu_skryptu_klraspi/.env_skopiowany", ".env")
            bash_command="virtualenv venv".split()
            process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            drukuj(f"stdout: {stdout}") 
            drukuj(f"stderr: {stderr}")

#https://stackoverflow.com/a/54636170/13231758
##     activate_this_file = "/path/to/virtualenv/bin/activate_this.py"
##
##exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'), dict(__file__=activate_this_file))

            if os.path.isdir("venv") == True:
                bash_command="source venv/bin/activate".split()
                process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                drukuj(f"stdout: {stdout}") 
                drukuj(f"stderr: {stderr}")

                if os.path.exists("requirements.txt") == True:
                    bash_command="pip3 install -r requirements.txt".split()
                    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    drukuj(f"stdout: {stdout}") 
                    drukuj(f"stderr: {stderr}")
    else:
        drukuj("hash się nie zmienił")


