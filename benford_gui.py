import PyPDF2
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from scipy.stats import chisquare
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import log10

def extract_numbers_from_pdf(file_path):
    if not file_path.endswith('.pdf'):
        messagebox.showwarning("Invalid file", "Please select a PDF file.")
        return []
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file_obj.close()
    numbers = []
    for word in text.split():
        if not any(char.isdigit() for char in word):
            continue
        if '.' in word:
            word = re.sub('^0*\.', '.', word)
        else:
            word = word.lstrip('0')
        leading_digit = next((char for char in word if char.isdigit()), None)
        if leading_digit is not None:
            numbers.append(int(leading_digit))
    return numbers

def benford_expected():
    return [log10(1 + 1/digit) for digit in range(1, 10)]

def interpret_p_value(p_val):
    if p_val < 0.01:
        return "The data significantly deviates from Benford's Law.\n It is likely that the document has been manipulated."
    elif p_val < 0.05:
        return "The data moderately deviates from Benford's Law.\n The document may have been altered."
    else:
        return "The data does not significantly deviate from Benford's Law.\n The document appears to be authentic."

canvas = None
def on_button_click():
    global canvas
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()
        canvas.get_tk_widget().destroy()

    result_label.pack_forget()
    interpretation_label.pack_forget()

    file_path = filedialog.askopenfilename()
    numbers = extract_numbers_from_pdf(file_path)
    numbers = [num for num in numbers if num != 0]
    if numbers:
        digit_count = defaultdict(int)
        total = 0
        for number in numbers:
            digit_count[number] += 1
            total += 1
        observed = [digit_count[i] / total for i in range(1, 10)]
        expected = benford_expected()
        chi_square_stat, p_val = chisquare(observed, f_exp=expected)

        result_text = f"Chi-Square Statistic: {chi_square_stat:.4f}, P-Value: {p_val:.4f}"
        result_label.config(text=result_text)
        result_label.pack()

        interpretation_text = interpret_p_value(p_val)
        interpretation_label.config(text=interpretation_text)
        interpretation_label.pack()

        fig = plt.Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)
        sorted_keys = sorted(digit_count.keys())
        bars = ax.bar(sorted_keys, [digit_count[i] / total * 100 for i in sorted_keys], tick_label=sorted_keys)
        ax.set_xlabel('Digits')
        ax.set_ylabel('Frequency (%)')
        ax.set_title('Frequency of Leading Digits')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}%',
                    ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window = tk.Tk()
window.title("Benford's Law Testing, by Calvin Wong")
window.geometry('800x600')
window.resizable(0, 0)

button = tk.Button(window, text="Open PDF", command=on_button_click)
button.pack()

result_label = tk.Label(window)
interpretation_label = tk.Label(window, wraplength=600)

window.mainloop()
