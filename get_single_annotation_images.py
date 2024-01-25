import json
from pathlib import Path
from typing import List

def import_annotations(file_path: str) -> dict:
    """
    Import annotations from a JSON file
    :param str file_path: Path to COCO annotations JSON file
    :return dict: JSON data imported into dictionary
    """
    json_file = Path(file_path)
    with open(json_file) as annotations:
        json_contents = json.load(annotations)

    return json_contents

def extract_image_ids(json_contents: dict) -> set:
    """
    Grabs IDs of images with only one annotation
    :param dict json_contents: Imported COCO JSON data
    :return set: Set of IDs of images that only have one image
    """
    image_ids = []
    for annotation in json_contents["annotations"]:
        image_id = annotation["image_id"]
        if image_id in image_ids:
            image_ids.remove(image_id)
        else:
            image_ids.append(image_id)

    return set(image_ids)


def get_links(id_set: set | list, json_contents: dict) -> List[tuple]:
    """
    Gets the links associated with images in an ID set or list
    :param set | list id_set: Set or list of image IDs to grab
    :param dict json_contents: Imported JSON contents
    :return List[tuple]: A list of tuples in the format (jpg_link, png_link)
    """
    images = []
    for image in json_contents["images"]:
        if image["id"] in id_set:
            jpg_image = image["flickr_640_url"]
            png_image = image["flickr_url"]
            images.append((jpg_image, png_image))

    return images


if __name__ == "__main__":
    json_data = import_annotations("./data/annotations.json")
    image_ids = extract_image_ids(json_data)
    print(image_ids)
    print(get_links(image_ids, json_data))
