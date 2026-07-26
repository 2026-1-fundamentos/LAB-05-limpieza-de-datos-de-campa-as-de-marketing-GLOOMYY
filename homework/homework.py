"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    from pathlib import Path

    import pandas as pd

    project_dir = Path(__file__).resolve().parent.parent
    input_dir = project_dir / "files" / "input"
    output_dir = project_dir / "files" / "output"

    input_files = sorted(input_dir.glob("*.csv.zip"))
    if not input_files:
        raise FileNotFoundError(
            f"No se encontraron archivos .csv.zip en {input_dir}"
        )

    # Pandas lee los CSV comprimidos directamente, por lo que no es necesario
    # crear copias descomprimidas en el disco.
    data = pd.concat(
        (pd.read_csv(file_path) for file_path in input_files),
        ignore_index=True,
    )

    client = data[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()
    client["job"] = (
        client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    )
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = client["credit_default"].eq("yes").astype("int64")
    client["mortgage"] = client["mortgage"].eq("yes").astype("int64")

    month_numbers = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    last_contact_date = pd.to_datetime(
        {
            "year": 2022,
            "month": data["month"].str.lower().map(month_numbers),
            "day": data["day"],
        },
        errors="raise",
    ).dt.strftime("%Y-%m-%d")

    campaign = data[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
        ]
    ].copy()
    campaign["previous_outcome"] = (
        data["previous_outcome"].eq("success").astype("int64")
    )
    campaign["campaign_outcome"] = (
        data["campaign_outcome"].eq("yes").astype("int64")
    )
    campaign["last_contact_date"] = last_contact_date

    economics = data[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].copy()

    output_dir.mkdir(parents=True, exist_ok=True)
    client.to_csv(output_dir / "client.csv", index=False)
    campaign.to_csv(output_dir / "campaign.csv", index=False)
    economics.to_csv(output_dir / "economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()
