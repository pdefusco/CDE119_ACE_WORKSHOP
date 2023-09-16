# Introduzione

Questa guida fornisce istruzioni per configurare il progetto nel tuo computer e una breve introduzione ai concetti principali legati al Servizio di Ingegneria dei Dati di Cloudera.

## Requisiti

Per eseguire i Lab, hai bisogno di:

* Un Virtual Cluster CDE abilitato per Spark 3 e Iceberg (Azure, AWS e Private Cloud sono accettati).

* Sono necessari pochi cambiamenti nel codice, ma è altamente consigliata la familiarità con Python e PySpark.

* Il Bonus Lab 1 richiede un Hive CDW Virtual Warehouse. Questo Lab è opzionale.

## Raccomandazioni Per L'Uso di Queste Guide

Gli script sono pronti all'uso e richiedono minime modifiche. Questa guida ti indicherà di apportare modifiche minori a alcuni degli script. Preparati a effettuare modifiche in un editor e a ricaricarli nella stessa CDE File Resource dopo ogni modifica. È altamente consigliato avere tutti gli script aperti in un editor come Atom.

Il tuo responsabile del workshop Cloudera caricherà i dataset richiesti su Cloud Storage prima del workshop. Se stai riproducendo questi Lab da solo, assicurati di aver inserito tutti i contenuti della cartella dei dati in un percorso di Cloud Storage a tua scelta.

Ad ogni utente verrà assegnato un nome utente e un percorso di Cloud Storage. Ogni script leggerà le tue credenziali da "parameters.conf", che avrai inserito nella tua File Resource. Prima di iniziare i Lab, apri "parameters.conf" situato nella cartella "resources_files" e modifica tutti e tre i campi con i valori forniti dal tuo responsabile del workshop Cloudera. Se stai riproducendo questi Lab da solo, dovrai assicurarti che questi valori riflettano il percorso di Cloud Storage in cui hai caricato i dati.

## Project Download

Clona questo repository GitHub nel tuo computer o nella macchina virtuale dove eseguirai gli script.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

In alternativa, se non hai git installato sulla tua macchina, crea una cartella sul tuo computer, vai a [questo URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) e scarica manualmente i file.

## Utente e Credenziali CDP

Questo HOL utilizza un file parameters.conf per memorizzare le credenziali necessarie. A ciascun utente viene richiesto di inserire il proprio Workload User CDP alla riga 4 e i path Cloud per i dati alle righe 2 e 3. La Workload Password CDP è automaticamente ereditata a livello di Ambiente CDP e non deve essere impostata.

Se stai partecipando a un evento Cloudera, il tuo coordinatore del workshop ti fornirà le credenziali sopra indicate. I dati saranno già stati caricati dal coordinatore del workshop.

Se stai riproducendo i lab nel tuo ambiente CDE senza l'aiuto di un coordinatore Cloudera, dovrai caricare i dati su un percorso cloud di tua scelta e ottenere il tuo Workload User dal tuo amministratore CDP.

## JOBS API URL

Il JOBS API URL è il punto di accesso al cluster per la API e la CLI. Sarà necessario durante la configurazione della CLI di CDE e in altre parti dei lab.

Nota il JOBS API URL del tuo cluster navigando nella scheda di Amministrazione e cliccando sull'icona Cluster Details per il tuo Cluster Virtuale.

![alt text](../../img/cde_virtual_cluster_details.png)

![alt text](../../jobsapiurl.png)

## Setup CLI di CDE

Durante i lab utilizzerai la CLI di CDE. Per configurare la CLI hai due opzioni: utilizzare il contenitore Docker fornito o installarlo manualmente sulla tua macchina locale.
Consigliamo vivamente di utilizzare il contenitore Docker, poiché la configurazione è molto più semplice.

#### Configurare la CLI con il Contenitore Docker Fornito

Per utilizzare il contenitore Docker fornito, esegui prima il comando seguente per scaricarlo:

```docker pull pauldefusco/cde_cli_workshop_1_19:latest```

Successivamente, avvia il contenitore. Il seguente comando avvia e ti connette al contenitore in esecuzione:

