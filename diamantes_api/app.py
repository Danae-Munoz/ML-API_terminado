from flask import Flask, request, jsonify, send_file
import joblib
import pandas as pd
import tempfile
import os

# Inicializar app
app = Flask(__name__)

# Cargar modelo entrenado (sin pipeline)
modelo = joblib.load('modelo_diamantes_pipeline.pkl')

# Obtener columnas que el modelo espera
columnas_esperadas = modelo.feature_names_in_

# Función para transformar y alinear los datos de entrada
def preparar_datos(json_data):
    df = pd.DataFrame([{
        'carat': float(json_data['carat']),
        'cut': json_data['cut'],
        'color': json_data['color'],
        'clarity': json_data['clarity'],
        'depth': float(json_data['depth']),
        'table': float(json_data['table']),
        'x': float(json_data['x']),
        'y': float(json_data['y']),
        'z': float(json_data['z']),
    }])

    df_dummies = pd.get_dummies(df, columns=['cut', 'color', 'clarity'], drop_first=False)


    # Asegurar todas las columnas que espera el modelo
    for col in columnas_esperadas:
        if col not in df_dummies.columns:
            df_dummies[col] = 0

    # Ordenar columnas
    df_dummies = df_dummies[columnas_esperadas]

    # 👇 Verificar qué se está enviando al modelo
    print("🔍 Datos que recibe el modelo:")
    print("Datos crudos:", json_data)
    print("Columnas activadas:", df_dummies.loc[0][df_dummies.loc[0] == 1].index.tolist())

    return df_dummies

# Ruta principal para predecir
@app.route('/predecir', methods=['POST'])
def predecir():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        prediccion = modelo.predict(df)[0]
        return jsonify({'precio_estimado': round(prediccion, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/batch_predecir', methods=['POST'])
def batch_predecir():
    if 'file' not in request.files:
        return jsonify({'error': 'No se adjuntó archivo.'}), 400

    file = request.files['file']
    df = pd.read_csv(file)
    predicciones = modelo.predict(df)
    df['precio_estimado'] = predicciones

    # Guardar resultado temporalmente
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    df.to_csv(temp_file.name, index=False)
    temp_file.close()

    return send_file(temp_file.name, as_attachment=True, download_name='diamantes_con_precios.csv', mimetype='text/csv')

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
