import tkinter as tk
from PIL import Image, ImageTk

# --- REGLA CRUCIAL ---
# Si la referencia al objeto ImageTk.PhotoImage no se mantiene,
# Python lo eliminará (garbage collection) y la imagen NO se mostrará
# en la interfaz. La mejor forma es guardarla como un atributo de un widget
# o de la ventana principal (root).
# --------------------

root = tk.Tk()

# 1. Cargar y Manipular con Image (Pillow)
img_pil = Image.open("C:/Users/Jesus/WorkSpace/Proyectos/Proyectos-con-python/proyecto-ajedrez-con-tkinter/contenido_grafico/menu_partide_icons/person.png") 
img_redimensionada = img_pil.resize((60, 60)) # La imagen ya está lista para mostrar

# 2. Convertir con ImageTk (Puente a Tkinter)
img_tk = ImageTk.PhotoImage(img_redimensionada) 

# 3. Mostrar en un Widget y Guardar la Referencia
label_imagen = tk.Label(root, image=img_tk)
label_imagen.image = img_tk # <<-- ¡Guardar la referencia aquí!
label_imagen.pack()

root.mainloop()