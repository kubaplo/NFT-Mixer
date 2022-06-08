import os, random
from exceptions import ComponentsPathError, LayersOrderFileError, ExceptionsFileError, RarityFileError
from PIL import Image

class Mixer:
    def __init__(self):
        self.data = None
        self.skipped_data = None
        self.total_images = None
        self.skipped_total_images = None
        self.possible_combinations = None
        self.components_path = None
        self.layers_order_path = None
        self.exceptions_path = None
        self.rarity_filename = None
        self.current_image = None
        self.current_traits = {}
        self.image_size = (1024, 1024) # Default value

    def get_absolute_path(self, path):
        return self.components_path + '/' + path

    def fetch_data(self):
        self.data = {}
        self.skipped_data = {}
        self.current_image = None
        self.current_traits = {}
        self.load_layers_order()
        self.load_components_directory()
        self.get_image_size()

    def load_components_directory(self):
        self.total_images = 0
        self.skipped_total_images = 0
        self.possible_combinations = 1
        try:
            with os.scandir(self.components_path) as scan:
                for file in scan:
                    if file.is_dir():
                        with os.scandir(file.path) as subscan:
                            for subfile in subscan:
                                if subfile.is_file() and subfile.name.split('.')[-1].lower() == 'png':
                                    if file.name in self.data:
                                        self.data[file.name].append(subfile.name)
                                        self.total_images += 1
                                    else:
                                        self.skipped_data[file.name].append(subfile.name)
                                        self.skipped_total_images += 1

                        if file.name in self.data and self.data[file.name]:
                            self.possible_combinations *= len(self.data[file.name])

        except:
            raise ComponentsPathError

        if not self.total_images:
            self.possible_combinations = 0

    def load_layers_order(self):
        dirs = []
        with os.scandir(self.components_path) as scan:
            for file in scan:
                if file.is_dir():
                    dirs.append(file.name)

        try:
            with open(self.layers_order_path, 'r') as file:
                order = file.read()

            order = order.split('\n')

        except:
            raise LayersOrderFileError

        for layer in order:
            if layer in dirs:
                self.data[layer] = []

        if not self.data:
            raise LayersOrderFileError

        for directory in dirs:
            if not directory in self.data:
                self.skipped_data[directory] = []

    def load_exceptions_file(self):
        pass

    def load_rarity_file(self):
        pass

    def get_image_size(self):
        image = None
        for directory in self.data:
            if len(self.data[directory]):
                image = self.data[directory][0]
                break

        if image:
            image = Image.open(self.get_absolute_path(f'{directory}/{image}'))
            self.image_size = image.size
            return image.size

    def generate(self):
        image = Image.new('RGBA', self.image_size, (0,0,0,0))
        for directory in self.data:
            item = random.choice(self.data[directory])
            layer = Image.open(self.get_absolute_path(f'{directory}/{item}'))
            image = Image.alpha_composite(image, layer)
            self.current_traits[directory] = item

        self.current_image = image

        return image