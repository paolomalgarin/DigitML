# COME FARE IL DEPLOY DI **DIGITML** SU XAMPP

> [!NOTE]  
> I problemi di compatibilità tra le librerie e python (es. tensorflow) dovrete risolverle da soli.  
> Si consiglia la versione 3.12 di python in questo momento (2025)

<br>

1. installare xampp sul computer
   * *fare il setup di xampp se è portable*
2. avviare xampp
3. installare python *(mettere python nella path, spuntando l'opzione sul setup)*
4. scaricare il repo
5. nella cartella `DigtiML - Machine Learning/bat_files`, aprire `setup.bat`
6. una volta terminato il setup aprire `start.bat`
4. rinominare la cartella `DigitML - WebApp` in `DigitML`
5. copiare la cartella appena rinominata *(DigitML)* nella cartella `htdocs` dentro xampp
   * *la cartella si trova premendo il tasto Explorer presente sullo xampp control panel*
6. dalla cartella `DigitML - API/build/exploded`, copiare il file `DigitML_API.war` in `tomcat\webapps`
   * *la cartella si trova sempre premendo il tasto Explorer presente sullo xampp control panel*
6. avviare apache e tomcat dallo xampp control panel
7. aprire sul browser `localhost/DigitML`
