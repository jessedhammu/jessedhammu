from pymarc import MARCReader, MARCWriter, Field, Subfield
import pandas as pd

# -------- CONFIG --------
input_mrc = r"E:\E-Books\T&F\books.mrc"
output_mrc = r"E:\E-Books\T&F\books_with_barcodes.mrc"
excel_file = r"E:\E-Books\T&F\barcodes.csv"   # or .csv

match_column = "isbn"
call_column = "call"
barcode_column = "barcode"
url_column = "url"

# -------- LOAD FILE --------
if excel_file.endswith(".csv"):
    df = pd.read_csv(excel_file)
else:
    df = pd.read_excel(excel_file)

# Clean ISBNs
df[match_column] = df[match_column].astype(str).str.replace("-", "").str.strip()

# Create lookup dict
data_map = df.set_index(match_column).to_dict(orient="index")

# -------- PROCESS MARC --------
with open(input_mrc, 'rb') as fh, open(output_mrc, 'wb') as out:
    reader = MARCReader(fh)
    writer = MARCWriter(out)

    for record in reader:
        isbn = None

        if record['020']:
            isbn = record['020']['a']
            if isbn:
                isbn = isbn.replace("-", "").strip()

        if isbn and isbn in data_map:
            data = data_map[isbn]

            barcode = str(data.get(barcode_column, "")).strip()
            callno = str(data.get(call_column, "")).strip()
            url = str(data.get(url_column, "")).strip()

            subfields = [
                Subfield('2', 'ddc'),
                Subfield('a', 'CUP'),
                Subfield('b', 'CUP'),
                Subfield('y', 'E')
            ]

            if callno:
                subfields.append(Subfield('o', callno))
            
            if barcode:
                subfields.append(Subfield('p', barcode))
         
            if url:
                subfields.append(Subfield('u', url))

            field_952 = Field(
                tag='952',
                indicators=[' ', ' '],
                subfields=subfields
            )

            record.add_field(field_952)

        writer.write(record)

    writer.close()

print("Done. Output file:", output_mrc)