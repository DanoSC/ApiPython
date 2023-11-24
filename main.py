from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import uvicorn
import requests

app = FastAPI()

#Esta es la URL desde la que vamos a sacar toda la informacion
url = 'https://catalegdades.caib.cat/api/views/rjfm-vxun/rows.json?accessType=DOWNLOAD'

headers = {
    'Accept': 'application/json'
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configurar el sistema de plantillas de Jinja2
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})


# Ruta para manejar las acciones del formulario
@app.post("/seleccionar_por_municipio/")
async def seleccionar_por_municipio(request: Request):
    try:
        # Especificar el valor deseado para la columna 10
        form_data = await request.form()
        municipio = form_data["municipio"]

        # Hacer una solicitud a la API y obtener los datos
        response = requests.get(url, headers=headers)
        data = response.json()

        view_info = data["meta"]["view"]
        dataset_name = view_info["name"]
        dataset_description = view_info["description"]
        columns = view_info["columns"]
        data_info = data["data"]

       # Crear una lista para almacenar los datos filtrados
        datos_filtrados = []

        
        # Iterar sobre las filas e imprimir solo las columnas de interés
        for row in data_info:
            # Verificar si el valor de la columna 10 coincide con el valor deseado
            if row[10] == municipio:
                # Crear un diccionario para representar una fila de la tabla
                row_data = {}

                # Iterar sobre las columnas y agregar los datos al diccionario
                for col_idx, column in enumerate(columns):
                    col_name = column["name"]
                    col_value = row[col_idx]
                    row_data[col_name] = col_value

                # Agregar la fila a la lista de datos filtrados
                datos_filtrados.append(row_data)

        # Generar el código HTML de la tabla
        tabla_html = "<table border='1'><tr>"
        # Agregar encabezados de columna
        for column in columns:
            tabla_html += f"<th>{column['name']}</th>"
        tabla_html += "</tr>"

        # Agregar filas de datos
        for row in datos_filtrados:
            tabla_html += "<tr>"
            for column in columns:
                col_name = column["name"]
                tabla_html += f"<td>{row[col_name]}</td>"
            tabla_html += "</tr>"
        tabla_html += "</table>"


        # Agregar la tabla a la página de resultados
        return HTMLResponse(content=tabla_html, status_code=200)
    except Exception as e:
        # Manejar errores de solicitud a la API
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de la API: {str(e)}")


@app.post("/seleccionar_por_cantidad/")
async def seleccionar_por_cantidad(request: Request):
    try:
        # Hacer una solicitud a la API y obtener los datos
        response = requests.get(url, headers=headers)
        data = response.json()

        # Acceder a la información
        view_info = data["meta"]["view"]
        dataset_name = view_info["name"]
        dataset_description = view_info["description"]
        columns = view_info["columns"]
        data_info = data["data"]

        # Especificar la columna de interés (indexada desde 0)
        columna_interes = 10

        # Contador para cada valor en la columna 10
        counter = {}

        # Iterar sobre las filas y contar los valores en la columna de interés
        for row in data_info:
            value = row[columna_interes]
    
            # Si el valor ya está en el contador, aumentar el recuento; de lo contrario, inicializarlo a 1
            counter[value] = counter.get(value, 0) + 1

        # Generar el código HTML de la tabla
        table_html = "<table border='1'><tr><th>Valor</th><th>Cantidad</th></tr>"

        # Agregar filas de datos
        for value, count in counter.items():
            table_html += f"<tr><td>{value}</td><td>{count}</td></tr>"

        table_html += "</table>"
        return HTMLResponse(content=table_html, status_code=200)
    except Exception as e:
        # Manejar errores de solicitud a la API
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de la API: {str(e)}")



# Ruta para manejar la acción "Seleccionar Todos"
@app.post("/seleccionar_todos/", response_class=HTMLResponse)
async def seleccionar_todos(request: Request):
    try:
        # Hacer una solicitud a la API y obtener los datos
        response = requests.get(url, headers=headers)
        data = response.json()

        view_info = data["meta"]["view"]
        dataset_name = view_info["name"]
        dataset_description = view_info["description"]
        columns = view_info["columns"]
        data_info = data["data"]

        table_data = []

        # Iterar sobre las filas e imprimir todas las columnas
        for row in data_info:
            # Crear un diccionario para representar una fila de la tabla
            row_data = {}
    
            # Iterar sobre las columnas y agregar los datos al diccionario
            for col_idx, column in enumerate(columns):
                col_name = column["name"]
                col_value = row[col_idx]
                row_data[col_name] = col_value
    
            # Agregar la fila a la lista de datos de la tabla
            table_data.append(row_data)

        # Generar el código HTML de la tabla
        table_html = "<table border='1'><tr>"
        # Agregar encabezados de columna
        for column in columns:
            table_html += f"<th>{column['name']}</th>"
        table_html += "</tr>"

        # Agregar filas de datos
        for row in table_data:
            table_html += "<tr>"
            for column in columns:
                col_name = column["name"]
                table_html += f"<td>{row[col_name]}</td>"
            table_html += "</tr>"
        table_html += "</table>"

        # Agregar la tabla a la página de resultados
        return HTMLResponse(content=table_html, status_code=200)
    except Exception as e:
        # Manejar errores de solicitud a la API
        raise HTTPException(status_code=500, detail=f"Error al obtener datos de la API: {str(e)}")



# -- MONTAR EL APP EN UVICORN DIRECTAMENTE
print()
if __name__ == "__main__":
    print("-> Inicio integrado de servicIo web")
    uvicorn.run(app, host="0.0.0.0", port=10000)
else:
    print("=> Iniciado desde el servidor web")
    print("   Módulo python iniciado:", __name__)
