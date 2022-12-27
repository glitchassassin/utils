import sys
import csv

def process_bank1(rows):
    if rows[0][0] != "Account Number":
        return None
    
    return [
        ["Date", "Check", "Description", "Amount"],
    ] +  [[row[1], row[2], row[3], ("-" + row[4]) if row[4] != "" else row[5]] for row in rows[1:]]

def process_bank2(rows):
    print("bank2", rows[1][0], rows[1][0] != "Date")
    if rows[1][0] != "Date":
        return None
    
    data = [
        ["Date", "Check", "Description", "Amount"],
    ]

    found_records = False
    for row in rows[1:]:
        if row[0] == "Posted Transactions":
            found_records = True
            continue
        if not found_records:
            continue
        value = ("-" + row[4]) if row[4] != "" else row[5]
        value = value.replace("$", "").replace(",", "")
        data.append([row[0], row[2], row[3], value])
    
    return data

def process_bank3(rows):
    print("bank3", rows[0][0], rows[0][0] != "Date")
    if rows[0][0] != "Date":
        return None
    
    return [
        ["Date", "Check", "Description", "Amount"],
    ] +  [[row[0], "", row[3], row[9]] for row in rows[1:]]

def render_markdown_table(data):
    headers = "|".join(data[0])
    table = f"|{headers}|\n"
    table += f"|{'|'.join(['---' for _ in headers])}|\n"
    for row in data[1:]:
        print(row)
        table += f"|{'|'.join(row)}|\n"
    return table

# load file from command line parameter.
# Parse the CSV file, pad each row with extra strings if needed 
# to make them all the same length, and convert it to a Markdown table.
# If the field is a number, right-align it.
def load_csv():
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        # test file to find matching handler

        print(rows[0:3])
        data = process_bank1(rows) or process_bank2(rows) or process_bank3(rows)
        if not data:
            print("Could not find matching bank format")
            return
        table = render_markdown_table(data)
        print(table)

if __name__ == '__main__':
    load_csv()