from utils import get_s3_client
import os
from tkinter.filedialog import askopenfilename

def upload_file_s3(file_path = None) -> str:
    #return file_name, mostly for clean up purposes.
    try:
        if file_path == None:
            file_path = askopenfilename()
        _, file_name = os.path.split(file_path)

        s3 = get_s3_client()
        s3.upload_file(file_path, "ohio-rekog", file_name)
        print("Successfully upload: {", file_name,"}")
        return file_path, file_name
    except Exception as ex:
        print(str(ex))
        return "fail"

def delete_file_s3(file_name: str) -> bool:
    try:
        s3 = get_s3_client()
        s3.delete_object(Bucket = "ohio-rekog", Key = file_name)
        return True
    except Exception as ex:
        print(str(ex))
        return False