# Introducción

Esta guía proporciona instrucciones para configurar el proyecto en tu computadora y una breve introducción a los conceptos principales relacionados con el Servicio de Ingeniería de Datos de Cloudera.

## Requisitos

Para llevar a cabo los labs Prácticos, necesitas:

* Un Clúster Virtual CDE habilitado para Spark 3 e Iceberg (compatible con Azure, AWS y Nube Privada).

* Se requieren muy pocos cambios de código, pero se recomienda tener familiaridad con Python y PySpark.

* El lab Adicional 1 requiere un Almacén Virtual Hive CDW. Este lab es opcional."

## Recomendaciones Antes de Comenzar

A lo largo de los labs, esta guía te indicará que realices pequeñas ediciones en algunos de los scripts. Por favor, prepárate para realizar cambios en un editor y volver a subirlos al mismo CDE File Resource después de cada modificación. Se recomienda encarecidamente tener todos los scripts abiertos en un editor como Atom.

Tu líder de taller Cloudera cargará los conjuntos de datos requeridos en el Almacenamiento en la Nube antes del taller. Si estás reproduciendo estos labs por tu cuenta, asegúrate de haber colocado todo el contenido de la carpeta de datos en una ruta de Almacenamiento en la Nube de tu elección.

A cada usuario se le asignará un nombre de usuario y una ruta de almacenamiento en la nube. Cada script leerá tus credenciales de "parameters.conf", el cual habrás colocado en tu File Resource. Antes de comenzar los labs, abre "parameters.conf" ubicado en la carpeta "resources_files" y edita los tres campos con los valores proporcionados por tu líder de taller Cloudera. Si estás reproduciendo estos labs por tu cuenta, debes asegurarte de que estos valores reflejen la ruta de Almacenamiento en la Nube donde cargaste los datos.

## Descarga del Proyecto

Clona este repositorio de GitHub en tu computadora o en la máquina virtual donde ejecutarás los script.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternativamente, si no tienes `git` instalado en tu máquina, crea una carpeta en tu computadora, dirígete a [esta URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) y descarga los archivios manualmente.

## Usuarios y Credenciales de CDP

Este HOL utiliza un archivo `parameters.conf` para almacenar las credenciales necesarias. A cada usuario se le solicita ingresar su Workload User CDP en la línea 4 y las rutas del Lago de Datos en las líneas 2 y 3. La Workload Password CDP se hereda automáticamente a nivel del Ambiente de CDP y no necesita ser configurada.

Si estás participando en un evento de Cloudera, tu Líder de Taller te proporcionará las credenciales mencionadas. Los datos ya habrán sido cargados por tu Líder de Taller.

Si estás reproduciendo los labs en tu Ambiente de CDE sin la ayuda de un Líder de Cloudera, deberás cargar los datos en una ruta de la Nube arbitraria y obtener tu Workload User de tu Administrador de CDP.

## Configuración de la CLI de CDE

A lo largo de los laboratorios, utilizarás la CLI de CDE. Para configurar la CLI, tienes dos opciones: utilizar el contenedor Docker proporcionado o instalarlo manualmente en tu máquina local.
* Recomendamos encarecidamente utilizar el contenedor Docker proporcionado*, ya que la configuración es mucho más sencilla.

#### Configurar la CLI con el contenedor Docker proporcionado

Para utilizar el contenedor Docker proporcionado, primero realiza la descarga con el siguiente comando:

```docker pull pauldefusco/cde_cli_workshop_1_19:latest```

A continuación, ejecuta el contenedor. El siguiente comando inicia la ejecución y te conecta al contenedor en ejecución:

```docker run -it pauldefusco/cde_cli_workshop_1_19:latest```

Para configurar la CLI, abre el archivo "config.yaml" y agrega tus credenciales:

```vi ~/.cde/config.yaml```

* usuario: este te será proporcionado por el líder del Taller de Cloudera. Si estás trabajando en el entorno de CDP de tu empresa, puedes obtener tu Usuario de CDP Workload desde la Consola de Gestión de CDP o consultando a tu Administrador de CDP.

* vcluster-endpoint: la URL de JOBS_API_URL proporcionada en la página Cluster Details. Esto se puede acceder desde la pestaña de Administración y haciendo clic en el ícono de Cluster Details para tu Clúster Virtual.

