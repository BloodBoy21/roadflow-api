def snake_to_camel(snake_str):
    return "".join(word.title() for word in snake_str.split("_"))
