# TACO Dataset Filtering
A small set of tools to filter the [TACO](https://paperswithcode.com/dataset/taco) image set for waste recognition.

# Functionality
##### `import_annotations(file_path: str) -> dict` </br>
Imports annotations from an `annotations.json` file in the format of the TACO dataset and [COCO data format](https://cocodataset.org/#format-data).</br>
Provide file path to `annotations.json` and returns Python dictionary of imported JSON contents.

----

##### `extract_image_ids(json_contents: dict) -> set` </br>
Creates a set of image IDs present in the json_contents of `annotations.json` which only have one annotation.

----

##### `get_links(id_set: set | list, json_contents: dict) -> List[tuple]` </br> 
Gets the links for a provided set or list of image IDs from the json_contents of the `annotations.json` file. Can be used for downloading images for batches or for confirming that only images with one piece of trash in them have been filtered.

----

##### `get_subcategory_proportions(id_set: set | list, json_contents: dict) -> dict` </br>
Gets the proportions of each subcategory (type of trash) given a set of image IDs and the json_contents of `annotations.json`. </br>

----

#### `generate_annotations_json_from_ids(id_set: set | list, json_contents: dict) -> dict` </br>
Creates a new Python dictionary following the scheme of `annotations.json` which only contains images whos IDs are given in the id_set. </br>
This can be used to build an `annotations.json` file with only single annotation images.

----

Made for [ZotBins](https://zotbins.github.io/)

<img src="https://github.com/theNatePi/TACO-Dataset-Filtering/assets/78774649/8ba1bc12-8997-43e3-b714-43d94b04e26b" alt="ZotBins Logo" width="120" color="white"/>
