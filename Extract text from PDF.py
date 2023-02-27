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
import numpy as np
import os

#Select the pdf to scan
files = easygui.fileopenbox(msg = 'Choose the file to scan',
                           title = 'File Selection', 
                           filetypes="\*.pdf" , #"*.PDF", "PDF-files"] ,
                           default = None, multiple=True) 

#Properites to search for
name = []
points = []
xco = []
yco = []
zco = []

for file in files:
    name.append(file.split("\\")[-1])
    # Open the PDF file using pdfplumber
    with pdfplumber.open(file) as pdf:
      # Loop through each page of the PDF
      for page in pdf.pages:
        # Extract the text from the page
        text = page.extract_text()
        # Use the regex search function to find the string after the keyword "BOREHOLE LOG"
        points.extend(re.findall(r"Sond.(.*)", text)[-1])#.group().split()[-1])
        points.extend(re.findall(r"Boring:(.*)", text))#.group().split()[-1])
        xco.extend(re.findall(r"X=(.*)",text))#.group().split()[-1])
        yco.extend(re.findall(r"Y=(.*)",text))#.group().split()[-1])
        zco.extend(re.findall(r"MV(.*)",text))#.group().split()[-1])
        xco.extend(re.findall(r"X:(.*)",text))#.group().split()[-1])
        yco.extend(re.findall(r"Y:(.*)",text))#.group().split()[-1])
        # xco.append(re.search(r"X-coördinaat:(.*)",text).group().split()[-1]) #single borehole per page
        # yco.append(re.search(r"Y-coördinaat:(.*)",text).group().split()[-1]) #singel borehole per page

# Print the extracted results
for n, b, x, y, z in zip(name, points, xco, yco, zco):
    print(f'{n},{b},{x},{y},{z}')

#Post processing:
for i in range(len(points)):
    points[i].strip()
    xco[i] = xco[i].split()[0]
    xco[i] = xco[i].replace('m',"")
    xco[i] = float(xco[i].replace(",","."))
    yco[i] = yco[i].split()[0]
    yco[i] = yco[i].replace('m',"")
    yco[i] = float(yco[i].replace(",","."))
    
for i in range(len(zco)):
    zlist = zco[i].split()
    for j, z in enumerate(zlist):
        if "NAP" in z:
            zpos = j
    zco[i] = zlist[zpos+1]
    zco[i] = zco[i].replace('m',"")
    zco[i] = float(zco[i].replace(",","."))
   
# Make dataframe and save csv:
data = {"ID": points,
        "X-coordinate": xco,
        "Y-coordinate": yco,
        "Z-coordinate": zco,
        "filename": name}

df = pd.DataFrame.from_dict(data)
path = os.path.dirname(file)
df.to_csv(f'{path}\\Extracted data.csv')
   