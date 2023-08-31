
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="farmacia"
)
cursor = db.cursor()

class Usuario:
    def __init__(self, id, nombre, contraseña, es_admin):
        self.id = id
        self.nombre = nombre
        self.contraseña = contraseña
        self.es_admin = es_admin

class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

def mostrar_usuarios():
    consulta = "SELECT * FROM usuarios"
    cursor.execute(consulta)
    for fila in cursor:
        id, nombre, contraseña, es_admin = fila
        tipo = "Administrador" if es_admin else "Usuario"
        print(f"ID:> {id} / Nombre:> {nombre} / Tipo:> {tipo}")

def registrar_usuario(nombre, contraseña, es_admin):
    consulta = "INSERT INTO usuarios (nombre, contraseña, es_admin) VALUES (%s, %s, %s)"
    valor = (nombre, contraseña, es_admin)
    cursor.execute(consulta, valor)
    db.commit()

def modificar_usuario(id, nombre, contraseña, es_admin):
    consulta = "UPDATE usuarios SET nombre = %s, contraseña = %s, es_admin = %s WHERE id = %s"
    valor = (nombre, contraseña, es_admin, id)
    cursor.execute(consulta, valor)
    db.commit()

def eliminar_usuario(id):
    consulta = "DELETE FROM usuarios WHERE id = %s"
    valor = (id,)
    cursor.execute(consulta, valor)
    db.commit()

def mostrar_productos():
    consulta = "SELECT * FROM productos"
    cursor.execute(consulta)
    for producto in cursor:
        id, nombre, precio, stock = producto
        print(f"ID: {id} / Nombre:> {nombre} / Precio:> {precio} / Stock:> {stock}")

def ingresar_producto(nombre, precio, stock):
    consulta = "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
    valor = (nombre, precio, stock)
    cursor.execute(consulta, valor)
    db.commit()

def modificar_producto(id, nombre, precio, stock):
    consulta = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s"
    valor = (nombre, precio, stock, id)
    cursor.execute(consulta, valor)
    db.commit()

def eliminar_producto(id):
    consulta = "DELETE FROM productos WHERE id = %s"
    valor = (id,)
    cursor.execute(consulta, valor)
    db.commit()

def agregar_sacar_stock(id, cantidad):
    consulta = "SELECT stock FROM productos WHERE id = %s"
    valor = [id]
    cursor.execute(consulta, valor)
    
    stock_actual = None
    for fila in cursor:
        stock_actual = fila[0]
        break
    
    if stock_actual != None:
        nuevo_stock = stock_actual + cantidad
        consulta_actualizar = "UPDATE productos SET stock = %s WHERE id = %s"
        valor_actualizar = (nuevo_stock, id)
        
        retorno = 1  
        try:
            cursor.execute(consulta_actualizar, valor_actualizar)
            db.commit()
        except mysql.connector.Error as error:
            print("Error al actualizar el stock:", error)
            db.rollback()
        else:
            retorno = 0 
            
        finally:
            db.close()
        return retorno
    else:
        print("Producto no encontrado.")
        return 1  

def ver_stock_compra():
    consulta = "SELECT id, nombre, stock FROM productos"
    cursor.execute(consulta)
    for producto in cursor:
        id, nombre, stock = producto
        if stock == 0:
            print(f"Producto:> {nombre} / Stock:> {stock}/ ¡Necesitas comprar más!")
        else:
            print(f"Producto:> {nombre} / Stock:> {stock} / Stock suficiente")

def ver_producto_especifico(id):
    consulta = "SELECT * FROM productos WHERE id = %s"
    valor = [id]
    cursor.execute(consulta, valor)
    
    for producto in cursor:
        id, nombre, precio, stock = producto
        print(f"ID:> {id} / Nombre:> {nombre} / Precio:> {precio} / Stock:> {stock}")
        break 
        
    else:
        print("Producto no encontrado.")


while True:
    nombre = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    usuario_actual = None
    
    consulta = "SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s"
    valor = (nombre, contraseña)
    cursor.execute(consulta, valor)
    
    for usuario in cursor:
        id, nombre, contraseña, es_admin = usuario
        usuario_actual = Usuario(id, nombre, contraseña, es_admin)
        print("Inicio de sesión exitoso.")
        break  
    else:
        print("Credenciales incorrectas. Intente nuevamente.")
        continue  
    break  
   

