from abc import ABC, abstractmethod

class IMatricula(ABC):
    """Clase abstracta que define el contrato para cualquier tipo de matrícula."""
    
    @abstractmethod
    def calcular_costo(self) -> float:
        """Método polimórfico que todas las subclases deben implementar."""
        pass


class MatriculaGeneral(IMatricula):
    """Es la matrícula base. Retorna siempre el monto inicial de S/ 60.00."""
    
    def __init__(self, estudiante: str):
        self.estudiante = estudiante
        self._monto_base = 60.00  # Atributo encapsulado

    def calcular_costo(self) -> float:
        # El cálculo base siempre inicia en 60.00
        return self._monto_base


class ModificadorMatricula(IMatricula):
    """
    Clase abstracta decoradora. 
    Hereda de IMatricula pero también CONTIENE un objeto IMatricula.
    Esto permite encadenar múltiples modificaciones una sobre otra.
    """
    def __init__(self, matricula_envuelta: IMatricula):
        # Guardamos la referencia al objeto que estamos decorando/envolviendo
        self._matricula = matricula_envuelta

    @abstractmethod
    def calcular_costo(self) -> float:
        # Delega el cálculo al objeto envuelto
        return self._matricula.calcular_costo()


class MatriculaExtemporanea(ModificadorMatricula):
    """Especialización que añade S/ 15.00 al monto."""
    
    def calcular_costo(self) -> float:
        # Llama al cálculo del objeto envuelto y le suma 15.00
        monto_acumulado = super().calcular_costo()
        return monto_acumulado + 15.00

class MatriculaIndiceDesaprobatorio(ModificadorMatricula):
    """Especialización que añade S/ 15.00 adicionales."""
    
    def calcular_costo(self) -> float:
        # Llama al cálculo del objeto envuelto y le suma 15.00
        monto_acumulado = super().calcular_costo()
        return monto_acumulado + 15.00

class MatriculaBeca(ModificadorMatricula):
    """Especialización que divide el monto a la mitad."""
    
    def calcular_costo(self) -> float:
        # Llama al cálculo del objeto envuelto y aplica el descuento del 50%
        monto_acumulado = super().calcular_costo()
        return monto_acumulado / 2.0


# ==========================================
# 5. PRUEBA DEL SISTEMA Y SOLUCIÓN DEL CASO
# ==========================================
if __name__ == "__main__":
    
    # --- CASO 1: LUIS HUAMANÍ CÁRDENAS ---
    # En este escenario, la beca se aplica al FINAL, sobre todo el monto acumulado.
    
    # 1. Se crea la matrícula base (60.00)
    matricula_luis = MatriculaGeneral("Luis Huamaní Cárdenas")
    
    # 2. Se envuelve con el recargo extemporáneo (60 + 15 = 75.00)
    matricula_luis = MatriculaExtemporanea(matricula_luis)
    
    # 3. Se envuelve con el recargo por índice (75 + 15 = 90.00)
    matricula_luis = MatriculaIndiceDesaprobatorio(matricula_luis)
    
    # 4. Finalmente, se envuelve con la beca que divide TODO a la mitad (90 / 2 = 45.00)
    matricula_luis = MatriculaBeca(matricula_luis)
    
    print("--- CASO LUIS (Beca al final) ---")
    print(f"Total a pagar: S/ {matricula_luis.calcular_costo():.2f}\n")


    # --- CASO 2: ROSA CCAHUANA PRADO ---
    # En este escenario, la beca solo cubre el costo base y los recargos se cobran completos.
    
    # 1. Se crea la matrícula base (60.00)
    matricula_rosa = MatriculaGeneral("Rosa Ccahuana Prado")
    
    # 2. Se envuelve PRIMERO con la beca (60 / 2 = 30.00)
    matricula_rosa = MatriculaBeca(matricula_rosa)
    
    # 3. Luego se envuelve con el recargo extemporáneo (30 + 15 = 45.00)
    matricula_rosa = MatriculaExtemporanea(matricula_rosa)
    
    # 4. Finalmente, el recargo por índice (45 + 15 = 60.00)
    matricula_rosa = MatriculaIndiceDesaprobatorio(matricula_rosa)
    
    print("--- CASO ROSA (Beca al inicio) ---")
    print(f"Total a pagar: S/ {matricula_rosa.calcular_costo():.2f}")