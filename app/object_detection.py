import requests
import time
import os
import subprocess

current_directory = os.path.dirname(os.path.abspath(__file__))
captured_folder  = os.path.join(current_directory, "captured_frames")

def capture_and_send_frame():
    try:
        image_path = f"{captured_folder}/image.jpg"
        skip_frames = 20
        command = f"fswebcam -r 1920x1080 --no-banner -S {skip_frames} {image_path}"
        subprocess.run(command, shell=True, check=True)

        with open(image_path, 'rb') as f:
            image_data = f.read()

        files = {'file': (image_path, image_data, 'image/jpeg')}
        
        try:
            response = requests.post('https://object-detection-server-8irf.onrender.com/detect', files=files)
            print('Data sent to API, response:', response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data to API: {e}")

        if response.status_code == 200:
            print('Image sent succesfully!')
        else:
            print('Failed to send the image. Status code: ', response.status_code)

        # Sleep for 4 hours
        time.sleep(10)
    except Exception as e:
        print('Error occurred while capturing or sending the image: ', e)
