from django.shortcuts import render
from .models import Diamond
from django.shortcuts import render
from .ml_model import predecir_precio_desde_json
from django.core.files.storage import default_storage
import requests
import pandas as pd
import io

def lista_diamantes(request):
    diamantes = Diamond.objects.all().order_by('-id')[:1000]

    return render(request, 'diamantes_app/lista.html', {'diamantes': diamantes})


def prediccion_view(request):
    resultado = None
    if request.method == 'POST':
        datos = {
            'carat': request.POST['carat'],
            'cut': request.POST['cut'],
            'color': request.POST['color'],
            'clarity': request.POST['clarity'],
            'depth': request.POST['depth'],
            'table': request.POST['table'],
            'x': request.POST['x'],
            'y': request.POST['y'],
            'z': request.POST['z'],
        }
        try:
            resultado = predecir_precio_desde_json(datos)
            # Guardar en la base de datos (asegúrate de convertir a float)
            Diamond.objects.create(
                carat=float(datos['carat']),
                cut=datos['cut'],
                color=datos['color'],
                clarity=datos['clarity'],
                depth=float(datos['depth']),
                table=float(datos['table']),
                x=float(datos['x']),
                y=float(datos['y']),
                z=float(datos['z']),
                price=float(resultado)
            )
            print("¡Diamante guardado correctamente!")
        except Exception as e:
            resultado = f'Error: {e}'
            print("Error al guardar:", e)
    return render(request, 'diamantes_app/prediccion.html', {'resultado': resultado})

def batch_prediccion_view(request):
    csv_resultado = None
    if request.method == 'POST' and 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
        # Guardar archivo temporalmente
        path = default_storage.save('tmp/' + archivo.name, archivo)
        file_path = default_storage.path(path)
        # Enviar a Flask
        with open(file_path, 'rb') as f:
            files = {'file': (archivo.name, f, 'text/csv')}
            response = requests.post('http://localhost:5000/batch_predecir', files=files)
            if response.status_code == 200:
                # Guardar el contenido del CSV recibido como archivo
                resultado_nombre = 'tmp/result_' + archivo.name
                file_content = io.BytesIO(response.content)
                resultado_path = default_storage.save(resultado_nombre, file_content)
                # Ahora puedes leer el archivo y agregar a la base de datos
                df_resultado = pd.read_csv(default_storage.path(resultado_path))
                for _, row in df_resultado.iterrows():
                    Diamond.objects.create(
                        carat=row['carat'],
                        cut=row['cut'],
                        color=row['color'],
                        clarity=row['clarity'],
                        depth=row['depth'],
                        table=row['table'],
                        x=row['x'],
                        y=row['y'],
                        z=row['z'],
                        price=row.get('precio_estimado', None)
                    )
                csv_resultado = default_storage.url(resultado_path)
            else:
                csv_resultado = 'Error: ' + response.text
    return render(request, 'diamantes_app/batch_prediccion.html', {'csv_resultado': csv_resultado})
