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
                    productName = str(input("Ingrese el nombre del producto: "))
                    productDescription = str(input("Ingrese la descripción del producto: "))
                    productCant = str(input("Ingrese la cantidad del producto (número entero): "))
                    productPrice = input("Ingrese el precio del producto (número decimal positivo:): ")
                    productCategory = str(input("Ingrese la categoria del producto: "))

                    if productName != "":
                        productName = productName.strip()
                    if productDescription != "":
                        productDescription = productDescription.strip()
                    if productCant != "":
                        productCant = productCant
                    if productPrice != "":
                        productPrice = float(productPrice)
                    if productCategory != "":
                        productCategory = productCategory.strip()

                    if productName == "":
                        raise ValueError("El nombre no puede estar vacío.")
                    if productCategory == "":
                        raise ValueError("La categoría no puede estar vacía.")
                    if not productCant.isnumeric():
                        raise ValueError("La cantidad debe ser un número entero positivo.")
                    else:
                        cantidad = int(productCant)
                    if not isinstance(productPrice, float):
                        raise ValueError("El precio debe ser un float entero positivo.")
                    else:
                        precio = float(productPrice)

                    products.add_product(productName, productDescription, cantidad, precio, productCategory)
                except ValueError as e:
                    print(Fore.RED, e, "Intente de nuevo. \n")
                finally:
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
                print(f" \
                    Producto #{product['id']}: \n \
                    - Nombre: {product['nombre']}\n \
                    - Descripción: {product['descripcion']}\n \
                    - Cantidad: {product['cantidad']}\n \
                    - Precio: {product['precio']} \n \
                    - Categoría: {product['categoria']} \
                ")
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
                        print(f" \
                                Producto #{product['id']}: \n \
                                - Nombre: {product['nombre']}\n \
                                - Descripción: {product['descripcion']}\n \
                                - Cantidad: {product['cantidad']}\n \
                                - Precio: {product['precio']} \n \
                                - Categoría: {product['categoria']} \
                        ")
                    continue_input = input("¿Desea modificar uno de los productos? (s/n): ").lower()
                    if continue_input == "s":
                        try:
                            productID = input("Ingrese el ID del producto: ")
                            productName = str(input("Ingrese el nombre del producto: "))
                            productDescription = str(input("Ingrese la descripción del producto: "))
                            productCant = str(input("Ingrese la cantidad del producto (número entero): "))
                            productPrice = input("Ingrese el precio del producto (número decimal positivo:): ")
                            productCategory = str(input("Ingrese la categoria del producto: "))

                            if productID != "":
                                productID = int(productID)
                            if productName != "":
                                productName = productName.strip()
                            if productDescription != "":
                                productDescription = productDescription.strip()
                            if productCant != "":
                                productCant = productCant
                            if productPrice != "":
                                productPrice = float(productPrice)
                            if productCategory != "":
                                productCategory = productCategory.strip()

                            if productName == "":
                                raise ValueError("El nombre no puede estar vacío.")
                            if productCategory == "":
                                raise ValueError("La categoría no puede estar vacía.")
                            if not productCant.isnumeric():
                                raise ValueError("La cantidad debe ser un número entero positivo.")
                            else:
                                cantidad = int(productCant)
                            if not isinstance(productPrice, float):
                                raise ValueError("El precio debe ser un float entero positivo.")
                            else:
                                precio = float(productPrice)

                            products.mod_product(productID, productName, productDescription, cantidad,
                                                 precio, productCategory)
                        except ValueError as e:
                            print(Fore.RED, e, "Intente de nuevo. \n")
                else:
                    print(f" \
                       Producto #{arr_product['id']}: \n \
                       - Nombre: {arr_product['nombre']}\n \
                       - Descripción: {arr_product['descripcion']}\n \
                       - Cantidad: {arr_product['cantidad']}\n \
                       - Precio: {arr_product['precio']} \n \
                       - Categoría: {arr_product['categoria']} \
                   ")
                    continue_input = input("¿Desea modificar el producto? (s/n): ").lower()
                    if continue_input == "s":
                        try:
                            productName = str(input("Ingrese el nombre del producto: "))
                            productDescription = str(input("Ingrese la descripción del producto: "))
                            productCant = str(input("Ingrese la cantidad del producto (número entero): "))
                            productPrice = input("Ingrese el precio del producto (número decimal positivo:): ")
                            productCategory = str(input("Ingrese la categoria del producto: "))

                            if productName != "":
                                productName = productName.strip()
                            if productDescription != "":
                                productDescription = productDescription.strip()
                            if productCant != "":
                                productCant = productCant
                            if productPrice != "":
                                productPrice = float(productPrice)
                            if productCategory != "":
                                productCategory = productCategory.strip()

                            if productName == "":
                                raise ValueError("El nombre no puede estar vacío.")
                            if productCategory == "":
                                raise ValueError("La categoría no puede estar vacía.")
                            if not productCant.isnumeric():
                                raise ValueError("La cantidad debe ser un número entero positivo.")
                            else:
                                cantidad = int(productCant)
                            if not isinstance(productPrice, float):
                                raise ValueError("El precio debe ser un float entero positivo.")
                            else:
                                precio = float(productPrice)

                            products.mod_product(arr_product['id'], productName, productDescription, cantidad, precio, productCategory)
                        except ValueError as e:
                            print(Fore.RED, e, "Intente de nuevo. \n")
            else:
                print(Fore.RED, "No se encontraron productos. Intente de nuevo. \n")

            input("Presione Enter para continuar...")
        case "4":
            print(Fore.CYAN + Style.BRIGHT + "Eliminar un producto")

            productID = str(input("Ingrese el ID del producto: "))
            if productID != "":
                productID = int(productID)

            arr_product = products.remove_product(productID)
        case "5":
            print(Fore.CYAN + Style.BRIGHT + "Reporte de productos")

            product_minCant = (input("Ingrese la cantidad minima de los productos que desea consultar: "))
            if product_minCant != "":
                product_minCant = product_minCant

            arr_products = products.report_products(product_minCant)
            for product in arr_products:
                print(Fore.GREEN + Style.BRIGHT)
                print(f" \
                                    Producto #{product['id']}: \n \
                                    - Nombre: {product['nombre']}\n \
                                    - Descripción: {product['descripcion']}\n \
                                    - Cantidad: {product['cantidad']}\n \
                                    - Precio: {product['precio']} \n \
                                    - Categoría: {product['categoria']} \
                                ")
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
