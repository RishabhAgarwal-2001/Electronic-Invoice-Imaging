# Electronic-Invoice-Imaging

09/08/2020:

Added 3 new files...
1] image_cut_and_rejoin.py cuts up the columns and rejoins them with space in between
  Input taken at Line No. 16
  Output at Line No. 107
  
2] image_to_hocr.py small file right now but this is the file that has to be appended with the "/n" removal code

3] hocr_to_table.py takes Input at Line No. 9 and givves An Excel Sheet as output (Line No. 228)


08/08/2020:

Uploaded table_processing.py right now... Did not use Column Crops because OCR performs horribly on Column Crops.

Subtle points of beauty (If I may call it that...) is that top header is mostly preserved... And table data is also entered in some structured pattern.

In all my tests, atleast there was no jagged table... Some data gets misplaced but only because OCR clubs it with neighbours.

If you can figure out how OCR can be made to work on a small column strip I will be able to further enhance Table Extraction 
P.S. I tried padding it with thin layer, thich layer, white, black, no padding, increaing width, increasing height but OCR continuously performed bad on it.
