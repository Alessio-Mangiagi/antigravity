# =============================================================================
# config.py — Costanti globali dell'applicazione
# Contiene: testi di esercitazione, layout tastiera QWERTY,
#           mappatura dita, colori e nomi dei diti.
# Modificare qui per aggiungere testi o cambiare i colori.
# =============================================================================

# ─── Testi di esercitazione suddivisi per difficoltà ─────────────────────────
TEXTS = {
    "Facile": [
        # originali
        "il gatto dorme sul tappeto rosso",
        "la casa è grande e molto bella",
        "oggi il sole splende nel cielo",
        "il cane corre veloce nel parco",
        "mangio una mela fresca ogni giorno",
        "il libro è posato sul tavolo",
        "la luna brilla nella notte scura",
        "bevo un caffè caldo ogni mattina",
        "il treno parte dalla stazione presto",
        "la bambina sorride e gioca felice",
        "il mare è blu e molto profondo",
        "vado a scuola ogni giorno di settimana",
        # nuove
        "il fiore sboccia in primavera",
        "la neve cade lenta dal cielo",
        "il bambino ride e corre forte",
        "mangio la pasta con il sugo",
        "il nonno legge il giornale mattina",
        "la gatta dorme vicino al fuoco",
        "bevo acqua fresca ogni pomeriggio",
        "il pane è caldo e profumato",
        "la finestra è aperta sul giardino",
        "il cielo è pieno di stelle",
        "porto lo zaino rosso a scuola",
        "la nonna cucina la torta buona",
        "il sole tramonta sul mare calmo",
        "il gatto gioca con la palla",
        "la strada è lunga e dritta",
        "mangio la frutta ogni mattina presto",
        "il fiume scorre lento tra i prati",
        "la porta è chiusa a chiave",
        "il vento soffia forte oggi pomeriggio",
        "la bici è parcheggiata fuori casa",
        "il latte è fresco e molto buono",
        "la lampada illumina la stanza piccola",
        "il topo corre sotto il tavolo",
        "la foglia cade gialla dal ramo",
        "bevo un tè caldo la sera",
        "il cavallo corre nel campo verde",
        "la bambina legge un libro colorato",
        "il pesce nuota nel lago blu",
        "la scuola inizia alle otto di mattina",
        "il cane dorme vicino alla porta",
        "la mamma prepara la colazione presto",
        "il papà guida la macchina blu",
        "la torta è dolce e molto buona",
        "il treno arriva in orario oggi",
        "la pioggia cade sul tetto rosso",
        "il bosco è verde e molto grande",
        "la montagna è alta e nevosa",
        "bevo il succo di arancia fresco",
        "il gallo canta al mattino presto",
        "la rosa è rossa e profumata",
        "il tavolo è fatto di legno chiaro",
        "la sedia è comoda e morbida",
        "il cielo è grigio e nuvoloso",
        "la farfalla vola tra i fiori",
        "il gelato è freddo e dolcissimo",
        "la rana salta vicino al laghetto",
        "il sole scalda il prato verde",
        "la carta è bianca e molto liscia",
        "il pomeriggio è tranquillo e sereno",
        "la formica cammina sul sentiero stretto",
        "il coniglio mangia la carota fresca",
        "la tartaruga cammina piano piano",
        "il cielo diventa arancione al tramonto",
        "la candela illumina la stanza buia",
        "il ruscello scorre tra le pietre",
        "la pecora bela nel campo aperto",
        "il nonno cammina nel parco ogni sera",
        "la mela rossa è caduta a terra",
        "il sole brilla forte in estate",
        "la chitarra suona una melodia dolce",
        "il bambino dorme nel letto caldo",
        "la nuvola bianca attraversa il cielo",
        "il gatto graffia il divano vecchio",
        "la bambina dipinge un quadro colorato",
        "il pappagallo parla nella gabbia grande",
        "la tazza è piena di caffè caldo",
        "il cane abbaia alla luna piena",
        "la cipolla fa piangere in cucina",
        "il pomodoro è rosso e maturo",
        "la barca galleggia sul lago calmo",
        "il trattore ara il campo di grano",
        "la mosca ronza vicino alla finestra",
        "il geco corre sul muro bianco",
        "la lumaca lascia una traccia lucida",
        "il limone è giallo e molto aspro",
        "la festa è allegra e rumorosa",
        "il pallone rotola verso la porta",
        "la cartella è pesante e piena",
        "il merlo canta sul ramo alto",
        "la pizza è calda e croccante",
        "il formaggio è giallo e saporito",
        "la giacca è appesa all'attaccapanni",
        "il cornetto è buono con la marmellata",
        "la radio suona una bella canzone",
        "il giardino è pieno di fiori belli",
        "la zia porta i dolci a casa",
        "il cielo di notte è pieno di stelle",
        "la lepre corre veloce nel bosco",
    ],
    "Medio": [
        # originali
        "la programmazione richiede pratica costante e molta dedizione per migliorare",
        "il computer moderno è diventato uno strumento potente e indispensabile",
        "studiare dattilografia migliora la velocità di scrittura in modo significativo",
        "scrivere con tutte e dieci le dita aumenta notevolmente la produttività",
        "ogni giorno di pratica porta grandi miglioramenti nella velocità di battitura",
        "la tastiera qwerty è lo standard più diffuso in tutto il mondo occidentale",
        "imparare a digitare velocemente è una competenza fondamentale nel mondo moderno",
        "la postura corretta durante la digitazione previene dolori alle mani e alla schiena",
        "i polsi devono rimanere sollevati mentre si digita per evitare infortuni",
        "ogni dito è responsabile di specifici tasti sulla tastiera italiana standard",
        # nuove
        "la memoria muscolare si sviluppa con la ripetizione costante degli esercizi",
        "digitare senza guardare la tastiera richiede concentrazione e allenamento continuo",
        "la velocità di scrittura aumenta progressivamente con la pratica quotidiana regolare",
        "mantenere una postura eretta durante la digitazione riduce la fatica muscolare",
        "le dita indice riposano sempre sui tasti guida della tastiera standard",
        "un monitor posizionato correttamente riduce l affaticamento degli occhi durante il lavoro",
        "la tecnica corretta di battitura evita tensioni inutili nei tendini delle mani",
        "praticare la dattilografia ogni giorno è il modo migliore per migliorare rapidamente",
        "il ritmo costante nella digitazione è più importante della velocità assoluta",
        "la precisione nella battitura deve sempre precedere la ricerca della velocità massima",
        "esercitarsi con testi diversi aiuta a familiarizzare con tutte le combinazioni di lettere",
        "la dattilografia professionale richiede anni di pratica e grande disciplina personale",
        "un dattilografo esperto non ha bisogno di guardare la tastiera mentre scrive",
        "il software di allenamento per la digitazione misura velocità e tasso di errori",
        "la mano sinistra controlla i tasti del lato sinistro della tastiera italiana",
        "correggere subito gli errori durante la scrittura rallenta la velocità complessiva",
        "la resistenza alla fatica migliora con sessioni di allenamento regolari e brevi",
        "digitare con le dita curve sui tasti garantisce maggiore controllo e precisione",
        "ogni sessione di pratica dovrebbe includere esercizi di riscaldamento per le dita",
        "la concentrazione mentale è fondamentale per mantenere alta la precisione di battitura",
        "imparare la posizione dei tasti speciali accelera la scrittura di testi tecnici",
        "la riga centrale della tastiera contiene i tasti di riferimento per le dita",
        "la battitura cieca aumenta la velocità perché elimina il movimento degli occhi",
        "un buon allenamento dattilografico include la pratica di parole comuni ad alta frequenza",
        "le pause regolari durante la digitazione prolungata prevengono il sovraccarico muscolare",
        "la velocità di battitura si misura tradizionalmente in parole al minuto digitate",
        "impostare obiettivi realistici aiuta a mantenere la motivazione durante l'allenamento",
        "la tastiera meccanica offre un feedback tattile che molti dattilografi preferiscono",
        "digitalizzare documenti cartacei richiede velocità di battitura e buona concentrazione",
        "il mignolo sinistro gestisce tasti come a e maiuscola sul lato della tastiera",
        "acquisire fluidità nella digitazione trasforma il lavoro al computer in attività piacevole",
        "la frequenza delle lettere in italiano influenza il design ergonomico delle tastiere",
        "i caratteri maiuscoli si ottengono tenendo premuto il tasto delle maiuscole",
        "un ambiente di lavoro ben illuminato riduce l affaticamento visivo durante la digitazione",
        "la digitazione professionale richiede precisione costante anche durante le sessioni lunghe",
        "la ripetizione metodica degli esercizi porta alla formazione di abitudini motorie solide",
        "mantenere le unghie corte facilita la digitazione corretta con la punta delle dita",
        "la temperatura ambiente influisce sulla flessibilità delle dita durante la battitura",
        "esercitarsi su testi letterari arricchisce il vocabolario e migliora la battitura",
        "la coordinazione tra le due mani è essenziale per una digitazione fluida ed efficace",
        "la tastiera ergonomica riduce il rischio di sindrome del tunnel carpale nel tempo",
        "l'altezza della sedia influisce direttamente sulla postura durante la digitazione prolungata",
        "imparare i simboli e la punteggiatura accelera la scrittura di testi professionali",
        "la battitura ritmica assomiglia alla pratica musicale per la sua natura ripetitiva",
        "registrare i propri progressi motiva a continuare l'allenamento con costanza e impegno",
        "le dita anulari controllano lettere meno frequenti ma comunque importanti nella scrittura",
        "un polso affaticato è segnale che la postura di battitura deve essere corretta",
        "la digitazione veloce e precisa è apprezzata in molte professioni moderne e tecnologiche",
        "esercitarsi con bigrammi e trigrammi frequenti migliora notevolmente la velocità di battitura",
        "la posizione neutra delle mani riduce lo stress articolare durante la digitazione lunga",
        "un piano di allenamento strutturato porta a progressi più rapidi e duraturi nel tempo",
        "la dattilografia è una disciplina che combina abilità motoria e concentrazione mentale",
        "scrivere testi complessi senza errori richiede grande padronanza della tastiera italiana",
        "il pollice gestisce la barra spaziatrice che separa le parole durante la digitazione",
        "le dita medie controllano i tasti centrali della fila superiore della tastiera italiana",
        "un riscaldamento adeguato delle mani prima della digitazione previene i crampi muscolari",
        "la battitura a dieci dita è considerata la tecnica più efficiente tra quelle esistenti",
        "la velocità ottimale di battitura dipende sia dalla precisione sia dalla tecnica utilizzata",
        "imparare a digitare correttamente fin dall'inizio evita la correzione di cattive abitudini",
        "il tasto di ritorno a capo è fondamentale per la formattazione corretta dei documenti",
        "la dattilografia si insegnava nelle scuole commerciali come competenza professionale essenziale",
        "un dattilografo professionista produce pochissimi errori anche scrivendo ad alta velocità",
        "la pratica deliberata con obiettivi chiari porta a miglioramenti rapidi nella battitura",
        "la coordinazione occhio mano è potenziata dalla pratica regolare della dattilografia moderna",
        "usare abbreviazioni nei documenti senza comprometterne la chiarezza richiede esperienza pratica",
        "i tasti funzione nella riga superiore accelerano molte operazioni nei programmi di scrittura",
        "la battitura al computer ha sostituito quasi completamente la vecchia macchina da scrivere",
        "imparare la dattilografia da giovani facilita l'acquisizione di una tecnica corretta e fluida",
        "la corretta tecnica dattilografica riduce il rischio di infortuni da lavoro ripetitivo",
        "ogni errore commesso durante la pratica è un'opportunità per migliorare la tecnica personale",
        "la digitazione veloce e pulita è una risorsa preziosa in qualsiasi ambiente professionale",
        "il tasto cancella serve per correggere gli errori commessi durante la scrittura veloce",
        "la posizione standard delle mani sulla tastiera si chiama posizione di riposo o home row",
        "la dattilografia è apprezzata nei concorsi pubblici dove si verifica la velocità di battitura",
        "digitare lunghi documenti senza affaticarsi richiede tecnica corretta e allenamento progressivo",
        "la digitazione fluente libera la mente per concentrarsi sul contenuto del testo scritto",
        "ogni minuto di pratica quotidiana porta benefici concreti alla velocità e alla precisione",
        "la distanza tra la tastiera e il corpo influisce sulla correttezza della postura digitante",
        "il feedback audio della tastiera aiuta alcuni dattilografi a mantenere un ritmo costante",
        "le abbreviazioni tachigrafiche erano usate prima dei computer per velocizzare la scrittura",
        "la dattilografia rimane una competenza rilevante nonostante i progressi nel riconoscimento vocale",
        "la concentrazione durante la pratica è più utile della semplice quantità di tempo trascorso",
        "il numero di errori per minuto è un indicatore importante della qualità della battitura",
        "la dattilografia richiede pazienza e perseveranza prima di vedere risultati concreti",
        "i tasti di punteggiatura devono essere appresi con la stessa cura delle lettere alfabetiche",
        "allenarsi con testi a velocità crescente aiuta a superare i propri limiti progressivamente",
        "la fluidità nella digitazione si riconosce dal ritmo regolare e dalla mancanza di pause",
        "la pratica dattilografica migliorata incrementa anche la qualità del lavoro al computer",
        "utilizzare un timer durante gli esercizi aiuta a monitorare i progressi nella velocità",
        "la tecnica corretta si impara meglio con la guida di un insegnante esperto di dattilografia",
    ],
    "Difficile": [
        # originali
        "La velocità di battitura si misura in parole per minuto e un dattilografo esperto raggiunge facilmente le ottanta parole al minuto con grande precisione e costanza nel tempo",
        "Imparare a digitare senza guardare la tastiera è fondamentale per diventare un professionista e aumentare notevolmente la produttività lavorativa in qualsiasi ambiente di lavoro moderno",
        "La tecnica delle dieci dita prevede che ogni dito sia responsabile di specifici tasti riducendo i movimenti inutili e aumentando la velocità complessiva di digitazione professionale",
        "Un buon dattilografo mantiene sempre i polsi sollevati dalla scrivania e le dita curve sopra i tasti garantendo una postura ergonomica e prevenendo infortuni nel lungo periodo",
        "La pratica costante e metodica della dattilografia porta risultati straordinari nel corso delle settimane trasformando una scrittura lenta e incerta in una digitazione fluida e sicura",
        # nuove
        "La memoria muscolare che si sviluppa attraverso la pratica ripetuta della dattilografia permette alle dita di raggiungere i tasti corretti in modo automatico e quasi istintivo",
        "Coloro che imparano la tecnica corretta fin dalle prime sessioni evitano di dover correggere successivamente le cattive abitudini che rallentano la crescita della velocità di battitura",
        "La postura ergonomica durante la digitazione prolungata non solo previene dolori alla schiena e alle mani ma aumenta anche la produttività complessiva nel corso della giornata lavorativa",
        "Il ritmo regolare e la precisione sono le due qualità che un dattilografo professionista deve coltivare con pari attenzione poiché la velocità senza precisione produce testi pieni di errori",
        "La tastiera italiana presenta alcune differenze rispetto alla tastiera anglosassone che il dattilografo deve conoscere a fondo per poter sfruttare appieno la propria velocità di digitazione",
        "Gli studi ergonomici hanno dimostrato che una corretta configurazione della postazione di lavoro riduce significativamente il rischio di sviluppare patologie muscoloscheletriche legate alla digitazione prolungata",
        "La dattilografia è una disciplina che richiede dedizione e costanza nel tempo giacché i progressi sono graduali ma diventano evidenti dopo alcune settimane di allenamento quotidiano regolare",
        "Acquisire la capacità di digitare senza alzare lo sguardo dalla schermata rappresenta un salto qualitativo enorme che libera la mente per concentrarsi interamente sul contenuto che si sta producendo",
        "I concorsi nazionali di dattilografia premiano i partecipanti capaci di unire velocità elevata e tasso di errore minimo dimostrando che le due qualità non sono affatto in contraddizione tra loro",
        "La tecnica a dieci dita distribuisce equamente il carico di lavoro tra tutte le dita riducendo la fatica e permettendo sessioni di digitazione molto più lunghe senza dolori o crampi muscolari",
        "Digitare testi tecnici ricchi di terminologia specialistica richiede una padronanza della tastiera talmente profonda da rendere automatica la ricerca di caratteri insoliti e combinazioni poco frequenti",
        "La pratica della dattilografia in giovane età porta benefici che durano tutta la vita professionale rendendo più agevole qualsiasi attività lavorativa che preveda l'uso intensivo del computer",
        "Gli esperti consigliano di iniziare ogni sessione di allenamento con esercizi di riscaldamento per le dita e i polsi al fine di prevenire infortuni e preparare i muscoli alla digitazione intensa",
        "La velocità di battitura di un professionista qualificato supera spesso le cento parole al minuto il che equivale a produrre un testo di media lunghezza nel tempo di una sola pausa caffè",
        "Il software specializzato per l'allenamento dattilografico è in grado di analizzare in dettaglio le prestazioni dell'utente identificando le coppie di lettere che causano maggiori rallentamenti e imprecisioni",
        "Una sessione di allenamento ben strutturata alterna fasi di esercizio intenso con momenti di riposo attivo che includono stretching delle mani e dei polsi per mantenere i muscoli in salute",
        "La dattilografia professionale richiede non solo rapidità di esecuzione ma anche una profonda conoscenza delle regole ortografiche e grammaticali della lingua in cui si sta scrivendo il testo",
        "La scelta della tastiera giusta è una decisione importante per chi lavora molte ore al giorno davanti al computer poiché il tipo di meccanismo influenza il comfort e la velocità di battitura",
        "Il passaggio dalla tecnica di battitura a due dita alla tecnica a dieci dita richiede un periodo di adattamento durante il quale la velocità inizialmente diminuisce prima di crescere significativamente",
        "La coordinazione bimanuale sviluppata attraverso la dattilografia ha effetti positivi su altre attività motorie complesse come suonare uno strumento musicale o eseguire lavori di precisione artigianale",
        "I dattilografi più veloci del mondo raggiungono velocità superiori alle duecento parole al minuto durante le gare ufficiali dimostrando quanto possa essere estremo il perfezionamento di questa tecnica",
        "La corretta inclinazione del polso durante la digitazione è un aspetto spesso trascurato dai principianti ma fondamentale per evitare la sindrome del tunnel carpale nel corso degli anni",
        "Lavorare come trascrittore professionista richiede di mantenere una velocità sostenuta per periodi prolungati il che rende indispensabile una tecnica impeccabile e una resistenza fisica ben allenata",
        "La formazione dattilografica sistematica nelle scuole secondarie potrebbe ridurre notevolmente il tempo che gli studenti impiegano a completare i compiti scritti al computer aumentando la loro produttività",
        "Ogni lettera dell alfabeto italiano presenta una frequenza di utilizzo diversa e i layout di tastiera ergonomici sono progettati per assegnare i caratteri più usati alle dita più forti e abili",
        "La transizione verso la digitalizzazione di tutti i documenti ha reso la dattilografia una competenza ancora più importante di quanto non fosse ai tempi delle macchine da scrivere meccaniche",
        "Un errore di battitura in un documento ufficiale o in un codice informatico può avere conseguenze gravi il che sottolinea quanto sia importante sviluppare una tecnica precisa oltre che veloce",
        "La dattilografia richiede che il praticante sviluppi una forma di attenzione divisa capace di seguire contemporaneamente il testo da trascrivere e il ritmo delle proprie dita sulla tastiera",
        "I programmi di riconoscimento vocale hanno avanzato enormemente negli ultimi anni ma la digitazione manuale rimane più precisa e controllabile in molti contesti professionali e creativi",
        "La pratica della dattilografia sviluppa una forma di intelligenza cinestetica che consente alle mani di muoversi in modo preciso e rapido senza richiedere una supervisione cosciente continua",
        "La produttività di un ufficio moderno dipende in larga misura dalla velocità di battitura dei suoi dipendenti il che giustifica pienamente l investimento in corsi di formazione dattilografica professionale",
        "Coloro che digitano regolarmente grandi quantità di testo sviluppano nel tempo una sensibilita tattile fine che permette loro di percepire immediatamente quando un tasto non e stato premuto correttamente",
        "La dattilografia è una delle poche competenze manuali che rimane altamente rilevante nell'era digitale resistendo alla pressione di strumenti automatici come i correttori ortografici e i completatori di testo",
        "Il concetto di battitura toccata deriva dal fatto che un dattilografo esperto tocca ogni tasto con una pressione precisa e costante senza mai sbattere le dita con forza eccessiva sulla tastiera",
        "Imparare a sfruttare tutte le scorciatoie da tastiera disponibili nei software di produttività può raddoppiare l efficienza lavorativa di un professionista che lavora molte ore al giorno al computer",
        "La digitalizzazione massiva dei testi storici ha creato una grande domanda di dattilografi capaci di trascrivere manoscritti antichi con elevata precisione e profonda conoscenza delle lingue storiche",
        "Un allenamento dattilografico efficace deve includere testi di vario tipo compresi brani tecnici letterari e giornalistici per abituare le dita a tutte le possibili combinazioni di lettere in italiano",
        "La respirazione regolare e rilassata durante la digitazione è un dettaglio spesso ignorato che tuttavia contribuisce in modo significativo a mantenere la concentrazione e ridurre la tensione muscolare",
        "I test di velocità di battitura standardizzati utilizzano testi di difficoltà calibrata per garantire che i risultati siano comparabili tra diversi partecipanti indipendentemente dal contenuto specifico del brano",
        "La valutazione oggettiva della propria velocità di battitura attraverso test periodici è fondamentale per capire se il proprio metodo di allenamento sta producendo i miglioramenti desiderati nel tempo",
        "La dattilografia è una competenza che si acquisisce gradualmente attraverso centinaia di ore di pratica e che poi rimane stabile nel tempo purché si continui a usare la tastiera regolarmente",
        "Le ricerche sull apprendimento motorio dimostrano che brevi sessioni di pratica quotidiana sono più efficaci di lunghe sessioni sporadiche per sviluppare la fluidità nella digitazione a tastiera",
        "La corretta disposizione della postazione di lavoro compresa la distanza dallo schermo e l'altezza della sedia influisce in modo diretto sulla velocità e sulla precisione della battitura professionale",
        "Scrivere sotto dettatura è una forma avanzata di dattilografia che richiede di ascoltare elaborare e digitare quasi simultaneamente mettendo alla prova sia la tecnica sia la concentrazione dell'operatore",
        "La dattilografia veloce è un requisito esplicito in molte offerte di lavoro nel settore amministrativo giornalistico e informatico dove la produzione rapida di testi scritti è parte integrante del ruolo",
        "La precisione nella battitura è particolarmente critica nella programmazione informatica dove un singolo carattere errato può causare il blocco dell'intero programma o la perdita di dati importanti",
        "I dattilografi professionisti che lavorano nei tribunali o nelle camere legislative devono essere in grado di trascrivere il parlato in tempo reale con una precisione assoluta e senza mai perdere il filo",
        "La formazione dattilografica tradizionale si svolgeva su macchine da scrivere meccaniche la cui resistenza dei tasti sviluppava una forza nelle dita superiore a quella richiesta dalle moderne tastiere digitali",
        "La capacità di produrre grandi quantità di testo scritto in poco tempo è diventata una competenza trasversale fondamentale in un mondo professionale sempre più dominato dalla comunicazione digitale scritta",
        "Un dattilografo esperto riesce a mantenere la stessa velocità di battitura sia su tastiere meccaniche sia su tastiere a membrana adattandosi rapidamente alle diverse sensazioni tattili dei due tipi di dispositivo",
        "La dattilografia richiede un equilibrio sottile tra velocità e accuratezza poiché spingere troppo sulla velocità aumenta gli errori mentre concentrarsi troppo sulla precisione riduce il ritmo di produzione",
        "Lo sviluppo di applicazioni per dispositivi mobili ha creato nuove forme di digitazione su touchscreen che richiedono tecniche diverse dalla dattilografia classica ma ugualmente importanti nel mondo moderno",
        "La revisione attenta dei testi digitati e una fase importante del processo di scrittura professionale che richiede occhio critico e conoscenza approfondita delle norme ortografiche e grammaticali italiane",
        "Partecipare a gare di dattilografia online è un modo efficace e motivante per misurare i propri progressi e confrontarsi con altri praticanti provenienti da tutto il mondo in un contesto competitivo amichevole",
        "La digitalizzazione del lavoro d'ufficio ha trasformato la dattilografia da specializzazione di pochi a competenza di base attesa da quasi tutti i lavoratori indipendentemente dal settore di appartenenza",
        "Il tasso di accuratezza è spesso considerato un indicatore più importante della velocità grezza poiché un testo pieno di errori richiede tempo aggiuntivo per la correzione che annulla il vantaggio della velocità",
        "La dattilografia è una delle poche competenze in cui la pratica porta quasi inevitabilmente al miglioramento a condizione che si utilizzi una tecnica corretta e si pratichi con regolarità e attenzione",
        "Un corso di dattilografia ben strutturato guida il discente attraverso una progressione logica di esercizi partendo dai tasti di base fino ad arrivare ai caratteri speciali e alle combinazioni complesse",
        "La capacità di digitalizzare informazioni in modo rapido e preciso diventa sempre più preziosa man mano che il volume di dati che le organizzazioni devono gestire ogni giorno cresce in modo esponenziale",
        "Nonostante i progressi dell intelligenza artificiale la dattilografia manuale rimane insostituibile in molti contesti professionali dove la privacy la sicurezza e il controllo del contenuto sono prioritari",
        "La padronanza della tastiera numerica posizionata sul lato destro della tastiera standard aumenta notevolmente la velocità di inserimento di dati numerici nelle applicazioni finanziarie e contabili professionali",
        "La digitazione di testi in lingue straniere richiede la conoscenza dei layout di tastiera specifici di ogni lingua e una pratica supplementare per acquisire la stessa fluidità della propria lingua madre",
        "Le persone che hanno imparato la dattilografia in giovane età riportano spesso di non ricordare consciamente la posizione dei singoli tasti a dimostrazione di quanto profondamente la memoria muscolare si radichi",
        "Un dattilografo che lavora in ambienti ad alto stress come le redazioni giornalistiche deve saper mantenere velocità e precisione anche sotto pressione temporale intensa e con distrazioni sonore continue",
        "La dattilografia professionale non si limita alla semplice trascrizione ma include anche la formattazione corretta dei documenti la gestione degli stili e l'uso efficiente degli strumenti del programma di scrittura",
        "La crescente importanza della comunicazione scritta digitale rende la velocità di battitura un fattore di competitività personale sempre più rilevante nelle carriere professionali di ogni settore lavorativo",
        "Il miglioramento della velocità di battitura è un processo continuo che non ha un limite definito poiché anche i dattilografi più veloci possono sempre affinare la propria tecnica e aumentare ulteriormente la velocità",
        "Gli effetti positivi della pratica dattilografica si estendono oltre la semplice velocità includendo miglioramenti nella concentrazione nella pazienza e nella capacità di lavorare in modo sistematico e metodico",
        "La scelta tra tastiera italiana e tastiera internazionale dipende dalle esigenze specifiche del dattilografo e dal tipo di testi che si trovera più frequentemente a produrre nel corso della propria carriera",
        "Un ambiente di lavoro silenzioso e privo di distrazioni favorisce la concentrazione necessaria per mantenere alta la precisione durante sessioni di digitazione lunghe è particolarmente impegnative dal punto di vista cognitivo",
        "La dattilografia rimane una delle competenze fondamentali insegnate nei corsi di segretariato e amministrazione aziendale confermando la sua rilevanza pratica nell organizzazione del lavoro moderno",
        "La padronanza della tastiera consente di trasformare i pensieri in testo scritto con minima frizione cognitiva permettendo al dattilografo esperto di concentrarsi interamente sulla qualità del contenuto prodotto",
        "La resistenza fisica delle mani e dei polsi si costruisce progressivamente attraverso l'allenamento regolare e non deve essere forzata con sessioni troppo lunghe specialmente nelle prime settimane di pratica",
        "I professionisti che digitano per molte ore al giorno dovrebbero seguire il principio delle pause attive alzandosi regolarmente e eseguendo esercizi di mobilità per prevenire problemi muscoloscheletrici cronici",
        "La dattilografia è uno di quegli strumenti trasparenti che quando padroneggiati scompaiono dalla coscienza del praticante permettendogli di focalizzarsi completamente sul significato di ciò che sta scrivendo",
        "L investimento di tempo nella formazione dattilografica si ripaga rapidamente considerando che le ore guadagnate grazie a una maggiore velocità di battitura si accumulano significativamente nel corso degli anni",
        "La tecnica dattilografica corretta è quella che consente di produrre il massimo numero di parole al minuto con il minimo dispendio di energia muscolare e il minor numero possibile di errori di battitura",
        "Imparare a correggere gli errori in modo efficiente senza interrompere il ritmo di scrittura è una competenza avanzata che distingue il dattilografo esperto da chi è ancora agli inizi del proprio percorso formativo",
        "La costanza nell'allenamento è la qualità più importante per chi vuole diventare un dattilografo veloce poiché nessun talento naturale può compensare la mancanza di pratica regolare e sistematica nel tempo",
        "La dattilografia professionale in italiano richiede particolare attenzione alla corretta gestione delle lettere accentate e degli apostrofi che compaiono frequentemente e richiedono l'uso di tasti specifici",
        "La scrittura veloce al computer ha cambiato il modo in cui le persone pensano e comunicano favorendo uno stile più spontaneo e informale che si avvicina alla conversazione orale rispetto alla scrittura tradizionale",
        "La capacità di produrre testi coerenti e ben strutturati a velocità elevata distingue il dattilografo professionista da chi sa semplicemente premere i tasti senza una strategia comunicativa consapevole",
        "La dattilografia e una competenza trasversale che trova applicazione in tutti i settori produttivi dalla sanita alla finanza dall'istruzione alla pubblica amministrazione rendendo chi la padroneggia più competitivo",
        "La pratica della copiatura di testi classici della letteratura italiana offre contemporaneamente un esercizio dattilografico efficace e un arricchimento culturale che va ben oltre la semplice velocità di battitura",
        "Il monitoraggio continuo della propria velocità e del tasso di errori permette di individuare con precisione le aree di debolezza sulle quali concentrare lo sforzo nelle sessioni di allenamento successive",
        "La dattilografia professionale moderna si estende ben oltre la semplice battitura includendo la capacità di formattare correttamente documenti complessi e di navigare con fluidità tra le funzioni dei software di scrittura",
        "Sviluppare una velocità di battitura elevata richiede di superare una serie di plateau nei quali le prestazioni sembrano stagnare prima di fare un balzo qualitativo verso un livello superiore di competenza",
        "I benefici della dattilografia si manifestano non solo nell efficienza lavorativa ma anche nella qualità cognitiva generale poiché la pratica regolare rafforza la concentrazione la memoria e la coordinazione neuromotoria",
        "La tastiera rimane lo strumento di input principale per i professionisti del sapere e investire nel perfezionamento della tecnica dattilografica è quindi un investimento diretto nella propria produttività e carriera",
        "La dattilografia di precisione richiesta nei servizi di sottotitolazione in tempo reale dimostra fino a che punto possa essere spinta questa competenza quando le circostanze professionali lo rendono necessario e premiante",
        "Il passaggio da una digitazione lenta e incerta a una fluente e automatica segna una trasformazione profonda nel rapporto tra la persona e il computer rendendolo uno strumento naturale di espressione del pensiero",
        "Coloro che si allenano sistematicamente con software dedicati riportano miglioramenti significativi nella velocità di battitura già dopo quattro settimane di pratica quotidiana di soli venti minuti ben focalizzati",
        "La dattilografia rappresenta un ponte tra il pensiero e la sua espressione scritta e quanto più questo ponte e solido e rapido tanto più il professionista può dedicarsi alla qualità del contenuto che produce",
        "La precisione nella battitura si costruisce attraverso la ripetizione consapevole di esercizi mirati che portano il sistema nervoso a codificare i movimenti corretti come risposta automatica agli stimoli visivi del testo",
        "La dattilografia unisce tecnica corporea e disciplina mentale in un equilibrio unico che quando raggiunto trasforma ogni sessione di scrittura in un atto fluido preciso e quasi meditativo nella sua regolarità ritmica",
    ],
}
# ─── Layout fisico tastiera QWERTY (righe dall'alto verso il basso) ───────────
KEYBOARD_ROWS = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],   # riga superiore
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],         # home row
    ["z", "x", "c", "v", "b", "n", "m"],                   # riga inferiore
    ["à", "è", "ì", "ò", "ù"],                             # tasti accentati italiani
]

