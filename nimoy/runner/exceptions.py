class InvalidFeatureBlockException(Exception):
    def __init__(self, spec_metadata, feature_name, block_ast_node, message, *args) -> None:
        super().__init__(*args)
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name
        self.block_ast_node = block_ast_node
        self.message = message
