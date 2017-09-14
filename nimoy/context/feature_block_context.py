class FeatureBlock:
    def __init__(self, block_type) -> None:
        super().__init__()
        self.block_type = block_type

    def __enter__(self):
        pass

    def __exit__(self, the_type, value, traceback):
        pass
