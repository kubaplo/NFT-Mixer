import os, random

class Mixer:
    def __init__(self):
        self.data = None
        self.total_images = None
        self.possible_combinations = None
        self.components_path = None
        self.exceptions_path = None
        self.rarity_filename = None
        self.current_image = None

    def fetch_data(self):
        self.data = {}
        self.total_images = 0
        self.possible_combinations = 1
        with os.scandir(self.components_path) as scan:
            for file in scan:
                if file.is_dir():
                    self.data[file.name] = []
                    with os.scandir(file.path) as subscan:
                        for subfile in subscan:
                            if subfile.is_file() and subfile.name.split('.')[-1].lower() == 'png':
                                self.data[file.name].append(subfile.name)
                                self.total_images += 1

                    if self.data[file.name]:
                        self.possible_combinations *= len(self.data[file.name])

        if not self.total_images:
            self.possible_combinations = 0