import csv


def parser(location):
    """str -> dictres[location] = res.get(location, []) + [title]
    Returns a dict with location as a key and title as a value
    """
    res = []
    with open(location, 'r', encoding="utf-8", errors='ignore') as f:
        for line in f:
            line = line.strip().split('\t')

            for l in range(len(line[0])):
                # Checking if the year is valid
                if line[0][l] == '(' and line[0][l+1: l+5].isdigit():
                    year = int(line[0][l+1: l+5])

                    title = line[0][:l]

                    location = line[-2] if line[-1][-1] == ')' else line[-1]

                    res.append([title, year, location])
                    break

        return res


x = parser("locations.list")
print(x)


with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["location", "year", "title"])
    for i in range(len(x)):
        writer.writerow([i] + x[i])

