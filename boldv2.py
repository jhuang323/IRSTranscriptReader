import re
from collections import defaultdict
import PyPDF2


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def parse_transcript(transcript_text):
    short_term_pattern = r"SHORT TERM CAPITAL GAINS AND LOSSES(.*?)(?=LONG TERM CAPITAL GAINS AND LOSSES|\Z)"
    long_term_pattern = r"LONG TERM CAPITAL GAINS AND LOSSES(.*?)(?=\Z)"

    short_term_section = re.search(short_term_pattern, transcript_text, re.DOTALL)
    long_term_section = re.search(long_term_pattern, transcript_text, re.DOTALL)

    short_term_data = process_section(short_term_section.group(1) if short_term_section else "")
    long_term_data = process_section(long_term_section.group(1) if long_term_section else "")

    return short_term_data, long_term_data


def process_section(section_text):
    data = defaultdict(lambda: {"proceeds": 0, "cost_basis": 0})

    pattern = r"FIN: (\w+).*?PROCEEDS: \$?([\d,.]+).*?COST BASIS: \$?([\d,.]+)"

    for match in re.finditer(pattern, section_text, re.DOTALL):
        fin, proceeds, cost_basis = match.groups()
        data[fin]["proceeds"] += float(proceeds.replace(",", ""))
        data[fin]["cost_basis"] += float(cost_basis.replace(",", ""))

    return dict(data)


def print_results(short_term, long_term):
    print("Short-term Capital Gains and Losses:")
    print_category_results(short_term)

    print("\nLong-term Capital Gains and Losses:")
    print_category_results(long_term)


def print_category_results(data):
    for fin, values in data.items():
        print(f"  FIN: {fin}")
        print(f"    Proceeds: ${values['proceeds']:.2f}")
        print(f"    Cost Basis: ${values['cost_basis']:.2f}")
        print(f"    Gain/Loss: ${values['proceeds'] - values['cost_basis']:.2f}")
        print()


# Main execution
pdf_path = "Wage and Income Transcript.pdf"  # Replace with the actual path to your PDF file
transcript_text = extract_text_from_pdf(pdf_path)
short_term, long_term = parse_transcript(transcript_text)
print_results(short_term, long_term)
