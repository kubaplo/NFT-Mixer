class ComponentsPathError(Exception):
    def __str__(self):
        return 'There was an error with selected components path!'

class LayersOrderFileError(Exception):
    def __str__(self):
        return 'There was an error with layers order file!'