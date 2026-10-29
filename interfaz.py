import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

from estilos import EXTENSIONES_IMAGENES, convertir_imagenes_a_pdf


class Interfaz(TkinterDnD.Tk):
    """Interfaz gráfica (Tkinter + tkinterdnd2) para convertir imágenes a PDF."""

    def __init__(self):
        super().__init__()
        self.title("img-a-pfd - Convertidor de imágenes a PDF")
        self.geometry("680x560")
        self.resizable(True, True)

        self.origen = None
        self.opcion_guardado = tk.StringVar(value="origen")
        self.destino = None
        self.subcarpetas = []

        self._crear_widgets()

    def _crear_widgets(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Arrastrá una carpeta con imágenes y soltéala aquí o usá el botón de selección:",
        ).pack(anchor="w")

        self.area_drop = ttk.Frame(frame, relief="solid", borderwidth=1)
        self.area_drop.pack(fill="both", expand=True, pady=4)
        self.area_drop.columnconfigure(0, weight=1)
        self.area_drop.rowconfigure(0, weight=1)
        self.lbl_drop = ttk.Label(self.area_drop, text="Solta la carpeta aquí")
        self.lbl_drop.grid(row=0, column=0, sticky="nsew")
        self.area_drop.drop_target_register(DND_FILES)
        self.area_drop.dnd_bind("<<Drop>>", self._on_drop)

        ttk.Button(frame, text="Seleccionar carpeta...", command=self._elegir_carpeta).pack(pady=4, anchor="w")

        self.lbl_estado = ttk.Label(frame, text="Ninguna carpeta seleccionada todavía.")
        self.lbl_estado.pack(anchor="w")

        frame_guardar = ttk.LabelFrame(frame, text="Opciones de guardado")
        frame_guardar.pack(fill="x", pady=6)

        ttk.Radiobutton(
            frame_guardar,
            text="Guardar el PDF en la misma carpeta que la subcarpeta origen",
            variable=self.opcion_guardado,
            value="origen",
        ).pack(anchor="w", pady=2)

        ttk.Radiobutton(
            frame_guardar,
            text="Elegir carpeta de destino manualmente",
            variable=self.opcion_guardado,
            value="destino",
        ).pack(anchor="w", pady=2)
        self.boton_destino = ttk.Button(
            frame_guardar,
            text="Elegir carpeta de destino...",
            command=self._elegir_destino,
            state="disabled",
        )
        self.boton_destino.pack(anchor="w", pady=2)

        frame_sub = ttk.LabelFrame(frame, text="Subcarpetas encontradas")
        frame_sub.pack(fill="both", expand=True, pady=6)

        self.lista_subcarpetas = tk.Listbox(frame_sub, height=6)
        self.lista_subcarpetas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_sub, orient="vertical", command=self.lista_subcarpetas.yview)
        self.lista_subcarpetas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.boton_convertir = ttk.Button(frame_sub, text="Convertir", command=self._convertir)
        self.boton_convertir.pack(pady=6, anchor="w")

    def _on_drop(self, event):
        rutas = self.tk.splitlist(event.data)
        carpeta = str(rutas[0]) if rutas else ""
        if os.path.isdir(carpeta):
            self._cargar_carpeta(carpeta)
        else:
            messagebox.showwarning("Carpeta inválida", "La ruta que soltaste no es una carpeta válida.")

    def _elegir_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
        if carpeta:
            self._cargar_carpeta(carpeta)

    def _elegir_destino(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino para los PDF")
        if carpeta:
            self.destino = carpeta
            self.boton_destino.config(state="normal")

    def _cargar_carpeta(self, carpeta):
        self.origen = carpeta
        subcarpetas = []
        for entrada in sorted(os.listdir(carpeta)):
            ruta_sub = os.path.join(carpeta, entrada)
            if not os.path.isdir(ruta_sub):
                continue
            imagenes = [
                f
                for f in os.listdir(ruta_sub)
                if os.path.isfile(os.path.join(ruta_sub, f)) and os.path.splitext(f)[1].lower() in EXTENSIONES_IMAGENES
            ]
            if imagenes:
                subcarpetas.append((entrada, ruta_sub))
        self.subcarpetas = subcarpetas
        self.lista_subcarpetas.delete(0, tk.END)
        for nombre, _ruta in subcarpetas:
            self.lista_subcarpetas.insert(tk.END, nombre)
        self.lbl_estado.config(text=f"Carpeta seleccionada: {carpeta} - {len(subcarpetas)} subcarpeta(s) con imágenes compatibles.")

    def _convertir(self):
        if not self.subcarpetas:
            messagebox.showwarning(
                "Sin subcarpetas",
                "No se encontraron subcarpetas con imágenes compatibles (.jpg, .jpeg, .png, .webp).",
            )
            return
        if self.opcion_guardado.get() == "destino" and not self.destino:
            messagebox.showwarning("Falta elegir destino", "Elegí una carpeta de destino antes de convertir.")
            return

        destino = self.origen if self.opcion_guardado.get() == "origen" else self.destino
        self.boton_convertir.config(state="disabled")
        self.lbl_estado.config(text="Convirtiendo...")

        exitos = []
        errores = []
        for nombre, ruta_sub in list(self.subcarpetas):
            try:
                pdf = convertir_imagenes_a_pdf(ruta_sub, ruta_salida=os.path.join(destino, f"{nombre}.pdf"))
                exitos.append((nombre, pdf))
            except Exception as e:  # noqa: BLE001
                errores.append((nombre, str(e)))

        self.boton_convertir.config(state="normal")

        if errores:
            messagebox.showerror("Error durante la conversión", "\n".join(f"{n}: {e}" for n, e in errores))
        if exitos:
            messagebox.showinfo(
                "Conversión completada",
                f"Se crearon {len(exitos)} PDF(s):\n" + "\n".join(pdf for _n, pdf in exitos),
            )


if __name__ == "__main__":
    Interfaz().mainloop()
