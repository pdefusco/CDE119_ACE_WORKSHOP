# Parte 1: Architettura di CDE

## Obiettivo

In questa sezione imparerai l'architettura flessibile di CDE e i suoi principali componenti. Questa è solo una lettura consigliata e non ci sono lavori associati ad essa.

## Introduzione al Servizio CDE

Cloudera Data Engineering (CDE) è un servizio per Cloudera Data Platform che consente di inviare lavori batch a cluster virtuali con ridimensionamento automatico. CDE ti consente di dedicare più tempo alle tue applicazioni e meno tempo all'infrastruttura.

Cloudera Data Engineering ti permette di creare, gestire e pianificare lavori Apache Spark senza l'onere di creare e mantenere cluster Spark. Con Cloudera Data Engineering, puoi definire cluster virtuali con una gamma di risorse CPU e memoria, e il cluster si ridimensiona in base alle necessità per eseguire i carichi di job Spark, contribuendo a controllare i costi cloud.

Il Servizio CDE può essere raggiunto dalla Pagina Principale di CDP cliccando sull'icona blu "Data Engineering".

![alt text](../../img/cdp_lp_0.png)

La Pagina Principale di CDE ti consente di accedere, creare e gestire Cluster Virtuali di CDE. All'interno di ciascun Cluster Virtuale di CDE puoi creare, monitorare e risolvere problemi di lavori Spark e Airflow.

Il Cluster Virtuale è associato all'Ambiente CDP. Ciascun Cluster Virtuale di CDE è mappato al massimo su un Ambiente CDP, mentre un Ambiente CDP può essere mappato su uno o più Cluster Virtuali.

Questi sono i componenti più importanti nel Servizio CDE:

