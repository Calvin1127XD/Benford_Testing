import PyPDF2
import matplotlib.pyplot as plt
from collections import defaultdict
import re

def extract_numbers_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        page_text = page_obj.extractText()
        text += page_text

        # Print out the numbers detected on this page for debugging
        print("Page " + str(page_num + 1) + ":")
        for word in page_text.split():
            if any(char.isdigit() for char in word):
                # Remove leading zeros for decimal numbers
                if '.' in word:
                    processed_word = re.sub('^0*\.', '.', word)
                # Remove leading zeros for whole numbers
                else:
                    processed_word = word.lstrip('0')
                # Extract leading digit
                leading_digit = next((char for char in processed_word if char.isdigit()), None)
                if leading_digit is not None:
                    print(f'{word} ; {leading_digit}')
        print()
    
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

def plot_digit_frequency(numbers):
    digit_count = defaultdict(int)
    for number in numbers:
        digit_count[number] += 1
    
    digits = list(digit_count.keys())
    frequencies = list(digit_count.values())
    
    plt.bar(digits, frequencies, tick_label=digits)
    plt.xlabel('Digits')
    plt.ylabel('Frequency')
    plt.title('Frequency of Leading Digits')
    plt.show()

if __name__ == "__main__":
    file_path = 'testing.pdf'  # Replace with your PDF file path
    numbers = extract_numbers_from_pdf(file_path)
    # Remove zeros from numbers
    numbers = [num for num in numbers if num != 0]
    plot_digit_frequency(numbers)
