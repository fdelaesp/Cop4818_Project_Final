"""
Seed the DB from data/combined_output_SPB.xlsx
Run:  python import_data.py
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

from app import create_app
from app.models import db, Indicator, DataPoint

# Path to your Excel file
EXCEL_PATH = Path(__file__).parent / "data" / "combined_output_SPB.xlsx"

def month_order(mes: str) -> int:
    order = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    try:
        return order.index(mes) + 1
    except ValueError:
        return 0  # unknown month

def parse_value(raw_val):
    """
    Convert raw Excel cell into a float.
    Strips "%" and converts to decimal when needed.
    """
    if pd.isna(raw_val):
        return None
    if isinstance(raw_val, str):
        rv = raw_val.strip().replace(",", "")
        if rv.endswith("%"):
            try:
                # "12.34%" → 0.1234
                return float(rv[:-1]) / 100.0
            except ValueError:
                return None
        else:
            try:
                return float(rv)
            except ValueError:
                return None
    # Already numeric
    return float(raw_val)

def main():
    # 1) Load the Excel sheet
    df = pd.read_excel(EXCEL_PATH)

    # 2) Boot Flask and DB
    app = create_app()
    with app.app_context():
        db.create_all()

        # 3) Ensure all Indicators exist
        for ind_name in df["Indicador"].unique():
            ind = Indicator.query.filter_by(name=ind_name).first()
            if not ind:
                ind = Indicator(name=ind_name, description="")
                db.session.add(ind)
        db.session.commit()

        # 4) Build DataPoint objects
        insert_rows = []
        for _, row in df.iterrows():
            ind = Indicator.query.filter_by(name=row["Indicador"]).first()
            val = parse_value(row["Valor"])
            insert_rows.append(
                DataPoint(
                    indicator_id = ind.id,
                    year         = int(row["Año"]),
                    month        = str(row["Mes"]),
                    value        = val,
                    unidad       = row.get("Unidad", ""),
                    grupo        = row.get("Grupo", ""),
                    subgrupo     = row.get("Subgrupo", ""),
                    categoria    = row.get("Categoría", "")
                )
            )
        # Bulk insert all at once
        db.session.bulk_save_objects(insert_rows)
        db.session.commit()

        # 5) Update each Indicator.latest_val & updated_at
        for ind in Indicator.query.all():
            latest = (
                DataPoint.query
                .filter_by(indicator_id=ind.id)
                .order_by(DataPoint.year.desc(), DataPoint.month.desc())
                .first()
            )
            if latest:
                ind.latest_val = latest.value
                ind.updated_at = datetime(
                    latest.year,
                    month_order(latest.month) or 1,
                    1
                )
        db.session.commit()
        print("✅ Database seeded from Excel.")

if __name__ == "__main__":
    main()
