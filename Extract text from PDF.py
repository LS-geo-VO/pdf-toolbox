# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 13:29:49 2023

@author: Z6C | L.Schadee

Get information from PDfs.
Based on https://www.viktor.ai/blog/91/ai-chatGRP-geotechnical-engineering
"""

import re
import pdfplumber
import easygui
import pandas as pd

#Select the pdf to scan
file = easygui.fileopenbox(msg = 'Choose the file to scan',
                           title = 'File Selection', default = None) 

#Probperites to search for
points = []
xco = []
yco = []

# Open the PDF file using pdfplumber
with pdfplumber.open(file) as pdf:
  # Loop through each page of the PDF
  for page in pdf.pages:
    # Extract the text from the page
    text = page.extract_text()
    # Use the regex search function to find the string after the keyword "BOREHOLE LOG"
    points.extend(re.findall(r"Boring:(.*)", text))#.group().split()[-1])
    xco.extend(re.findall(r"X:(.*)",text))#.group().split()[-1])
    yco.extend(re.findall(r"Y:(.*)",text))#.group().split()[-1])
    # xco.append(re.search(r"X-coördinaat:(.*)",text).group().split()[-1]) #single borehole per page
    # yco.append(re.search(r"Y-coördinaat:(.*)",text).group().split()[-1]) #singel borehole per page

# Print the extracted results
for b, x, y in zip(points, xco, yco):
    print(f'{b},{x},{y}')

#Post processing:
for i in range(len(xco)):
    xco[i] = float(xco[i].replace(",","."))
    yco[i] = float(yco[i].replace(",","."))
   
# Make dataframe and save csv:
data = { "ID": points,
        "X-coordinate": xco,
        "Y-coordinate": yco}

df = pd.DataFrame.from_dict(data)

df.to_csv(file+'.csv')
   