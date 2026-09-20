from assessment_pipeline.parser_registry import (
    ParserRegistry,
)

registry = ParserRegistry()

print()

for extension in sorted(
    registry.supported_extensions
):
    print(
        extension,
        "->",
        type(
            registry.get_parser(
                extension
            )
        ).__name__,
    )
