#!/usr/bin/env python3

import sys
import json
import os

# Operación (patch o restore) desde la línea de comandos
operation = sys.argv[1]

# Directorio del script actual
script_dir = os.path.dirname(os.path.realpath(__file__))

# Rutas de los archivos
product_path = r"C:\Program Files\Positron\resources\app\product.json"
patch_path = os.path.join(script_dir, "patch.json")
cache_path = os.path.join(script_dir, "cache.json")

class term_colors:
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    SUCCESS = "\033[92m"

# Verifica si el archivo product.json existe
if not os.path.exists(product_path):
    print(term_colors.WARNING + "WARN: " + term_colors.ENDC + product_path + " no existe. Skipping...")
    exit(0)

# Crear archivo cache.json si no existe
if not os.path.exists(cache_path):
    with open(cache_path, "w") as file:
        file.write("{}")

# Función para aplicar el parche
def patch():
    print("Aplicando parche para Positron en " + product_path)
    with open(product_path, "r") as product_file:
        product_data = json.load(product_file)
    with open(patch_path, "r") as patch_file:
        patch_data = json.load(patch_file)
    cache_data = {}
    for key in patch_data.keys():
        if key in product_data:
            cache_data[key] = product_data[key]
        product_data[key] = patch_data[key]
    with open(product_path, "w") as product_file:
        json.dump(product_data, product_file, indent="\t")
    with open(cache_path, "w") as cache_file:
        json.dump(cache_data, cache_file, indent="\t")
    print(term_colors.SUCCESS + "Parche aplicado con éxito!" + term_colors.ENDC)

# Función para restaurar el archivo original
def restore():
    print("Restaurando archivo original en " + product_path)
    with open(product_path, "r") as product_file:
        product_data = json.load(product_file)
    with open(patch_path, "r") as patch_file:
        patch_data = json.load(patch_file)
    with open(cache_path, "r") as cache_file:
        cache_data = json.load(cache_file)
    for key in patch_data.keys():
        if key in product_data:
            del product_data[key]
    for key in cache_data.keys():
        product_data[key] = cache_data[key]
    with open(product_path, "w") as product_file:
        json.dump(product_data, product_file, indent="\t")
    print(term_colors.SUCCESS + "Archivo restaurado con éxito!" + term_colors.ENDC)

# Ejecutar la operación seleccionada
if operation == "patch":
    patch()
elif operation == "restore":
    restore()
