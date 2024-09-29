import pdfplumber

def extract_and_group_by_gain_loss_code(pdf_path):
    data = {}
    current_code = None
    current_proceeds = 0
    current_cost_basis = 0

    # Extract text using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        total_text = ""
        for page in pdf.pages:
            total_text += page.extract_text()
    lines = total_text.split("\n")

    # Iterate through the lines to find and capture relevant data
    for line in lines:
        if "Type of Gain or Loss Code:" in line:
            current_code = line.split("Type of Gain or Loss Code:")[-1].strip()
            if current_code not in data:
                data[current_code] = {'Total Proceeds': 0, 'Total Cost or Basis': 0}

        if "Proceeds:" in line:
            value = line.split("Proceeds:")[-1].strip().replace(',', '').replace('$', '')
            try:
                proceeds_value = float(value)
                if current_code:
                    data[current_code]['Total Proceeds'] += proceeds_value
                else:
                    print(f"Warning: Proceeds value found without a preceding 'Type of Gain or Loss Code': {proceeds_value}")
            except ValueError:
                pass  # Silently skip non-numeric values

        if "Cost or Basis:" in line:
            value = line.split("Cost or Basis:")[-1].strip().replace(',', '').replace('$', '')
            try:
                cost_basis_value = float(value)
                if current_code:
                    data[current_code]['Total Cost or Basis'] += cost_basis_value
                else:
                    print(f"Warning: Cost or Basis value found without a preceding 'Type of Gain or Loss Code': {cost_basis_value}")
            except ValueError:
                pass  # Silently skip non-numeric values

    # Print the aggregated data
    for code, values in data.items():
        print(f"Type of Gain or Loss Code: {code}")
        print(f"Total Proceeds: ${values['Total Proceeds']:.2f}")
        print(f"Total Cost or Basis: ${values['Total Cost or Basis']:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    pdf_path = r"Wage and Income Transcript.pdf"
    extract_and_group_by_gain_loss_code(pdf_path)
