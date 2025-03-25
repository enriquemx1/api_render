from flask import Flask, jsonify, request
from pickle import load as pload
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Cargar el modelo
with open('model_dict_car_eval_rf.pkl', 'rb') as file:
    model_dict = pload(file)

@app.route('/', methods=['POST'])
def predict_car_eval():
    if request.method == 'POST':
        data = request.get_json()
        buying = data.get('buying') 
        maint = data.get('maint')
        doors = data.get('doors')
        persons = data.get('persons') 
        lug_boot = data.get('lug_boot') 
        safety = data.get('safety')
        try: 
            if (
                buying in ['high', 'low', 'med', 'vhigh'] and 
                maint in ['high', 'low', 'med', 'vhigh'] and
                doors in ['2', '3', '4', '5more'] and
                persons in ['2', '4', 'more'] and
                lug_boot in ['big', 'med', 'small'] and
                safety in ['high', 'low', 'med']
            ):
                # Predecir
                prediction = model_dict['model'].predict(
                    [[buying, maint, doors, persons, lug_boot, safety]]
                )
                logger.info('prediction_successful')
            else: 
                logger.error('invalid value')
                return jsonify({'error': 'invalid value'}), 400
        except Exception as e:
            logger.error(f'invalid value: {e}')
            return jsonify({'error': 'invalid value'}), 400
        # Obtener la clase predicha
        class_prediction = model_dict['target_classes'][int(prediction[0])]
        return jsonify({'prediction': class_prediction})

if __name__ == '__main__':
    app.run()

