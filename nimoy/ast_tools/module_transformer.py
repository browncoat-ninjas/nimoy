import ast
import _ast


class ModuleTransformer(ast.NodeTransformer):
    def visit_Module(self, module_node):
        import_statements = ModuleTransformer._gather_all_import_statements(module_node)
        is_unittest_already_imported = ModuleTransformer._import_statements_include_unittest(import_statements)

        if not is_unittest_already_imported:
            module_node.body.insert(0, _ast.Import(
                names=[_ast.alias(name='unittest')]
            ))
        return module_node

    @staticmethod
    def _gather_all_import_statements(module_node):
        import_statements = [module_statement for module_statement in module_node.body if
                             isinstance(module_statement, _ast.Import)]
        return import_statements

    @staticmethod
    def _import_statements_include_unittest(import_statements):
        return any(
            ModuleTransformer._is_unittest_import_statement(import_statement) for import_statement in import_statements)

    @staticmethod
    def _is_unittest_import_statement(import_statement):
        return any(import_name.name == 'unittest' for import_name in import_statement.names)
