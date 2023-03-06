# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:42:28 2023

@author: Z6C | L.Schadee

Get information from 1st page of PDFs in directory and rename files.
Based on https://www.viktor.ai/blog/91/ai-chatGRP-geotechnical-engineering
"""
import easygui
import os
import re
import pdfplumber
import pandas as pd

#Select the pdf to scan
path = easygui.diropenbox(msg = 'Choose the directory to scan',
                          title = 'Folder Selection', default = None)

#Basic loop to exctact identification and rename file:
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        if os.path.splitext(file)[1].upper() == '.PDF':		#SEARCH FOR FILES WITH GIVEN EXTENSION:
            current_file = os.path.join(dirpath, file)            
            # Open the PDF file using pdfplumber
            with pdfplumber.open(current_file) as pdf:
                # Read first page of the PDF
                page = pdf.pages[0]
                # Extract the text from the page
                text = page.extract_text()
                pdf.close()
                if re.search(r"Sond.(.*)",text): #layout Fugro CPT
                    new_file = re.search(r"Sond. (.*)", text).group(1).strip()
                    new_file = os.path.join(dirpath, new_file+".pdf")
                    try:
                        os.rename(current_file, new_file)                
                    except:
                        new_file = re.search(r"Sond. (.*)", text).group(1).strip()
                        print(f"PDF: {file} \tID: {new_file} is skipped")
                elif re.search(r"Boring:(.*)", text): #layout Borehole
                    new_file = re.search(r"Boring:(.*)", text).group(1).split()[0]
                    new_file = os.path.join(dirpath, new_file+".pdf")
                    try:
                        os.rename(current_file, new_file)                
                    except:
                        new_file = re.search(r"Boring:(.*)", text).group(1).split()[0]
                        print(f"PDF: {file} \tID: {new_file} is skipped")                
                elif re.search(r"X =(.*)",text): #layout Inpijn CPT 1
                    new_file = re.search(r"Sondering:(.*)", text).group().split()[-1]
                    new_file = os.path.join(dirpath, new_file+".pdf")
                    try:
                        os.rename(current_file, new_file)                
                    except:
                        new_file = re.search(r"Sondering:(.*)", text).group().split()[-1]
                        print(f"PDF: {file} \tID: {new_file} is skipped")
                elif re.search(r"X:(.*)",text): #layout Inpijn CPT 2
                    new_file = re.search(r"Sondering:(.*)", text).group(1).strip()
                    new_file = os.path.join(dirpath, new_file+".pdf")
                    os.rename(current_file, new_file)

os._exit()
#To complicated search below
#Properties to search for
name = []
points = []
xcos = []
ycos = []
# zcos = []

for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        if os.path.splitext(file)[1].upper() == '.PDF':		#SEARCH FOR FILES WITH GIVEN EXTENSION:
            name.append(file.split("\\")[-1])
            # Open the PDF file using pdfplumber
            with pdfplumber.open(os.path.join(dirpath, file)) as pdf:
              # Read first page of the PDF
              page = pdf.pages[0]
              # Extract the text from the page
              text = page.extract_text()
              # Use the regex search function to find the string in CPT plotted in multiple layouts
              if re.search(r"X =(.*)",text): #layout 1
                  points.append(re.search(r"Sondering:(.*)", text).group().split()[-1])
                  xcos.append(re.search(r"X =(.*)",text).group().split()[-1].replace(".",""))
                  ycos.append(re.search(r"Y =(.*)",text).group().split()[-1].replace(".",""))
              elif re.search(r"X:(.*)",text): #layout 2
                  points.append(re.search(r"Sondering:(.*)", text).group(1).strip())    
                  xcos.append(re.search(r"X:(.*)",text).group(1).split()[0])
                  ycos.append(re.search(r"Y:(.*)",text).group(1).split()[0])
              # zcos.append(re.search(r"MAAIVELD =(.*)",text))             
              # xcos.append(re.search(r"X =(.*)",text).group().split()[-1]))
              # ycos.append(re.search(r"Y =(.*)",text).group().split()[-1]))
              # zcos.append(re.search(r"maaiveld = N.A.P. (.*)",text))
              # Use the regex search function to find the string in Borehole
              elif re.search(r"Boring:(.*)", text):
                  points.append(re.search(r"Boring:(.*)", text).group(1).split()[0])
                  xcos.append(re.search(r"x-coordinaat(.*)",text).group().split()[-1].replace(",","."))
                  ycos.append(re.search(r"y-coordinaat(.*)",text).group().split()[-1].replace(",","."))
              else:
                  points.append("NA")
                  xcos.append("9999")
                  ycos.append("9999")

 
#Post processing:
for i in range(len(xcos)):
    points[i].strip()
    xcos[i] = xcos[i].split()[0]
    xcos[i] = xcos[i].replace('m',"")
    xcos[i] = float(xcos[i].replace(",","."))
    ycos[i] = ycos[i].split()[0]
    ycos[i] = ycos[i].replace('m',"")
    ycos[i] = float(ycos[i].replace(",","."))
    
# Make dataframe and save csv:
data = {"ID": points,
        "X-coordinate": xcos,
        "Y-coordinate": ycos,
        # "Z-coordinate": zcos,
        "filename": name}

df = pd.DataFrame.from_dict(data)
df.to_csv(f'{path}\\Extracted data.csv', index=False)
