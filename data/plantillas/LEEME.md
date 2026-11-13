# Plantillas de importación

## saldo_inicial.csv

Una fila por cliente que hoy tiene deuda en cuenta corriente. Se abre con Excel y se guarda como CSV (separado por `;`).

| Columna | Obligatoria | Ejemplo | Nota |
|---|---|---|---|
| Cliente | Sí | Almacén Don Pepe | Como figura en FactuPyme |
| CUIT | Recomendada | 20-12345678-6 | Sin CUIT, el cliente se identifica por el nombre y no se pueden cruzar las facturas de ARCA |
| Saldo | Sí | 125.000,50 | Lo que debe a la fecha de corte. Un saldo a favor (negativo) se carga después como ajuste |
| Fecha | Sí | 15/10/2026 | Fecha del comprobante impago más antiguo (para la antigüedad) |
| Vencimiento | No | 14/11/2026 | Si falta: Fecha + condición de pago |
| Condición de pago (días) | No | 30 | Si falta: 30 días |
| Teléfono | No | 2954 123456 | Se guarda **sin consentimiento**: no se usa para mensajes hasta registrarlo |

Borrá la fila de ejemplo antes de importar.
