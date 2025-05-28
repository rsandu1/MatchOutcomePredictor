import requests
from bs4 import BeautifulSoup

def fetch_grid_data_from_doc(doc_url):
    """
    Fetches and parses the table from the given Google Doc URL.
    Returns a dictionary with (x, y) keys and character values.
    """
    if "/edit" in doc_url:
        doc_url = doc_url.replace("/edit", "/export?format=html")
    elif "?usp=sharing" in doc_url:
        doc_url = doc_url.split("?")[0] + "/export?format=html"

    response = requests.get(doc_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    grid_map = {}
    max_x = max_y = 0

    for row in rows:
        cells = row.find_all(['td', 'th'])
        if len(cells) != 3:
            continue

        try:
            x = int(cells[0].text.strip())
            char = cells[1].text.strip()
            y = int(cells[2].text.strip())
        except ValueError:
            continue

        grid_map[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return grid_map, max_x, max_y


def print_grid(grid_map, max_x, max_y):
    """
    Prints the character grid from the given grid_map and dimensions.
    """
    for y in reversed(range(max_y + 1)):
        line = ''
        for x in range(max_x + 1):
            line += grid_map.get((x, y), ' ')
        print(line)


# Example usage:
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
grid_map, max_x, max_y = fetch_grid_data_from_doc(url)
print_grid(grid_map, max_x, max_y)
