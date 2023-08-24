# Parte 5: Laboratorios Adicionales

## Objectivo

Hasta ahora, has explorado los aspectos principales de Spark, Airflow e Iceberg en CDE. Los siguientes laboratorios te brindan la oportunidad de explorar CDE con más detalle.

Cada Laboratorio Adicional se puede realizar de manera independiente. En otras palabras, puedes realizar todos o solo algunos seleccionados, y en el orden que prefieras.

### Bonus Lab 1: Orquestación de CDE Airflow (En Detalle)

La Parte 2 del laboratorio te presentó un DAG básico de Airflow en CDE. Sin embargo, las capacidades de Airflow incluyen una amplia variedad de operadores, la capacidad de almacenar valores de contexto temporales, conectarse a sistemas de terceros y, en general, la capacidad de implementar casos de uso de orquestación más avanzados.

Usando "07-Airflow-Logic-DAG.py", crearás un nuevo Trabajo de CDE Airflow con otros operadores populares, como el operador SimpleHttpOperator, para enviar/recibir solicitudes de API.

Primero debes configurar una Conexión al punto final de la API al que harás referencia en el código del DAG. Regresa a la pestaña de Administración de CDE, abre los "Detalles del Clúster" de tu Clúster Virtual y luego haz clic en el ícono de "Airflow" para acceder a la interfaz de usuario de Airflow."

![alt text](../../img/airflow_connection_0.png)

![alt text](../../img/airflow_connection_1.png)

Abre las Conexiones de Airflow en el menú desplegable de Administración, como se muestra a continuación.

![alt text](../../img/airflow_connection_2.png)

Las Conexiones de Airflow te permiten predefinir configuraciones de conexión para que puedan ser referenciadas dentro de un DAG para varios propósitos. En nuestro caso, crearemos una nueva conexión para acceder a la 'API de Chistes Aleatorios' y, en particular, al punto final 'Programación'.

![alt text](../../img/airflow_connection_3.png)

Completa los siguientes campos como se muestra a continuación y guarda.

```
Connection Id: random_joke_connection
Connection Type: HTTP
Host: https://official-joke-api.appspot.com/
```

![alt text](../../img/airflow_connection_4.png)

Ahora abre el archivo '07-Airflow-Logic-DAG.py' y familiarízate con el código. Algunos de los aspectos más destacados de este DAG incluyen:

* Revisa la línea 127. La ejecución de tareas ya no sigue una secuencia lineal. El Paso 3 se ejecuta solo cuando tanto el Paso 1 como el Paso 2 han sido completados exitosamente.
* En las líneas 75-77, el operador DummyOperator se usa como marcador de posición y punto de inicio para la ejecución de tareas.
* En las líneas 106-115, el operador SimpleHttpOperator se usa para enviar una solicitud a un punto final de la API. Esto proporciona un punto de integración opcional entre CDE Airflow y sistemas de terceros u otros servicios de Airflow, ya que las solicitudes y respuestas pueden ser procesadas por el DAG.
* En la línea 109, el valor de 'connection_id' es el mismo que el usado en la Conexión de Airflow que acabas de crear.
* En la línea 110, el valor de 'endpoint' determina el punto final de la API al que se dirigirán las solicitudes. Esto se agrega a la URL base que estableciste en la Conexión de Airflow.
* En la línea 112, la respuesta se captura y se analiza mediante el método 'handle_response' especificado entre las líneas 98-104.
* En la línea 114, usamos la opción 'do_xcom_push' para escribir la respuesta como una variable de contexto del DAG. Ahora la respuesta se almacena temporalmente durante la duración del trabajo de Airflow y puede ser reutilizada por otros operadores.
* En las líneas 120-124, el operador Python ejecuta el método '_print_random_joke' declarado en las líneas 117-118 y muestra la respuesta de la llamada a la API.

Como en el ejemplo anterior, primero crea (pero no ejecutes) tres trabajos de Spark de CDE utilizando "07_A_pyspark_LEFT.py", "07_B_pyspark_RIGHT.py" y "07_C_pyspark_JOIN.py".

Luego, abre "07-Airflow-Logic-DAG.py" en tu editor y actualiza tu nombre de usuario en la línea 50. Asegúrate de que los nombres de los trabajos en las líneas 54-56 reflejen los nombres de los tres trabajos de Spark de CDE tal como los ingresaste en la interfaz de trabajo de CDE.

