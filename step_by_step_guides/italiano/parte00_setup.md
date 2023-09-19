# Introduzione

Questa pagina fornisce istruzioni per configurare gli asset di dati necessari. Segui i passaggi di seguito come una checklist per assicurarti di essere pronto per iniziare.

## Indice

* [1. Requisiti](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#1-requisiti)
* [2. Raccomandazioni Per L'Uso di Queste Guide](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#2-raccomandazioni-per-luso-di-queste-guide)
* [3. Download del Progetto](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#3-download-del-progetto)
* [4. Utente e Credenziali di CDP](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#4-utente-e-credenziali-cdp)
* [5. Caricamento Dati su Cloud Storage](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#5-caricamento-dati-su-cloud-storage)
* [6. Configurazione parameters.conf](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#6-configurazione-parametersconf)
* [7. Jobs API URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#7-jobs-api-url)
* [8. Configurazione CDE CLI](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#8-configurazione-cde-cli)
  * [8A. Configurazione della CLI con il Contenitore Docker Fornito](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#8a-configurare-la-cli-con-il-contenitore-docker-fornito)
  * [8B. Installazione Manuale della CLI](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#8b-installazione-manuale-della-cli)
* [Indice Guide](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte00_setup.md#indice-guide)

## 1. Requisiti

Per eseguire i Laboratori sono necessari:

* Un cluster virtuale CDE abilitato per Spark 3 e Iceberg (Azure, AWS e Cloud Privato ok). Il servizio CDE deve essere nella versione 1.19.3.

* Sono necessari pochi cambiamenti di codice ma è altamente consigliata la familiarità con Python e PySpark.

* Il Laboratorio Bonus 2 richiede un Warehouse Virtuale Hive CDW. Questo laboratorio è opzionale.

* Un'installazione funzionante della CLI di CDE. Per questo hai due opzioni: scaricare l'immagine Docker fornita o installare la CLI sulla tua macchina locale. Ulteriori dettagli sono forniti di seguito nel passaggio 7.

## 2. Raccomandazioni Per L'Uso di Queste Guide

Questa guida ti indicherà di apportare piccole modifiche a alcuni dei script man mano che procedi con i laboratori.

Sii preparato a effettuare modifiche in un editor e a ricaricarle nello stesso File Resource di CDE dopo ogni modifica. È altamente consigliato avere tutti gli script aperti in ogni momento in un editor come Atom o Sublime Text.

## 3. Download del Progetto

Clona questo repository Git sulla tua macchina locale.

```
mkdir ~/Documents/cde_ace_hol
cd ~/Documents/cde_ace_hol
git clone https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git
```

In alternativa, se non hai git installato sulla tua macchina, crea una cartella sul tuo computer, vai a [questo URL](https://github.com/pdefusco/CDE119_ACE_WORKSHOP.git) e scarica manualmente i file.

## 4. Utente e Credenziali CDP

Se stai partecipando a un evento Cloudera, il tuo Workshop Lead ti fornirà le credenziali sopra menzionate.

Se stai riproducendo i laboratori nel tuo ambiente CDE senza l'aiuto di un Workshop Lead di Cloudera, dovrai caricare i dati in un percorso Cloud arbitrario e ottenere il tuo Utente di Carico di Lavoro dal tuo Amministratore di CDP.

## 5. Caricamento Dati su Cloud Storage

Carica la cartella "data" in una location di Cloud Storage a tua scelta.

Se stai partecipando a un evento HOL pubblico con infrastruttura fornita da Cloudera, i dati saranno già stati caricati dal tuo Workshop Lead.

Se stai riproducendo questi lab nella tua stessa implementazione di CDE, assicurati di aver inserito tutti i contenuti della cartella dei dati in una posizione di Cloud Storage a tua scelta.

## 6. Configurazione parameters.conf

Ogni script leggerà le tue credenziali da "parameters.conf". Le istruzioni per caricare questo nel tuo File Resource di CDE sono fornite nella parte 2.

Prima di iniziare i lab, apri "parameters.conf" situato nella cartella "resources_files" e modifica tutti e tre i campi con i valori forniti dal tuo Cloudera ACE Workshop Lead.

Se stai riproducendo questi laboratori da solo, dovrai assicurarti che questi valori riflettano il path di Cloud Storage in cui hai caricato i dati.

## 7. Jobs API URL

Il JOBS API URL è il punto di accesso al cluster per la API e la CLI. Sarà necessario durante la configurazione della CLI di CDE e in altre parti dei lab.

Fai nota del JOBS API URL del tuo cluster navigando nella scheda di Amministrazione e cliccando sull'icona Cluster Details del tuo Cluster Virtuale.

![alt text](../../img/cde_virtual_cluster_details.png)

![alt text](../../img/jobsapiurl.png)

## 8. Configurazione CDE CLI

Durante tutto il corso dei laboratori, utilizzerai la CDE CLI. Per configurare la CLI, hai due opzioni: utilizzare il contenitore Docker fornito o installarlo manualmente sulla tua macchina locale.

*Raccomandiamo vivamente di utilizzare il contenitore Docker fornito*, poiché la configurazione è molto più semplice.

#### 8A. Configurare la CLI con il Contenitore Docker Fornito

Per utilizzare il contenitore Docker fornito, esegui prima il comando seguente per scaricarlo:

```docker pull pauldefusco/cde_cli_workshop_1_19:latest```

Successivamente, avvia il contenitore. Il seguente comando avvia e ti connette al contenitore in esecuzione:

```docker run -it pauldefusco/cde_cli_workshop_1_19:latest```

Per configurare la CLI, apri il file "config.yaml" e aggiungi le tue credenziali:

```vi ~/.cde/config.yaml```

* utente: questo ti sarà fornito dal tuo Responsabile del Workshop Cloudera. Se stai lavorando nell'ambiente CDP della tua azienda, puoi ottenere il tuo Utente di Carico di Lavoro CDP dalla Console di Gestione CDP o chiedendo al tuo Amministratore CDP.

* vcluster-endpoint: il JOBS API URL fornito nella pagina dei Dettagli del Cluster.

Testa la CLI eseguendo il seguente comando. Se il tuo cluster è nuovo, potrebbe non essere trovata nessuna esecuzione di lavori, ma l'output ti aiuterà a verificare che puoi connetterti al cluster.

```cde run list```

#### 8B. Installazione Manuale della CLI

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

## Indice Guide

* La [Parte 1](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part01_cde_architecture.md#cde-architecture) fornisce un'introduzione all'Architettura del Servizio CDE. Imparerai sui principali componenti di CDE, inclusi l'Ambiente, il Cluster Virtuale e altro ancora.
* Nella [Parte 2](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part02_spark.md#part-2-developing-spark-jobs-in-cde) svilupperai e dispiegherai quattro Spark Jobs utilizzando l'interfaccia di CDE, la CLI di CDE e le Sessioni Interattive di CDE. Uno dei Job si concentrerà su Apache Iceberg.
* Nella [Parte 3](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part03_airflow.md#part-3-orchestrating-pipelines-with-airflow) creerai una Pipeline Airflow per orchestrare più Spark Jobs.
* Nella [Parte 4](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part04_spark_migration_tool.md#part-4-using-the-cde-spark-migration-tool-to-convert-spark-submits-to-cde-spark-submits) utilizzerai lo strumento di migrazione Spark di CDE per convertire Spark Jobs in CDE Spark Jobs.
* Nella [Parte 5](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#part-5-bonus-labs) potrai esplorare una varietà di argomenti in maggiore dettaglio, inclusa la CLI di CDE, Airflow e l'API di CDE.
* La [Parte 6](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part06_next_steps.md#conclusions-and-next-steps)  fornisce un riassunto e alcuni progetti correlati. Se stai usando o valutando CDE oggi, assicurati di visitare questa pagina per conoscere i progetti correlati.
