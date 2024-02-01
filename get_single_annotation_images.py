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
    unique_image_ids = []
    multiple_annotations_ids = []
    for annotation in json_contents["annotations"]:
        image_id = annotation["image_id"]
        if image_id in unique_image_ids:
            unique_image_ids.remove(image_id)
            multiple_annotations_ids.append(image_id)
        elif image_id not in multiple_annotations_ids:
            unique_image_ids.append(image_id)

    return set(unique_image_ids)


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


def get_subcategory_proportions(id_set: set | list, json_contents: dict) -> dict:
    """
    Returns the proportions of every img class within the single-class imgs
    :param set | list id_set: Set or list of image IDs to grab
    :param dict json_contents: Imported JSON contents
    :return dict: A descending sorted dict of image superclass as the key and proportion as the value
    """
    # Get image category name from "categories", "annotations" within annotations.json
    subcategory_props = dict()
    category_id_to_subcategory = {category["id"]: category["supercategory"] for category in json_contents["categories"]}

    for annotation in json_contents["annotations"]:
        image_id = annotation["image_id"]
        category_id = annotation["category_id"]

        if image_id in id_set:
            # Update supercategory_frequencies
            supercategory = category_id_to_subcategory[category_id]
            subcategory_props[supercategory] = subcategory_props.get(supercategory, 0) + 1
    
    for key, value in subcategory_props.items():
        subcategory_props[key] = value / len(id_set)
    
    subcategory_props = dict(sorted(subcategory_props.items(), key=lambda item: item[1], reverse=True))

    return subcategory_props


def generate_annotations_json_from_ids(id_set: set | list, json_contents: dict) -> dict:
    output_json = {"info": json_contents["info"],
                   "scene_annotations": json_contents["scene_annotations"],
                   "licenses": json_contents["licenses"], "categories": json_contents["categories"],
                   "scene_categories": json_contents["scene_categories"], "annotations": [],
                   "images": []}

    for image in json_contents["images"]:
        if image["id"] in id_set:
            output_json["images"].append(image)
    
    for annotation in json_contents["annotations"]:
        if annotation["image_id"] in id_set:
            output_json["annotations"].append(annotation)
            
    return output_json


if __name__ == "__main__":
    json_data = import_annotations("./data/annotations.json")
    image_ids = extract_image_ids(json_data)

    # Information about the number and ids of images with 1 annotation:
    # print(image_ids)
    # print(get_links(image_ids, json_data))

    # ------

    # Information about the proportions of super categories in one annotation images
    # print(get_subcategory_proportions(image_ids, json_data))

    # ------

    # Get the annotations_json file from one annotation image ids

    # print(generate_annotations_json_from_ids(image_ids, json_data))
    # correct_annotations = generate_annotations_json_from_ids(image_ids, json_data)
    # print(correct_annotations)