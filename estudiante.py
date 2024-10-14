from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import datetime

# Crear la aplicación web
app = Flask(__name__)

# Ruta del archivo CSV
data_path = 'estudiantes.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"El archivo {data_path} no se encuentra.")

# Cargar los datos iniciales del CSV
data = pd.read_csv(data_path)

# Función para graficar clusters
def graficar_clusters():
    plt.scatter(data['Nota'], data['Comportamiento'], c=data['Grupo'], cmap='viridis')
    plt.xlabel('Nota')
    plt.ylabel('Comportamiento')
    plt.title('Agrupación de Estudiantes por Rendimiento y Comportamiento')
    plt.colorbar()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'cluster_{timestamp}.png'  # Nombre de archivo único
    plt.savefig(f'static/{nombre_archivo}')  # Guardar la imagen en static
    plt.close()
    return nombre_archivo

@app.route('/', methods=['GET', 'POST'])
def predecir():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            nombre = request.form['nombre']
            edad = int(request.form['edad'])
            nota = float(request.form['nota'])
            comportamiento = float(request.form['comportamiento'])

            # Agregar nuevo estudiante a los datos y guardar en CSV
            nuevo_estudiante = pd.DataFrame([[nombre, edad, nota, comportamiento]], columns=['Nombre', 'Edad', 'Nota', 'Comportamiento'])
            global data
            data = pd.concat([data, nuevo_estudiante], ignore_index=True)
            data.to_csv(data_path, index=False)  # Guardar datos en CSV

            # Preparar datos para K-Means
            X = data[['Nota', 'Comportamiento']]
            kmeans = KMeans(n_clusters=3, random_state=20)
            kmeans.fit(X)

            # Añadir el grupo de cada estudiante al DataFrame
            data['Grupo'] = kmeans.labels_

            # Generar gráfico
            imagen = graficar_clusters()

            # Predecir el grupo para los nuevos datos
            prediccion = kmeans.predict([[nota, comportamiento]])[0]

            # Redirigir a la página de resultados con el éxito
            return redirect(url_for('resultado.thml', nombre=nombre, grupo=prediccion, nota=nota, comportamiento=comportamiento, imagen=imagen))
        except Exception as e:
            return render_template('index.html', success=False)

    return render_template('index.html')

@app.route('/resultado')
def resultado():
    nombre = request.args.get('nombre')
    grupo = request.args.get('grupo')
    nota = request.args.get('nota')
    comportamiento = request.args.get('comportamiento')
    imagen = request.args.get('imagen')

    return render_template('resultado.html', nombre=nombre, grupo=grupo, nota=nota, comportamiento=comportamiento, imagen=imagen)

if __name__ == '__main__':
    app.run(debug=True)
