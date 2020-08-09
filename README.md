# Electronic Invoice Imaging - jrs


USER GUIDE
=================================================================================
## 1) Installation:
Following are the Command Line Instructions to be run on a Linux Based OS to setup your system for the Software-
 ``` virtualenv venv ``` 
 ``` source venv/bin/activate ``` 
 ``` git clone https://github.com/RishabhAgarwal-2001/Electronic-Invoice-Imaging.git ```
 ``` pip install -r requirements.txt ```

## (2) Usage:
Navigate to “src” folder and type in the following command to test on a pdf of your choice-
``` python3 main.py -i "path/to/input/pdf" -o "path/to/output/spreadsheet ```

*************************************************************************
# WORKING OF THE LIBRARY

The input pdf is first converted to a “png” Image which is segmented into two parts based on the location of the table. One part contains the metadata while the other contains the table. A salient feature of our Implementation is that these 2 parts are then processed separately.

## (1) Handling MetaData - 
The MetaData is passed through the CLAHE Image Enhancement Algorithm. The Horizontal and Vertical lines in the enhanced Image are detected and the Image is segmented based on these lines. The main reason for choosing this step is to increase the Robustness of our software.
Each of the crops is passed through a text localizer which identifies local grouping of text. The Image is again cropped based on these smaller groups.
Each of these individual groups are then passed through the Tesseract-OCR engine. The text recognized by the OCR is first passed through a spell checker based on the model of “bag-of-words” and Levenith distance(edit distance). Potential keywords are then searched for in the recognized and rectified text. A Dictionary of key-value pairs is built based on these keywords. The identified fields are then filled into the spreadsheet.

## (2) Handling Table Data - 
Columns are detected in the Table. The image is split according to the individual columns and then re-combined with padding between the columns to form a new image with columns being space-separated. This step is performed to avoid cluttering of text and misidentification of data thereafter. 
The image is then passed through the Tesseract-OCR engine which returns a “.hocr” file. The “.hocr” file is then used to build the table based on the bounding boxes of the words identified. The header of the table is used to determine the columns. Data recognized by the OCR is then fed into a spreadsheet. 
Both of the spreadsheets are combined and presented to the user.

Salient Features
=================================================================================
Our Software does Justice to the theme of the Project- “Electronic Invoicing Using Image Processing”. It does not employ enormous Deep Learning models (Except for the OCR engine) and does not rely on large amounts of training data.
We do not expect the User to input any kind of “Template Format” or other Information about the pdf. Due to it’s programme structure, the Software is Robust enough to work on all Formats.
MetaData and Table of an invoice are different entities with a different structure and purpose. Acknowledging their difference, we process them independently. Thus, the amount or type of MetaData, it’s presence or absence thereof does not cause the table output to change or become Jagged, and vice versa.
Groups of words on multiple lines can also form a table entry, such as name/description of a product. We have tried to output this text in a single cell.
We assume the Excel Sheet generated will be used in further processing and data extraction/analysis. Hence, we have maintained a format for the MetaData. Information such as Shipping Address, GST Number, etc. will be filled in the same row/column each time irrespective of Template Format. 














Limitations and Bottlenecks
=================================================================================

1) For both the MetaData and the Table, the pre-processed Image is passed to the Tesseract-OCR engine. The OCR is in the critical path for all operations, hence, the output depends almost entirely on how well the OCR detects text from the Image.

2) This problem gets amplified when the OCR does not detect even a single letter from the name of the column. When column headers are skipped, the data of that column (if present and detected) does not have any place of its own, and gets merged with one of the neighbouring columns. This might cause a jagged table.

3) Quality of image has a profound effect on the quality of output. Though various pre-processing techniques have been applied, output still depends entirely on the quality of invoice.

Remarks
========================================================================

We believe we have stressed enough on the role of the accuracy of OCR on the output. However, for each invoice input, the table processing generates a file “output_hocr.html”.
If you think the final Excel Sheet generated by the Software is not up to the mark, and should you forgive our imprudence, we request you to open this file in any browser. This will help you get a better judgement of whether it is our Software that has erred you or the OCR.
