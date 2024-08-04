from PIL import Image
import numpy as np


def resize_crop(img, w, h):
    """
    Scaling, centering and cropping the image 
    to the specified size (w, h)
    """
    img_w, img_h = img.size
    ratio = img_w / img_h
    if ratio > (w / h):
        new_w = int(h * ratio)
        img = img.resize((new_w, h))
        crop_x = round(new_w / 2 - w / 2)
        img = img.crop((crop_x, 0, crop_x + w, h))
    else:
        new_h = int(w / ratio)
        img = img.resize((w, new_h))
        crop_y = round(new_h / 2 - h / 2)
        img = img.crop((0, crop_y, w, crop_y + h))
    return img


def correct_filename(filename, default='png'):
    """
    Verify that the filename is valid:
    - if there is no extension in the end of the 
      filename, the default extension will be added;
    - if filename has unsupported extension, it will
      be replaced by the default extension.
    """
    # Set of all supported by PIL extensions
    supported = {ex[1:] for ex, f 
                 in Image.registered_extensions().items() 
                 if f in Image.SAVE}

    sep = filename.split('.')
    if len(sep) == 1 or sep[-1] not in supported:
        # If there is no extension or it is unsupported
        return f'{filename}.{default}'
    else:
        # If filename is valid
        return filename


def open_img(image_name):
    """
    image_name can be represented as a str (path to image)
    or as an Image.Image object
    """
    if isinstance(image_name, str):
        return Image.open(image_name)
    elif isinstance(image_name, Image.Image):
        return image_name
    else:
        assert False, 'Image must be defined as str or Image!'


def hide(source_img, 
         secret_img, 
         save_as=None, 
         visibility=2):
    """
    Hide secret image inside source image

    PARAMETERS
    ----------
    source_img : str or PIL.Image.Image
        path to source image (or PIL Image object)
        
    secret_img : str or PIL.Image.Image
        path to secret image (or PIL Image object)
        
    save_as : str or None
        path to save the result (if None, the 
        result will not be saved)
        
    visibility : int from 1 to 7
        how many low-order bits will be occupied 
        by the secret image
    """
    # Check visibility value
    error = 'visibility must be int from 1 to 7!'
    assert visibility in [*range(1, 8)], error
    
    # Loading images
    source = open_img(source_img)
    secret = resize_crop(open_img(secret_img), 
                         *source.size)

    # Hiding secret in source
    source = np.array(source) >> visibility << visibility
    secret = np.array(secret) >> (8 - visibility)
    result_img = Image.fromarray(source + secret)

    # Saving the result if necessary
    if isinstance(save_as, str):
        filename = correct_filename(save_as)
        result_img.save(f'{filename}')
        print(f'The result was saved in {filename}')

    return result_img


def unhide(image, 
           save_as=None, 
           visibility=2):
    """
    Exctract hidden image from given image

    PARAMETERS
    --–-------
    image : str or PIL.Image.Image
        path to image (or PIL Image object)
        
    save_as : str or None
        path to save the result (if None, the 
        result will not be saved)
        
    visibility : int from 1 to 7
        how many low-order bits will be occupied 
        by the secret image
    """
    # Check visibility value
    error = 'visibility must be int from 1 to 7!'
    assert visibility in [*range(1, 8)], error
    
    # Open and unhide
    hidden = np.array(open_img(image)) << (8 - visibility)
    hidden_img = Image.fromarray(hidden)

    # Saving the result if necessary
    if isinstance(save_as, str):
        filename = correct_filename(save_as)
        hidden_img.save(f'{filename}')
        print(f'The result was saved in {filename}')

    return hidden_img
    