```docker run -it pauldefusco/cde_cli_workshop_1_19:latest```

Per configurare la CLI, apri il file "config.yaml" e aggiungi le tue credenziali:

```vi ~/.cde/config.yaml```

* utente: questo ti sarà fornito dal tuo Responsabile del Workshop Cloudera. Se stai lavorando nell'ambiente CDP della tua azienda, puoi ottenere il tuo Utente di Carico di Lavoro CDP dalla Console di Gestione CDP o chiedendo al tuo Amministratore CDP.

* vcluster-endpoint: il JOBS API URL fornito nella pagina dei Dettagli del Cluster. Puoi accedervi dalla scheda Amministrazione e facendo clic sull'icona Dettagli del Cluster per il tuo Cluster Virtuale.

![alt text](../../img/cde_virtual_cluster_details.png)

Testa la CLI eseguendo il seguente comando. Se il tuo cluster è nuovo, potrebbe non essere trovata nessuna esecuzione di lavori, ma l'output ti aiuterà a verificare che puoi connetterti al cluster.

```cde run list```

#### Installazione della CLI di CDE

Passaggio 1: Scarica il Client CLI:
```
    * Vai alla pagina panoramica di Cloudera Data Engineering facendo clic sulla voce Data Engineering nella console di gestione della piattaforma Cloudera Data Platform (CDP).
    * Nella console web di CDE, seleziona un ambiente.
    * Fai clic sull'icona Dettagli del Cluster per il virtual cluster a cui desideri accedere.
    * Fai clic sul collegamento sotto CLI TOOL per scaricare il client CLI.
    * Modifica le autorizzazioni del file cde scaricato per renderlo eseguibile:
```

Passaggio 2: Sull'host con il client CLI, crea o modifica il file di configurazione in ```~/.cde/config.yaml```. Puoi creare più profili nel file ```~/.cde/config.yaml``` e utilizzarli durante l'esecuzione dei comandi.

Passaggio 3: Nel file di configurazione, specifica il Workload User CDP e l'endpoint del Virtual Cluster come segue. Il Worklaod User CDP è il tuo user:

```
user: <CDP_user>
vcluster-endpoint: <CDE_virtual_cluster_endpoint>
```

Passaggio 4: Salva il file di configurazione. Se non l'hai già fatto, assicurati che il file "cde" sia eseguibile eseguendo il comando ```chmod +x /path/to/cde```. Testa la CLI eseguendo il seguente comando. Se il tuo cluster è nuovo, potrebbe non essere trovata alcuna esecuzione ma l'output ti aiuterà a verificare che puoi connetterti al cluster.

```cde run list```

Per ulteriori informazioni sulla CLI, visita la [documentazione](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html)

## Index

* La [Parte 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part01_cde_architecture.md#cde-architecture) fornisce un'introduzione all'Architettura del Servizio CDE. Imparerai sui principali componenti di CDE, inclusi l'Ambiente, il Cluster Virtuale e altro ancora.
* Nella [Parte 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) svilupperai e dispiegherai quattro Spark Jobs utilizzando l'interfaccia di CDE, la CLI di CDE e le Sessioni Interattive di CDE. Uno dei Job si concentrerà su Apache Iceberg.
* Nella [Parte 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part03_airflow.md#part-3-orchestrating-pipelines-with-airflow) creerai una Pipeline Airflow per orchestrare più Spark Jobs.
* Nella [Parte 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_spark_migration_tool.md#part-4-using-the-cde-spark-migration-tool-to-convert-spark-submits-to-cde-spark-submits) utilizzerai lo strumento di migrazione Spark di CDE per convertire Spark Jobs in CDE Spark Jobs.
* Nella [Parte 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#part-5-bonus-labs) potrai esplorare una varietà di argomenti in maggiore dettaglio, inclusa la CLI di CDE, Airflow e l'API di CDE.
* La [Parte 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part06_next_steps.md#conclusions-and-next-steps)  fornisce un riassunto e alcuni progetti correlati. Se stai usando o valutando CDE oggi, assicurati di visitare questa pagina per conoscere i progetti correlati.
