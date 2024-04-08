from pdfminer.high_level import extract_text
import pytesseract
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import cv2
import numpy as np
import pdfplumber
import os
import docx
import zipfile
from dotenv import load_dotenv
import asyncio
import time
from zipfile import is_zipfile
import logging

logger = logging.getLogger('name_des_loggers')
load_dotenv()


#Liest den Inhalt einer Textdatei und speichert jede Zeile als Element in einer Liste.
def lese_datei_in_liste(name):
    """
    Öffnet eine Textdatei und speichert jede Zeile als Element in einer Liste.

    :param name: Der Dateiname der zu öffnenden Datei.
    :return: Eine Liste, wobei jedes Element eine Zeile aus der Datei ist.
    """
    pfad = f"C:\\Users\\lowe\\OneDrive - Software AG\\Desktop\\BachelorArbeitTexte\\{name}.txt"
    try:
        with open(pfad, 'r', encoding='utf-8') as datei:
            zeilen = datei.readlines()
        return [zeile.strip() for zeile in zeilen]  # Entfernt Zeilenumbrüche und Leerzeichen am Anfang/Ende
    except FileNotFoundError:
        print(f"Die Datei {pfad} wurde nicht gefunden.")
        return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")   
        return []

#Extrahiert Text aus einer .docx-Datei.
def extract_Text_from_docx(docx_path):  
    doc = docx.Document(docx_path)
    page_text = []
    for paragraph in doc.paragraphs:
        page_text.append(paragraph.text)
    return '\n'.join(page_text)

#Extrahiert Bilder aus einer .docx-Datei.
def extract_images_from_docx(docx_path):
    ListOfImages=list()
    with zipfile.ZipFile(docx_path, 'r') as z:
        for file_info in z.infolist():
            if file_info.filename.startswith('word/media/'):
                image_data = z.read(file_info.filename)
                ListOfImages.append(image_data)
    return ListOfImages              

#Überprüft, ob eine PDF-Datei Vektorgrafiken enthält.
def contains_vector_graphics(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Vektorgrafiken sind im 'rects', 'curves', 'lines' etc. enthalten
            if page.rects or page.curves or page.lines:
                return True
    return False

#Bestimmt das wahrscheinlichste Profilbild aus einer Liste von Bildern.
def FindRealProfilePicture(ListOfImages):
    if ListOfImages==[]:
        return []
    AllPicsWithFaces=list()
    # Laden des vortrainierten Modells
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for img_bytes in ListOfImages:

        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            continue
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Gesichtserkennung, usw.
        except Exception as e:
            continue

        # Gesichter im Bild erkennen
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Prüfen, ob Gesichter gefunden wurden
        if len(faces) > 0:
            AllPicsWithFaces.append(img_bytes)
    if len(AllPicsWithFaces)==0:
        return ListOfImages[0]
    return AllPicsWithFaces[0]       



#Extrahiert Bilder aus einer PDF-Datei.
def ExtractImageInPdf(pdf_path):
    doc = fitz.open(pdf_path)
    ListOfImages=list()
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            ListOfImages.append(image_bytes)
    doc.close()
    return ListOfImages

#Schneidet das Gesicht aus Bildern aus.
def crop_face_from_image(images, output_path, padding_pixel=110):
    for i, image in enumerate(images):
        # Konvertiere PIL-Image in NumPy-Array
        image_np = np.array(image)
        # Konvertiere RGB zu BGR (OpenCV verwendet BGR statt RGB)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        #Lädt trainiertes modell
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=15, minSize=(30, 30))
        if len(faces) == 0:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for i, (x, y, w, h) in enumerate(faces):
            höhe, breite = image_bgr.shape[:2]
            x = max(0, x - padding_pixel)
            y = max(0, y - padding_pixel)
            w += 2 * padding_pixel
            h += 2 * padding_pixel
            face_image = image_bgr[y:y+h, x:x+w]
            
            # Erstelle den neuen Pfad
            new_output_path = os.path.join(output_path, "images", "ProfilPic.png")
            # Speichere das Bild im neuen Pfad
            cv2.imwrite(new_output_path, face_image)
            return

