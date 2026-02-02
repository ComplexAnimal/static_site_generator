def extract_title(markdown):
    lines = markdown.split("\n")
    title = None
    for line in lines:
        if line[:2] == "# ":
            title = line[2:].strip()
            break
    if not title:
        raise Exception("Error: No h1 heading found")
    else:
        return title