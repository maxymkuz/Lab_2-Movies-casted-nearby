def parser(location, ipt_year, ipt_country):
    """str -> dict
    Returns a dict with location as a key and title as a value
    """
    res = {}
    with open(location, 'r', encoding="utf-8", errors='ignore') as f:
        for line in f:
            line = line.strip().split('\t')

            for l in range(len(line[0])):
                # Checking if the year is valid
                if line[0][l] == '(' and line[0][l + 1: l + 5].isdigit():
                    year = int(line[0][l + 1: l + 5])

                    if year != ipt_year:
                        break
                    title = line[0][:l]
                    location = line[-2] if line[-1][-1] == ')' else line[-1]
                    if location.endswith(ipt_country):
                        res[location] = res.get(location, []) + [title]
                    break
        lst = [[key] + res[key] for key in res]
        lst.sort(key=lambda x: len(x), reverse=True)
        return lst
