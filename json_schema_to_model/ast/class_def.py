import ast

from json_schema_to_model import json_schema
from json_schema_to_model.json_schema.utils import convert_schema_id_to_name
from .types import AstName, convert_json_schema_type_to_ast_name


def create_class_def(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    Create a class definition AST object
    """

    assert schema.id is not None
    name = convert_schema_id_to_name(schema.id)

    if schema.allOf:
        return _create_class_def_using_all_of(schema)

    class_def = ast.ClassDef(
        bases=[AstName.TypedDict],
        body=[],
        decorator_list=[],
        keywords=[],
        name=name,
    )

    for k, v in schema.properties.items():
        type_value = _get_type_value(v)

        annotation: ast.Name | ast.Subscript
        if k in schema.required:
            annotation = type_value
        else:
            annotation = ast.Subscript(
                slice=type_value,
                value=AstName.NotRequired,
            )

        prop_def = ast.AnnAssign(
            annotation=annotation,
            simple=1,
            target=ast.Name(id=k),
        )

        class_def.body.append(prop_def)

    return class_def


def _create_class_def_using_all_of(
    schema: json_schema.types.ObjectSchema,
) -> ast.ClassDef:
    """
    If an object schema uses the `allOf` keyword, then use multiple inheritence
    for all of the refs in `allOf`.

    This solution is not fully JSON Schema compliant. For example, it won't
    support schemas that specify both `allOf` and `required`:

    ```
    {
        "id": "#Foo",
        "type": "object",
        "allOf": [{"$ref": "Bar"}, {"$ref": "Baz"}],
        "required": ["name"]
    }
    ```

    The only way to support using both `allOf` and `required` is to stop using
    multiple inheritence and merge the schemas before creating the ClassDef.
    This can be done but would take some work.
    """

    assert schema.allOf is not None
    assert schema.id is not None

    bases = [
        ast.Name(id=convert_schema_id_to_name(s.ref)) for s in schema.allOf.__root__
    ]

    return ast.ClassDef(
        bases=bases,
        body=[ast.Pass()],
        decorator_list=[],
        keywords=[],
        name=convert_schema_id_to_name(schema.id),
    )


def _get_type_value(
    schema: json_schema.types.Schema,
) -> ast.Name | ast.Subscript:
    type_value: ast.Name | ast.Subscript

    if isinstance(schema, json_schema.types.ArraySchema):
        type_value = _create_list(schema)
    elif isinstance(schema, json_schema.types.AllOfSchema):
        raise NotImplementedError()
    elif isinstance(schema, json_schema.types.AnyOfSchema):
        type_value = _create_union(schema.anyOf.__root__)
    elif isinstance(schema, json_schema.types.Ref):
        type_value = ast.Name(id=convert_schema_id_to_name(schema.ref))
    else:
        if json_schema.types.is_enumable_schema(schema):
            type_value = _create_literal_union(schema)
        else:
            type_value = convert_json_schema_type_to_ast_name(schema.type)

    return type_value


def _create_list(schema: json_schema.types.ArraySchema) -> ast.Subscript:
    """
    Create a `list` AST object
    """

    slice: ast.Name | ast.Subscript
    if len(schema.items) == 0:
        raise Exception("empty array items")
    if len(schema.items) == 1:
        subschema = schema.items[0]

        if isinstance(subschema, json_schema.types.AllOfSchema):
            raise NotImplementedError()
        elif isinstance(subschema, json_schema.types.AnyOfSchema):
            raise NotImplementedError()
        elif isinstance(subschema, json_schema.types.Ref):
            slice = ast.Name(id=convert_schema_id_to_name(subschema.ref))
        else:
            slice = convert_json_schema_type_to_ast_name(subschema.type)
    else:
        slice = _create_union(schema.items)

    return ast.Subscript(
        slice=slice,
        value=AstName.list,
    )


def _create_literal_union(
    schema: json_schema.types.EnumableSchema,
) -> ast.Subscript:
    """
    Create a `Literal` AST object
    """

    assert schema.enum is not None

    dims: list[ast.Constant] = []
    for member in schema.enum:
        dims.append(ast.Constant(value=member))

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=AstName.Literal,
    )


def _create_union(schemas: list[json_schema.types.Schema]) -> ast.Subscript:
    """
    Create a `Union` AST object
    """

    dims: list[ast.Name] = []
    for schema in schemas:
        if isinstance(schema, json_schema.types.AllOfSchema):
            raise NotImplementedError()
        elif isinstance(schema, json_schema.types.AnyOfSchema):
            raise NotImplementedError()
        elif isinstance(schema, json_schema.types.Ref):
            dims.append(ast.Name(id=convert_schema_id_to_name(schema.ref)))
        else:
            dims.append(convert_json_schema_type_to_ast_name(schema.type))

    return ast.Subscript(
        slice=ast.Tuple(dims=dims),
        value=AstName.Union,
    )
