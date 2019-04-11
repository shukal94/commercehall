from flask import Flask, request, json
from PIL import Image, ImageDraw


app = Flask(__name__)
zoom = 3


@app.route("/", methods=['GET', 'POST'])
def draw_scheme():
    state_matrix = json.request
    state_dictionary = {'Not_Available': 'red',
                        'Available': 'green',
                        'Cashbox': 'yellow',
                        'Rack': 'blue',
                        'Done': 'black'}
    draw_image(state_matrix, state_dictionary)
    return "Done"


def draw_image(state_matrix, state_dictionary):
    img = Image.new('RGB', (700*zoom, 500*zoom), color='white')
    draw = ImageDraw.Draw(img)
    point_y = 0
    for point_rows in state_matrix:
        point_x = 0
        for point_columns in point_rows:
            if point_columns != 'Done':
                if point_columns == 'Available':
                    draw.rectangle(
                        (
                            point_y,
                            point_x,
                            (point_y + 1),
                            (point_x + 1)
                        ),
                        fill=state_dictionary[point_columns]
                    )
                else:
                    temp_img = Image.open(point_columns + '.jpg')
                    new_size = calculate_new_size(point_x,
                                                  point_y,
                                                  state_dictionary,
                                                  state_matrix)
                    temp_img = temp_img.resize((new_size[1], new_size[0]), Image.ANTIALIAS)
                    img.paste(temp_img, (point_y, point_x))
            point_x += 1
        point_y += 1
    img.save('Scheme.png')


def calculate_new_size(point_x, point_y, state_dictionary, state_matrix):
    furniture = state_dictionary[state_matrix[point_y][point_x]]
    temp_point_y = point_y
    temp_point_x = point_x
    detect_size = True
    while detect_size:
        if state_dictionary[state_matrix[temp_point_y][point_x]] != furniture:
            return [temp_point_x - point_x, temp_point_y - point_y]
        temp_point_x = point_x
        while state_dictionary[state_matrix[temp_point_y][temp_point_x]] == furniture:
            state_matrix[temp_point_y][temp_point_x] = 'Done'
            temp_point_x += 1
        temp_point_y += 1


if __name__ == '__main__':
    app.run()
