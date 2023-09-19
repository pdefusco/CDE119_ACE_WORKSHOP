# Introducción

Esta página proporciona instrucciones para configurar los activos de datos necesarios. Siga los pasos a continuación como una lista de verificación para asegurarse de que está listo para empezar.

## Tabla de contenidos

* [1. Requisitos]()
* [2. Recomendaciones antes de empezar]()
* [3. Descarga del proyecto]()
* [4. Usuario y credenciales de CDP]()
* [5. Carga de datos en la nube]()
* [6. Configuración de parameters.conf]()
* [7. JOBS API URL]
* [8. Configuración de CDE CLI]()
    * [8A. Configuración de la CLI con el contenedor Docker proporcionado]()
    * [8B. Instalación de la CLI en su máquina local]()
* [Índice]()

## 1. Requisitos

Para llevar a cabo los labs, necesitas:

* Un clúster virtual CDE con Spark 3 habilitado y compatible con Iceberg (Azure, AWS y nube privada son válidos). El servicio CDE debe estar en la versión 1.19.3.

* Se requieren cambios mínimos en el código, pero se recomienda tener familiaridad con Python y PySpark.

* El Bonus Lab 2 requiere un Hive Virtual Warehouse de CDW. Este lab es opcional.

* Una instalación funcional de la CLI de CDE. Para ello, tiene dos opciones: descargar la imagen Docker proporcionada o instalar la CLI en su máquina local. Se proporcionan más detalles a continuación en el paso 7.

## 2. Recomendaciones Antes de Empezar

Esta guía le indicará que realice pequeñas ediciones en algunos de los scripts a medida que avance con los laboratorios. Prepárese para realizar cambios en un editor y volver a cargarlos en el mismo recurso de archivos de CDE después de cada cambio. Se recomienda encarecidamente tener todos los scripts abiertos en todo momento en un editor como Atom o Sublime Text.

## 3. Descarga del Proyecto

Clona este repositorio de Git en tu computadora.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternativamente, si no tienes `git` instalado en tu máquina, crea una carpeta en tu computadora, dirígete a [esta URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) y descarga los archivios manualmente.

## 4. Usuarios y Credenciales de CDP

Si estás participando en un evento de Cloudera, su líder de taller le proporcionará las credenciales mencionadas anteriormente.

Si estás reproduciendo los laboratorios en su entorno de CDE sin la ayuda de un líder de Cloudera, deberá cargar los datos en una ruta de Cloud arbitraria y obtener su Usuario de Trabajo de su Administrador de CDP.

## 5. Carga de Datos en la Nube

Carga la carpeta "data" en la nube.

Si estás asistiendo a un evento HOL público con infraestructura proporcionada por Cloudera, los datos ya habrán sido cargados por tu líder de taller.

Si estás reproduciendo estos laboratorios en tu propia implementación de CDE, asegúrete de haber colocado todo el contenido de la carpeta "data" en una ubicación de almacenamiento en la nube de tu elección.

## 6. Configuración de parameters.conf

Cada script leerá tus credenciales de "parameters.conf". Las instrucciones para cargar esto en tu CDE Files Resource se proporcionan en la parte 2.

Antes de comenzar los labs, abre "parameters.conf" ubicado en la carpeta "resources_files" y edite los tres campos con los valores proporcionados por tu líder de taller de Cloudera ACE.

Si estás reproduciendo estos labs por tu cuenta, deberá asegurarte de que estos valores reflejen la ruta de almacenamiento en la nube donde cargaste los datos.

## 7. Jobs API URL

La JOBS API URL es el punto de entrada al clúster para la API y la CLI. Será necesario en la Configuración de la CLI de CDE y en otras partes de los laboratorios.

Toma nota de la JOBS API URL de tu clúster navegando a la pestaña de Administración y haciendo clic en el ícono Cluster Details para tu Clúster Virtual.

![alt text](../../img/cde_virtual_cluster_details.png)

![alt text](../../img/jobsapiurl.png)

## 8. Configuración de la CLI de CDE

A lo largo de los laboratorios, utilizarás la CLI de CDE. Para configurar la CLI, tienes dos opciones: utilizar el contenedor Docker proporcionado o instalarlo manualmente en tu máquina local.

*Recomendamos encarecidamente utilizar el contenedor Docker proporcionado*, ya que la configuración es mucho más sencilla.

#### 8A. Configurar la CLI con el contenedor Docker proporcionado

