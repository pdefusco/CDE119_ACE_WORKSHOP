# Parte 4: Utilizzo della Spark Migration Tool di CDE per Convertire Spark Submits in Spark Submits CDE

## Obbiettivo

Il comando spark-submit è un'utilità per eseguire o inviare un programma di applicazione Spark o PySpark (o job) al cluster specificando opzioni e configurazioni. L'applicazione che stai inviando può essere scritta in Scala, Java o Python (PySpark).

La CLI di CDE fornisce un modo simile, sebbene non identico, per eseguire "spark-submits" in CDE. Tuttavia, adattare molti spark-submit a CDE potrebbe diventare un ostacolo nella migrazione. Il team di ingegneria di Cloudera ha creato uno strumento di migrazione Spark per facilitare la conversione.

## Indice

* [Istruzioni Passo per Passo](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte04_spark_migration_tool.md#istruzioni-passo-per-passo)
* [Riepilogo](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte04_spark_migration_tool.md#riepilogo)

### Istruzioni Passo Per Passo

>**⚠ Avviso**  
>Lo strumento di migrazione Spark Submit richiede di avere la CLI di CDE installata sulla tua macchina. Assicurati di aver completato i passaggi di installazione nella Parte 3.

>**⚠ Avviso**  
>Questo tutorial utilizza Docker per semplificare il processo di installazione dello strumento di migrazione Spark Submit. Se non hai Docker installato sulla tua macchina, dovrai seguire [questo tutorial di Vish Rajagopalan](https://github.com/SuperEllipse/cde-spark-submit-migration) al suo posto.

Vai alla Console di Gestione CDP e scarica il file delle tue credenziali utente. Il file delle credenziali include un'ID di Chiave di Accesso CDP e una Chiave Privata CDP.

![alt text](../../img/mgt_console1.png)

![alt text](../../img/mgt_console2.png)

![alt text](../../img/mgt_console3.png)

![alt text](../../img/mgt_console4.png)

Successivamente, accedi ai Dettagli del Cluster Virtuale CDE e copia il JOBS_API_URL.

![alt text](../../img/jobsapiurl.png)

Avvia il container Docker fornito per eseguire i comandi seguenti.

```
docker run -it pauldefusco/cde_spark_submit_migration_tool:latest
```

Ora sei all'interno del container in esecuzione. Successivamente, attiva lo strumento di migrazione Spark Submit eseguendo il seguente comando shell.

```
cde-env.sh activate -p vc-1
```

Vai alla cartella .cde e inserisci l'ID della chiave di accesso CDP e la chiave privata scaricati in precedenza nei rispettivi campi nel file delle credenziali.

Successivamente, apri il file config.yaml situato nella stessa cartella. Sostituisci il valore del cdp console alla riga 3 con l'URL della console CDP (ad esempio, `https://console.us-west-1.cdp.cloudera.com/`).

Poi, inserisci il tuo JOBS_API_URL nel campo "vcluster-endpoint" alla riga 8.

Infine, esegui il seguente spark-submit. Questo è un esempio di submit preso da un cluster CDH legacy.

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

Nel giro di poco dovresti ottenere un output nel tuo terminale, compreso un ID di esecuzione del job che conferma la corretta sottomissione del job a CDE. Nell'esempio di screenshot qui sotto, l'ID di esecuzione del job è 9.

![alt text](../../img/job_submit_confirm1.png)

Vai alla pagina Job Runs del tuo CDE Virtual Cluster e verifica che il job sia in esecuzione o sia stato eseguito con successo.

![alt text](../../img/job_submit_confirm3.png)

>**⚠ Avviso**  
>Se non riesci a eseguire il comando spark-submit potrebbe essere necessario rimuovere l'impostazione tls dal file config.yaml. In altre parole, cancella completamente la riga 4.

## Riepilogo

Il comando spark-submit è l'unico comando utilizzato per sottomettere un'applicazione Spark a un cluster. Il comando fornisce una vasta varietà di opzioni e configurazioni per l'esecuzione dell'applicazione come job, ad esempio il numero e le risorse assegnate al driver e agli executor di Spark.

Il CDE CLI fornisce un comando molto simile, il CDE spark-submit, che può essere utilizzato per sottomettere applicazioni Spark ai cluster virtuali CDE. Lo Strumento di Migrazione CDE Spark Submit è stato creato per consentirti di convertire uno o più comandi spark-submit in CDE spark-submit. Questo richiede un'installazione breve ed è disponibile nella pagina dei Dettagli del Servizio Cluster Virtuale.

Congratulazioni per aver completato le attività principali di questo workshop! Nella [sezione successiva](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte05_extra.md#parte-5-lab-extra) puoi approfondire CDE con quattro argomenti aggiuntivi: un [caso d'uso più avanzato di CDE Airflow](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/english/part05_bonus_labs.md#bonus-lab-1-cde-airflow-orchestration-in-depth); un [Airflow DAG che utilizza l'operatore CDW](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte05_extra.md#bonus-lab-2-utilizzo-di-cde-airflow-con-cdw) per orchestrare query CDW da un DAG Airflow di CDE; e un [Lab più approfondito sulla CDE CLI](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte05_extra.md#bonus-lab-3-approfondimento-utilizzo-della-cde-cli-per-ottimizzare-i-casi-duso-di-produzione-della-cde); e un'[Applicazione Python per monitorare contemporaneamente più di un cluster CDE sfruttando l'API di CDE](https://github.com/pdefusco/CDE119_ACE_WORKSHOP/blob/main/step_by_step_guides/italiano/parte05_extra.md#bonus-lab-4-utilizzo-di-python-con-la-api-di-cde).
