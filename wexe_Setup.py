# -*- coding: utf-8 -*-
### Fichier d'installation de script ###

##################################
# Importation de fonctions externes :
import sys, os
from cx_Freeze import setup, Executable

##################################
# Ne pas ouvrir de console
if sys.platform == "win32":
	base = "Win32GUI"

##################################
# Préparation des cibles
executables = [Executable("ginkoTime.py", base = base)]

##################################
# Construction du dictionnaire des options
BuildOptions = dict(
					compressed = False,
					includes = ["wx", "BeautifulSoup"],
					include_files = ["ginko.ini","icon.png"],
					path = sys.path
					)

##################################
# Création du Setup
setup (
		name = "ginkoTime",
		version = "0.1",
		description = "Horaire des bus en temps réel",
		options = dict(build_exe = BuildOptions),
		executables = executables
		)
