from nimoy.ast_tools.feature_blocks import WHEN, THEN


class FeatureBlock:
    def __init__(self, block_type, thrown_exceptions) -> None:
        super().__init__()
        self.block_type = block_type
        self.thrown_exceptions = thrown_exceptions

    def __enter__(self):
        pass

    def __exit__(self, the_type, value, traceback):
        if self.block_type == WHEN and the_type:
            self.thrown_exceptions.append((the_type, value, traceback))
            return True
        if self.block_type == THEN and not the_type and self.thrown_exceptions:
            last_thrown_exception = self.thrown_exceptions.pop()
            if last_thrown_exception:
                raise last_thrown_exception[0](last_thrown_exception[1]).with_traceback(last_thrown_exception[2])

        return None
