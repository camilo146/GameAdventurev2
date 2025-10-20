# Sistema de Llaves - Guía Completa

## 🔑 **¿Cómo Funciona el Sistema de Llaves?**

El sistema de llaves es un mecanismo de progresión que añade estrategia al aprendizaje. Las llaves se obtienen al completar ciertos quizzes y se usan para acceder a contenido avanzado.

## 🎯 **Tipos de Puertas y Sus Requisitos**

### 🟤 **Puertas Obligatorias (Café/Marrón)**
- **Propósito**: Bloquean el camino principal
- **Llaves requeridas**: Varían según el nivel
- **Función**: Progresión forzada del juego

### 🟣 **Puertas Opcionales Secretas (Morado)**
- **Propósito**: Acceso a áreas secretas con bonus
- **Llaves requeridas**: 0-2 llaves
- **Función**: Contenido opcional para exploradores

### 🟢 **Puertas Opcionales Bonus (Verde)**
- **Propósito**: Power-ups y monedas extra
- **Llaves requeridas**: 1-3 llaves (aumenta por nivel)
- **Función**: Recompensas por coleccionar llaves

### 🟠 **Puertas de Llave Especial (Naranja)**
- **Propósito**: **OTORGAN LLAVES** al completar el quiz
- **Llaves requeridas**: 0-3 llaves (según nivel)
- **Función**: **Fuente principal de llaves**

## 🔄 **Mecánica de Obtención de Llaves**

### **Paso 1: Encontrar Puerta de Llave Especial** 🟠
```
Mario se acerca → Puerta brilla → Presiona E → Quiz se activa
```

### **Paso 2: Responder Quiz Correctamente** ✅
```python
if respuesta_correcta and puerta.tipo == TipoPuerta.LLAVE_ESPECIAL:
    self.llaves_acumuladas += 1  # +1 llave obtenida
```

### **Paso 3: Contador Visual Actualizado** 📊
- El contador en la esquina superior derecha muestra las llaves acumuladas
- Se actualiza inmediatamente tras obtener una nueva llave

### **Paso 4: Usar Llaves en Otras Puertas** 🔓
```python
def puede_intentar_abrir(self, llaves_jugador: int) -> bool:
    return llaves_jugador >= self.llaves_requeridas
```

## 📋 **Distribución de Llaves por Nivel**

### **🎮 Nivel 1** - Tutorial del Sistema
| Puerta | Tipo | Posición | Llaves Req. | Función |
|--------|------|----------|-------------|---------|
| Puerta 1 | 🟤 Obligatoria | X=460 | 0 | Bloqueo principal |
| Puerta 2 | 🟤 Obligatoria | X=940 | 0 | Bloqueo principal |
| Puerta 3 | 🟠 Llave Especial | X=2800 | 0 | **+1 LLAVE** |
| Puerta 4 | 🟣 Secreta | X=1800 | 0 | Bonus opcional |

**Resultado**: +1 llave acumulada

### **🎮 Nivel 2** - Introducción a la Estrategia
| Puerta | Tipo | Llaves Req. | Función |
|--------|------|-------------|---------|
| Obligatoria | 🟤 | 0 | Progresión |
| Bonus | 🟢 | 0 | Recompensa libre |
| Llave Especial | 🟠 | 1 | **+1 LLAVE** (necesita 1 para acceder) |

**Resultado**: +1 llave acumulada (total: 2)

### **🎮 Nivel 3** - Estrategia Intermedia
| Puerta | Tipo | Llaves Req. | Función |
|--------|------|-------------|---------|
| Obligatoria 1 | 🟤 | 1 | Progresión (necesita llave) |
| Obligatoria 2 | 🟤 | 1 | Progresión (necesita llave) |
| Llave Especial | 🟠 | 2 | **+1 LLAVE** (necesita 2 para acceder) |

**Resultado**: +1 llave acumulada (total: 3)

### **🎮 Nivel 4** - Estrategia Avanzada
| Puerta | Tipo | Llaves Req. | Función |
|--------|------|-------------|---------|
| Obligatoria 1 | 🟤 | 2 | Progresión avanzada |
| Obligatoria 2 | 🟤 | 2 | Progresión avanzada |
| Secreta | 🟣 | 1 | Bonus para expertos |
| Llave Especial | 🟠 | 3 | **+1 LLAVE** (máximo acceso) |