# ─── Colore assegnato a ogni dito — palette normale ───────────────────────────
FINGER_COLORS = {
    "mignolo_sx": "#e74c3c",   # rosso
    "anulare_sx": "#e67e22",   # arancione
    "medio_sx":   "#f1c40f",   # giallo
    "indice_sx":  "#2ecc71",   # verde
    "indice_dx":  "#3498db",   # blu
    "medio_dx":   "#9b59b6",   # viola
    "anulare_dx": "#1abc9c",   # verde acqua
    "mignolo_dx": "#e91e63",   # rosa
    "pollice":    "#95a5a6",   # grigio (barra spazio)
}

# ─── Palette Okabe-Ito per daltonismo (deuteranopia / protanopia) ─────────────
# Evita coppie rosso/verde che risultano indistinguibili per i daltonici.
# Fonte: https://jfly.uni-koeln.de/color/
FINGER_COLORS_COLORBLIND = {
    "mignolo_sx": "#E69F00",   # arancione caldo
    "anulare_sx": "#56B4E9",   # celeste
    "medio_sx":   "#F0E442",   # giallo
    "indice_sx":  "#009E73",   # verde-blu
    "indice_dx":  "#0072B2",   # blu scuro
    "medio_dx":   "#D55E00",   # arancione bruciato
    "anulare_dx": "#CC79A7",   # viola-rosa
    "mignolo_dx": "#648FFF",   # blu lavanda
    "pollice":    "#BBBBBB",   # grigio chiaro
}

