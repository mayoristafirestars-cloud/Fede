"""Numeración de comprobantes sin repetidos."""


def siguiente_numero(conn, empresa_id: int, tipo: str) -> int:
    """
    Incrementa y devuelve el próximo número para (empresa, tipo).
    Debe llamarse dentro de la misma transacción que inserta el comprobante:
    el UPDATE toma el bloqueo de escritura, así dos emisiones simultáneas no
    pueden recibir el mismo número, y si la emisión falla el número se devuelve.
    """
    conn.execute(
        "INSERT OR IGNORE INTO secuencias (empresa_id, tipo, ultimo) VALUES (?, ?, 0)",
        (empresa_id, tipo),
    )
    conn.execute(
        "UPDATE secuencias SET ultimo = ultimo + 1 WHERE empresa_id = ? AND tipo = ?",
        (empresa_id, tipo),
    )
    return conn.execute(
        "SELECT ultimo FROM secuencias WHERE empresa_id = ? AND tipo = ?",
        (empresa_id, tipo),
    ).fetchone()[0]
