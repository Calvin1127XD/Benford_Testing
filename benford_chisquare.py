import PyPDF2
import matplotlib.pyplot as plt
from collections import defaultdict
import re
from math import log10
from scipy.stats import chisquare

def extract_numbers_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file_obj.close()
    
    # Extract numbers from the text
    numbers = []
    for word in text.split():
        # Skip if not a number
        if not any(char.isdigit() for char in word):
            continue
        # Remove leading zeros for decimal numbers
        if '.' in word:
            word = re.sub('^0*\.', '.', word)
        # Remove leading zeros for whole numbers
        else:
            word = word.lstrip('0')
        # Extract leading digit
        leading_digit = next((char for char in word if char.isdigit()), None)
        if leading_digit is not None:
            numbers.append(int(leading_digit))
    return numbers

def benford_expected():
    # Expected distribution according to Benford's Law
    return [log10(1 + 1/digit) for digit in range(1, 10)]

def benford_test(numbers):
    digit_count = defaultdict(int)
    total_count = 0
    for number in numbers:
        digit_count[number] += 1
        total_count += 1
    # Actual distribution
    actual_distribution = [digit_count[digit] / total_count for digit in range(1, 10)]
    # Expected distribution
    expected_distribution = benford_expected()
    # Chi-squared test
    chi_squared_stat, p_val = chisquare(actual_distribution, f_exp=expected_distribution)
    print(f"Chi-squared statistic: {chi_squared_stat}")
    print(f"p-value: {p_val}")

if __name__ == "__main__":
    file_path = 'testing.pdf'  # Replace with your PDF file path
    numbers = extract_numbers_from_pdf(file_path)
    # Remove zeros from numbers
    numbers = [num for num in numbers if num != 0]
    benford_test(numbers)
