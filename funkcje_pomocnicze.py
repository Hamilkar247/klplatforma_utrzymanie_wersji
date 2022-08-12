# - *- coding: utf-8 - *-

from inspect import trace
import sys
import os
from datetime import datetime, timedelta
import traceback
from dotenv import load_dotenv

class ExceptionEnvProjektu(Exception):
    pass

class ExceptionNotExistFolder(Exception):
    pass

class ExceptionWindows(Exception):
    pass

#############

class FunkcjePomocnicze():

    def __init__(self, nazwa_programu):
        self.nazwa_programu=nazwa_programu

    def data_i_godzina(self):
        now = datetime.now()
        current_time = now.strftime("%d/%m/%y %H:%M:%S")
        return current_time
    
    def drukuj(self, obiekt_do_wydruku):
        try:
            print(self.data_i_godzina()+" "+self.nazwa_programu+" "+str(obiekt_do_wydruku))
        except Exception as e:
            print(e)
            print(traceback.print_exc())
    
    def przerwij_i_wyswietl_czas(self):
        czas_teraz = datetime.now()
        current_time = czas_teraz.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        sys.exit()
    
    #########################
    

    
    def file_istnienie(self, path_to_file, komunikat):
        if os.path.exists(path_to_file) == False:
            self.drukuj(f"{komunikat}")
            raise self.exceptionEnvProjektu
        return True
    
    def folder_istnienie(self, path_to_folder, komunikat):
        if os.path.isdir(path_to_folder) == False:
            self.drukuj(f"{komunikat}")
            raise self.exceptionEnvProjektu
        return True
    
    def folder_istnienie_2(self, path_to_folder, komunikat):
        if os.path.isdir(path_to_folder) == False:
            self.drukuj(f"{komunikat}")
            raise self.exceptionNotExistFolder
        return path_to_folder
    
    def zmienna_env_file(self, tag_in_env, komunikat):
        path_to_file=os.getenv(tag_in_env)
        if os.path.exists(path_to_file) == False:
            self.drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_file}")#sprawdz czy plik .env istnieje")
            raise self.exceptionEnvProjektu
        return path_to_file
    
    def zmienna_env_folder(self, tag_in_env, komunikat):
        path_to_folder=os.getenv(tag_in_env)
        if os.path.isdir(path_to_folder) == False:
            self.drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_folder}")#sprawdz czy plik .env istnieje")
            raise self.exceptionEnvProjektu
        return path_to_folder
    
    def usun_flare(self, folder_do_sprawdzenia, flara_do_sprawdzenia):
        if os.path.isdir(folder_do_sprawdzenia):
            if os.path.exists(flara_do_sprawdzenia):
                os.remove(flara_do_sprawdzenia)
                self.drukuj("usuwam flare")
    
    def stworz_flare_z_pid(self, flara_path):
        flara_file=open(flara_path, "w")
        flara_file.write(f"{str(os.getpid())}")
        flara_file.close()
    