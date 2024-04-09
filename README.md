# DataExtraction

Das Script extrahiert aus .docx- und allen gängigen PDF-Dateien sowohl den Text, als auch ein Profilbild. Hierbei werden alle Bilder durch eine KI von OpenCV auf Gesichter überprüft und das erste Bild als Profilbild gewertet. 

##Flussdiagramm der Datenextraktion:

![image](https://github.com/LorenzWenzel/DataExtraction/assets/73563833/01ccf414-4ff2-4ac0-ac86-faa0503536a9)



1.	**Docx für Textextraktion in .docx-Dateien**: Zum Extrahieren von Text kann python-docx das standardisierte Format von .docx-Dateien ausnutzen, um die Inhalte aus der document.xml herauszulesen (vgl. Abbildung 2). License: MIT Lizens (MIT)( python-docx · PyPI)
2.	**Pdfpblumber zum Erkennen von Vektorgrafiken in PDFs**: Diese Bibliothek ist in der Lage die komplexe Natur von PDFs zu durchdringen. Sie erkennt Rechtecke, Kurven und Linien innerhalb des PDF-Objekts, die auf das Vorhandensein von Vek-torgraphiken hinweisen. Lizens: MIT License (MIT) (GitHub - jsvine/pdfplumber: Plumb a PDF for detailed information about each char, rectangle, line, et cetera — and easily extract text and tables.) (pdfplumber · PyPI)
3.	**PyMuPDF (fitz) zum Extrahieren der Bilder in PDFs**: Diese Bibliothek kann Bil-der aus PDF-Dateien identifizieren und extrahieren. Lizens: GNU AFFERO GPL 3.0. (pdfplumber · PyPI)
4.	**Pdf2Image zum Konvertieren von PDF zu Bild**: Diese Bibliothek wird dazu ver-wendet PDF-Dateien in ein Bildformat zu konvertieren, welches von Python interpre-tiert und verarbeitet werden kann. Lizenz: MIT License (MIT). (pdf2image · PyPI)
5.	**Pytesseract für OCR**: Pytesseract ist eine Implementierung von Tesseract-OCR und extrahiert Text durch optische Zeichenerkennung (vgl. Abschnitt ‎2.3.2). Lizenz: Apache Software License (Apache License 2.0). (pytesseract · PyPI)
6.	**OpenCV (cv2) für Gesichtserkennung und Gesichtsausschnitt**: OpenCV nutzt das vortrainierte Modell „haarcascade_frontalface_default.xml“, um Gesichter identifi-zieren zu können. Dieses Modell ist in der Lage, verschiedene Gesichtsmerkmale in Bildern zu erkennen. Durch charakteristische Merkmale, wie Augen, Nase und Mund sollen mögliche Profilbilder klassifiziert werden können. (OpenCV: Cascade Classifier) Lizenz: Apache 2 License. (License - OpenCV)