**Resultado**: +1 llave acumulada (total: 4)

### **🎮 Nivel 5** - Maestría Total
| Puerta | Tipo | Llaves Req. | Función |
|--------|------|-------------|---------|
| Obligatoria | 🟤 | 3 | Acceso final a princesa |
| Bonus 1 | 🟢 | 1 | Power-up final |
| Bonus 2 | 🟢 | 2 | Power-up final |
| Bonus 3 | 🟢 | 3 | Power-up final |

**Resultado**: Uso estratégico de todas las llaves acumuladas

## 💡 **Estrategias de Uso de Llaves**

### **Estrategia Conservadora** 🛡️
- Guardar llaves para puertas obligatorias
- Acceder solo a puertas de llave especial garantizadas
- Minimizar riesgo de quedarse sin llaves

### **Estrategia Exploradora** 🗺️
- Abrir puertas secretas para descubrir bonus
- Conseguir power-ups early para facilitar el juego
- Equilibrar exploración con progresión

### **Estrategia Coleccionista** 💎
- Abrir todas las puertas de llave especial posibles
- Acumular máximo número de llaves
- Acceder a todo el contenido bonus del nivel final

## 🎯 **Flujo de Decisión del Jugador**

```
¿Tengo suficientes llaves para esta puerta?
├─ SÍ → ¿Es obligatoria para progresar?
│  ├─ SÍ → Abrir inmediatamente
│  └─ NO → ¿Vale la pena el bonus?
│     ├─ SÍ → Abrir para bonus
│     └─ NO → Conservar para después
└─ NO → Buscar puertas de llave especial 🟠
```

## 📊 **Sistema de Visualización**

### **Contador HUD** (Esquina Superior Derecha)
```python
def _dibujar_contador_llaves(self, superficie):
    # Muestra: "🔑 Keys: X"
    texto = f"🔑 Keys: {self.quiz_manager.llaves_acumuladas}"
```

### **Indicadores en Puertas**
- **Brillo dorado**: Mario está cerca, puede interactuar
- **Símbolo de llave**: Muestra cuántas llaves requiere
- **Color distintivo**: Identifica el tipo de puerta instantáneamente

### **Mensajes de Estado**
- **"Not enough keys"**: Cuando falta llaves para abrir
- **"Key obtained!"**: Cuando se obtiene una nueva llave
- **"Door unlocked!"**: Cuando se abre correctamente

## 🔄 **Ciclo de Aprendizaje y Recompensa**

```
1. APRENDER → Responder quiz correctamente
2. RECOMPENSAR → Obtener llave (si es puerta especial)
3. DECIDIR → Elegir cómo usar las llaves
4. PROGRESAR → Avanzar con conocimiento + estrategia
5. REPETIR → Siguiente nivel con más desafío
```

## 💾 **Persistencia del Sistema**

### **Datos Guardados**:
```python
{
    "llaves_acumuladas": 3,
    "llaves_gastadas": 1,
    "preguntas_correctas": 15,
    "preguntas_incorrectas": 2,
    # ... otras estadísticas
}
```

### **Recuperación**:
- Las llaves se mantienen entre sesiones
- Progreso educativo se preserva
- Estadísticas acumulativas persisten

## 🎓 **Impacto Educativo del Sistema**

### **Motivación Intrínseca**:
- **Recompensa inmediata**: Llave por respuesta correcta
- **Progresión visible**: Contador aumenta claramente
- **Estrategia educativa**: Más conocimiento = más opciones

### **Refuerzo del Aprendizaje**:
- **Repetición positiva**: Más llaves = más intentos de aprender
- **Consecuencias claras**: Sin conocimiento = sin progresión
- **Decisiones informadas**: Strategy based on understanding

El sistema de llaves transforma el aprendizaje en una **experiencia estratégica gratificante**, donde el conocimiento de inglés se convierte en la moneda del progreso. 🎮🔑📚✨