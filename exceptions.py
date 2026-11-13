class EmptySoupError(Exception):
    def __init__(self, class_name: str):
        self.message = (
            f"The {class_name} soup is empty! "
            f"It seems like the website did not want to share the soup..."
        )
        super().__init__(self.message)