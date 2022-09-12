from pyzbar.pyzbar import decode # https://pypi.org/project/pyzbar/
import cv2
import glob
import argparse
import os


def resize_cv_image(img,scale_percentage):
    '''
    resize_cv_image resizes OpenCV image by certain percentage 
    :img: source cv image
    :scale_percentage: how much to scale image (30 => 30% smaller image)
    :return: resized cv image
    '''
    width = int(img.shape[1] * scale_percentage / 100)
    height = int(img.shape[0] * scale_percentage / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def blur_cv_image(img,blur_ammount):
    '''
    blur_cv_image bluers OpenCV image
    :img: source OpenCV image
    :blur_ammount: how much to blur (for example 10)
    :return: blurred openCV image
    '''
    ksize = (blur_ammount, blur_ammount)
    return cv2.blur(img , ksize)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sorts images to folders based on first 2D/3D barcode found')
    parser.add_argument("-p", "--path", type=str, required=True, help='Where to look for images (example: images/*.jpg)')
    parser.add_argument("-z", "--zoom", type=int, required=True, help='How much should we Zoom read images (example: 30 => image will be resized to 30%% of orginal')
    args = parser.parse_args()
    try:
        unprocessed_files = glob.glob(args.path)
    except:
        print(f"Unable to read files from path:{args.path}")
        exit()
    print(f"Found {len(unprocessed_files)} to process")
    if not os.path.exists("output"):
        try:
            os.mkdir("output")
        except Exception as err:
            print("Unable to create output directory")
            print(err)
            exit()
    for file in unprocessed_files:
        print(f"Processing {file} - ",end="")
        try:
            img = cv2.imread(file)
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
        except Exception as err:
            print(f"\nError occured while trying to read in image {file}")
            print(err)
            exit()
        try:
            img = blur_cv_image(img,7)
            img = resize_cv_image(img,args.zoom)
            code = decode(img)
            if code == []:
                print("No barcode found")
                continue
            else:
                payload = code[0].data.decode()
                if not os.path.exists("output/"+payload):
                    try:
                        os.mkdir("output/"+payload)
                    except Exception as err:
                        print("Unable to create output directory output/{payload}")
                        print(err)
                        exit()
                print(payload)
                try:
                    filename = file.split("\\")[-1]
                    os.rename(file,"output/"+payload+"/"+filename)
                except Exception as err:
                    print("Unable to move file: {file}")
                    print(err)
                    exit()
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
        except Exception as err:
            print(f"\nError occured while trying to process image {file}")
            print(err)
            exit()
