from aiogram.utils.formatting import Pre, Text, Strikethrough


# возвращает форматированный текст вида Пользователь user: мой текст
def format_with_author(name, text, crossed=False):
    return Text(f"Пользователь {name}:\n", Pre(text)).as_kwargs() if not crossed else Text(
        Strikethrough(f"Пользователь {name}:\n"), Pre(text)).as_kwargs()
