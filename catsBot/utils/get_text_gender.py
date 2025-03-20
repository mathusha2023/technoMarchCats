def get_text_gender(int_gender):  # 0 - мальчик, 1 - девочка, 2 - любой
    if int_gender == 0:
        return "мальчик"
    elif int_gender == 1:
        return "девочка"
    else:
        return "любой"
