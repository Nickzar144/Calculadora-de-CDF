import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CDFView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CDF")
        self.geometry("1400x1100")
        self.configure(bg="#f2f2f2")
        self._crear_widgets()

    def _crear_widgets(self):
        lbl_titulo = tk.Label(
            self,
            text="Cuadro de Distribución de Frecuencias",
            font=("Arial", 16, "bold"),
            bg="#f2f2f2"
        )
        lbl_titulo.pack(pady=10)

        frame_contenedor = tk.Frame(self, bg="#f2f2f2")
        frame_contenedor.pack(pady=10)

        # IZQUIERDA: entrada / texto / botones
        frame_izq = tk.Frame(frame_contenedor, bg="#f2f2f2")
        frame_izq.pack(side="left", padx=5, anchor="n")

        lbl_ingreso = tk.Label(frame_izq, text="Ingrese datos:", bg="#f2f2f2", font=("Arial", 10))
        lbl_ingreso.pack(pady=2)

        self.entry_dato = tk.Entry(frame_izq, width=25, font=("Arial", 10))
        self.entry_dato.pack(pady=2)
        self.entry_dato.bind("<Return>", self._copiar_datos)

        frame_text = tk.Frame(frame_izq, bg="#f2f2f2")
        frame_text.pack(pady=2)

        self.text_datos = tk.Text(frame_text, width=60, height=8, font=("Arial", 10))
        self.text_datos.pack(side="left", fill="y")
        scrollbar_text = tk.Scrollbar(frame_text, command=self.text_datos.yview)
        scrollbar_text.pack(side="left", fill="y")
        self.text_datos.config(yscrollcommand=scrollbar_text.set)

        frame_botones = tk.Frame(frame_izq, bg="#f2f2f2")
        frame_botones.pack(pady=2)

        self.btn_generar = tk.Button(frame_botones, text="Generar CDF",
                                     bg="#007bff", fg="white", font=("Arial", 10, "bold"), width=12)
        self.btn_generar.pack(side="left", padx=5)

        self.btn_limpiar = tk.Button(frame_botones, text="Limpiar Datos",
                                     bg="#dc3545", fg="white", font=("Arial", 10, "bold"), width=12,
                                     command=self.limpiar_datos)
        self.btn_limpiar.pack(side="left", padx=5)

        # DERECHA: tabla
        frame_der = tk.Frame(frame_contenedor, bg="#f2f2f2")
        frame_der.pack(side="left", padx=5, anchor="n")

        columnas = ("xi-1", "x'i", "xi", "ni", "Ni", "Ni*", "hi", "Hi", "Hi*")
        self.tabla = ttk.Treeview(frame_der, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col)
            ancho = 90 if col in ("xi-1", "x'i", "xi") else 70
            self.tabla.column(col, anchor="center", width=ancho)
        self.tabla.pack(padx=5, pady=5)

        self.lbl_resumen = tk.Label(frame_der, text="", bg="#f2f2f2", font=("Arial", 10))
        self.lbl_resumen.pack(pady=5)

        # Frame para gráficas
        self.frame_graficas = tk.Frame(self, bg="#f2f2f2")
        self.frame_graficas.pack(pady=20, fill="both", expand=True)

    def _copiar_datos(self, event=None):
        texto = self.entry_dato.get()
        if texto.strip():
            if self.text_datos.get("1.0", "end").strip():
                self.text_datos.insert("end", ", " + texto)
            else:
                self.text_datos.insert("end", texto)
            self.entry_dato.delete(0, "end")

    def mostrar_cdf(self, tabla, resumen):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in tabla:
            self.tabla.insert("", "end", values=(
                fila["Límite Inferior"],
                fila["Límite Superior"],
                fila["Marca de Clase"],
                fila["Frecuencia"],
                fila["Ni"],
                fila.get("Ni*", 0),
                fila["Frecuencia Relativa"],
                fila["Hi"],
                fila["Hi*"]
            ))
        texto = (
            f"n = {resumen['n']} | Xmin = {resumen['Xmin']} | Xmax = {resumen['Xmax']} | "
            f"R = {resumen['R']} | k = {resumen['k']} | A = {resumen['A']}"
        )
        self.lbl_resumen.config(text=texto)

    def mostrar_graficas(self, clases, hi, Hi, Hi_mayor):
        for w in self.frame_graficas.winfo_children():
            w.destroy()

        fig = Figure(figsize=(12, 6), dpi=100)

        # HISTOGRAMA
        ax1 = fig.add_subplot(121)
        if len(clases) < 2:
            return
        centros = [(clases[i] + clases[i+1]) / 2 for i in range(len(clases)-1)]
        ancho = (clases[1] - clases[0]) if len(clases) > 1 else 1.0
        ax1.bar(centros, hi, width=ancho, edgecolor="black", color="aquamarine", align="center")
        ax1.set_title("Histograma (frecuencia relativa)")
        ax1.set_ylabel("Frecuencia relativa")
        ax1.set_ylim(0, max(hi) * 1.1 if hi else 1)

        # OJIVAS
        ax2 = fig.add_subplot(122)

        # --- Ojiva menor que ---
        limites_superiores = clases[1:]
        x_menor_line = [clases[0]] + limites_superiores
        y_menor_line = [0.0] + Hi
        line_menor, = ax2.plot(x_menor_line, y_menor_line, color="green", linewidth=1.5, label="Ojiva menor que")
        ax2.scatter(limites_superiores, Hi, color="green", s=30)

        # --- Ojiva mayor que ---
        limites_inferiores = clases[:-1]
        x_mayor_points = limites_inferiores
        y_mayor_points = Hi_mayor
        ax2.scatter(x_mayor_points, y_mayor_points, color="red", s=30)
        # Línea terminando visualmente en Y=0 en el último límite superior
        x_mayor_line = x_mayor_points + [clases[-1]]
        y_mayor_line = y_mayor_points + [0]
        line_mayor, = ax2.plot(x_mayor_line, y_mayor_line, color="red", linewidth=1.5, label="Ojiva mayor que")

        # --- Tooltip --- (Para mostrar las coordenadas exactas cuando se pasa el cursor)
        annot = ax2.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                             bbox=dict(boxstyle="round", fc="w"),
                             arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(event):
            """Funcion que actualiza las coordenas donde se muestra el tooltip"""
            if event.xdata is not None and event.ydata is not None:
                annot.xy = (event.xdata, event.ydata)
                text = f"x={event.xdata:.2f}, y={event.ydata:.2f}"
                annot.set_text(text)
                annot.get_bbox_patch().set_alpha(0.9)

        def hover(event):
            """Funcion que muestra el tooltip con coordenadas si es que el cursor
            esta sobre la linea de las ojivas"""
            vis = annot.get_visible()
            if event.inaxes == ax2:
                for line in [line_menor, line_mayor]:
                    cont, _ = line.contains(event)
                    if cont:
                        update_annot(event)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover) # Ejecuta el hover

        """Ajustes para la grafica de las ojivas"""
        ax2.set_xticks(clases) # Coordina las etiquetas del eje X con los limites del clase 
        ax2.set_xlim(clases[0] - 2, clases[-1] + 2)
        ax2.set_ylim(0.0, 1.02)
        ax2.set_title("Ojivas (menor que y mayor que)")
        ax2.set_xlabel("Clases")
        ax2.set_ylabel("Frecuencia acumulada relativa")
        ax2.legend()

        fig.tight_layout(pad=4.0)
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar_datos(self): # Limpia los datos XD
        self.text_datos.delete("1.0", "end")
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.lbl_resumen.config(text="")
        for w in self.frame_graficas.winfo_children():
            w.destroy()
