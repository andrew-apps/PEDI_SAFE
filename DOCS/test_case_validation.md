---
title: "Casos de Prueba para Validación - PediSafe"
source: "Casos de prueba para validar el sistema de triaje"
language: "es"
last_updated: "2026-01-09"
---

# Casos de Prueba para Validación del Sistema

## 🧪 Casos Críticos de Prueba

### Caso 1: Bebé con Fiebre Moderada (DEBERÍA SER AMARILLO)
```
Entrada: "8 meses, 38.5°C rectal, 5 horas de fiebre, muy irritable pero consolable, 2 pañales mojados en 24h, rechaza biberón"

Análisis:
- Edad: 8 meses (6-12 meses)
- Temperatura: 38.5°C (<38.9°C umbral NARANJA)
- Comportamiento: Irritable pero consolable (no es emergencia)
- Hidratación: 2 pañales/24h (disminuida pero no deshidratación severa)
- Duración: 5 horas (corta)

Clasificación Correcta: 🟡 AMARILLO
Razón: Sin signos de emergencia vital, sin deshidratación severa, temperatura bajo umbral de urgencia
Acción: Contactar pediatra en 24h, manejo domiciliario
```

### Caso 2: Bebé con Fiebre Alta (DEBERÍA SER NARANJA)
```
Entrada: "4 meses, 39.2°C rectal, 8 horas, muy irritable, rechaza alimentación, 1 pañal mojado en 12h"

Análisis:
- Edad: 4 meses (3-6 meses)
- Temperatura: 39.2°C (>38.3°C umbral NARANJA)
- Comportamiento: Muy irritable
- Hidratación: 1 pañal/12h (signos de deshidratación)
- Duración: 8 horas

Clasificación Correcta: 🟠 NARANJA
Razón: Temperatura sobre umbral para edad + signos de deshidratación
Acción: Contactar pediatra AHORA
```

### Caso 3: Recién Nacido con Fiebre (DEBERÍA SER ROJO)
```
Entrada: "2 meses, 38.2°C rectal, 3 horas, un poco irritable pero come bien"

Análisis:
- Edad: 2 meses (<3 meses)
- Temperatura: 38.2°C (CUALQUIER fiebre en <3 meses = ROJO)
- Comportamiento: Irritable leve (irrelevante)
- Hidratación: Buena (irrelevante)

Clasificación Correcta: 🔴 ROJO
Razón: CUALQUIER fiebre en <3 meses es emergencia
Acción: Llamar 911 o ir a urgencias INMEDIATAMENTE
```

### Caso 4: Niño Mayor con Fiebre y Síntomas Leves (DEBERÍA SER VERDE)
```
Entrada: "5 años, 37.8°C oral, 1 día, tos leve, jugando normalmente, bebiendo bien"

Análisis:
- Edad: 5 años (>12 meses)
- Temperatura: 37.8°C (<39.0°C umbral AMARILLO)
- Comportamiento: Jugando normalmente
- Hidratación: Buena
- Duración: 1 día

Clasificación Correcta: 🟢 VERDE
Razón: Fiebre baja con buen estado general
Acción: Cuidado domiciliario
```

## 🚨 Casos Límite Importantes

### Caso 5: Fiebre con Signos de Alarma (DEBERÍA SER ROJO)
```
Entrada: "1 año, 39°C, dificultad para respirar, tiraje intercostal"

Análisis:
- Edad: 1 año
- Temperatura: 39°C
- Signos de alarma: DIFICULTAD RESPIRATORIA

Clasificación Correcta: 🔴 ROJO
Razón: Signos de emergencia vital presentes
Acción: Llamar 911 INMEDIATAMENTE
```

### Caso 6: Fiebre Persistente (DEBERÍA SER NARANJA)
```
Entrada: "3 años, 38.7°C, 4 días con fiebre, comportamiento normal, bien hidratado"

Análisis:
- Edad: 3 años
- Temperatura: 38.7°C
- Duración: 4 días (>72 horas)
- Comportamiento: Normal
- Hidratación: Buena

Clasificación Correcta: 🟠 NARANJA
Razón: Fiebre persistente >72 horas requiere evaluación
Acción: Contactar pediatra hoy
```

## 📋 Validación de Errores Comunes

### Error 1: Alucinación de Síntomas
```
Entrada: "8 meses, 38.5°C, irritabilidad, 2 pañales"

Respuesta Incorrecta: "menciona convulsión" ❌
Problema: El agente INVENTA síntomas que no existen
Validación: Solo usar información explícitamente proporcionada
```

### Error 2: Clasificación por Temperatura Solamente
```
Entrada: "4 años, 40°C, jugando felizmente, bien hidratado"

Respuesta Incorrecta: 🔴 ROJO (solo por temperatura) ❌
Respuesta Correcta: 🟠 NARANJA (temperatura alta pero buen estado general)
Validación: El comportamiento es más importante que la temperatura
```

### Error 3: Ignorar Factores de Edad
```
Entrada: "2 meses, 38.2°C, bebé feliz"

Respuesta Incorrecta: 🟢 VERDE ❌
Respuesta Correcta: 🔴 ROJO
Validación: CUALQUIER fiebre ≥38.0°C en <3 meses es emergencia

NOTA IMPORTANTE: 37.8°C NO es fiebre (rango normal: 36.5-37.5°C). 
Solo temperaturas ≥38.0°C (100.4°F) se consideran fiebre en bebés según AAP/NHS.
```

## 🎯 Criterios de Validación

### Para Cada Respuesta del Agente:
1. **¿Clasificó correctamente el nivel?** (ROJO/NARANJA/AMARILLO/VERDE)
2. **¿Usó solo información proporcionada?** (no inventó síntomas)
3. **¿Consideró todos los factores relevantes?** (edad, temperatura, comportamiento, hidratación, duración)
4. **¿Recomendó la acción correcta?** (urgencias/pediatra/casa)
5. **¿Incluyó disclaimer de seguridad?**
6. **¿Citó fuentes correctamente?**

### Señales de Alerta del Sistema:
- Alucinación de síntomas
- Clasificación inconsistente con las guías
- Ignorar factores de comportamiento
- No verificar edad correctamente
- Recomendaciones peligrosas (ej. dosis específicas)

## 🔄 Proceso de Testing

1. **Ejecutar cada caso de prueba**
2. **Comparar respuesta con clasificación esperada**
3. **Verificar razonamiento del agente**
4. **Validar fuentes citadas**
5. **Revisar seguridad y disclaimer**
6. **Documentar discrepancias**

---
**Nota**: Estos casos deben ejecutarse después de cada actualización del sistema para asegurar consistencia y seguridad.
