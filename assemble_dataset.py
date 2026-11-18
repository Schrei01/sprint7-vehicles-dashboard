"""Reconstruye el CSV original a partir de las partes almacenadas en GitHub."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = sorted((ROOT / "dataset_parts").glob("vehicles_us.part*"))
OUTPUT = ROOT / "vehicles_us.csv"


def main() -> None:
    """Unir las partes y validar la cantidad de registros del proyecto."""
    if len(PARTS) != 11:
        raise RuntimeError(f"Se esperaban 11 partes del dataset; hay {len(PARTS)}")
    with OUTPUT.open("wb") as destination:
        for part in PARTS:
            destination.write(part.read_bytes())
    with OUTPUT.open("rb") as csv_file:
        row_count = sum(1 for _ in csv_file)
    if row_count != 51_526:
        raise RuntimeError(f"CSV incompleto: {row_count} líneas")
    print(f"Dataset creado: {OUTPUT.name}, {row_count - 1:,} anuncios")


if __name__ == "__main__":
    main()
