# Introducción

Esta guía proporciona instrucciones para configurar el proyecto en tu máquina local y una breve introducción a los conceptos principales relacionados con el Servicio de Ingeniería de Datos de Cloudera.

## Requisitos

Para llevar a cabo los labs Prácticos, necesitas:

* Un Clúster Virtual CDE habilitado para Spark 3 e Iceberg (compatible con Azure, AWS y Nube Privada).
* Se requieren muy pocos cambios de código, pero se recomienda tener familiaridad con Python y PySpark.
* El lab Adicional 1 requiere un Almacén Virtual Hive CDW. Este lab es opcional."

## Recomendaciones Antes de Comenzar

A lo largo de los labs, esta guía te indicará que realices pequeñas ediciones en algunos de los scripts. Por favor, prepárate para realizar cambios en un editor y volver a subirlos al mismo Recurso de Archivo CDE después de cada modificación. Se recomienda encarecidamente tener todos los scripts abiertos en todo momento en un editor como Atom.

Tu líder de taller Cloudera ACE cargará los conjuntos de datos requeridos en el Almacenamiento en la Nube antes del taller. Si estás reproduciendo estos labs por tu cuenta, asegúrate de haber colocado todo el contenido de la carpeta de datos en una ruta de Almacenamiento en la Nube de tu elección.

A cada usuario se le asignará un nombre de usuario y una ruta de almacenamiento en la nube. Cada script leerá tus credenciales de "parameters.conf", el cual habrás colocado en tu Recurso de Archivo CDE. Antes de comenzar los labs, abre "parameters.conf" ubicado en la carpeta "resources_files" y edita los tres campos con los valores proporcionados por tu líder de taller Cloudera ACE. Si estás reproduciendo estos labs por tu cuenta, también debes asegurarte de que estos valores reflejen la ruta de Almacenamiento en la Nube donde cargaste los datos.

## Descarga del Proyecto

Clona este repositorio de GitHub en tu máquina local o en la máquina virtual donde ejecutarás LOSS script.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

Alternativamente, si no tienes `git` instalado en tu máquina, crea una carpeta en tu computadora local dirígete a [esta URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) y descarga los archivios manualmente.

## Usuarios y Credenciales de CDP

Este lab Práctico utiliza un archivo `parameters.conf` para almacenar las credenciales necesarias. A cada usuario se le solicita ingresar su Nombre de Usuario de Carga de Trabajo en la línea 4 y las rutas del Lago de Datos en las líneas 2 y 3. La Contraseña de Carga de Trabajo se hereda automáticamente a nivel del Entorno de CDP y no necesita ser configurada.

Si estás participando en un Evento de Cloudera, tu Líder de Taller te proporcionará las credenciales mencionadas. Los datos ya habrán sido cargados por tu Líder de Taller.

Si estás reproduciendo los labs en tu Entorno de CDE sin la ayuda de un Líder de Cloudera, deberás cargar los datos en una ruta de la Nube arbitraria y obtener tu Nombre de Usuario de Carga de Trabajo de tu Administrador de CDP.

## Índice

* La [Parte 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte01_arquitectura_cde.md#parte-1-arquitectura-de-cde) proporciona una introducción a la Arquitectura del Servicio CDE. Aprenderás acerca de los principales componentes de CDE, incluyendo el Ambiente, el Clúster Virtual y más.
* En la [Parte 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte02_spark.md#parte-2-desarrollo-e-implementaci%C3%B3n-de-jobs-de-spark-en-cde) desarrollarás e implementarás cuatro Jobs de Spark utilizando la interfaz de usuario de CDE, la línea de comandos de CDE y las Sesiones Interactivas de CDE. Uno de los trabajos se centrará en Apache Iceberg.
* En la [Parte 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte03_airflow.md#parte-3-orquestaci%C3%B3n-de-pipelines-de-ingegneria-de-datos-con-airflow) crearás un workflow de Airflow para orquestar múltiples Trabajos de Spark.
* En la [Parte 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte04_spark_migration_tool.md#parte-4-utilizo-de-la-spark-migration-tool-de-cde-para-convertir-spark-submits-en-cde-spark-submits) utilizarás la herramienta de Migración de Spark de CDE para convertir Jobs de Spark en Jobs de Spark de CDE.
* En la [Parte 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte05_extras.md#parte-5-labs-adicionales) podrás explorar una variedad de temas con más detalle, incluyendo la CLI de CDE, Airflow y la API de CDE..
* La [Parte 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espanol/parte06_proyectos_relacionados.md#parte-6-conclusiones-y-pr%C3%B3ximos-pasos) proporciona un resumen y algunos proyectos relacionados. Si estás utilizando o evaluando CDE actualmente, asegúrate de visitar esta página para conocer más  proyectos relacionados.
