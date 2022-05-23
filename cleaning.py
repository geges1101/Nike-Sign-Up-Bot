import email


emails = []
emails_file = []

with open("results", "r") as f:
    while True:
        text = f.readline()
        if not text:
            break
        emails.append(text)

with open('emails', 'r') as f:
    while True:
        text = f.readline()
        if not text:
            break
        text = text.split(':')
        emails_file.append(text[0])

for _ in emails:
    for x in emails_file:
        if _ in x:
            emails_file.remove(x)


with open('emails', 'w') as f:
    for _ in emails_file:
        f.write(_)