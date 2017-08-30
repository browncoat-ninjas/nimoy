import ast
import _ast


class ModuleTransformer(ast.NodeTransformer):
    def visit_Module(self, module_node):
        import_statements = ModuleTransformer._gather_all_import_statements(module_node)

        required_modules = ['unittest', 'nimoy']
        [ModuleTransformer._import_module_if_not_imported(module_node, import_statements, required_module) for
         required_module in required_modules]
        return module_node

    @staticmethod
    def _import_module_if_not_imported(module_node, import_statements, required_module):
        is_module_already_imported = ModuleTransformer._import_statements_include(import_statements, required_module)
        if not is_module_already_imported:
            ModuleTransformer._add_module_dependency(module_node, required_module)

    @staticmethod
    def _gather_all_import_statements(module_node):
        import_statements = [module_statement for module_statement in module_node.body if
                             isinstance(module_statement, _ast.Import)]
        return import_statements

    @staticmethod
    def _import_statements_include(import_statements, module_name):
        return any(ModuleTransformer._is_module_import_statement(import_statement, module_name) for import_statement in
                   import_statements)

    @staticmethod
    def _is_module_import_statement(import_statement, module_name):
        return any(import_name.name == module_name for import_name in import_statement.names)

    @staticmethod
    def _add_module_dependency(module_node, module_name):
        module_node.body.append(_ast.Import(names=[_ast.alias(name=module_name)]))
