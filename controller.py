from model import CDFModel
from view import CDFView

class CDFController:
    def __init__(self):
        self.modelo = CDFModel()
        self.vista = CDFView()

        # Conectar botones
        self.vista.btn_generar.config(command=self.generar_cdf)
        self.vista.btn_limpiar.config(command=self.limpiar_datos)

        # Iniciar la aplicación
        self.vista.mainloop()

    def generar_cdf(self):
        texto = self.vista.text_datos.get("1.0", "end").strip()
        if not texto:
            self.vista.lbl_resumen.config(text="Error: no se ingresaron datos.")
            return
        try:
            datos = [float(x) for x in texto.replace(",", " ").split()]
        except ValueError:
            self.vista.lbl_resumen.config(text="Error: ingrese solo números separados por comas o espacios.")
            return

        self.modelo.limpiar_datos()
        self.modelo.agregar_datos(datos)

        tabla, resumen, clases, hi, Hi, Hi_mayor = self.modelo.calcular_cdf()

        self.vista.mostrar_cdf(tabla, resumen)
        self.vista.mostrar_graficas(clases, hi, Hi, Hi_mayor)

    def limpiar_datos(self):
        self.modelo.limpiar_datos()
        self.vista.limpiar_datos()
