import ast

from nimoy.ast_tools.specs import SpecTransformer
from nimoy.runner.metadata import RunnerContext
from nimoy.runner.spec_finder import Location
from nimoy.specification import Specification


class SpecificationTransformerSpec(Specification):
    def where_methods_are_extracted_from_features(self):
        with given:
            spec_definition = """from nimoy.specification import Specification
            
class JimbobSpec(Specification):
    
    def my_feature(self):
        with setup:
            a = value_of_a
        
        with expect:
            a == 5
        
        with where:
            value_of_a = [5]
        
            """
            node = ast.parse(spec_definition, mode='exec')

        with when:
            found_metadata = []
            SpecTransformer(RunnerContext(), Location('some_spec.py'), found_metadata).visit(node)
        with then:
            len(node.body[1].body) == 2  # The where method should have been extracted to class level
            node.body[1].body[1].name == 'my_feature_where'
