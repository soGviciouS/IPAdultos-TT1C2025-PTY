import os
import products as products
from colorama import Fore, Back, Style

# products.init(True)
products.init()

### Variables globales
option = ""

### Inicio del programa
print(Back.BLACK + Fore.MAGENTA + Style.BRIGHT + "Bienvenido al sistema de gestión de productos \n")

while option != "0":
    # Menú principal
    print(Back.BLACK + Fore.MAGENTA + "#######################")
    print(Back.BLACK + Fore.CYAN +
          "Seleccione una opción:\n" \
          "1. Agregar un producto\n" \
          "2. Mostrar los productos\n" \
          "3. Buscar / Modificar un producto\n" \
          "4. Eliminar un producto\n" \
          "5. Reporte de productos\n" \
          "0. Salir\n"
          )
    print(Back.BLACK + Fore.MAGENTA + "#######################")
    option = input(Back.BLACK + Fore.CYAN + Style.BRIGHT + "Ingrese la opción: ")
    match option:
        case "1":
            continue_input = "s"
            while continue_input == "s":
                print(Fore.CYAN + Style.BRIGHT + "Agregar un producto")
                try:
                    valitated_data = products.validate_product()
                    products.add_product(valitated_data[0], valitated_data[1], valitated_data[2], valitated_data[3], valitated_data[4])
                    print("Se agregó el producto.")
                except ValueError as e:
                    print(e, "Intente de nuevo. \n")
                continue_input = input("¿Desea agregar otro producto? (s/n): ").lower()
                if continue_input != "s":
                    continue_input = "n"

            input("Presione Enter para continuar...")
            os.system('cls||clear')
        case "2":
            print(Fore.CYAN + Style.BRIGHT + "Mostrar productos")

            arr_products = products.show_products()
            for product in arr_products:
                print(Fore.GREEN + Style.BRIGHT)
                products.show_product(product['nombre'], product['descripcion'], product['cantidad'], product['precio'], product['categoria'], product['id'])
                print(Back.BLACK + Fore.MAGENTA + "#######################")
            if not arr_products:
                print("No hay productos para mostrar.")

            input("Presione Enter para continuar...")
            os.system('cls||clear')
        case "3":
            print(Fore.CYAN + Style.BRIGHT + "Buscar un producto")

            product_findKey = (input("Ingrese el ID, el nombre o la categoria del producto: "))
            if product_findKey != "":
                productID = product_findKey

            arr_product = products.show_product(product_findKey)
            if arr_product:
                print(Fore.GREEN + Style.BRIGHT)
                print(len(arr_product))
                if len(arr_product) > 0:
                    for product in arr_product:
                        products.show_product(product['nombre'], product['descripcion'], product['cantidad'], product['precio'], product['categoria'], product['id'])
                    continue_input = input("¿Desea modificar uno de los productos? (s/n): ").lower()
                    if continue_input == "s":
                        try:
                            valitated_data = (products.validate_product(True))
                            products.mod_product(valitated_data[0], valitated_data[1], valitated_data[2], valitated_data[3], valitated_data[4], valitated_data[5])
                        except ValueError as e:
                            print(Fore.RED, e, "Intente de nuevo. \n")
                else:
                    products.show_product(arr_product['nombre'], arr_product['descripcion'], arr_product['cantidad'], arr_product['precio'], arr_product['categoria'], arr_product['id'])
                    continue_input = input("¿Desea modificar el producto? (s/n): ").lower()
                    if continue_input == "s":
                        try:
                            valitated_data = (products.validate_product(True))
                            products.mod_product(valitated_data[0], valitated_data[1], valitated_data[2], valitated_data[3], valitated_data[4], valitated_data[5])
                        except ValueError as e:
                            print(Fore.RED, e, "Intente de nuevo. \n")
            else:
                print(Fore.RED, "No se encontraron productos. Intente de nuevo. \n")

            input("Presione Enter para continuar...")
            os.system('cls||clear')
        case "4":
            print(Fore.CYAN + Style.BRIGHT + "Eliminar un producto")

            productID = input("Ingrese el ID del producto: ")
            if productID != "":
                productID = int(productID)

            arr_product = products.remove_product(productID)
            input("Presione Enter para continuar...")
            os.system('cls||clear')
        case "5":
            print(Fore.CYAN + Style.BRIGHT + "Reporte de productos")

            product_minCant = (input("Ingrese la cantidad minima de los productos que desea consultar: "))
            if product_minCant != "":
                product_minCant = product_minCant

            arr_products = products.report_products(product_minCant)
            for product in arr_products:
                print(Fore.GREEN + Style.BRIGHT)
                products.show_product(product['nombre'], product['descripcion'], product['cantidad'], product['precio'], product['categoria'], product['id'])
                print(Back.BLACK + Fore.MAGENTA + "#######################")
            if not arr_products:
                print("No hay productos para mostrar.")

            input("Presione Enter para continuar...")
            os.system('cls||clear')
        case "0":
            print(Fore.GREEN + "Saliendo del sistema. ¡Hasta luego!")
            break
        case _:
            print(Fore.RED + Style.BRIGHT + "Opción no válida. Intente de nuevo.")
