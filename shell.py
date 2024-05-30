import mini

while True:
    text = input('mini > ')
    result, error = mini.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)