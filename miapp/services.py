# Servicios auxiliares para buscar códigos CIE y traducir términos médicos.
# Este módulo primero intenta usar la base de datos local y luego consulta una API externa.
import requests

from deep_translator import GoogleTranslator

from miapp.models import DiagnosticoCIE


# Traduce texto en inglés a español usando el servicio de Google.
def traducir_texto(texto):

    try:

        return GoogleTranslator(
            source='en',
            target='es'
        ).translate(texto)

    except:

        return texto


# Convierte términos comunes en español a inglés para poder buscar en la API externa.
def traducir_entrada(termino):

    traducciones = {

        'rodilla': 'knee',

        'hombro': 'shoulder',

        'cuello': 'neck',

        'espalda': 'back',

        'lumbar': 'lumbar',

        'cadera': 'hip',

        'tobillo': 'ankle',

        'codo': 'elbow',

        'muñeca': 'wrist',

        'mano': 'hand',

        'pierna': 'leg',

        'pie': 'foot',

        'brazo': 'arm'

    }

    return traducciones.get(
        termino.lower(),
        termino
    )


# Busca códigos CIE en la base local. Si no hay resultados, consulta una API externa.
def buscar_cie(termino):

    # BUSCAR PRIMERO EN MYSQL
    resultados_db = DiagnosticoCIE.objects.filter(
        nombre_es__icontains=termino
    )

    resultados = []

    if resultados_db.exists():

        for r in resultados_db:

            resultados.append({

                'codigo': r.codigo,

                'nombre': r.nombre_es

            })

        return resultados

    # Si el término no existe en la base local, consultar API externa para obtener sugerencias.

    termino_en = traducir_entrada(termino)

    #  códigos ICD-10-CM.
    url = f'https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code,name&terms={termino_en}'

    try:

        # Envía la solicitud a la API externa de ICD-10-CM.
        response = requests.get(url)

        if response.status_code == 200:

            # La API devuelve un JSON con varias secciones.
            # data[1] contiene los códigos y data[3] contiene los nombres.
            data = response.json()

            codigos = data[1]

            nombres = data[3]

            # Recorre todos los códigos devueltos por la API.
            for i in range(len(codigos)):

                codigo = codigos[i]

                # Algunos nombres vienen como lista [texto, texto traducido].
                # Si es lista, usamos el segundo elemento como el término en inglés.
                if isinstance(nombres[i], list):

                    nombre_en = nombres[i][1]

                else:

                    nombre_en = nombres[i]

                # Traduce el nombre del diagnóstico del inglés al español.
                nombre_es = traducir_texto(
                    nombre_en
                )

                # Guardar el diagnóstico en la base local para futuras búsquedas.
                DiagnosticoCIE.objects.get_or_create(

                    codigo=codigo,

                    defaults={

                        'nombre_es': nombre_es,

                        'nombre_en': nombre_en

                    }

                )

                # Agregar el resultado para devolverlo al usuario.
                resultados.append({

                    'codigo': codigo,

                    'nombre': nombre_es

                })

    except Exception as e:

        # Si ocurre un error en la petición o en el procesamiento, lo mostramos.
        print("ERROR:", e)

    return resultados