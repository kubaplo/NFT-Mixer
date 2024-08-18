# Preview
NFT Mixer allows to randomly merge image layers to create unique pictures:

![Initial screen with directory selection](/demo/1.gif)

# Requirements
This project uses `PyQt5` library for UI and `pillow` for image-related operations. Install these packages with the following command:
```
pip install PyQt5 pillow
```

# Usage

After starting `nftmixerapp.py` you will be asked to provide 4 directories with all of the necessary configuration files.

![Initial screen with directory selection](/demo/1.png)

### Structure of directory with components (step 1):
* components (folder that you will select in "step 1")
  * layer1
    * item11.png
    * item12.png
    * ...
  * layer2
    * item21.png
    * item22.png
    * ...
  * ...

### Content of `layers.json` file (step 2):
`layers.json` file contains the order of layers in which they should be placed on top of each other. Each layer should be the exact name of the folder from the previous step, layers should be separated by new lines. This file could look like this:
```
layer1
layer2
final-top-layer
```

### Content of `exceptions.json` file (step 3, optional):
This file defines which layers and items can't go together. Item names should be unique among all layers for this feature to work properly. The file should contain one list which will hold multiple sublists - every sublist is a separate exception rule. Example content of `exceptions.json` file:
```
[
  ["item11", "item22"],
  ["item12, "item21"]
]
```
The above rule means that item11 won't appear alongside item22 and item12 won't appear with item21.
You can also specify a directory in the exception rule. Directory must end with slash "/":
```
[
  ["item11", "layer2/"]
]
```
This rule means that when item11 will be randomly chosen then layer2 will be omitted. It is useful in scenarios where some items don't play well with certain layers.

### Content of `rarity.json` files (step 4, optional):
`rarity.json` file should be placed in each layer directory. It must contain a list of dictionaries, in the following format:
```
[
	{"weight": 2, "items": ["item11", "item12"]},
	{"weight": 1, "items": ["item-rare13"]}
]
```
The `weight` parameter could be any integer. The bigger the integer the higher the probability for specified items to be randomly chosen.

After this initial configuration you will be able to see some statistics and generate NFTs, either manually or automatically:

![Dashboard](/demo/2.png)