#Speichert Bilder aus einem gegebenen Datensatz.
def save_possible_images(images_data,PossiblePics):
    for i, image_data in enumerate(images_data):
        file_name = f"{PossiblePics}{i+1}.png"
        save_image(image_data, file_name)

# Speichert ein Bild basierend auf den Bilddaten.
def save_image(image_data, file_name):
    # Pfad zum Verzeichnis, in dem die Bilder gespeichert werden sollen
    image_directory = "/app/images"
    # Vollständiger Pfad zum Bild, einschließlich des Verzeichnisses
    full_path = os.path.join(image_directory, file_name)
    with open(full_path, "wb") as image_file:
        image_file.write(image_data)

#Verarbeitet Bilder aus einer .docx-Datei, um ein Profilbild zu identifizieren.
def process_docx_pic(docx_path):
    Pics = extract_images_from_docx(docx_path)
    ProfilPic = FindRealProfilePicture(Pics)
    ProfilPicPath=f"ProfilPic.png"
    if ProfilPic:
        save_image(ProfilPic,ProfilPicPath)

#Verarbeitet den Text einer PDF-Datei, optional mit OCR, falls der Text zu kurz ist.
def process_pdf_text(pdf_path):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD_PATH")
    
    POPLER_PATH=os.getenv("POPLER_PATH")

    # Extrahieren Sie den Text aus der PDF mit pdfminer
    pdf_text = extract_text(pdf_path).strip()
    if "ThisdocumentusesencryptionpoweredbyMicrosoftInformationProtection" in pdf_text.replace("\n", "").replace(" ",""):
        raise Exception("The Docutment is protected with encryption and cannnot be analyzed")
    #Wenn der Text eindeutig zu kurz ist soll OCR angewendet werden. 
    if len(pdf_text) <= 30:
        pdf_text=""
        #  mit PyMuPDF PDF-Datei öffnen
        
        images = convert_from_path(pdf_path,500,poppler_path=POPLER_PATH)

        for i in range(len(images)):
            # Wenden Sie OCR an, um Text zu erhalten
            text = pytesseract.image_to_string(images[i], lang='deu')
            pdf_text += text + '\n'  
    return pdf_text     
     
#Verarbeitet Bilder aus einer PDF-Datei, um ein Profilbild zu identifizieren.     
def process_pdf_pic(pdf_path):

    POPLER_PATH=os.getenv("POPLER_PATH")
    #wenn es ein nicht reines Bild-PDF ist
    if contains_vector_graphics(pdf_path):
        #Extrahieren des Bildes aus der PDF mit PyMuPDF
        ListOfImages=ExtractImageInPdf(pdf_path)
        if ListOfImages:
            #save_possible_images(ListOfImages,"PossiblePics")
            ProfilPic=FindRealProfilePicture(ListOfImages)
            
            ProfilPicPath=f"ProfilPic.png"
            if ProfilPic:
                save_image(ProfilPic,ProfilPicPath)
    else:
        images = convert_from_path(pdf_path,500,poppler_path=POPLER_PATH)
        crop_face_from_image(images,"")    


#Überprüft, ob eine Datei eine PDF ist.
def is_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(5)  # Lesen der ersten 5 Bytes
            return header == b'%PDF-'
    except IOError:
        print("Fehler beim Öffnen der Datei.")
        return False         


#Hauptfunktion. 
#Extrahiert den Text aus docx oder PDF- Dateien und lädt ihn in die Variable Text. 
#Extrahiert Text und speichert dieses
#Analysiert den Text asynchron durch GPT in verschiedenen Kategorien und gibt diese in einem Schlüssel-Werte-Paar aus.
def main():

    file_path = os.getenv("CV_FILE_PATH")

    #is it a docx or a pdf?
    if is_zipfile(file_path):
        Text=extract_Text_from_docx(file_path)
        process_docx_pic(file_path)    
    elif is_pdf(file_path):
        try:
            Text=process_pdf_text(file_path)
        except Exception as e:
            return e
        process_pdf_pic(file_path)
    else:
        pass
    return Text