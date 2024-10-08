import os, random, json
from exceptions import ComponentsPathError, LayersOrderFileError
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
        self.auto_generating = False
        self.auto_saving = False

    def get_absolute_path(self, path):
        return self.components_path + '/' + path

    def fetch_data(self):
        self.data = {}
        self.skipped_data = {}
        self.current_image = None
        self.current_traits = {}

        self.load_layers_order()
        self.load_exceptions_file()
        self.load_components_directory()
        self.load_rarity_files()
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
        self.exception_list = None
        try:
            with open(self.exceptions_path, 'r') as file:
                data = file.read()

            data = data.replace('\t', '')
            self.exception_list = json.loads(data)

        except:
            pass

    def load_rarity_files(self):
        self.rarity_levels = {}
        self.rarity_files = 0
        for directory in self.data:
            path = self.get_absolute_path(directory) + '/' + self.rarity_filename
            if os.path.isfile(path):
                try:
                    with open(path, 'r') as file:
                        data = file.read()
                    data = data.replace('\t', '')
                    data = json.loads(data)

                    self.max_rarity_level = 0
                    for level in data:
                        for item in level['items']:
                            self.rarity_levels[item] = int(level['weight'])
                            if int(level['weight']) > self.max_rarity_level:
                                self.max_rarity_level = int(level['weight'])

                    self.rarity_files += 1
                except:
                    pass

        if not self.rarity_levels:
            self.max_rarity_level = 1

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
        self.current_traits = {}
        image = Image.new('RGBA', self.image_size, (0,0,0,0))

        for directory in self.data:
            skip = False
            cleared_items = [*self.data[directory]]

            # Exclude disallowed combinations:
            if self.exception_list:
                for trait in self.current_traits:
                    for rule in self.exception_list:
                        for exception in rule:
                            if self.current_traits[trait] == exception:
                                for e in rule:
                                    if e[-1] == '/' and e[:-1] == directory:
                                        skip = True
                                        break
                                    if e + '.png' in cleared_items:
                                        cleared_items.remove(e + '.png')

            if not skip and cleared_items:
                weighted_items = {}
                for item in cleared_items:
                    weighted_items[item] = self.rarity_levels.get('.'.join(item.split('.')[:-1]), self.max_rarity_level)

                item = random.choices(list(weighted_items.keys()), list(weighted_items.values()), k=1)[0]

                layer = Image.open(self.get_absolute_path(f'{directory}/{item}'))
                image = Image.alpha_composite(image, layer)
                self.current_traits[directory] = '.'.join(item.split('.')[:-1])

            else:
                self.current_traits[directory] = 'none'

        self.current_image = image

        return image

    def save(self, path):
        last = 0
        with os.scandir(path) as scan:
            for file in scan:
                if file.is_file() and file.name.split('.')[-1].lower() == 'png':
                    try:
                        n = int('.'.join(file.name.split('.')[:-1]))
                        if n > last:
                            last = n
                    except:
                        pass

        self.current_image.save(f'{path}/{last+1}.png')

    def count_exception_rules(self):
        if self.exception_list != None:
            return len(self.exception_list)

    def get_weights_with_items(self):
        weights = sorted(set(self.rarity_levels.values()))
        result = {}
        for item in self.rarity_levels:
            for weight in weights:
                if self.rarity_levels[item] == weight:
                    result[weight] = result.get(weight, []) + [item]

        return result