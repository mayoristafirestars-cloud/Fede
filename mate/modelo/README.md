# Adaptador para un modelo propio

Esta carpeta deja que un programa de Mate le pida a **otra IA** que no es la que trae Mate
(por ejemplo un modelo que corre en tu computadora con Ollama o LM Studio). No cambia nada del
lenguaje: son archivos nuevos que se usan con `usar python`.

## El acuerdo

```
modelo.pedir_al_modelo(instrucciones, pregunta)
```

Recibe dos textos y devuelve **siempre** un texto JSON que describe un objeto, por ejemplo
`{"producto":"cinta_5m"}`. Con `de_json(...)` queda como un mapa de Mate.

Si algo sale mal, la función **falla** con un error que se ataja con `intentar`:

| Qué pasó | El error dice |
|---|---|
| El modelo contestó algo que no es JSON | `el modelo contestó algo que no es JSON: ...` |
| Contestó un JSON que no es un objeto (una lista, un texto suelto) | `el modelo contestó un JSON que no es un objeto entre llaves: ...` |
| No contestó nada | `el modelo no contestó nada` |
| No se pudo llegar hasta el modelo | `no se pudo llegar al modelo ...` |
| El servicio contestó con un error (clave, nombre del modelo) | `el modelo contestó con el error 401 ...` |

## Usarlo desde un programa

La carpeta `modelo` tiene que estar **al lado del programa** (copiala ahí).

```
usar python "modelo/modelo.py"

funcion elegir_producto(pregunta) {
    intentar {
        sea contestado = modelo.pedir_al_modelo("Decí qué producto pide el cliente.", pregunta)
        devolver de_json(contestado).producto
    } si falla motivo {
        devolver nada
    }
}
```

## En las pruebas

`modelo.simular_modelo([...])` deja preparado lo que va a contestar, en orden, y desde ahí no
se usa la red. El texto `"!conexion"` simula que no se pudo llegar al modelo.

```
prueba "elige la cinta" {
    modelo.simular_modelo([a_json({producto: "cinta_5m"})])
    asegurar elegir_producto("la de 5 m") == "cinta_5m"
}

prueba "si se cae la conexión no se rompe" {
    modelo.simular_modelo(["!conexion"])
    asegurar elegir_producto("la de 5 m") == nada
}
```

Otras dos funciones: `modelo.pedidos_al_modelo()` devuelve lo que se le pidió (instrucciones,
pregunta y respuesta) y `modelo.proveedor()` dice `"simulado"` o `"propio"`.

Un texto de un renglón no puede llevar comillas adentro: para armar el JSON de una respuesta
simulada usá `a_json({producto: "cinta_5m"})`.

## A qué modelo le pide

- **Sin configurar nada, a uno simulado.** No sale a internet y no gasta.
- **A uno de verdad**, cuando existe la variable `MATE_MODELO_PROPIO_URL` con la dirección de
  un servicio que habla como "chat completions". En PowerShell:

```bash
$env:MATE_MODELO_PROPIO_URL = "http://localhost:11434/v1/chat/completions"
```

```bash
$env:MATE_MODELO_PROPIO_NOMBRE = "el-nombre-de-tu-modelo"
```

- Si el servicio pide clave, va en `MATE_MODELO_PROPIO_CLAVE`. Nunca en un programa.
- Con `MATE_MODELO_PROPIO_SIMULADO=1` se usa el simulado aunque haya dirección.

## Probar esta carpeta

```bash
python mate\mate.py probar mate\modelo\probar_modelo.mate
```

```bash
python -m pytest mate\modelo -q
```

## Lo que hay que saber

- Con una dirección configurada, **también `probar` sale a buscar al modelo** si la prueba no
  llamó antes a `simular_modelo`. El adaptador corre por `usar python`, fuera del control de Mate.
- Lo que se pide por acá **no pasa por los frenos, el tope de gasto, las lecciones ni la traza**:
  eso hoy solo vale para `consultar_ia()`. Unirlo es el paso de integración que queda.
- Se probó con un servicio de mentira en la misma máquina. **No se probó contra un modelo real**
  ni en Windows.
