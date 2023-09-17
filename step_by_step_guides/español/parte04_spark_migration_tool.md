# Parte 4: Utilizo de la Spark Migration Tool de CDE para Convertir Spark Submits en CDE Spark Submits

## Objectivo

El comando spark-submit es una utilidad para ejecutar o enviar un programa de aplicación Spark o PySpark (o Job) al clúster, especificando opciones y configuraciones. La aplicación que estás enviando puede estar escrita en Scala, Java o Python (PySpark).

La CLI de CDE proporciona una manera similar aunque no idéntica de ejecutar "spark-submits" en CDE. Sin embargo, adaptar muchos spark-submits a CDE podría convertirse en un obstáculo en tu migración. El equipo de Ingeniería de Cloudera creó una herramienta de Migración de Spark para facilitar la conversión.

## Tabla de Contenidos

* [Instrucciones Paso a Paso](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte04_spark_migration_tool.md#instrucciones-paso-a-paso)
* [Resumen](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte04_spark_migration_tool.md#resumen)

#### Instrucciones Paso a Paso

>**⚠ Warning**  
>La herramienta de migración de Spark Submit requiere tener instalada la CLI de CDE en tu máquina. Asegúrate de haber completado los pasos de instalación en la Parte 3.

>**⚠ Warning**  
>Este tutorial utiliza Docker para agilizar el proceso de instalación de la herramienta de migración de Spark Submit. Si no tienes Docker instalado en tu máquina, tendrás que seguir este tutorial de [Vish Rajagopalan](https://github.com/SuperEllipse/cde-spark-submit-migration) en su lugar.

Accede a la Consola de Gestión de CDP y descarga tu archivo de credenciales de usuario. El archivo de credenciales incluye un ID de Clave de Acceso CDP y una Clave Privada CDP.

![alt text](../../img/mgt_console1.png)

![alt text](../../img/mgt_console2.png)

![alt text](../../img/mgt_console3.png)

![alt text](../../img/mgt_console4.png)

A continuación, dirígete a los Detalles del Clúster Virtual de CDE y copia la URL de JOBS_API_URL.

![alt text](../../img/jobsapiurl.png)

Inicia el Docker Container de ejemplo.

```
docker run -it pauldefusco/cde_spark_submit_migration_tool:latest
```

Ahora estás dentro del contenedor en ejecución. A continuación, activa la herramienta de migración de Spark-Submit ejecutando el siguiente comando en la terminal.

```
cde-env.sh activate -p vc-1
```

Navega hasta la carpeta .cde y coloca el CDP Access Key ID y la Private Key que descargaste anteriormente en los campos correspondientes del archivo de credenciales.

A continuación, abre el archivo config.yaml ubicado en la misma carpeta. Reemplaza el valor de cdp console en la línea 3 con la URL de la Consola de CDP (por ejemplo `https://console.us-west-1.cdp.cloudera.com/`).
Luego, ingresa tu JOBS_API_URL en el campo "vcluster-endpoint" en la línea 8.

Finalmente, ejecuta el siguiente spark-submit. Este es un ejemplo de envío tomado de un clúster CDH heredado."

```
spark-submit \
--master yarn \
--deploy-mode cluster \
--num-executors 2 \
--executor-cores 1 \
--executor-memory 2G \
--driver-memory 1G \
--driver-cores 1 \
--queue default \
06-pyspark-sql.py
```

Pronto deberías obtener resultados en tu terminal, incluido un ID de ejecución de Job que confirma la correcta presentación del Job en CDE. En el ejemplo de captura de pantalla a continuación, el ID de ejecución de Job es 9.

![alt text](../../img/job_submit_confirm1.png)

Dirígete a la página de ejecuciones de Jobs en tu CDE Virtual Cluster y valida que el Job esté en ejecución o se haya ejecutado con éxito.

![alt text](../../img/job_submit_confirm3.png)

>**⚠ Warning**  
>Si no puedes ejecutar el spark-submit, es posible que debas eliminar la configuración tls del archivo config.yaml. En otras palabras, borra por completo la línea 4.

## Resumen

El comando spark-submit es el único utilizado para enviar una aplicación Spark a un clúster. El comando ofrece una amplia variedad de opciones y configuraciones para ejecutar la aplicación como un Job, por ejemplo, el número y los recursos asignados al controlador y los ejecutores de Spark.

El CLI de CDE proporciona un comando muy similar, el CDE spark-submit, que se puede utilizar para enviar aplicaciones Spark a clústeres virtuales de CDE. La Herramienta de Migración de Spark Submit de CDE se creó para permitirte convertir uno o más comandos spark-submit en CDE spark-submit. Esto requiere una breve instalación y está disponible para ti desde la página de Detalles del Servicio de Clúster Virtual.

¡Felicitaciones por llegar al final de los labs principales de este taller! En [la siguiente sección](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#parte-5-labs-adicionales) vas a ampliar tus conocimientos sobre CDE con quatro temas adicionales: [un caso de uso más avanzado de CDE Airflow;](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#bonus-lab-1-orquestaci%C3%B3n-de-cde-airflow-en-detalle); un [DAG de Airflow que utiliza el Operador de CDW](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#bonus-lab-2-usando-cde-airflow-con-cdw) para orquestar consultas en CDW desde un DAG de CDE Airflow; y una vista más [detallada del CLI de CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#bonus-lab-3-uso-del-cde-cli-para-optimizar-casos-de-uso-de-producci%C3%B3n-de-cde-en-detalle); y una [Aplicación en Python para monitorear más de un clúster de CDE al mismo tiempo utilizando la API de CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#bonus-lab-4-uso-de-python-con-la-api-de-cde); y un [Job de PySpark que utiliza Great Expectations para garantizar la calidad, precisión y completitud de los datos]().
