class InvalidMethodBlockException(Exception):
    def __init__(self, spec_metadata, method_name, block_ast_node, message, *args) -> None:
        super().__init__(*args)
        self.spec_metadata = spec_metadata
        self.method_name = method_name
        self.block_ast_node = block_ast_node
        self.message = message
