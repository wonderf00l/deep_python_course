def text_filter(file, keywords):
    with open(file, 'r', encoding='UTF-8') as text:
        return [
            string.rstrip('\n') for string in text
            for word in keywords
            if word.lower() in string.lower().split()
        ]


print(text_filter('some_text.txt', ['hello', 'роза', '123']))
print(text_filter('some_text_1.txt', ['hello', 'роза', '123']))
