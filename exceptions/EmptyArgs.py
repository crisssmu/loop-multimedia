
class EmptyArgs(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def empty_selection(path, index_moni, type_media):
        for arg in [path, index_moni, type_media]:
            if arg == -1:
                raise EmptyArgs("Todos los argumentos deben ser proporcionados")
    def empty_file(file_path):
        if not file_path:
            raise EmptyArgs("No hay ningun archivo o no has seleccionado uno")

    def empty_time(duration):
        if duration <= 0:
            raise EmptyArgs("Rellenar los campos de tiempo")