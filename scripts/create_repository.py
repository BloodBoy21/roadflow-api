import argparse
from pathlib import Path
from string import Template


MONGO_TEMPLATE = Template('''from .base import MongoRepository
from models.mongo.${model_snake} import ${model}, ${model}Base


class ${model}Repository(MongoRepository[${model}]):
    """Repository for managing ${model_snake} in MongoDB."""

    def __init__(self):
        super().__init__(collection="${collection}", model=${model})
''')

SQL_TEMPLATE = Template('''from .base import SQLRepository
from models.${model_snake} import ${model}Read


class ${model}Repository(SQLRepository[${model}Read]):
    """Repository for managing ${model_snake} in SQL."""

    def __init__(self):
        super().__init__(model=${model}Read,collection="${model}")
''')


def snake_case(name):
    import re

    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\\1_\\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\\1_\\2", s1).lower()


def generate_repo(model, repo_type):
    model_snake = snake_case(model)
    collection = model_snake + "s"

    if repo_type == "mongo":
        content = MONGO_TEMPLATE.substitute(
            model=model,
            model_snake=model_snake,
            collection=collection,
        )
        filepath = Path(f"repository/mongo/{model_snake}_repository.py")
    elif repo_type == "sql":
        content = SQL_TEMPLATE.substitute(
            model=model,
            model_snake=model_snake,
        )
        filepath = Path(f"repository/sql/{model_snake}_repository.py")
    else:
        raise ValueError("Repository type must be 'mongo' or 'sql'.")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content)
    print(f"✅ Generated: {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate repository file.")
    parser.add_argument(
        "--type",
        required=True,
        choices=["mongo", "sql"],
        help="Type of repository (mongo or sql)",
    )
    parser.add_argument(
        "--model", required=True, help="Name of the model (e.g., Workflow, User)"
    )
    parser.add_argument(
        "--collection",
        default=None,
        help="Collection name for MongoDB (optional, defaults to model name in snake_case)",
    )
    parser.add_argument(
        "--table",
        default=None,
        help="Table name for SQL (optional, defaults to model name)",
    )

    args = parser.parse_args()
    generate_repo(args.model, args.type)
