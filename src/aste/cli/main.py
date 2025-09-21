"""CLI interface for generating data structure code."""

import argparse
import sys
from typing import Any

from rich.console import Console

from aste.datastructures.factory import DataStructureFactory
from aste.utils.json_schema import infer_fields_from_json
from aste.utils.json_schema import load_json_from_file
from aste.utils.json_schema import load_json_from_url


console = Console()


def main() -> None:
    """
    Generate code for various Python data structures using AST.

    Examples
    --------
    >>> # From JSON file
    >>> # python -m aste.cli.main --json user.json --type dataclass
    >>> # From URL
    >>> # python -m aste.cli.main --url https://api.example.com/user --type pydantic
    >>> # Default example
    >>> # python -m aste.cli.main --type dataclass
    """
    parser = argparse.ArgumentParser(
        description="Generate Python data structures from JSON using AST."
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["typed_dict", "dataclass", "pydantic", "namedtuple", "attrs"],
        default="typed_dict",
        help="Type of data structure to generate",
    )
    parser.add_argument(
        "-n",
        "--name",
        default="GeneratedModel",
        help="Name of the generated class",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Path to JSON file",
    )
    parser.add_argument(
        "-u",
        "--url",
        help="URL to fetch JSON from",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (default: <classname>_<type>.py)",
    )
    args = parser.parse_args()

    json_data: dict[str, Any] | None = None
    if args.json:
        try:
            console.print(f"[cyan]Loading JSON from file: {args.json}[/cyan]")
            json_data = load_json_from_file(args.json)
        except FileNotFoundError:
            console.print(f"[red]Error: File not found: {args.json}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error loading JSON file: {e}[/red]")
            sys.exit(1)
    elif args.url:
        try:
            console.print(f"[cyan]Fetching JSON from URL: {args.url}[/cyan]")
            json_data = load_json_from_url(args.url)
        except Exception as e:
            console.print(f"[red]Error fetching JSON from URL: {e}[/red]")
            sys.exit(1)

    if json_data:
        fields = infer_fields_from_json(json_data)
        console.print(f"[green]Inferred {len(fields)} fields from JSON[/green]")
    else:
        # Default example fields
        console.print("[yellow]Using default example fields[/yellow]")
        fields = {"user_id": "int", "username": "str", "is_active": "bool"}

    class_name = args.name

    builder = DataStructureFactory.get_builder(args.type)
    generated_code = builder.build(class_name, fields)

    console.print("\n[bold cyan]Generated Code:[/bold cyan]")
    console.print(generated_code)

    output_filename = (
        args.output if args.output else f"{class_name.lower()}_{args.type}.py"
    )

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    console.print(f"\n[green]✓ Code saved to {output_filename}[/green]")


if __name__ == "__main__":
    main()