##### Ambiente CDP
Una sottoinsieme logico del tuo account provider cloud che include una rete virtuale specifica. Gli Ambienti CDP possono trovarsi in AWS, Azure, RedHat OCP e Cloudera ECS. Per ulteriori informazioni, consulta [Ambienti CDP][CDP Environments](https://docs.cloudera.com/management-console/cloud/overview/topics/mc-core-concepts.html). In termini pratici, un ambiente è equivalente a un Data Lake poiché ogni ambiente è automaticamente associato ai propri servizi SDX per la sicurezza, la governance e la tracciabilità.

##### Servizio CDE
Il cluster Kubernetes a lunga durata e i servizi che gestiscono i cluster virtuali. Il servizio CDE deve essere abilitato su un ambiente prima che tu possa creare qualsiasi cluster virtuale.

##### Cluster Virtuale
Un singolo cluster con ridimensionamento automatico con intervalli definiti di CPU e memoria. I Cluster Virtuali in CDE possono essere creati e eliminati su richiesta. I lavori sono associati ai cluster. Fino alla versione CDE 1.18 era disponibile solo un tipo di Cluster Virtuale. Dalla versione 1.19 puoi scegliere tra due Tipi di Cluster:

*Core (Tier 1)*: Opzioni di trasformazione e ingegnerizzazione basate su batch che includono:
* Cluster con Autoscaling Automatico
* Spot Instances
* SDX/Lakehouse
* Lifecycle dei Job
* Monitoraggio dei Job
* Orchestrazione Workflow

*All Purpose (Tier 2)*: Sviluppo tramite sessioni interattive e distribuzione di carichi di job batch e in streaming. Questa opzione include tutte le opzioni del Tier 1 con l'aggiunta delle seguenti:
* Sessioni Shell - CLI e Web
* JDBC/SparkSQL (Disponibile a partire da ottobre 2023 con CDE 1.20)
* IDE (Disponibile a partire da ottobre 2023 con CDE 1.20)

I cluster Core sono raccomandati come ambienti di produzione. I cluster All Purpose sono invece progettati per essere utilizzati come ambienti di sviluppo e test. Per ulteriori informazioni sulle versioni CDE 1.19.1 e 1.19.2, visita questa pagina nella [documentazione](https://docs.cloudera.com/data-engineering/cloud/release-notes/topics/cde-whats-new-1.19.html).

##### Jobs
Codice dell'applicazione insieme a configurazioni e risorse definite. I lavori possono essere eseguiti su richiesta o pianificati. L'esecuzione individuale di un job è chiamata job run. I Job possono essere di tipo Spark o Airflow.

##### Resource
Una collezione definita di file, come un file Python o un file JAR dell'applicazione, dipendenze e qualsiasi altro file di riferimento necessario per un job. Le Resource possono essere di tipo File o Python.

##### Job Run
Un'istanza individuale di esecuzione di un Job.

##### CDE Session

Le sessioni interattive CDE offrono agli ingegneri dei dati punti finali flessibili per iniziare a sviluppare applicazioni Spark ovunque, in un terminale basato sul web, nell'interfaccia della riga di comando locale, nell'IDE preferito e persino tramite JDBC da strumenti di terze parti.

##### Apache Iceberg

Apache Iceberg è un formato di tabella aperto nativo per il cloud, ad alte prestazioni, per l'organizzazione di set di dati analitici di scala petabyte su un sistema di file o uno store di oggetti. In combinazione con Cloudera Data Platform (CDP), gli utenti possono creare un'architettura open data lakehouse per l'analisi multi-funzione e per distribuire pipeline su larga scala end-to-end.

Open Data Lakehouse su CDP semplifica l'analisi avanzata su tutti i dati con una piattaforma unificata per dati strutturati e non strutturati e servizi dati integrati per abilitare qualsiasi caso di utilizzo di analisi, dalla ML (Machine Learning) all'BI, all'analisi di flussi e all'analisi in tempo reale. Apache Iceberg è il componente chiave del lakehouse open.

Iceberg è compatibile con una varietà di motori di calcolo, inclusi Spark. CDE ti consente di distribuire Cluster Virtuali abilitati per Iceberg.

Per ulteriori informazioni visita la [documentazione](https://iceberg.apache.org/).

##### Interfaccia CDE

Ora che hai acquisito le basi di CDE, dedica qualche momento a familiarizzare con la pagina di accesso di CDE.

La Home Page fornisce una panoramica generale di tutti i servizi e cluster CDE. È stata ridisegnata nella versione 1.19 per includere anche collegamenti rapidi per diverse azioni, come la creazione di Job e Resource CDE o la visita alla documentazione.

In alto, hai dei collegamenti rapidi per creare Jobs e Resources di CDE.

![alt text](../../img/new_home_119.png)

Scorri verso il basso fino alla sezione dei Cluster Virtuali CDE e noterai che vengono mostrati tutti i Cluster Virtuali e ciascun Ambiente CDP / Servizio CDE associato.

![alt text](../../img/new_home_119_2.png)

Successivamente, apri la pagina di Amministrazione sulla scheda a sinistra. Anche questa pagina mostra i Servizi CDE a sinistra e i Cluster Virtuali associati a destra.

![alt text](../../img/service_cde.png)

Apri la pagina Dettagli del Servizio CDE e osserva le seguenti informazioni chiave e collegamenti:

* Versione CDE
* Intervallo di ridimensionamento dei nodi
* Data Lake CDP e Ambiente
* Grafici Graphana. Fai clic su questo link per ottenere un cruscotto delle risorse Kubernetes del servizio in esecuzione.
* Resource Scheduler. Fai clic su questo link per visualizzare l'interfaccia utente Yunikorn.

![alt text](../../img/service_cde_2.png)

Scorri verso il basso e apri la scheda Configurazioni. Nota che qui vengono definite le Tipologie di Istanza e gli intervalli di ridimensionamento automatico delle istanze.

![alt text](../../img/cde_configs.png)

Per saperne di più sulle altre importanti configurazioni del servizio, visita [Abilitazione di un Servizio CDE](https://docs.cloudera.com/data-engineering/cloud/enable-data-engineering/topics/cde-enable-data-engineering.html) nella Documentazione CDE.

Torna alla pagina di Amministrazione e apri la pagina Dettagli del Cluster Virtuale.

![alt text](../../img/cde_virtual_cluster_details.png)

Questa vista include altre importanti informazioni sulla gestione del cluster. Da qui puoi:

* Scaricare i binari CLI CDE. La CLI è consigliata per inviare lavori e interagire con CDE. È trattata nella Parte 3 di questa guida.
* Visitare la documentazione API per conoscere l'API CDE e creare richieste di esempio nella pagina Swagger.
* Accedere all'interfaccia utente di Airflow per monitorare i tuoi lavori Airflow, configurare connessioni personalizzate, variabili e altro ancora.

Apri la scheda Configurazioni. Nota che puoi selezionare tra Cluster Tier Core e All Purpose.
Inoltre, questa vista offre opzioni per impostare intervalli di ridimensionamento automatico CPU e memoria, versione di Spark e opzioni Iceberg.
CDE supporta Spark 2.4.8, 3.2.3 e 3.3.0.

![alt text](../../img/vc_details_1.png)

![alt text](../../img/vc_details_2.png)

![alt text](../../img/vc_details_3.png)

Per saperne di più sull'architettura CDE, visita [Creating and Managing Virtual Clusters](https://docs.cloudera.com/data-engineering/cloud/manage-clusters/topics/cde-create-cluster.html) e [Recommendations for Scaling CDE Deployments](https://docs.cloudera.com/data-engineering/cloud/deployment-architecture/topics/cde-general-scaling.html)

## Riepilogo

Un servizio CDE definisce i tipi di istanze di calcolo, gli intervalli di autoscaling delle istanze e il Data Lake associato a esso. I dati e gli utenti associati al servizio sono soggetti da SDX e dalle impostazioni dell'ambiente CDP. Puoi sfruttare SDX Atlas e Ranger per visualizzare i metadati delle tabelle e dei job e per garantire l'accesso utente e ai dati tramite politiche dettagliate di sicurezza.

All'interno di un servizio CDE è possibile distribuire uno o più cluster virtuali CDE. L'intervallo di autoscaling del servizio è il conteggio delle istanze di calcolo consentite min/max. L'intervallo di autoscaling del cluster virtuale è il CPU e la memoria min/max che possono essere utilizzati da tutti i job CDE all'interno del cluster. L'intervallo di autoscaling del cluster virtuale è naturalmente limitato dalla CPU e dalla memoria disponibili a livello di servizio.

CDE supporta le versioni di Spark 2.4.8, 3.2.3 e 3.3.0. I cluster virtuali CDE vengono distribuiti con una sola versione di Spark per cluster virtuale.

Questa architettura flessibile ti consente di isolare i tuoi carichi di job e limitare l'accesso all'interno di diversi cluster di calcolo in autoscaling, definendo contemporaneamente regole di controllo dei costi a livello aggregato. Ad esempio, puoi definire servizi a livello di organizzazione e cluster virtuali all'interno di essi come DEV, QA, PROD, ecc.

CDE sfrutta la pianificazione delle risorse e le politiche di ordinamento YuniKorn, come la pianificazione gang e l'impacchettamento dei contenitori, per ottimizzare l'utilizzo delle risorse e migliorare l'efficienza dei costi. Per ulteriori informazioni sulla pianificazione gang, consulta l'articolo del blog Cloudera [Spark on Kubernetes – Gang Scheduling with YuniKorn](https://blog.cloudera.com/spark-on-kubernetes-gang-scheduling-with-yunikorn/).

L'autoscaling dei job CDE Spark è controllato dalla Dynamic Allocation di Apache Spark. La dynamic allocation scala gli executor dei job su e giù secondo necessità durante l'esecuzione dei job. Questo può fornire notevoli vantaggi in termini di prestazioni allocando tutte le risorse necessarie per l'esecuzione dei job e restituendo risorse quando non sono necessarie, consentendo così ai job concorrenti di potenzialmente eseguirsi più velocemente.

[Nella prossima sezione](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) svilupperai e distribuirai i tuoi primi job Spark in CDE per iniziare a costruire una pipeline di ETL e Reporting su larga scala.