![alt text](../../img/cde_virtual_cluster_details.png)

Prueba la CLI ejecutando el siguiente comando. Si tu clúster es nuevo, es posible que no se encuentren ejecuciones de trabajos, pero la salida te ayudará a asegurarte de que puedes conectarte al clúster.

```cde run list```

#### Instalación de la CLI de CDE

Paso 1: Descarga el Cliente de la CLI:
```
    * Navega a la página de Resumen de Cloudera Data Engineering haciendo clic en el mosaico de Data Engineering en la consola de gestión de Cloudera Data Platform (CDP).
    * En la consola web de CDE, selecciona un entorno.
    * Haz clic en el icono de Detalles del Clúster para el clúster virtual al que deseas acceder.
    * Haz clic en el enlace bajo HERRAMIENTA DE LA CLI para descargar el cliente de la CLI.
    * Cambia los permisos del archivo cde descargado para que sea ejecutable:
```

Paso 2: Determina la URL del Punto de Acceso del Clúster Virtual:
```
    * Navega a la página de Resumen de Cloudera Data Engineering.
    * En la columna de Entornos, selecciona el entorno que contiene el clúster virtual al que deseas acceder mediante la CLI.
    * En la columna de Clústeres Virtuales a la derecha, haz clic en el icono de Detalles del Clúster para el clúster virtual al que deseas acceder.
    * Haz clic en URL DE LA JOBS API para copiar la URL en tu portapapeles."
```

Paso 3: En el host con el cliente de la CLI, crea o edita el archivo de configuración en ```~/.cde/config.yaml```. Puedes crear varios perfiles en el archivo ```~/.cde/config.yaml``` y se pueden utilizar al ejecutar comandos.

Paso 4: En el archivo de configuración, especifica el usuario de CDP y el punto de acceso del clúster virtual de la siguiente manera. El usuario de CDP es tu Workload User:

```
user: <CDP_user>
vcluster-endpoint: <CDE_virtual_cluster_endpoint>
```

Paso 5: Guarda el archivo de configuración. Si aún no lo has hecho, asegúrate de que el archivo "cde" sea ejecutable ejecutando ```chmod +x /path/to/cde```. Prueba la CLI ejecutando el siguiente comando. Si tu clúster es nuevo, es posible que no se encuentren ejecuciones de trabajos, pero la salida te ayudará a asegurarte de que puedes conectarte al clúster.

```cde run list```

Para obtener más información sobre la CLI, visita la [Documentación de CDE](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html)

## Índice

* La [Parte 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte01_arquitectura_cde.md#parte-1-arquitectura-de-cde) proporciona una introducción a la Arquitectura del Servicio CDE. Aprenderás acerca de los principales componentes de CDE, incluyendo el Ambiente, el Clúster Virtual y más.
* En la [Parte 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte02_spark.md#parte-2-desarrollo-e-implementaci%C3%B3n-de-jobs-de-spark-en-cde) desarrollarás e implementarás cuatro Jobs de Spark utilizando la interfaz de usuario de CDE, la línea de comandos de CDE y las Sesiones Interactivas de CDE. Uno de los trabajos se centrará en Apache Iceberg.
* En la [Parte 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte03_airflow.md#parte-3-orquestaci%C3%B3n-de-pipelines-de-ingegneria-de-datos-con-airflow) crearás un workflow de Airflow para orquestar múltiples Trabajos de Spark.
* En la [Parte 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte04_spark_migration_tool.md#parte-4-utilizo-de-la-spark-migration-tool-de-cde-para-convertir-spark-submits-en-cde-spark-submits) utilizarás la herramienta de Migración de Spark de CDE para convertir Jobs de Spark en Jobs de Spark de CDE.
* En la [Parte 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#parte-5-labs-adicionales) podrás explorar una variedad de temas con más detalle, incluyendo la CLI de CDE, Airflow y la API de CDE..
* La [Parte 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte06_proyectos_relacionados.md#parte-6-conclusiones-y-pr%C3%B3ximos-pasos) proporciona un resumen y algunos proyectos relacionados. Si estás utilizando o evaluando CDE actualmente, asegúrate de visitar esta página para conocer más  proyectos relacionados.
