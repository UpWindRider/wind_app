import requests
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

def dibujar_flecha(angulo, velocidad, velocidad_rafaga, alturas):

  angulo = float(angulo)
  velocidad = float(velocidad)
  velocidad_rafaga = float(velocidad_rafaga)
  alturas = float(alturas)

  print(velocidad_rafaga, 'rafaga')

  angulo_rad = np.deg2rad(angulo)

  fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

  ax1 = plt.subplot(221, projection='polar')

  ax1.set_theta_zero_location('N')
  ax1.set_theta_direction(-1)

  ax1.arrow(angulo_rad, 1, 0, -1, head_width=0.5, head_length=0.1, fc='blue', ec='blue')

  ax1.set_ylim(0, 1)
  ax1.set_yticks([])
  ax1.set_xticks([])
  ax1.set_aspect('equal')
  ax1.set_title('Dirección del Viento')

  direcciones = ['N', 'NE', 'E','SE', 'S', 'SW', 'W', 'NW']
  angulos = np.linspace(0, 2 * np.pi, len(direcciones), endpoint=False)

  ax1.set_xticks(angulos)
  ax1.set_xticklabels(direcciones)

  ax2 = plt.subplot(222)
  ax2.bar(['Velocidad del Viento', 'Velocidad de Ráfaga'], [velocidad, velocidad_rafaga], color=['red', 'orange'], width=0.4)
  max_valor = max(velocidad, velocidad_rafaga)
  ax2.set_ylim(0, max_valor + 10)
  ax2.set_title('Velocidad del Viento')
  ax2.set_ylabel('Velocidad (Nudos)')

    # Mostrar el valor encima de las barras
  for i, v in enumerate([velocidad, velocidad_rafaga]):
      ax2.annotate(f'{v:.1f}', xy=(i, v), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

  ax3 = plt.subplot(223)
    
  bars = ax3.bar(['','Altura del Rio',''], [0,int(alturas),0], color=['b','b','b'], width=0.2)
  #ax3.bar(['Altura del Rio'],[alturas], color=['b'], width=0.4)
  ax3.set_title('Altura de la Marea')
  #ax3.set_xlabel('Tiempo')
  ax3.set_ylabel('Altura (cm)')
  ax3.set_ylim(0, 340)
  ax3.grid(visible=True, axis='y', color='gray', linestyle='--')

  for bar in bars:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{yval}', ha='center', va='bottom')

  plt.tight_layout()
  plt.show()

def get_data():
  # os.getenv obtiene el string definido para la variable de entorno
  url = os.getenv('URL')
  url_marea = os.getenv('URL_MAREA')

  print(f"\n\n URL: ${url} \n\n ")
  print(f"\n\n URL: ${url_marea} \n\n ")
  # Hacer la solicitud GET
  response = requests.get(url)
  response_marea =requests.get(url_marea)

  # Verificar si la solicitud fue exitosa
  if response.status_code and response_marea.status_code == 200:
        # El try catch sirve para 'intentar' desestructurar u obtener valores del data.
        # En caso de que no exista un atributo o no sea del tipo numerico, se atrapa 'catch' el problema
        # y se imprime el error referido al mismo {e}
        try:
            data = response.json()
            data_marea = response_marea.json()
            
            print(data_marea)
            print(data)

            lista = data['feeds']
            lista_marea = data_marea['feeds']
            viento_avg = lista[0]['field3']
            viento_racha = lista[0]['field2']
            viento_dir = lista[0]['field4']
            alturas = lista_marea[0]['field1']

            # Convertir a float, si falla, se lanzará ValueError o TypeError
            viento_avg = float(viento_avg)
            viento_racha = float(viento_racha)
            viento_dir = float(viento_dir)
            alturas = float(alturas)

            # Llamar a la función de visualización
            dibujar_flecha(viento_dir, viento_avg, viento_racha, alturas)

        except (KeyError, ValueError, TypeError) as e:
            print(f"Error processing data: {e}")
            # Aca se podria registrar el error creando logs, para tener una lectura centralizada de errores de la app.
            # Se podria usar librerias como logging
            return

  else:
      print(f"Error al hacer la solicitud: {response.status_code}")