Para utilizar el contenedor Docker proporcionado, primero realiza la descarga con el siguiente comando:

```docker pull pauldefusco/cde_cli_workshop_1_19:latest```

A continuación, ejecuta el contenedor. El siguiente comando inicia la ejecución y te conecta al contenedor en ejecución:

```docker run -it pauldefusco/cde_cli_workshop_1_19:latest```

Para configurar la CLI, abre el archivo "config.yaml" y agrega tus credenciales:

```vi ~/.cde/config.yaml```

* usuario: este te será proporcionado por el líder del Taller de Cloudera. Si estás trabajando en el entorno de CDP de tu empresa, puedes obtener tu Usuario de CDP Workload desde la Consola de Gestión de CDP o consultando a tu Administrador de CDP.

* vcluster-endpoint: la JOBS API URL de tu clúster.

![alt text](../../img/cde_virtual_cluster_details.png)

Prueba la CLI ejecutando el siguiente comando. Si tu clúster es nuevo, es posible que no se encuentren ejecuciones de trabajos, pero la salida te ayudará a asegurarte de que puedes conectarte al clúster.

```cde run list```

#### 8B. Instalación de la CLI de CDE

Paso 1: Descarga el Cliente de la CLI:
```
    * Navega a la página de Resumen de Cloudera Data Engineering haciendo clic en el mosaico de Data Engineering en la consola de gestión de Cloudera Data Platform (CDP).
    * En la consola web de CDE, selecciona un entorno.
    * Haz clic en el icono de Detalles del Clúster para el clúster virtual al que deseas acceder.
    * Haz clic en el enlace bajo HERRAMIENTA DE LA CLI para descargar el cliente de la CLI.
    * Cambia los permisos del archivo cde descargado para que sea ejecutable:
```

Paso 2: En el host con el cliente de la CLI, crea o edita el archivo de configuración en ```~/.cde/config.yaml```. Puedes crear varios perfiles en el archivo ```~/.cde/config.yaml``` y se pueden utilizar al ejecutar comandos.

Paso 3: En el archivo de configuración, especifica el usuario de CDP y el punto de acceso del clúster virtual de la siguiente manera. El usuario de CDP es tu Workload User:

```
user: <CDP_user>
vcluster-endpoint: JOBS API URL de tu clúster
```

Paso 4: Guarda el archivo de configuración. Si aún no lo has hecho, asegúrate de que el archivo "cde" sea ejecutable ejecutando ```chmod +x /path/to/cde```. Prueba la CLI ejecutando el siguiente comando. Si tu clúster es nuevo, es posible que no se encuentren ejecuciones de trabajos, pero la salida te ayudará a asegurarte de que puedes conectarte al clúster.

```cde run list```

Para obtener más información sobre la CLI, visita la [Documentación de CDE](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html)

## Índice

* La [Parte 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte01_arquitectura_cde.md#parte-1-arquitectura-de-cde) proporciona una introducción a la Arquitectura del Servicio CDE. Aprenderás acerca de los principales componentes de CDE, incluyendo el Ambiente, el Clúster Virtual y más.
* En la [Parte 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte02_spark.md#parte-2-desarrollo-e-implementaci%C3%B3n-de-jobs-de-spark-en-cde) desarrollarás e implementarás cuatro Jobs de Spark utilizando la interfaz de usuario de CDE, la línea de comandos de CDE y las Sesiones Interactivas de CDE. Uno de los trabajos se centrará en Apache Iceberg.
* En la [Parte 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte03_airflow.md#parte-3-orquestaci%C3%B3n-de-pipelines-de-ingegneria-de-datos-con-airflow) crearás un workflow de Airflow para orquestar múltiples Trabajos de Spark.
* En la [Parte 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte04_spark_migration_tool.md#parte-4-utilizo-de-la-spark-migration-tool-de-cde-para-convertir-spark-submits-en-cde-spark-submits) utilizarás la herramienta de Migración de Spark de CDE para convertir Jobs de Spark en Jobs de Spark de CDE.
* En la [Parte 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#parte-5-labs-adicionales) podrás explorar una variedad de temas con más detalle, incluyendo la CLI de CDE, Airflow y la API de CDE..
* La [Parte 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte06_proyectos_relacionados.md#parte-6-conclusiones-y-pr%C3%B3ximos-pasos) proporciona un resumen y algunos proyectos relacionados. Si estás utilizando o evaluando CDE actualmente, asegúrate de visitar esta página para conocer más  proyectos relacionados.
