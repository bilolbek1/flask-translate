from flask import Flask, request, render_template, url_for, jsonify
from translate import Translator
from cars import cars_list


app = Flask(__name__)


def tran(from_lan, to_lan, text):
    result = Translator(from_lang=from_lan, to_lang=to_lan)
    return result.translate(text)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        text_translate = request.form.get('text-translate')
        from_language = request.form.get('from-language')
        to_language = request.form.get('to-language')
        result = tran(from_lan=from_language, to_lan=to_language, text=text_translate)
        return render_template('home.html', result=result)


@app.route('/cars/', methods=['GET', 'POST'])
def cars():
    if request.method == 'GET':
        if len(cars_list) > 0:
            return jsonify(cars_list)
        else:
            'There is no car', 404
    else:
        name = request.json['name']        
        year = request.json['year']        
        color = request.json['color']        
        speed = request.json['speed']   

        new_car = {
            'id': cars_list[-1]['id']+1,
            "name": name,
            'year': year,
            'color': color,
            'speed': speed
        }
        cars_list.append(new_car)

        data = {
            'message': 'You have successfully created new car',
            'data': new_car
            }
        return jsonify(data)
    

@app.route('/cars/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def car_detail(id):
    if request.method == 'GET':
        for car in cars_list:
            if car['id'] == id:
                return jsonify(car)
        return f"Not found", 404
    
    if request.method == 'PUT':
        for car in cars_list:
            if car['id'] == id:
                car['name'] = request.json['name']        
                car['year'] = request.json['year']        
                car['color'] = request.json['color']        
                car['speed'] = request.json['speed']
        
            data = {
                'message': 'You have successfully edited car',
                'data': cars_list[id]
            }   
        return jsonify(data)
    
    
##### CARS_LIST BU LIST VA UNDA DICLAR BOR BIZ CARNI OCHIRISH UCHUN "ID" NI OLISHIMIZ
##### KERAK VA ENOMURATE ORQALI ID NI OLISH IMKONINI BERAMIZ
    if request.method == 'DELETE':
        for index, car in enumerate(cars_list):
            if car['id'] == id:
                cars_list.pop(index)
                return jsonify(cars_list)
     


@app.route('/api/translate', methods=['GET', 'POST'])
def api_translate():
    if request.method == 'POST':
        from_lang = request.json['from_lan']
        to_lang = request.json['to_lan']
        text = request.json['text']
        result_ = tran(from_lan=from_lang, to_lan=to_lang, text=text)

        return jsonify(result_)
    else:
        return f"Method not allowed", 400
    

if __name__=="__main__":
    app.run(port=4200, debug=True)
