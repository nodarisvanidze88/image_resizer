from PIL import Image, ImageDraw
import shutil
import os

MODIFIED_IMAGES = 'modified_images'
UNRESIZABLE_IMAGES = 'unresizable_images'
TEST_IMAGES = 'test_images'
def main():
    source_path = initial_sources("Add the source folder path: ")
    destination_path = initial_sources("Add destination folder path: ")
    modified_path = folder_creator(destination_path,MODIFIED_IMAGES)
    unresizable_path = folder_creator(destination_path,UNRESIZABLE_IMAGES)
    test_path = folder_creator(destination_path,TEST_IMAGES)
    file_names = get_file_name_list(source_path)
    if len(file_names)==0:
        print('Foldershi ar aris suratebi jpg gafartoebit')
        main()
    current_width,current_height,crop_size,new_width,new_height = test_image_crop(source_path,test_path,file_names)
    for i in file_names:
        new_current_path = os.path.join(source_path,i)
        new_output_path = os.path.join(modified_path,i)
        ignored_images_path = os.path.join(unresizable_path,i)
        crop_and_resize_image(new_current_path,new_output_path,crop_size,(current_width,current_height),(new_width,new_height),mode='main',new_output=ignored_images_path)
    input()
    
def initial_sources(txt):
    while True:
        source_path = input(txt)
        check_folder = os.path.exists(source_path)
        if check_folder:
            return source_path
        else:
            print("Incorrect Path, add correctly")

def folder_creator(path, folder_name):
    folder_path = os.path.join(path,folder_name)
    check = os.path.exists(folder_path)
    if not check:
        os.makedirs(folder_path, exist_ok=True)
    return folder_path

def get_file_name_list(path, folder_name=""):
    source_folder = path if not folder_name else os.path.join(path,folder_name)
    return [file for file in os.listdir(source_folder) if os.path.isfile(
        os.path.join(source_folder,file)) and file.lower().endswith('.jpg')]

def get_source_image_specification():
    current_width = number_input_validator("Add current image width: ")
    current_height = number_input_validator("Add current image height: ")
    crop_size = number_input_validator("Add size of crop from top: ", current_height)
    new_width = number_input_validator("Add new image width: ")
    new_height = number_input_validator("Add new image height: ")
    return current_width,current_height,crop_size,new_width,new_height

def test_image_crop(input_path, output_path, image_list):
    while True:
        current_width,current_height,crop_size,new_width,new_height = get_source_image_specification()
        status = False
        for i in image_list:
            new_input_path = os.path.join(input_path,i)
            new_output_path = os.path.join(output_path,i)
            check = crop_and_resize_image(new_input_path,new_output_path,crop_size,(current_width, current_height),(new_width, new_height))
            if check:
                user = input("Naxe aba kaia?(ki/ara) ").lower()
                if user == 'ki':
                    status = True
                break
        
        if status:
            return current_width,current_height,crop_size,new_width,new_height
        else:
            print("Savaraudod zomebi romlebic sheiyvane amseti failebi ar arsebobs, cade tavidan")
                
def crop_and_resize_image(input_path, output_path, crop_height, current_sizes, new_size, mode="test", new_output=''):
    try:
        with Image.open(input_path) as img:
            width, height = img.size

            # Check image dimensions
            if current_sizes[0] != width and current_sizes[1] != height and mode == 'test':
                return False
            elif (current_sizes[0] != width or current_sizes[1] != height) and mode != 'test':
                shutil.copy(input_path, new_output)
                return False
            elif current_sizes[0] != width and current_sizes[1] != height and mode != 'test':
                return False

            # Add white rectangle instead of cropping
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (width, crop_height)], fill="white")

            # Resize the image
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path)

            if mode == "test":
                os.startfile(output_path)
                return True

            print(f"Image successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def number_input_validator(txt, test=0):
    while True:
        try:
            user = int(input(txt))
            if test!=0 and test < user:
                print('Crop size can not be more then image height')
                continue
        except ValueError:
            print("Add only numbers")
        else:
            return user
        
if __name__=='__main__':
    main()