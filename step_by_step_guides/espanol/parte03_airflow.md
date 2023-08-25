# Parte 3: Orquestación de Pipelines de Ingegneria de Datos con Airflow

## Objetivo

CDE ofrece un servicio nativo de Airflow que te permite orquestar tuberías complejas en CDE. Aunque está diseñado principalmente para orquestar Jobs CDE Spark, CDE Airflow te permite ejecutar consultas en CDW e integrar herramientas de orquestación y DevOps de terceros.

Este tutorial se divide en dos secciones. Primero construirás tres Jobs de Airflow para programar, orquestar y monitorear la ejecución de Jobs Spark y más. Luego construirás un DAG de Airflow con el Editor de Airflow de Cloudera, una herramienta sin código que te permite crear DAGs de Airflow de manera simplificada.

### Conceptos de Airflow

En Airflow, un DAG (Grafo Dirigido Acíclico) se define en un script de Python que representa la estructura del DAG (tareas y sus dependencias) como código.

Por ejemplo, para un DAG simple que consta de tres tareas: A, B y C. El DAG puede especificar que A debe ejecutarse correctamente antes de que B pueda ejecutarse, pero C puede ejecutarse en cualquier momento. También puede especificar que la tarea A debe finalizar después de 5 minutos, y que B puede reiniciarse hasta 5 veces en caso de fallos. El DAG también puede especificar que el flujo de Job se ejecuta todas las noches a las 10 p.m., pero no debe comenzar hasta una fecha determinada.

