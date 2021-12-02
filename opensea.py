#!/bin/env python3

# importing os module
import os
import requests
import shutil # to save it locally
from tenacity import retry, wait_exponential, TryAgain


def mkdir_p(path):
    try:
        # similar to `mkdir -p` in bash
        # makedirs for recursion; exist_ok = True for no error if dir exists
        os.makedirs(path, exist_ok = True) 
    except OSError as error:
        print("Directory '%s' can not be created" % directory)



@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def get_addresses_from_opensea_collection(collection="degenimals", offset=0, limit=1):
    try:
        url = f"https://api.opensea.io/api/v1/assets?order_direction=desc&collection={collection}&offset={offset}&limit={limit}"
        response = requests.get(url)
        rj = response.json()
    except Exception as e:
        raise TryAgain
    return rj

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def get_image_from_url(image_url,image_pathname, ext="jpg"):
    try:
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(image_pathname + f".{ext}",'wb') as f:
                shutil.copyfileobj(r.raw, f)
                print("Avatar image saved")
            f.close
    except Exception as e:
        raise TryAgain

def main():
    mkdir_p("assets/image")
    mkdir_p("assets/metadata")

    for i in range(10):
        json = get_addresses_from_opensea_collection(collection="degenimals", offset=i, limit=1)
        name = json["assets"][0]["name"]
        print(f"Found Degenimal: {name}!")

        metadata_path = os.path.join("assets/metadata",name + ".json")
        # if metadata exists, skip
        if not os.path.exists(metadata_path):
            with open(metadata_path,"w") as f:
                f.write(str(json))
            f.close()
            print("Metadata saved")
        else:
            print("Metadata exists, skipped...")

        image_path = os.path.join("assets/image",name)
        # if asset image already exists, skip
        if not os.path.exists(image_path):
            image_url = json["assets"][0]["image_url"]
            get_image_from_url(image_url,image_path)
        else:
            print("Avatar image exists, skipped...")
        
        print()
            

if __name__ == "__main__":
    main()