Finalmente, vuelve a cargar el guión en tu Recurso de Archivos de CDE. Crea un nuevo trabajo de CDE de tipo Airflow y selecciona el guión de tu Recurso de CDE.

>**Nota**
>El operador SimpleHttpOperator se puede usar para interactuar con sistemas de terceros e intercambiar datos hacia y desde una ejecución de trabajo de CDE Airflow. Por ejemplo, podrías desencadenar la ejecución de trabajos fuera de CDP o ejecutar la lógica del DAG de CDE Airflow según las entradas de sistemas de terceros.

>**Note**  
>Puedes usar CDE Airflow para orquestar consultas SQL en CDW, el servicio de datos del Almacén de Datos Cloudera, con el operador CDWOperator respaldado por Cloudera. Si deseas obtener más información, por favor visita [Laboratorio Adicional 2: Usando CDE Airflow con CDW.](https://github.com/pdefusco/CDE_Tour_ACE_HOL/blob/main/step_by_step_guides/english.md#bonus-lab-1-using-cde-airflow-with-cdw).

>**Nota**  
>Además, hay disponibles otros operadores, incluidos los operadores Python, HTTP y Bash en CDE. Si deseas obtener más información sobre Airflow en CDE, consulta la referencia [Using CDE Airflow](https://github.com/pdefusco/Using_CDE_Airflow).


### Bonus Lab 2: Usando CDE Airflow con CDW

Puedes utilizar el operador CDWRunOperator para ejecutar consultas de CDW desde un DAG de CDE Airflow. Este operador ha sido creado y es completamente respaldado por Cloudera.

##### Pasos de Configuración de CDW

Antes de poder utilizar el operador en un DAG, debes establecer una conexión entre CDE Airflow y CDW. Para completar estos pasos, debes tener acceso a un almacén virtual de CDW.

Actualmente, CDE admite operaciones de CDW para cargas de trabajo ETL en almacenes virtuales de Apache Hive. Para determinar el nombre de host de CDW que debes usar para la conexión:

Navega a la página de Resumen del Almacén de Datos Cloudera haciendo clic en el mosaico "Data Warehouse" en la consola de gestión de Cloudera Data Platform (CDP).

![alt text](../../img/bonus1_step00_A.png)

En la columna de "Virtual Warehouses", encuentra el almacén al que deseas conectarte.

![alt text](../../img/bonus1_step00_B.png)

Haz clic en el menú de tres puntos para el almacén seleccionado y luego en "Copy JDBC URL".

![alt text](../../img/bonus1_step00_C.png)

Pega la URL en un editor de texto y toma nota del nombre del host. Por ejemplo, comenzando con la siguiente URL, el nombre del host sería:

```
Original URL: jdbc:hive2://hs2-aws-2-hive.env-k5ip0r.dw.ylcu-atmi.cloudera.site/default;transportMode=http;httpPath=cliservice;ssl=true;retries=3;

Hostname: hs2-aws-2-hive.env-k5ip0r.dw.ylcu-atmi.cloudera.site
```

##### Pasos de Configuración de CDE

Navega a la página de Resumen de Cloudera Data Engineering haciendo clic en el mosaico "Data Engineering" en la consola de gestión de Cloudera Data Platform (CDP).

En la columna de "Servicios de CDE", selecciona el servicio que contiene el clúster virtual que estás utilizando, y luego en la columna de "Clústeres Virtuales", haz clic en "Detalles del Clúster" para el clúster virtual que deseas. Luego, haz clic en "AIRFLOW UI".

![alt text](../../img/bonus1_step00_D.png)

Desde la interfaz de usuario de Airflow, haz clic en el enlace "Connection" en la pestaña "Admin".

![alt text](../../img/bonus1_step00_E.png)

Haz clic en el signo de más para agregar un nuevo registro y luego completa los campos:

* Conn Id: Crea un identificador único de conexión, como "cdw_connection".
* Conn Type: Selecciona "Hive Client Wrapper".
* Host: Ingresa el nombre del host de la URL de conexión JDBC. No ingreses la URL completa de JDBC.
* Schema: default
* Login: Ingresa el nombre de usuario y contraseña de tu carga de trabajo.

Haz clic en "Save".

![alt text](../../img/bonus1_step1.png)

##### Editando el Archivo Python del DAG

Ahora estás listo para usar el CDWOperator en tu DAG de Airflow. Abre el script "bonus-01_Airflow_CDW.py" y familiarízate con el código.

La clase del operador se importa en la línea 47.

```
from cloudera.cdp.airflow.operators.cdw_operator import CDWOperator
```

Una instancia de la clase CDWOperator se crea en las líneas 78-86.

```
cdw_query = """
show databases;
"""

dw_step3 = CDWOperator(
    task_id='dataset-etl-cdw',
    dag=example_dag,
    cli_conn_id='cdw_connection',
    hql=cdw_query,
    schema='default',
    use_proxy_user=False,
    query_isolation=True
)
```

Observa que la sintaxis SQL que se ejecuta en el Almacén Virtual CDW se declara como una variable separada y luego se pasa a la instancia del Operador como un argumento. La conexión también se pasa como un argumento en la línea.

Finalmente, observa que las dependencias de tareas incluyen tanto los pasos spark como dw:

```
spark_step >> dw_step
```

Luego, crea un nuevo trabajo CDE Airflow con el nombre "CDW Dag". Sube el nuevo archivo DAG al mismo recurso CDE o a uno nuevo como parte del proceso de creación.

![alt text](../../img/bonus1_step2.png)

Navega a la página de Ejecución de Trabajos CDE y abre la interfaz de usuario del flujo de trabajo en ejecución. Luego abre la Vista de Árbol y valida que el trabajo haya tenido éxito.

![alt text](../../img/bonus1_step3.png)


### Bonus Lab 3: Uso del CDE CLI para Optimizar Casos de Uso de Producción de CDE (En Detalle)

La mayoría de los casos de uso de producción de CDE dependen de la API y CLI de CDE. Con ellas, puedes interactuar fácilmente con CDE desde un entorno de desarrollo integrado (IDE) local y crear integraciones con sistemas externos de terceros. Por ejemplo, puedes implementar flujos de trabajo de múltiples clústeres CDE con GitLabCI o Python.

En esta parte del taller, adquirirás familiaridad con la CLI de CDE al volver a ejecutar los mismos trabajos e interactuar con el servicio de forma remota.

Puedes utilizar la CLI o la API de CDE para ejecutar trabajos de Spark y Airflow de forma remota en lugar de hacerlo a través de la interfaz de usuario de CDE, como se ha mostrado hasta este punto. En general, se recomienda el uso de la CLI de CDE en lugar de la interfaz de usuario cuando se ejecutan envíos de Spark desde una máquina local. En cambio, se recomienda la API cuando se integran Trabajos de Spark o Trabajos de Airflow de CDE (o ambos) con sistemas de orquestación de terceros. Por ejemplo, puedes utilizar GitLab CI para construir canalizaciones de CDE en múltiples clústeres virtuales. Para un ejemplo detallado, consulta [GitLab2CDE](https://github.com/pdefusco/Gitlab2CDE).

Suponemos que ya has instalado la CLI siguiendo las instrucciones en la Parte 1. Si aún no lo has hecho, por favor instala la CLI de CDE ahora.

Primero, crea un entorno virtual de Python e instala los requisitos.


#### Uso de la CLI de CDE

###### Ejecutar un Job de Spark:

Este comando ejecutará el script como un simple envío de Spark. Esto es ligeramente diferente de crear un Trabajo de tipo Spark en CDE, ya que la definición del trabajo no será reutilizable.

>**⚠ Advertencia**  
> Los comandos CLI a continuación están diseñados para copiar/pegar en tu terminal tal como están y ejecutarlos desde el directorio "cde_tour_ace_hol". Sin embargo, es posible que debas actualizar la ruta del script en cada comando si los ejecutas desde una carpeta diferente.

```
cde spark submit --conf "spark.pyspark.python=python3" cde_cli_jobs/01_pyspark-sql.py
```

###### Verificar el Estado del Job::

Este comando te permitirá obtener información relacionada con el trabajo de Spark anterior. Asegúrate de reemplazar el indicador "id" con el ID proporcionado cuando ejecutaste el último script, por ejemplo, 199.

```
cde run describe --id 199
```

###### Revisar la Salida:

Ejecute este comando para mostrar los registros del trabajo anterior. Asegúrate de reemplazar el indicador "id" con el ID proporcionado cuando ejecutaste el último script.

```
cde run logs --type "driver/stdout" --id 199
```

###### Crear un Recurso de CDE:

Ejecute este comando para crear un File Resource de CDE:

```
cde resource create --name "my_CDE_Resource"
```

###### Subir archivo(s) al File Resource:

Ejecute este comando para cargar el script "01_pyspark-sql.py" en el File Resource.

```
cde resource upload --local-path "cde_cli_jobs/01_pyspark-sql.py" --name "my_CDE_Resource"
```

###### Validar el File Resource:

Ejecute este comando para obtener informaciónes relacionadas con el File Resource.

```
cde resource describe --name "my_CDE_Resource"
```

###### Programar un Job de Spark de CDE con el Archivo Subido al File Resource

Ejecute este comando para crear un Job de Spark de CDE utilizando el archivo subido al Recurso de CDE.

```
cde job create --name "PySparkJob_from_CLI" --type spark --conf "spark.pyspark.python=python3" --application-file "/app/mount/01_pyspark-sql.py" --cron-expression "0 */1 * * *" --schedule-enabled "true" --schedule-start "2022-11-28" --schedule-end "2023-08-18" --mount-1-resource "my_CDE_Resource"
```

###### Validar el Job:

Ejecute este comando para obtener informaciónes sobre los Jobs de CDE cuyo nombre contiene la cadena "PySparkJob".

```
cde job list --filter 'name[like]%PySparkJob%'
```

###### Aprender a Usar la CLI de CDE

La CLI de CDE ofrece muchos más comandos. Para familiarizarte con ella, puedes usar el comando "help" y aprender mientras avanzas. Aquí tienes algunos ejemplos:

```
cde --help
cde job --help
cde run --help
cde resource --help
```

Para obtener más información sobre la CLI de CDE, por favor visita [Using the Cloudera Data Engineering command line interface](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html) en la Documentación de CDE.


### Bonus Lab 4: Uso de Python con la API de CDE

Cloudera Data Engineering (CDE) ofrece una API sólida para la integración con tus plataformas existentes de integración y entrega continua (CI/CD). En este ejemplo, usaremos Python para crear e implementar trabajos de Spark en CDE desde tu máquina local. El mismo código puede ejecutarse en otras plataformas y herramientas de terceros.

##### Introducción a la API de CDE

La API del servicio Cloudera Data Engineering está documentada en Swagger. Puedes ver la documentación de la API y probar llamadas individuales a la API accediendo al enlace API DOC en cualquier clúster virtual:

En la consola web de Data Engineering, selecciona un entorno.
Haz clic en el ícono Detalles del Clúster en cualquiera de los clústeres virtuales listados.
Haz clic en el enlace bajo API DOC.

##### Flujo de Trabajo Básico de la API

Obtener el Token de CDE y Configurar la Variable de Ambiente:

```
export CDE_TOKEN=$(curl -u <workload_user> $(echo '<grafana_charts>' | cut -d'/' -f1-3 | awk '{print $1"/gateway/authtkn/knoxtoken/api/v1/token"}') | jq -r '.access_token')
```

Crear un File Resource de ejemplo:

```
curl -H "Authorization: Bearer $ACCESS_TOKEN" -X POST \
  "$JOBS_API_URL/resources" -H "Content-Type: application/json" \
  -d "{ \"name\": \"cml2cde_api_resource\"}"
```

Validar la Creación del File Resource:

```
curl -H "Authorization: Bearer $ACCESS_TOKEN" -X GET "$JOBS_API_URL/resources/cml2cde_api_resource"
```

Subir el Script del Jobs de Spark:

```
curl -H "Authorization: Bearer $ACCESS_TOKEN" -X PUT \
  "$JOBS_API_URL/resources/cml2cde_api_resource/Data_Extraction_Sub_150k.py" \
  -F "file=@/home/cdsw/cml2cde_tutorial_code/Data_Extraction_Sub_150k.py"
```

Crear un Job de Spark en CDE:

```
curl -H "Authorization: Bearer $ACCESS_TOKEN" -X POST "$JOBS_API_URL/jobs" \
          -H "accept: application/json" \
          -H "Content-Type: application/json" \
          -d "{ \"name\": \"cml2cde_api_job\", \"type\": \"spark\", \"retentionPolicy\": \"keep_indefinitely\", \"mounts
```

Ejecutar el Job de Spark en CDE:

```
curl -H "Authorization: Bearer $ACCESS_TOKEN" -X POST "$JOBS_API_URL/jobs/cml2cde_api_job/run"
```

##### sando Python

Puedes utilizar la biblioteca Requests de Python para envolver los métodos anteriores. Por ejemplo, puedes crear una función para obtener el Token de CDE de la siguiente manera:

```
import requests

def set_cde_token():
    rep = os.environ["JOBS_API_URL"].split("/")[2].split(".")[0]
    os.environ["GET_TOKEN_URL"] = os.environ["JOBS_API_URL"].replace(rep, "service").replace("dex/api/v1", "gateway/authtkn/knoxtoken/api/v1/token")
    token_json = !curl -u $WORKLOAD_USER:$WORKLOAD_PASSWORD $GET_TOKEN_URL
    os.environ["ACCESS_TOKEN"] = json.loads(token_json[5])["access_token"]
    return json.loads(token_json[5])["access_token"]
```

Una vez que hayas configurado correctamente la variable JOBS_API_URL, puedes ejecutar el siguiente código para obtener el Token de CDE:

```
JOBS_API_URL = "https://ewefwfw.cde-6fhtj4hthr.my-cluster.ylcu-atmi.cloudera.site/dex/api/v1"

tok = set_cde_token()
```

Aunque esto puede funcionar en un entorno interactivo, recomendamos utilizar Sesiones de CDE ya que te permiten usar directamente las consolas PySpark y Spark Scala. En general, la API es una excelente opción para construir aplicaciones. Por ejemplo, podrías usar Python para enviar una solicitud a la API de CDE con el fin de monitorear los Recursos de CDE:

```
url = os.environ["JOBS_API_URL"] + "/resources"
myobj = {"name": "cml2cde_python"}
headers = {"Authorization": f'Bearer {tok}',
          "Content-Type": "application/json"}

x = requests.get(url, headers=headers)
x.json()["resources"][-3:-1]
```

Como ejemplo, creamos [CDE Alerter](https://github.com/pdefusco/CDE_Alerter) y el módulo cde_python. CDE Alerter es una aplicación en Python que monitorea continuamente el estado de los trabajos de CDE en múltiples Clusters Virtuales de CDE. Te permite señalar los trabajos de CDE que duran más de un número de segundos proporcionado. Utiliza cde_python, un envoltorio personalizado en Python para la API de CDE, para enviar periódicamente solicitudes al Cluster Virtual de CDE. La idea general es que puedes usar Python para implementar un conjunto de reglas comerciales en caso de un evento particular en un Cluster de CDE.

Para ejecutar esta aplicación en tu máquina local, se requieren pocos o ningún cambio en el código. Necesitarás Python 3.6 o superior, una cuenta de Gmail con autenticación de dos pasos y una contraseña de aplicación. A continuación, se proporcionan los pasos para configurar correctamente una cuenta de Gmail. No recomendamos usar tu cuenta de Gmail existente, si tienes una, y en su lugar crear una nueva cuenta, como se muestra a continuación.

## Instrucciones

#### Paso 0: Configuración del proyecto

Clona este repositorio de GitHub en tu máquina local o en la máquina virtual donde ejecutarás el script.

```
mkdir ~/Documents/CDE_Alerter
cd ~/Documents/CDE_Alerter
git clone https://github.com/pdefusco/CDE_Alerter.git
```

Alternativamente, si no tienes GitHub, crea una carpeta en tu ordenador local; luego, dirígete a [esta URL](https://github.com/pdefusco/CDE_Alerter.git) y descarga los archivos.


#### Paso 1: Crea un Entorno Virtual de Python e Instala los Requisitos

Aunque un Entorno Virtual de Python es opcional, se recomienda encarecidamente. Para crear uno e instalar los requisitos, ejecuta los siguientes comandos:

```
#Create
python3 -m venv venv

#Activate
source venv/bin/activate

#Install single package
pip install pandas #Optionally use pip3 install

#Install requirements
pip install -r requirements.txt #Optionally use pip3 install
```

![alt text](../../img/alerter_img01.png)


#### Paso 2: Edita Clusters.txt y Prueba la Conexión con CDE

El archivo clusters.txt contiene una lista de JOBS_API_URL y direcciones de correo electrónico, que reflejan el/los clúster(es) que deseas supervisar y las direcciones de correo electrónico para recibir notificaciones.

Añade tu JOBS_API_URL y dirección de correo electrónico a clusters.txt y elimina cualquier otra entrada. La aplicación funciona con una o varias entradas de clúster. Luego, asegúrate de que tu máquina o VM pueda acceder al Clúster Virtual de CDE ejecutando el siguiente comando en la terminal:

```
python3 connection_tester.py jobs_api_url cdpusername cdppwd
```

La salida en la terminal debería confirmar que se ha creado exitosamente un recurso de prueba.


#### Step 3: Run the script

Antes de poder ejecutar el script, necesitarás:

* La JOBS_API_URL para el Clúster Virtual al que deseas supervisar.
* La contraseña de la aplicación de Gmail (no solo la contraseña de inicio de sesión de la cuenta). Si necesitas ayuda para configurar esto por primera vez:
  1. Recomendado: [Crear una Nueva Cuenta de Gmail](https://support.google.com/mail/answer/56256?hl=en)
  2. [Activar la Autenticación de 2 Pasos y Crear una Contraseña de Aplicación](https://www.youtube.com/watch?v=hXiPshHn9Pw)
* El Workload User y la Workload Password de CDP con los que te autenticarás en el Clúster Virtual.

Para ejecutar el script, ejecuta el siguiente comando en python en el directorio donde clonaste tu proyecto.

```
python3 alerter.py https://z4xgdztf.cde-6fr6l74r.go01-dem.ylcu-atmi.cloudera.site/dex/api/v1 cdpusername cdppwd mysecregapppwdhere 1800 me@myco.com mycolleague@myco.com
```

La contraseña de la aplicación de Gmail debe ingresarse como cuarto argumento (por ejemplo, reemplazando "mysecregapppwdhere" arriba).

El script detectará automáticamente si han transcurrido más de 1800 segundos (30 minutos) entre la hora de inicio y la hora de finalización de cualquiera de tus trabajos de CDE.

Si alguno de los trabajos de CDE cumple con los criterios, el script enviará automáticamente una notificación a los correos electrónicos proporcionados. Puedes ingresar dos destinatarios de correo electrónico agregándolos como los dos últimos argumentos en la ejecución del script.

Como ejemplo, si reducimos la ventana de tiempo de 1800 segundos a 18 segundos, el script detectará algunos trabajos y mostrará la siguiente salida en la terminal.

![alt text](../../img/alerter_img_02A.png)

Si ningún trabajo de CDE cumple con los criterios, no se realizará ninguna acción.

![alt text](../../img/alerter_img02.png)


#### Paso 4: Programar el Script como un Cron Job

El script puede ejecutarse tan frecuentemente como desees. Por ejemplo, podrías programar una tarea cron para ejecutar el script cada minuto con el siguiente comando:

```
* * * * * /usr/bin/python ~/path/to/proj/cde_alerter/alerter.py
```


## Resumen

En esta sección revisamos tres casos de uso más avanzados de CDE: un DAG de CDE Airflow más avanzado, un DAG de Airflow que utiliza el Operador CDW y una vista más detallada de la CLI de CDE.

Puedes utilizar CDE Airflow con operadores de código abierto para implementar lógica empresarial avanzada en tus DAGs. La versión 1.20 de CDE ampliará aún más esta funcionalidad al proporcionar la capacidad de utilizar un conjunto más amplio de operadores de Airflow, complementos y otras características de código abierto.

El CDWOperator ha sido contribuido por Cloudera para permitir a los usuarios orquestar consultas en CDW desde un DAG de Airflow. Puedes conectarte a una o más Almacenes Virtuales CDW desde el mismo DAG de CDE Airflow.

Finalmente, la CLI de CDE es la elección ideal para aquellos que utilizan CDE a gran escala. Aunque la interfaz de usuario de CDE Jobs es una excelente herramienta de observabilidad, no recomendamos construir tus Spark Jobs con la interfaz de usuario con demasiada frecuencia. La CLI ofrece más opciones, incluida la capacidad de enviar trabajos de CDE a más de un Clúster Virtual CDE desde el mismo programa de terminal. En general, puedes utilizar la CLI para construir más trabajos de CDE de manera más rápida una vez que te familiarices con ella.

¡Gracias por completar los Laboratorios Adicionales! Antes de continuar, visita la pagina de [Proyectos Relacionados](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part06_next_steps.md#part-6-conclusions-and-next-steps) para un breve resumen y proyectos y artículos recomendados. Estos son especialmente útiles si ya estás utilizando o planeas utilizar CDE en el futuro.