# ─── Colori feedback testo nell'area di digitazione ───────────────────────────
# 'normal'     → verde/rosso/blu  (palette classica)
# 'colorblind' → celeste/arancione/giallo  (Okabe-Ito)
TEXT_COLORS = {
    "normal": {
        "correct_fg": "#a6e3a1",   # verde → carattere corretto
        "wrong_fg":   "#1e1e2e",
        "wrong_bg":   "#f38ba8",   # rosso → errore
        "cursor_fg":  "#1e1e2e",
        "cursor_bg":  "#89b4fa",   # blu → posizione attuale
        "pending_fg": "#45475a",   # grigio → non ancora digitato
    },
    "colorblind": {
        "correct_fg": "#56B4E9",   # celeste → carattere corretto
        "wrong_fg":   "#1e1e2e",
        "wrong_bg":   "#FE6100",   # arancione → errore
        "cursor_fg":  "#1e1e2e",
        "cursor_bg":  "#F0E442",   # giallo → posizione attuale
        "pending_fg": "#45475a",
    },
}


def get_finger_colors(colorblind: bool = False) -> dict:
    """Restituisce la palette colori dita in base alla modalità attiva."""
    return FINGER_COLORS_COLORBLIND if colorblind else FINGER_COLORS


def get_text_colors(colorblind: bool = False) -> dict:
    """Restituisce i colori del feedback testo in base alla modalità attiva."""
    return TEXT_COLORS["colorblind" if colorblind else "normal"]

