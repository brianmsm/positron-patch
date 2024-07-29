#!/usr/bin/env python3

import sys
import json
import os
import shutil

# Operación (patch o restore) desde la línea de comandos
operation = sys.argv[1]

# Directorio del script actual
script_dir = os.path.dirname(os.path.realpath(__file__))

# Rutas de los archivos
product_path = r"C:\Program Files\Positron\resources\app\product.json"
patch_path = os.path.join(script_dir, "patch.json")
backup_path = os.path.join(script_dir, "product_backup.json")

class term_colors:
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    SUCCESS = "\033[92m"

# Verifica si el archivo product.json existe
if not os.path.exists(product_path):
    print(term_colors.WARNING + "WARN: " + term_colors.ENDC + product_path + " no existe. Skipping...")
    exit(0)

# Función para crear un respaldo del archivo original
def create_backup():
    if not os.path.exists(backup_path):
        shutil.copyfile(product_path, backup_path)
        print("Respaldo creado en " + backup_path)
    else:
        print("Respaldo ya existe en " + backup_path)

# Función para aplicar el parche
def patch():
    create_backup()
    print("Aplicando parche para Positron en " + product_path)
    with open(product_path, "r") as product_file:
        product_data = json.load(product_file)
    with open(patch_path, "r") as patch_file:
        patch_data = json.load(patch_file)
    for key in patch_data.keys():
        product_data[key] = patch_data[key]
    with open(product_path, "w") as product_file:
        json.dump(product_data, product_file, indent="\t")
    print(term_colors.SUCCESS + "Parche aplicado con éxito!" + term_colors.ENDC)

# Función para restaurar el archivo original
def restore():
    if os.path.exists(backup_path):
        shutil.copyfile(backup_path, product_path)
        print(term_colors.SUCCESS + "Archivo restaurado con éxito desde " + backup_path + term_colors.ENDC)
    else:
        print(term_colors.WARNING + "WARN: No se encontró un respaldo en " + backup_path + term_colors.ENDC)

# Ejecutar la operación seleccionada
if operation == "patch":
    patch()
elif operation == "restore":
    restore()
