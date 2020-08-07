# Electronic-Invoice-Imaging

Uploaded table_processing.py right now... Did not use Column Crops because OCR performs horribly on Column Crops.

Subtle points of beauty (If I may call it that...) is that top header is mostly preserved... And table data is also entered in some structured pattern.

In all my tests, atleast there was no jagged table... Some data gets misplaced but only because OCR clubs it with neighbours.

If you can figure out how OCR can be made to work on a small column strip I will be able to further enhance Table Extraction 
P.S. I tried padding it with thin layer, thich layer, white, black, no padding, increaing width, increasing height but OCR continuously performed bad on it.
