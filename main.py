# main, this file extracts frames from a video capture and  
# then calls OCR (optical character recognition) script to collect data from frames.
from extract_frames import extract_frames
from OCR import OCR
import os



def main():
    # Define the input video path and the output folder for the extract function 

    video_path = 'AZ_data_616_00022_250408/clockwise_constant.mov'
    output_folder = 'extracted_frames'
    master_data_output_folder = "master_data_values.txt"

    extract_frames(video_path, output_folder)

    MASTER_OCR_magnitude_list = []
    MASTER_OCR_values_list    = []
    MASTER_DATA = []
    

    # List all files in the output folder
    image_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]

    # Loop through each image file and call OCR()
    for image_file in image_files:
        # Get the full path of the image
        image_path = os.path.join(output_folder, image_file)
        
        # Call the OCR function with the image path, save in temp list 
        frame_master_data_list, frame_OCR_mag_list, frame_OCR_values_list = OCR(image_path, "AZ")       #AZ processes AZ data, EL processes EL data

        #append data to master lists
        MASTER_DATA.append(frame_master_data_list)   #magnitudes and number values 
        MASTER_OCR_magnitude_list.append(frame_OCR_mag_list) #magnitude only 
        MASTER_OCR_values_list.append(frame_OCR_values_list) #number values only


    #print(MASTER_DATA) # prints combined magnitudes and numbers together
    item_print_count = 0000
    for item in MASTER_DATA:
        print("Frame: ",item_print_count, item) #prints a list of values for a given frame of data 
        item_print_count = item_print_count + 1
         
    #saves values into text file
    with open(master_data_output_folder, "w") as file:
        for item in MASTER_DATA:
            file.write(str(item))
            file.write("\n")











if __name__ == "__main__":
    main()