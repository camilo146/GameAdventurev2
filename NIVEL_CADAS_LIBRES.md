# 🎮 Nivel Rediseñado - Caídas Libres y Power-ups (ACTUALIZADO)

## 🗺️ **Mapa del Nivel 1 Actualizado - Versión Accesible**

```
    [PLAT1] [PLAT2]       [PLAT3]      [PLAT4]     [PLAT5]
      ⭐      💰           💰           💰          💰
═══════════     ═══════════     ══════════     ═══════════════════════════
0-480      640-960     1120-1440     1600-3200
   ↕         ↕            ↕             ↕
INICIAL   HUECO 1     HUECO 2       HUECO 3        ÁREA FINAL
(160px)   (160px)     (160px)      (CONECTADA)
```

## ✅ **CORRECCIONES APLICADAS**

### 🚨 **Problema 1: Mario no moría al caer**
- **Antes**: Límite de muerte en `ALTO + 100` (muy bajo)
- **Después**: Límite de muerte en `ALTO + 50` (muerte más rápida)
- **Resultado**: ✅ Mario muere rápidamente al caer al vacío

### 🏃‍♂️ **Problema 2: Plataformas muy lejanas**
- **Antes**: Huecos de 300px (imposibles de saltar)
- **Después**: Huecos de 160px (saltables con carrerilla)
- **Resultado**: ✅ Plataformas alcanzables con salto normal

## 🏗️ **Estructura de Espacios de Caída Libre**

### 📍 **PRIMER HUECO DE CAÍDA LIBRE (600-900px)**
- ❌ **SIN plataformas de apoyo**
- ✅ Plataformas flotantes para cruzar:
  - 🔩 Metal en 700px (altura 400)
  - ☁️ Nube en 800px (altura 450)
- 💰 Monedas flotantes para incentivar el riesgo
- ⭐ Bloque con power-up encima de plataforma metal

### 📍 **SEGUNDO HUECO DE CAÍDA LIBRE (1200-1500px)**
- ❌ **SIN plataformas de apoyo**
- ✅ Plataformas flotantes para cruzar:
  - 🔩 Metal en 1300px (altura 400)
  - ☁️ Nube en 1420px (altura 350)
- 💰 Monedas flotantes estratégicas
- 🧱 Bloques decorativos sobre plataformas

### 📍 **TERCER HUECO DE CAÍDA LIBRE (1800-2100px)**
- ❌ **SIN plataformas de apoyo**
- ✅ Plataformas flotantes para cruzar:
  - 🟤 Normal en 1900px (altura 450)
  - 🔩 Metal en 2000px (altura 400)
- 💰 Monedas flotantes desafiantes
- ⭐ Bloque final con flor de fuego

## 🎁 **Sistema de Power-ups Mejorado**

### 📦 **Bloques con Power-ups**
1. **Bloque 1** (340, 430): 🍄 **Hongo** - Sobre plataforma normal
2. **Bloque 2** (520, 330): 🌸 **Flor** - Sobre plataforma nube
3. **Bloque 3** (720, 380): 🍄 **Hongo** - Sobre plataforma metal
4. **Bloque 4** (2020, 380): 🌸 **Flor** - Sobre plataforma final

### ✨ **Características de los Power-ups**
- 🟨 **Brillo dorado animado** en bloques con power-ups
- ❓ **Símbolo de interrogación** visible
- 📍 **Aparecen desde dentro del bloque** cuando se golpea
- 🎯 **Posicionamiento estratégico** sobre plataformas sólidas

## 🪙 **Distribución de Monedas**

### 💰 **Monedas Seguras** (sobre plataformas)
- Área inicial: 1 moneda
- Después del primer hueco: 1 moneda
- Después del segundo hueco: 1 moneda
- Área final: 1 moneda

### 💰 **Monedas de Riesgo** (flotantes cerca de huecos)
- 6 monedas flotantes sobre los espacios de caída libre
- Requieren saltos precisos para recolectar
- Incentivan el riesgo vs recompensa

## 🎯 **Objetivos del Diseño**

### ✅ **Caídas Libres Reales**
- Espacios de 300px sin apoyo = caída garantizada
- Solo plataformas flotantes opcionales para cruzar
- Riesgo real de perder una vida

### ✅ **Power-ups Integrados**
- Aparecen desde dentro de los bloques
- Ubicación lógica sobre plataformas estables
- Brillo visual para identificar bloques especiales

### ✅ **Experiencia Desafiante**
- 3 huecos de caída libre progresivos
- Monedas flotantes que requieren precisión
- Balance entre riesgo y recompensa

---
*🎮 Mario Bros Replica - Diseño de Nivel con Caídas Libres Auténticas*