while True:
    print("---> Menú Principal <---")
    print("1. Registrar un usuario")
    print("2. Modificar un usuario")
    print("3. Eliminar un usuario")
    print("4. Mostrar todos los usuarios")
    print("5. Ingresar producto")
    print("6. Modificar producto")
    print("7. Agregar o sacar stock de un producto")
    print("8. Ver stock de los productos")
    print("9. Ver todos los productos")
    print("10. Ver un producto en especial")
    print("11. Cambiar precio de un producto")
    print("12. Eliminar un producto")
    print("13. Salir")

    opc = int(input("Seleccione una opción: "))

    if opc == 1:
        if usuario_actual.es_admin:
            nombre = input("Ingrese el nombre del nuevo usuario: ")
            contraseña = input("Ingrese la contraseña del nuevo usuario: ")
            es_admin = input("¿Es un usuario administrador? (sí/no): ").lower() == "sí"
            registrar_usuario(nombre, contraseña, es_admin)
            print("Usuario registrado exitosamente.")
        else:
            print("No tienes permiso para registrar usuarios.")
    elif opc == 2:
        if usuario_actual.es_admin:
            id_usuario = int(input("Ingrese el ID del usuario a modificar: "))
            nuevo_nombre = input("Ingrese el nuevo nombre del usuario: ")
            nueva_contraseña = input("Ingrese la nueva contraseña del usuario: ")
            nuevo_es_admin = input("¿Es un usuario administrador? (sí/no): ").lower() == "sí"
            modificar_usuario(id_usuario, nuevo_nombre, nueva_contraseña, nuevo_es_admin)
            print("Usuario modificado exitosamente.")
        else:
            print("No tienes permiso para modificar usuarios.")
    elif opc == 3:
        if usuario_actual.es_admin:
            id_usuario = int(input("Ingrese el ID del usuario a eliminar: "))
            eliminar_usuario(id_usuario)
            print("Usuario eliminado exitosamente.")
        else:
            print("No tienes permiso para eliminar usuarios.")
    elif opc == 4:
        mostrar_usuarios()
    elif opc == 5:
        nombre_producto = input("Ingrese el nombre del nuevo producto: ")
        precio_producto = float(input("Ingrese el precio del nuevo producto: "))
        stock_producto = int(input("Ingrese el stock del nuevo producto: "))
        ingresar_producto(nombre_producto, precio_producto, stock_producto)
        print("Producto ingresado exitosamente.")
    elif opc == 6:
        id_producto = int(input("Ingrese el ID del producto a modificar: "))
        nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
        nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
        nuevo_stock = int(input("Ingrese el nuevo stock del producto: "))
        modificar_producto(id_producto, nuevo_nombre, nuevo_precio, nuevo_stock)
        print("Producto modificado exitosamente.")
    elif opc == 7:
        id_producto = int(input("Ingrese el ID del producto: "))
        cantidad = int(input("Ingrese la cantidad a agregar o para sacar con '-' xx cantidad ): "))
        agregar_sacar_stock(id_producto, cantidad)
        print("Stock actualizado exitosamente.")
    elif opc == 8:
        ver_stock_compra()
    elif opc == 9:
        mostrar_productos()
    elif opc == 10:
        id_producto = int(input("Ingrese el ID del producto: "))
        ver_producto_especifico(id_producto)
    elif opc == 11:
        id_producto = int(input("Ingrese el ID del producto a cambiar el precio: "))
        nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
        modificar_producto(id_producto, None, nuevo_precio, None)
        print("Precio del producto modificado exitosamente.")
    elif opc == 12:
        id_producto = int(input("Ingrese el ID del producto a eliminar: "))
        
        print("--> Submenú de Eliminación de Producto <---")
        print("1. Confirmar eliminación")
        print("2. Cancelar")
        
        sub_opc = int(input("Seleccione una opción: "))
        if sub_opc == 1:
            eliminar_producto(id_producto)
            print("Producto eliminado exitosamente.")
        elif sub_opc == 2:
            print("Eliminación cancelada.")
        else:
            print("Opción inválida.")
    elif opc == 13:
        print("Sistema apagado")
        break
    else:
        print("Opción inválida. Intente nuevamente.")


cursor.close()
db.close()









