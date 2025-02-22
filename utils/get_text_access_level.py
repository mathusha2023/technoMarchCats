def get_text_access_level(access_level):
    if access_level == 1:
        return "пользователь"
    elif access_level == 2:
        return "администратор"
    elif access_level == 3:
        return "супер-админ"