Para obtener más información sobre los DAGs de Airflow, consulta la documentación de Apache Airflow [aquí](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html). Para un ejemplo de DAG en CDE, consulta la documentación de DAG de CDE Airflow [aquí](https://docs.cloudera.com/data-engineering/cloud/orchestrate-workflows/topics/cde-airflow-editor.html).

#### La interfaz de Airflow

La interfaz de Airflow facilita la supervisión y solución de problemas de tus canalizaciones de datos. Para obtener una descripción completa de la interfaz de usuario de Airflow, consulta la documentación de la interfaz de usuario de Apache Airflow [aquí](https://airflow.apache.org/docs/apache-airflow/stable/ui.html).

#### ¿Qué es un Job de Airflow en CDE?

Los Jobs de CDE pueden ser de dos tipos: Spark y Airflow. Los Jobs de Airflow en CDE se utilizan típicamente para orquestar Jobs de Spark en CDE, así como otras acciones de Ingeniería de Datos.

Los Jobs de CDE de tipo Airflow consisten principalmente en DAGs de Airflow contenidos en un archivo Python. Más sobre los DAGs a continuación.

Existen tres formas de construir un Job de Airflow en CDE:

* Usando la interfaz web de CDE. Para obtener más información, consulta  [Running Jobs in Cloudera Data Engineering](https://docs.cloudera.com/data-engineering/cloud/manage-jobs/topics/cde-run-job.html).
* Usando la herramienta de línea de comandos de CDE. Para obtener más información, consulta [Cloudera Data Engineering command line interface](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html).
* Utilizando los puntos finales de la API REST de CDE. Para obtener más información, consulta [CDE API Jobs](https://docs.cloudera.com/data-engineering/cloud/jobs-rest-api-reference/index.html)

Además, puedes automatizar las migraciones desde Oozie en CDP Public Cloud Data Hub, CDP Private Cloud Base, CDH y HDP a Jobs CDE de Spark y Airflow con la [oozie2cde API](https://github.com/pdefusco/Oozie2CDE_Migration).


## Despliegue de una Tubería de Orquestación con Airflow

#### Revisando el Código Básico del DAG de Airflow

Abre "03-Airflow-Dag.py" en la carpeta "cde_airflow_jobs", familiarízate con el código y observa lo siguiente:

* Airflow te permite descomponer pipelines complejos de Spark en diferentes pasos, aislando problemas y proporcionando opciones de reintentos de ser necesario. Los operadores CDEJobRunOperator, BashOperator y PythonOperator se importan en las líneas 44-46. Esto te permite ejecutar un CDE Spark Job, un comando Bash y código Python, respectivamente, todo dentro del mismo flujo de Job.

```
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
```

* Cada bloque de código en las líneas 74, 80, 86, 92 y 102 instancia un Operador. Cada uno de ellos se almacena como una variable llamada "Step 1" a "Step 5".

```
step1 = CDEJobRunOperator(
  task_id='etl',
  dag=intro_dag,
  job_name=cde_job_name_03_A #job_name needs to match the name assigned to the Spark CDE Job in the CDE UI
)

step2 = CDEJobRunOperator(
    task_id='report',
    dag=intro_dag,
    job_name=cde_job_name_03_B #job_name needs to match the name assigned to the Spark CDE Job in the CDE UI
)

step3 = BashOperator(
        task_id='bash',
        dag=intro_dag,
        bash_command='echo "Hello Airflow" '
        )

step4 = BashOperator(
    task_id='bash_with_jinja',
    dag=intro_dag,
    bash_command='echo "yesterday={{ yesterday_ds }} | today={{ ds }}| tomorrow={{ tomorrow_ds }}"',
)

#Custom Python Method
def _print_context(**context):
    print(context)

step5 = PythonOperator(
    task_id="print_context_vars",
    python_callable=_print_context,
    dag=intro_dag
)
```

* Los pasos 2 y 3 son instancias de CDEJobRunOperator y se utilizan para ejecutar Jobs de Spark en CDE. En las líneas 89 y 95, los nombres de los Jobs de Spark de CDE deben declararse tal como aparecen en la interfaz de usuario de Jobs de CDE. En este caso, los campos hacen referencia a los valores asignados en las líneas 55 y 56.

<pre>

<b>cde_job_name_03_A = "job3A"
cde_job_name_03_B = "job3B"</b>

#Using the CDEJobRunOperator
step1 = CDEJobRunOperator(
  task_id='etl',
  dag=intro_dag,
  <b>job_name=cde_job_name_03_A</b>
)

step2 = CDEJobRunOperator(
    task_id='report',
    dag=intro_dag,
    <b>job_name=cde_job_name_03_B</b>
)
</pre>

* Finalmente, las dependencias entre tareas se especifican en la línea 119. Los pasos del 1 al 5 se ejecutan en secuencia, uno después de que el otro se complete. Si alguno de ellos falla, los Jobs restantes de CDE no se activarán.

```
step1 >> step2 >> step3 >> step4 >> step5
```

#### Implementación del Código Básico del DAG de Airflow

Crea dos Jobs de CDE Spark (en la interfaz de usuario o con la CLI) utilizando los scripts "04-A-ETL.py" y "04-B-Reports.py", *pero no los ejecutes aún.*

Carga los scripts desde tu máquina local y crea un nuevo File Resource. Asegúrate de nombrarlo con tu nombre para que no choque con otros participantes del taller.

![alt text](../../img/newjobs_1.png)

![alt text](../../img/newjobs_2.png)

![alt text](../../img/newjobs_3.png)

Luego, abre "03-Airflow-Dag.py" e ingresa los nombres de los dos Jobs de CDE Spark tal como aparecen en la interfaz de usuario de CDE Jobs en las líneas 55 y 56.

Además, ten en cuenta que las credenciales almacenadas en parameters.conf no están disponibles para los Jobs de CDE Airflow. Por lo tanto, actualiza la variable "username" en la línea 51 con algo único.

La variable "username" se lee en la línea 67 para crear una variable dag_name que a su vez se usará en la línea 70 para asignar un nombre de DAG único al instanciar el objeto DAG.

>**⚠ Warning**  
>CDE requiere un nombre de DAG único para cada Job de CDE Airflow, de lo contrario, devolverá un error al crear el Job.

Finalmente, modifica las líneas 63 y 64 para asignar una fecha de inicio y finalización que tenga lugar en el futuro.

>**⚠ Warning**   
> Si no editas la fecha de inicio y finalización, el Job de CDE Airflow podría fallar. El parámetro de Fecha de Inicio debe reflejar una fecha pasada, mientras que la Fecha de Finalización debe estar en el futuro. Si estás obteniendo dos ejecuciones idénticas del Job de Airflow, has configurado ambas fechas en el pasado.

Carga el guión actualizado en tu File Resource junto con el archivo parameters.conf. El nuevo Resource debería tener ahora un total de cuatro archivos.

![alt text](../../img/fileinnewresource.png)

Luego, regresa a la Home Page de CDE y crea un nuevo Job de CDE de tipo Airflow.

![alt text](../../img/cdeairflowdag_1.png)

Como antes, selecciona tu Clúster Virtual y nombre del Job. Luego, crea y ejecuta.

![alt text](../../img/cdeairflowdag_2.png)

Crea un nuevo File Resource para esto o reutiliza tu Resource existente si ya tienes uno de un paso anterior.

![alt text](../../img/cdeairflowdag_3.png)

![alt text](../../img/cdeairflowdag_4.png)

Dirígete a la pestaña "Job Runs" y observa que el DAG de Airflow se está ejecutando. Mientras está en progreso, regresa a la Home Page de CDE, baja hasta la sección de Clústeres Virtuales y abre los Detalles del Clúster Virtual. Luego, abre la Interfaz de Usuario de Airflow.

![alt text](../../img/reachairflowui.png)

Familiarízate con la Interfaz de Usuario de Airflow. Luego, abre la página de "DAR Runs" y valida la ejecución del Job de CDE Airflow.

![alt text](../../img/cdeairflow119.png)

![alt text](../../img/cdeairflow119_2.png)

![alt text](../../img/cdeairflow119_3.png)

Para obtener más información sobre CDE Airflow, por favor visita [Orchestrating Workflows and Pipelines](https://docs.cloudera.com/data-engineering/cloud/orchestrate-workflows/topics/cde-airflow-editor.html) en la documentación de CDE.


## Despliegue de Pipeline de Orquestación con el Airflow Editor de Cloudera

Puede utilizar el Editor de Airflow de CDE para construir DAGs sin escribir código. Esta es una excelente opción si su DAG consiste en una larga secuencia de Jobs CDE Spark o Jobs CDW Hive.

Desde la interfaz de usuario de Jobs de CDE, cree un nuevo Job CDE de tipo Airflow como se muestra a continuación. Asegúrese de seleccionar la opción "Editor". Luego haga clic en crear.

![alt text](../../img/bonus2_step00.png)

Desde el Lienzo del Editor, arrastre y suelte la acción de Script de Shell. Esto es equivalente a instanciar el BashOperator. Haga clic en el icono en el lienzo y aparecerá una ventana de opciones en el lado derecho. Ingrese "dag start" en la sección de Comando Bash.

![alt text](../../img/bonus2_step01.png)

Desde el Lienzo, coloque dos Acciones de Job CDE. Configúrelas con el Nombre del Job "sql_job". Ya creó este Job CDE Spark en la parte 2.

![alt text](../../img/bonus2_step02.png)

A continuación, arrastre y suelte una acción de Python. En la sección de código, agregue *print("DAG Terminated")* como se muestra a continuación.

![alt text](../../img/bonus2_step03.png)

Finalmente, complete el DAG conectando cada acción.

![alt text](../../img/bonus2_step04.png)

Para cada uno de los dos Jobs CDE, abra la acción haciendo clic en el icono en el lienzo. Seleccione "Depende del Anterior" y luego "todos_exitosos" en la sección "Regla de Disparo".

![alt text](../../img/bonus2_step05.png)

Ejecute el DAG y obsérvelo desde la interfaz de usuario de Ejecuciones de Job CDE.

![alt text](../../img/bonus2_step06.png)

![alt text](../../img/bonus2_step07.png)

## Resumen
Apache Airflow es una plataforma para crear, programar y ejecutar tuberías de Ingeniería de Datos. Es ampliamente utilizado por la comunidad para crear flujos de Job dinámicos y robustos para casos de uso de Ingeniería de Datos por lotes.

CDE incrusta Apache Airflow a nivel de Clúster Virtual de CDE. Se despliega automáticamente para el usuario de CDE durante la creación del Clúster Virtual de CDE y no requiere mantenimiento por parte del Administrador de CDE.

Un Job CDE Airflow le permite implementar un DAG de Airflow como un Job CDE. El caso de uso principal es la orquestación de Jobs CDE Spark. El Editor de Airflow de Cloudera simplifica el código DAG al proporcionar una interfaz sin código / con bajo código para construir DAGs. Si utiliza principalmente CDE para poner en producción muchos Jobs CDE Spark, el Editor de Airflow puede ser una excelente elección. El DAG de Airflow, en cambio, utiliza Python para construir la lógica del DAG. Es una opción muy buena si utiliza operadores de código abierto de Airflow o necesita aplicar lógica empresarial compleja a su flujo de Job.

Si desea experimentar con un caso de uso de Airflow más avanzado en CDE, visite  [Bonus Lab 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-1-cde-airflow-orchestration-in-depth).

[En la próxima sección](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_spark_migration_tool.md#part-4-using-the-cde-spark-migration-tool-to-convert-spark-submits-to-cde-spark-submits) experimentarás con la Spark Migration Tool de CDE para convertir Spark-Submits en CDE Spark-Submits de manera programática.
