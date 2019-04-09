from flask import Flask, request, json
from PIL import Image, ImageDraw


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def make_matrix():
    a = request.json
    dict = {'Not_Available': 'red', 'Available': 'green', 'Cashbox': 'yellow', 'Rack': 'blue'}
    img = Image.new('RGB', (1400, 1000), color='white')
    draw = ImageDraw.Draw(img)
    pointer_y = 0
    zoom = 2
    for point_rows in a:
        pointer_x = 0
        for point_columns in point_rows:
            if pointer_x>200\
                    and pointer_x<240\
                    and pointer_y>200\
                    and pointer_y<210:
                point_columns = 'Cashbox'
            draw.rectangle(
                (
                    (pointer_x)*zoom,
                    (pointer_y)*zoom,
                    (pointer_x+1)*zoom,
                    (pointer_y+1)*zoom
                ),
                fill=dict[point_columns]
            )
            if point_columns == 'Cashbox':
                temp_pointer_x = pointer_x
                temp_pointer_y = pointer_y
                size = [0,0]
                while a[temp_pointer_x][temp_pointer_y] == point_columns:
                    size[1] += 1
                    temp_pointer_y += 1
                temp_pointer_y = pointer_y
                while a[temp_pointer_x][temp_pointer_y] == point_columns:
                    size[0] += 1
                    temp_pointer_x += 1
            pointer_x = pointer_x+1
        pointer_y = pointer_y+1
    img.save('Схема.png')
    return json.jsonify(size)


if __name__ == '__main__':
    app.run()
