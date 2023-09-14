# Parte 1: Arquitectura de CDE

## Objectivo

En esta sección aprenderás sobre la arquitectura flexible de CDE y sus componentes principales.

## Tabla de Contenido

* [Introducción al Servicio CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#introducci%C3%B3n-al-servicio-cde)
  * [Ambiente CDP](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#ambiente-cdp)
  * [Servicio CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#servicio-cde)
  * [Clúster Virtual](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#cl%C3%BAster-virtual)
  * [CDE Jobs](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#jobs)
  * [CDE Resource](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#cde-resource)
  * [Job Run](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#job-run)
  * [CDE Sessions](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#cde-session)
  * [Apache Iceberg](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#apache-iceberg)
  * [Interfaz de usuario CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#interfaz-de-usuario-de-cde)
* [Resumen](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/espa%C3%B1ol/parte01_arquitectura_cde.md#resumen)

## Introducción al Servicio CDE

Cloudera Data Engineering (CDE) es un servicio para la Plataforma de Datos de Cloudera que te permite desplegar jobs por lotes en clústeres virtuales de Autoscaling. CDE te permite dedicar más tiempo a tus aplicaciones y menos tiempo a la infraestructura.

Cloudera Data Engineering te permite crear, gestionar y programar trabajos de Apache Spark sin la sobrecarga de crear y mantener clústeres Spark. Con Cloudera Data Engineering, defines clústeres virtuales con una variedad de recursos de CPU y memoria, y el clúster aumenta o disminuye según sea necesario para ejecutar tus cargas de trabajo de Spark, lo que ayuda a controlar tus costos en la nube.

Puedes acceder al Servicio CDE desde la Página de Inicio de CDP haciendo clic en el ícono azul "Data Engineering".

![alt text](../../img/cdp_lp_0.png)

La Home Page de CDE te permite acceder, crear y gestionar Clústeres Virtuales de CDE. Dentro de cada Clúster Virtual de CDE puedes crear, supervisar y solucionar problemas en Trabajos de Spark y Airflow.

El Clúster Virtual está vinculado al Ambiente de CDP. Cada Clúster Virtual de CDE está asignado a un máximo de un Ambiente de CDP, mientras que un Entorno de CDP puede estar asignado a uno o más Clústeres Virtuales.

Estos son los componentes más importantes en el Servicio CDE:

##### Ambiente CDP
Un subconjunto lógico de tu cuenta en el proveedor de la nube, que incluye una red virtual específica. Los Entornos de CDP pueden estar en AWS, Azure, RedHat OCP y Cloudera ECS. Para obtener más información, consulta [Ambientes CDP](https://docs.cloudera.com/management-console/cloud/overview/topics/mc-core-concepts.html). Hablando en términos prácticos, un entorno es equivalente a un Lago de Datos, ya que cada entorno se asocia automáticamente con sus propios servicios SDX para Seguridad, Gobernanza y Linaje.

##### Servicio CDE
El clúster y los servicios de Kubernetes de larga duración que gestionan los clústeres virtuales. El servicio CDE debe habilitarse en un entorno antes de poder crear clústeres virtuales.

##### Clúster Virtual
Un clúster individual de autoscaling con rangos y limites de CPU y memoria predefinidos. Los Clústeres Virtuales en CDE se pueden crear y eliminar a pedido. Los trabajos están asociados con los clústeres. Hasta la versión 1.18 de CDE, solo estaba disponible un tipo de Clúster Virtual. Desde la Versión 1.19, puedes elegir entre dos Niveles de Clúster:

*Core (Nivel 1)*: Las opciones de transformación e ingeniería basadas en lotes incluyen:

* Clúster de Autoescalado
* Instancias Spot
* SDX/Lakehouse
* Ciclo de Vida de Trabajo
* Monitorización
* Orquestación de Flujo de Trabajo

*All Purpose (Nivel 2)*: Desarrolla usando sesiones interactivas e implementa cargas de trabajo tanto de lotes como de transmisión. Esta opción incluye todas las opciones del Nivel 1, con la adición de lo siguiente:

* Sesiones de Shell - CLI y Web
* JDBC/SparkSQL (Disponible a partir de octubre de 2023 con CDE 1.20)
* IDE (Disponible a partir de octubre de 2023 con CDE 1.20)

Se recomiendan los clústeres Core como ambientes de Producción. Los clústeres de Uso General están diseñados para ser utilizados como entornos de Desarrollo y Pruebas.
Para obtener más información sobre las versiones 1.19.1 y 1.19.2 de CDE, visita esta página en la [documentación](https://docs.cloudera.com/data-engineering/cloud/release-notes/topics/cde-whats-new-1.19.html).

##### Jobs
Código de la aplicación junto con configuraciones y recursos definidos. Los trabajos se pueden ejecutar a pedido o programarse. Una ejecución individual de trabajo se llama ejecución de trabajo.

##### CDE Resource
Una colección definida de archivos, como un archivo Python o un archivo JAR de aplicación, dependencias y cualquier otro archivo de referencia necesario para un trabajo.

##### Job Run
Una ejecución individual de trabajo.

##### CDE Session
Las sesiones interactivas de CDE brindan a los ingenieros de datos puntos finales flexibles para comenzar a desarrollar aplicaciones Spark desde cualquier lugar, ya sea en una terminal basada en web, CLI local, IDE favorito e incluso a través de JDBC desde herramientas de terceros.

##### Apache Iceberg
Apache Iceberg es un formato de tabla abierto nativo de la nube y de alto rendimiento para organizar conjuntos de datos analíticos de escala de petabytes en un sistema de archivos o almacenamiento de objetos. Combinado con Cloudera Data Platform (CDP), los usuarios pueden construir una arquitectura de lago de datos abierta para análisis multifuncionales y para implementar canalizaciones de gran escala de principio a fin.

El Open Lakehouse en CDP simplifica el análisis avanzado en todos los datos con una plataforma unificada para datos estructurados y no estructurados, y servicios de datos integrados para habilitar cualquier caso de uso de análisis, desde ML, BI hasta análisis de transmisión y análisis en tiempo real. Apache Iceberg es el ingrediente secreto del lago de datos abierto.

Iceberg es compatible con una variedad de motores de cómputo, incluido Spark. CDE te permite implementar Clústeres Virtuales habilitados para Iceberg.

Para obtener más información, visita la [documentación](https://iceberg.apache.org/).

##### Interfaz de Usuario de CDE
Ahora que has cubierto los conceptos básicos de CDE, dedica unos momentos a familiarizarte con la página de Inicio de CDE.

La Página de Inicio ofrece una descripción general de alto nivel de todos los Servicios y Clústeres de CDE. Se rediseñó en la versión 1.19 para incluir también accesos directos a diferentes acciones, como crear Jobs y Resources de CDE o visitar la documentación.

En la parte superior, tienes accesos directos para crear Jobs y Resources de CDE.

![alt text](../../img/new_home_119.png)

Desplázate hacia abajo hasta la sección de Clústeres Virtuales de CDE y observa que se muestran todos los Clústeres Virtuales y cada Entorno de CDP / Servicio CDE asociado.

![alt text](../../img/new_home_119_2.png)

Luego, abre la página de Administración en la pestaña izquierda. Esta página también muestra los Servicios de CDE a la izquierda y los Clústeres Virtuales asociados a la derecha.

![alt text](../../img/service_cde.png)

Abre la página de Detalles del Servicio de CDE y observa la siguiente información clave y enlaces:

* Versión de CDE
* Rango de Escalado Automático de Nodos
* Data Lake y Ambiente de CDP
* Graphana Charts. Haz clic en este enlace para obtener un panel de control de los recursos en ejecución del Servicio Kubernetes.
* Resource Scheduler. Haz clic en este enlace para ver la interfaz de usuario web de Yunikorn.

![alt text](../../img/service_cde_2.png)

Desplázate hacia abajo y abre la pestaña de Configuraciones. Observa que aquí es donde se definen los Tipos de Instancia y los rangos de Escalado Automático de Instancias.

![alt text](../../img/cde_configs.png)

Para obtener más información sobre otras configuraciones importantes del servicio, visita [Enabling a CDE Service](https://docs.cloudera.com/data-engineering/cloud/enable-data-engineering/topics/cde-enable-data-engineering.html) en la Documentación de CDE.

Regresa a la página de Administración y abre la página de Detalles del Clúster de un Clúster Virtual.

![alt text](../../img/cde_virtual_cluster_details.png)

Esta vista incluye otra información importante de gestión del clúster. Desde aquí puedes:

* Descargar los binarios de la CLI de CDE. Se recomienda la CLI para enviar trabajos e interactuar con CDE. Se aborda en la Parte 3 de esta guía.
* Visitar la Documentación de la API para aprender sobre la API de CDE y construir solicitudes de muestra en la página Swagger.
* Acceder a la interfaz de usuario de Airflow para supervisar tus Jobs de Airflow, configurar conexiones personalizadas, variables y más.

Abre la pestaña de Configuración. Observa que puedes seleccionar entre Clústeres de Nivel Core y Uso General. Además, esta vista ofrece opciones para configurar los rangos de escalado automático de CPU y memoria, la versión de Spark y las opciones de Iceberg se configuran aquí. CDE admite Spark 2.4.8, 3.2.3 y 3.3.0..

![alt text](../../img/vc_details_1.png)

![alt text](../../img/vc_details_2.png)

![alt text](../../img/vc_details_3.png)

Para obtener más información sobre la Arquitectura de CDE, visita [Creating and Managing Virtual Clusters](https://docs.cloudera.com/data-engineering/cloud/manage-clusters/topics/cde-create-cluster.html) y [Recommendations for Scaling CDE Deployments](https://docs.cloudera.com/data-engineering/cloud/deployment-architecture/topics/cde-general-scaling.html)

## Resumen

Un Servicio de CDE define tipos de instancias de cómputo, rangos de escalado automático de instancias y el Lago de Datos asociado de CDP. Los Datos y Usuarios asociados con el Servicio están sujetos por SDX y las configuraciones del Entorno de CDP. Puedes aprovechar SDX Atlas y Ranger para visualizar metadatos de tablas y trabajos y asegurar el acceso de usuarios y datos con políticas detalladas.

Dentro de un Servicio de CDE, puedes implementar uno o varios Clústeres Virtuales de CDE. El Rango de Escalado Automático del Servicio es un recuento de instancias de cómputo mínimas/máximas permitidas. El Rango de Escalado Automático del Clúster Virtual es el mínimo/máximo de CPU y Memoria que pueden ser utilizados por todos los Trabajos de CDE dentro del clúster. El Rango de Escalado Automático del Clúster Virtual está naturalmente limitado por la CPU y la Memoria disponibles a nivel de Servicio.

CDE admite las versiones de Spark 2.4.8, 3.2.3 y 3.3.0. Los Clústeres Virtuales de CDE se implementan con una única Versión de Spark por Clúster Virtual.

Esta arquitectura flexible te permite aislar tus cargas de trabajo y limitar el acceso dentro de diferentes clústeres de cómputo de escalado automático, al tiempo que predefiniste las pautas de gestión de costos a nivel agregado. Por ejemplo, puedes definir Servicios a nivel de organización y Clústeres Virtuales dentro de ellos como DEV, QA, PROD, etc.

CDE aprovecha la programación de recursos y las políticas de ordenamiento de YuniKorn, como la programación en grupo y el empaquetamiento de contenedores, para optimizar la utilización de recursos y mejorar la eficiencia de costos. Para obtener más información sobre la programación en grupo, consulta la entrada de blog de Cloudera [Spark on Kubernetes – Gang Scheduling with YuniKorn](https://blog.cloudera.com/spark-on-kubernetes-gang-scheduling-with-yunikorn/).

El escalado automático de trabajos de Spark en CDE está controlado por la asignación dinámica de Apache Spark. La asignación dinámica escala los ejecutores de trabajo hacia arriba y hacia abajo según sea necesario para la ejecución de los trabajos. Esto puede ofrecer grandes beneficios en rendimiento al asignar tantos recursos como sean necesarios para el trabajo en ejecución, y al liberar recursos cuando no son necesarios para que los trabajos concurrentes potencialmente puedan ejecutarse más rápido.

[En la sección siguiente](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) desarrollarás e implementarás tus primeros Trabajos de Spark en CDE para comenzar a construir una Canalización de ETL e Informes a gran escala.
