import fitz  # PyMuPDF

# Path to the PDF file
pdf_path = r"Wage and Income Transcript.pdf"

# Open the PDF file
with fitz.open(pdf_path) as doc:

    # Loop through each page
    for page_num in range(len(doc)):
        # Get the page
        page = doc[page_num]

        # Get the text blocks on the page
        blocks = page.get_text("dict")["blocks"]

        # Iterate through each text block
        for block in blocks:
            # Check if the block is a text block
            if block["type"] == 0:
                # Iterate through each line in the block
                for line in block["lines"]:
                    # Iterate through each span (continuous text with the same style) in the line
                    for span in line["spans"]:
                        # Print the keys of the span dictionary to inspect the available keys
                        print(f"Available keys in the span dictionary: {list(span.keys())}")



