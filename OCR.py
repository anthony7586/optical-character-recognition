# this is the main file for the program, functionality the program takles a video feed, slices it into frames, 
# then generates text data from the visual video.
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import cv2
import os

def remove_newlines(text):
    return text.replace('\n','')

def OCR(image_path, mode):
    #print("running main...") 

    # Path to your Tesseract installation (only required on Windows)
    # use the installer to download from the github. https://github.com/UB-Mannheim/tesseract/wiki
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows path

    # Open an image file
    image = Image.open(image_path)

    if image:
        print('image ', image_path, ' opened sucessfully.')

    # Convert to grayscale
    image = image.convert('L')

    image_wo_median_filter = image #this copy is to get the magnitude values


    # Apply thresholding (you can experiment with the threshold value)
    #image = image.point(lambda p: p > 190 and 255)
    # Apply a threshold to retain only pure white pixels (255)
    # Set all pixels that are 255 to 255 (white) and all others to 0 (black)
    image = image.point(lambda p: 255 if p > 220 else 0) # used to analyze numbers only 
    image_wo_median_filter = image.point(lambda p: 255 if p > 250 else 0) # used to analyze magnitudes only 

    # Optionally, apply noise reduction or smoothing, this makes th enumbers slightly skinnier making them harder to read. 
    # may be useful in another instance so wwill keep line below around
    image = image.filter(ImageFilter.MedianFilter(3)) # used to analyze numbers only 
    image = image_wo_median_filter.filter(ImageFilter.MedianFilter(3)) # used to analyze magnitudes only 

    # Define a Region of Interest (ROI) as a tuple: (x1, y1, x2, y2)
    # Example: Top-left corner (x1, y1) and bottom-right corner (x2, y2) of the bounding box, the video image feed is 1280x720 60fps 
    x1, y1 = 250, 136  # start coordinates for top-left AZ coarse text coordinates 
    x2, y2 = 500, 160  # start coordinates for bottom-right AZ course text coordinates 


    if mode == "AZ":
        #print ("executing AZ mode ")
        AZ_COURSE  = image.crop((x1+1, y1+2, x2, y2+2))           # Crop the image to the ROI 
        AZ_FINE    = image.crop((x1+1, y1 +20, x2, y2+22))
        AZ_SUM     = image.crop((x1+1, y1 +40, x2, y2+42))
        AZ_CRS_CMD = image.crop((x1+1, y1 +60, x2, y2+62))
        AZ_VOLTAGE = image.crop((x1+1, y1 +80, x2, y2+82))

        magnitude_AZ_COURSE  = image_wo_median_filter.crop((x1-60, y1,      x1+50, y2+5))           # Crop the image to the ROI to scan for sign + or - 
        magnitude_AZ_FINE    = image_wo_median_filter.crop((x1-60, y1 +18,  x1+50, y2+25))
        magnitude_AZ_SUM     = image_wo_median_filter.crop((x1-60, y1 +38,  x1+50, y2+45))
        magnitude_AZ_CRS_CMD = image_wo_median_filter.crop((x1-60, y1 +58,  x1+50, y2+65))
        magnitude_AZ_VOLTAGE = image_wo_median_filter.crop((x1-60, y1 +78,  x1+50, y2+85))

        #magnitude_AZ_COURSE.show()        #show to verify preper ROI magnitude values
        #magnitude_AZ_FINE.show()
        #magnitude_AZ_SUM.show()
        #magnitude_AZ_CRS_CMD.show()
        #magnitude_AZ_VOLTAGE.show()

        #AZ_COURSE.show()        #show to verify preper ROI for numerical values
        #AZ_FINE.show()
        #AZ_SUM.show()
        #AZ_CRS_CMD.show()
        #AZ_VOLTAGE.show()

        #preform ocr 
        AZ_COURSE_text   =   remove_newlines(pytesseract.image_to_string(AZ_COURSE    , config='outputbase digits'))      # Use config to extract only digits
        AZ_FINE_text     =   remove_newlines(pytesseract.image_to_string(AZ_FINE      , config='outputbase digits'))    # Use config to extract only digits
        AZ_SUM_text      =   remove_newlines(pytesseract.image_to_string(AZ_SUM       , config='outputbase digits'))   # Use config to extract only digits
        AZ_CRS_CMD_text  =   remove_newlines(pytesseract.image_to_string(AZ_CRS_CMD   , config='outputbase digits'))       # Use config to extract only digits
        AZ_VOLTAGE_text  =   remove_newlines(pytesseract.image_to_string(AZ_VOLTAGE   , config='outputbase digits'))       # Use config to extract only digits


        # Set Tesseract configurations
        custom_mag_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=+-'
        magnitude_AZ_COURSE_text  =  remove_newlines(pytesseract.image_to_string(magnitude_AZ_COURSE , config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_AZ_FINE_text    =  remove_newlines(pytesseract.image_to_string(magnitude_AZ_FINE   , config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_AZ_SUM_text     =  remove_newlines(pytesseract.image_to_string(magnitude_AZ_SUM    , config=custom_mag_config))  # Use config to extract only magnitude 
        magnitude_AZ_CRS_CMD_text =  remove_newlines(pytesseract.image_to_string(magnitude_AZ_CRS_CMD, config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_AZ_VOLTAGE_text =  remove_newlines(pytesseract.image_to_string(magnitude_AZ_VOLTAGE, config=custom_mag_config))  # Use config to extract only magnitude

        if len(magnitude_AZ_COURSE_text ) == 0: magnitude_AZ_COURSE_text  = '-'
        if len(magnitude_AZ_FINE_text   ) == 0: magnitude_AZ_FINE_text    = '-'
        if len(magnitude_AZ_SUM_text    ) == 0: magnitude_AZ_SUM_text     = '-'
        if len(magnitude_AZ_CRS_CMD_text) == 0: magnitude_AZ_CRS_CMD_text = '-'   
        if len(magnitude_AZ_VOLTAGE_text) == 0: magnitude_AZ_VOLTAGE_text = '-'   

        #print("\n\n")
        #print("mag list: ", OCR_magnitude_list)
        #print("value list: ", OCR_values_list)
        #print("\n\n")

        # Print or return the extracted text (numbers)
        #print("AZ COURSE:"   , magnitude_AZ_COURSE_text  , AZ_COURSE_text   )
        #print("AZ FINE:"     , magnitude_AZ_FINE_text    , AZ_FINE_text     )
        #print("AZ_SUM:"      , magnitude_AZ_SUM_text     , AZ_SUM_text      )    
        #print("AZ_CRS:"      , magnitude_AZ_CRS_CMD_text , AZ_CRS_CMD_text  )
        #print("AZ VOLTAGE:"  , magnitude_AZ_VOLTAGE_text , AZ_VOLTAGE_text  )

        # store values in list 
        OCR_values_list = [AZ_COURSE_text,AZ_FINE_text,AZ_SUM_text, AZ_CRS_CMD_text, AZ_VOLTAGE_text] 
        # store magnitude in arrary, magnitude must be in same order as OCR value list 
        OCR_magnitude_list = [magnitude_AZ_COURSE_text,magnitude_AZ_FINE_text,magnitude_AZ_SUM_text, magnitude_AZ_CRS_CMD_text, magnitude_AZ_VOLTAGE_text] 
        # Area of magnitude+data , example: [-num,+num,-num,+num,-num]
        master_data = [OCR_magnitude_list[0]+OCR_values_list[0],OCR_magnitude_list[1]+OCR_values_list[1],OCR_magnitude_list[2]+OCR_values_list[2],OCR_magnitude_list[3]+OCR_values_list[3],OCR_magnitude_list[4]+OCR_values_list[4]]





    if mode == "El":
        #print ("executing EL mode ")
        EL_COURSE  = image.crop((x1+1, y1 +100, x2, y2+102))
        EL_FINE    = image.crop((x1+1, y1 +120, x2, y2+122))
        EL_SUM     = image.crop((x1+1, y1 +140, x2, y2+142))
        EL_CRS_CMD = image.crop((x1+1, y1 +160, x2, y2+162))
        EL_VOLTAGE = image.crop((x1+1, y1 +180, x2, y2+185))

        magnitude_EL_COURSE  = image_wo_median_filter.crop((x1-60, y1 +98,  x1+50, y2+105))
        magnitude_EL_FINE    = image_wo_median_filter.crop((x1-60, y1 +118, x1+50, y2+125))
        magnitude_EL_SUM     = image_wo_median_filter.crop((x1-60, y1 +138, x1+50, y2+145))
        magnitude_EL_CRS_CMD = image_wo_median_filter.crop((x1-60, y1 +158, x1+50, y2+165))
        magnitude_EL_VOLTAGE = image_wo_median_filter.crop((x1-60, y1 +178, x1+50, y2+185))

        #magnitude_EL_COURSE.show()         #show to verify preper ROI magnitude values
        #magnitude_EL_FINE.show()
        #magnitude_EL_SUM.show()
        #magnitude_EL_CRS_CMD.show()
        #magnitude_EL_VOLTAGE.show()

        #EL_COURSE.show()       #display to verify proper ROI of numerical EL values
        #EL_FINE.show()
        #EL_SUM.show()
        #EL_CRS_CMD.show()
        #EL_VOLTAGE.show()

        #preform ocr 
        EL_COURSE_text  =   remove_newlines(pytesseract.image_to_string(EL_COURSE   , config='outputbase digits'))      # Use config to extract only digits
        EL_FINE_text    =   remove_newlines(pytesseract.image_to_string(EL_FINE     , config='outputbase digits'))    # Use config to extract only digits
        EL_SUM_text     =   remove_newlines(pytesseract.image_to_string(EL_SUM      , config='outputbase digits'))   # Use config to extract only digits
        EL_CRS_CMD_text =   remove_newlines(pytesseract.image_to_string(EL_CRS_CMD  , config='outputbase digits'))       # Use config to extract only digits
        EL_VOLTAGE_text =   remove_newlines(pytesseract.image_to_string(EL_VOLTAGE  , config='outputbase digits'))       # Use config to extract only digits

        magnitude_EL_COURSE_text  =  remove_newlines(pytesseract.image_to_string(magnitude_EL_COURSE , config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_EL_FINE_text    =  remove_newlines(pytesseract.image_to_string(magnitude_EL_FINE   , config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_EL_SUM_text     =  remove_newlines(pytesseract.image_to_string(magnitude_EL_SUM    , config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_EL_CRS_CMD_text =  remove_newlines(pytesseract.image_to_string(magnitude_EL_CRS_CMD, config=custom_mag_config))  # Use config to extract only magnitude
        magnitude_EL_VOLTAGE_text =  remove_newlines(pytesseract.image_to_string(magnitude_EL_VOLTAGE, config=custom_mag_config))  # Use config to extract only magnitude

        if len(magnitude_EL_COURSE_text ) == 0: magnitude_EL_COURSE_text  = '-'  
        if len(magnitude_EL_FINE_text   ) == 0: magnitude_EL_FINE_text    = '-'  
        if len(magnitude_EL_SUM_text    ) == 0: magnitude_EL_SUM_text     = '-'  
        if len(magnitude_EL_CRS_CMD_text) == 0: magnitude_EL_CRS_CMD_text = '-'
        if len(magnitude_EL_VOLTAGE_text) == 0: magnitude_EL_VOLTAGE_text = '-'

        #print("\n\n")
        #print("mag list: ", OCR_magnitude_list)
        #print("value list: ", OCR_values_list)
        #print("\n\n")

        # Print or return the extracted text (numbers)
        #print("EL_COURSE:"   , magnitude_EL_COURSE_text  , EL_COURSE_text   ) 
        #print("EL_FINE_text:", magnitude_EL_FINE_text    , EL_FINE_text     )   
        #print("EL_SUM:"      , magnitude_EL_SUM_text     , EL_SUM_text      )    
        #print("EL_CRS_CMD:"  , magnitude_EL_CRS_CMD_text , EL_CRS_CMD_text  )
        #print("EL_VOLTAGE:"  , magnitude_EL_VOLTAGE_text , EL_VOLTAGE_text  )

        # store values in list 
        OCR_values_list = [EL_COURSE_text, EL_FINE_text, EL_SUM_text,EL_CRS_CMD_text,EL_VOLTAGE_text]
        # store magnitude in arrary, magnitude must be in same order as OCR value list 
        OCR_magnitude_list = [magnitude_EL_COURSE_text, magnitude_EL_FINE_text, magnitude_EL_SUM_text,magnitude_EL_CRS_CMD_text,magnitude_EL_VOLTAGE_text]
        # Area of magnitude+data , example: [-num,+num,-num,+num,-num]
        master_data = [OCR_magnitude_list[0]+OCR_values_list[0],OCR_magnitude_list[1]+OCR_values_list[1], OCR_magnitude_list[2]+OCR_values_list[2], OCR_magnitude_list[3]+OCR_values_list[3],OCR_magnitude_list[4]+OCR_values_list[4]]

    

 
    return master_data , OCR_magnitude_list, OCR_values_list
    



    




if __name__ == "__main__":
    OCR()