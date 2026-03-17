from pymarc import MARCReader, MARCWriter, Field, Subfield
import pandas as pd

# -------- CONFIG --------
input_mrc = r"E:\E-Books\T&F\books.mrc"
output_mrc = r"E:\E-Books\T&F\books_with_barcodes.mrc"
excel_file = r"E:\E-Books\T&F\barcodes.csv"   # or .csv

match_column = "isbn"          # column name in Excel
barcode_column = "barcode"     # column name in Excel

# -------- LOAD EXCEL --------
if excel_file.endswith(".csv"):
    df = pd.read_csv(excel_file)
else:
    df = pd.read_excel(excel_file)

# Clean ISBNs (important)
df[match_column] = df[match_column].astype(str).str.replace("-", "").str.strip()

# Create lookup dictionary
barcode_map = dict(zip(df[match_column], df[barcode_column]))

# -------- PROCESS MARC --------
with open(input_mrc, 'rb') as fh, open(output_mrc, 'wb') as out:
    reader = MARCReader(fh)
    writer = MARCWriter(out)

    for record in reader:
        isbn = None

        # Extract ISBN from 020$a
        if record['020']:
            isbn = record['020']['a']
            if isbn:
                isbn = isbn.replace("-", "").strip()

        # Match and add barcode
        if isbn and isbn in barcode_map:
            barcode = str(barcode_map[isbn])

            field_952 = Field(
    tag='952',
    indicators=[' ', ' '],
    subfields=[
        Subfield(code='2', value='ddc'),
        Subfield(code='a', value='CUP'),
        Subfield(code='b', value='CUP'),
        Subfield(code='e', value='Today and Tomorrow'),
        Subfield(code='p', value=barcode),
        Subfield(code='y', value='E')
    ]
)

            record.add_field(field_952)

        writer.write(record)

    writer.close()

print("Done. Output file:", output_mrc)