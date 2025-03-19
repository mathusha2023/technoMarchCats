from aiogram.utils.formatting import Pre, Text, Strikethrough


# используй ** перед результатом функции, чтобы сделать вывод единым текстом
def format_with_author(name, text, crossed=False):
    return Text(f"Пользователь {name}:\n", Pre(text)).as_kwargs() if not crossed else Text(
        Strikethrough(f"Пользователь {name}:\n"), Pre(text)).as_kwargs()