# ─── Nome leggibile di ogni dito (mostrato nel suggerimento durante l'esercizio) ──
FINGER_NAMES = {
    "mignolo_sx": "Mignolo sinistro",
    "anulare_sx": "Anulare sinistro",
    "medio_sx":   "Medio sinistro",
    "indice_sx":  "Indice sinistro",
    "indice_dx":  "Indice destro",
    "medio_dx":   "Medio destro",
    "anulare_dx": "Anulare destro",
    "mignolo_dx": "Mignolo destro",
    "pollice":    "Pollice (spazio)",
}

# ─── Mappatura tasto → dito responsabile (tecnica 10 dita) ───────────────────
# Ogni lettera è assegnata al dito che la tecnica a 10 dita prescrive.
KEY_FINGER = {
    # Mignolo sinistro: colonna sinistra
    "q": "mignolo_sx", "a": "mignolo_sx", "z": "mignolo_sx",
    # Anulare sinistro
    "w": "anulare_sx", "s": "anulare_sx", "x": "anulare_sx",
    # Medio sinistro
    "e": "medio_sx",   "d": "medio_sx",   "c": "medio_sx",
    # Indice sinistro: copre due colonne (r-f-v e t-g-b)
    "r": "indice_sx",  "f": "indice_sx",  "v": "indice_sx",
    "t": "indice_sx",  "g": "indice_sx",  "b": "indice_sx",
    # Indice destro: copre due colonne (y-h-n e u-j-m)
    "y": "indice_dx",  "h": "indice_dx",  "n": "indice_dx",
    "u": "indice_dx",  "j": "indice_dx",  "m": "indice_dx",
    # Medio destro
    "i": "medio_dx",   "k": "medio_dx",
    # Anulare destro
    "o": "anulare_dx", "l": "anulare_dx",
    # Mignolo destro: colonna destra + tasti accentati italiani
    "p": "mignolo_dx",
    "è": "mignolo_dx", "é": "mignolo_dx",
    "à": "mignolo_dx", "ì": "mignolo_dx", "ò": "mignolo_dx", "ù": "mignolo_dx",
    # Pollici → barra spazio
    " ": "pollice",
}

# "><(((º> sabusabu <º)))><"
