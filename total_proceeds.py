import fitz  # PyMuPDF

def extract_value(text, keyword):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # Check for exact keyword and ensure "Gross Proceeds" is not in the line
        if line.strip().startswith(keyword) and "Gross" not in line:
            value = line.split(":")[1].strip()  # take the part after the colon as the value
            # If the value is empty, get the value from the next line
            if value == "":
                value = lines[i + 1].strip()
            return value
    return "N/A"

# Open the PDF file
with fitz.open(r"Wage and Income Transcript.pdf") as doc:
    # Initialize total proceeds
    total_proceeds = 0

    # Loop through each page
    for page_num in range(len(doc)):
        # Get the text of the page
        text = doc[page_num].get_text()

        # Extract and print the information
        proceeds = extract_value(text, 'Proceeds:')

        print(f"Information on Page {page_num + 1}:")
        print(f"Proceeds: {proceeds}")
        print("----------------------------------------")

        # Add the values to total proceeds
        try:
            proceeds_value = float(proceeds.replace('$', ''))
            total_proceeds += proceeds_value
        except ValueError:
            continue  # Skip if the value is not a number

    # Print the total proceeds summary
    print("Total Proceeds:")
    print(f"${total_proceeds:.2f}")

