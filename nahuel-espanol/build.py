# Genera los guiones de la cuenta de español de Nahuel (HTML -> PDF y guiones.md).
# Los guiones se hablan en inglés (el público aprende español); las notas de dirección van en castellano.
# [AJUSTAR] = dato personal de Nahuel que hay que confirmar o reemplazar antes de grabar.
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
FONTS = pathlib.Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else ""
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"

# pilar -> estilo de edición del repo que mejor le queda
P_STORY = "MI HISTORIA"
P_METHOD = "EL MÉTODO"
P_APPS = "APPS Y HERRAMIENTAS"
P_LESSON = "MINI CLASE"
P_POLY = "4 IDIOMAS"

S = [
    # ---------------- MI HISTORIA ----------------
    dict(pillar=P_STORY, title="I Speak 4 Languages and I'm Not Gifted", edit="Cine Frame", length="35-45 s", kw="ZERO",
         hook="I'm 25, I'm from Argentina, and I speak four languages. And no, I'm not gifted.",
         alts=["Four languages by 25. Here's the part nobody wants to hear.",
               "People think I have a talent for languages. I have a system."],
         body=["Spanish is my native language. Then came English, then French, then Italian. [AJUSTAR: en qué orden y a qué edad]",
               "And for years I did it the school way: grammar charts, vocabulary lists, tests. I could conjugate a verb, but I couldn't order a coffee.",
               "What changed everything was simple: I stopped studying the language and started living in it.",
               "Music, series, YouTube, people, all in that language. Speaking before I felt ready. Every single day, even for 15 minutes.",
               "That's it. That's the 'talent'.",
               "So now I want to do it the other way around: teach you Spanish the way I actually learned my languages."],
         screen=["4 LANGUAGES · 25 YEARS OLD", "NOT TALENT → A SYSTEM", "STUDY IT ✗ · LIVE IN IT ✓"],
         cta="Comment ZERO and I'll send you the exact plan I'd follow to learn Spanish from zero.",
         note="Video de presentación. Fijalo arriba en el perfil. Mirá a cámara, tono de charla, sin apuro. Si sabés decir una frase en cada idioma, metela al inicio como golpe de 3 segundos."),
    dict(pillar=P_STORY, title="Years of Classes vs. a Few Months of This", edit="Cine Frame", length="35-45 s", kw="ZERO",
         hook="I took English classes for years. I learned more in [AJUSTAR: 3] months doing this.",
         alts=["School didn't teach me English. This did.",
               "If you took Spanish in high school and remember nothing, this is for you."],
         body=["In school I had English for years. [AJUSTAR: cuántos años] I knew the rules, I passed the exams… and the first time a native spoke to me, I froze.",
               "Then [AJUSTAR: qué pasó: un viaje, un trabajo, una serie, una pareja, un amigo] and suddenly I had a reason to understand.",
               "I watched things I actually liked, with subtitles in English. I repeated sentences out loud like a crazy person. I talked to people and made a million mistakes.",
               "In a few months I could hold a conversation. Not perfect. Real.",
               "The difference wasn't the teacher. It was hours of real language, and having a reason.",
               "If you took Spanish in high school and remember nothing, it's not your fault. You just never got enough real Spanish."],
         screen=["YEARS OF CLASSES → FROZE", "[AJUSTAR] MONTHS OF REAL INPUT → TALKING", "IT'S NOT YOUR FAULT"],
         cta="Follow me and I'll show you how to get those hours of real Spanish without moving to another country.",
         note="Contá TU historia real. Si no hubo viaje, mejor: el mensaje 'se puede sin mudarte' vende más."),
    dict(pillar=P_STORY, title="My Most Embarrassing Language Mistake", edit="B-roll + stacked text", length="30-40 s", kw="OOPS",
         hook="I once said something in Italian so wrong the whole table went silent.",
         alts=["Every language learner has this story. Here's mine.",
               "Never say 'estoy embarazada' when you're embarrassed. But first, my worst one."],
         body=["[AJUSTAR: tu error real en italiano/francés/inglés, contado con detalle: dónde estabas, qué quisiste decir, qué dijiste, cómo reaccionaron]",
               "And you know what? I never made that mistake again. That's the thing about mistakes: the embarrassing ones are the ones you remember forever.",
               "In Spanish, the classic one for English speakers is this: you want to say 'I'm embarrassed' and you say 'estoy embarazada'.",
               "Which means… 'I'm pregnant.'",
               "If you're embarrassed, say 'me da vergüenza' or 'qué vergüenza'.",
               "So go make mistakes. They're the fastest teacher you'll ever have."],
         screen=["ESTOY EMBARAZADA = I'M PREGNANT 🤰", "ME DA VERGÜENZA = I'M EMBARRASSED"],
         cta="Comment your worst language mistake. I'll read the best ones in my next video.",
         note="Este tipo de video junta muchos comentarios: el CTA pide historias, no keyword. Las mejores respuestas = próximo video."),
    dict(pillar=P_STORY, title="What 4 Languages Actually Gave Me", edit="Cine Frame", length="30-40 s", kw="ZERO",
         hook="Nobody tells you the real reason to learn a language. It's not your résumé.",
         alts=["Learning languages changed my life, and not how you think.",
               "Here's what speaking 4 languages actually feels like."],
         body=["Yes, it helps with work. [AJUSTAR: un ejemplo concreto: un trabajo, un cliente, un viaje]",
               "But the real thing is this: in every language you get a slightly different version of yourself.",
               "I'm funnier in Spanish. More direct in English. [AJUSTAR: cómo sos en francés e italiano]",
               "You get to laugh at jokes you'd never understand. Have conversations with people you'd never meet. Feel at home in places that aren't yours.",
               "And Spanish opens more doors than almost any other language: more than 20 countries and around 500 million native speakers.",
               "That's what you're really learning. Not words. Access."],
         screen=["NOT YOUR RÉSUMÉ", "20+ COUNTRIES · ~500M NATIVE SPEAKERS", "NOT WORDS. ACCESS."],
         cta="Follow if you want that version of yourself in Spanish. I'll show you how, step by step.",
         note="Video emocional, ideal con música suave y B-roll de viajes/calle. Ritmo lento."),

    # ---------------- EL MÉTODO ----------------
    dict(pillar=P_METHOD, title="How I'd Learn Spanish in 3 Months (Starting From Zero)", edit="Glass explainer", length="50-60 s", kw="ROADMAP",
         hook="If I had to learn Spanish from zero in 3 months, this is exactly what I'd do.",
         alts=["3 months, 1 hour a day. Here's the plan.",
               "You can't be fluent in 3 months. But you can do this."],
         body=["First, let's be honest: in 3 months you won't be fluent. But you can hold a real, simple conversation. That's the goal.",
               "Month 1: sounds and words. Spanish only has 5 vowel sounds, learn them in week one. Then the 500 most common words with a flashcard app, 20 minutes a day.",
               "Plus 20 minutes of easy Spanish you can almost understand. Videos made for learners. Don't study it, just watch.",
               "Month 2: open your mouth. A tutor online, 2 or 3 times a week. Learn the past tense. Write 5 lines a day about your day.",
               "Month 3: conversations. Three a week, minimum. Series with Spanish subtitles. And write down the 20 mistakes you make the most, and fix only those.",
               "One hour a day. Every day. That's 90 hours. Most people never get there in years of classes."],
         screen=["MONTH 1 · SOUNDS + 500 WORDS", "MONTH 2 · TUTOR + PAST TENSE", "MONTH 3 · 3 CONVERSATIONS/WEEK", "1 HOUR/DAY = 90 HOURS"],
         cta="Comment ROADMAP and I'll send you the full 3-month plan, day by day.",
         note="Pieza central de la cuenta: el 'ROADMAP' es el imán de leads (PDF gratis por DM con ManyChat). Hacé carrusel del mismo tema."),
    dict(pillar=P_METHOD, title="How I'd Learn Spanish in 6 Months", edit="Glass explainer", length="50-60 s", kw="ROADMAP",
         hook="6 months is the sweet spot. Here's how I'd use every one of them.",
         alts=["Give me 6 months and 1 hour a day, and this is what you'll be able to do.",
               "The 6-month Spanish plan I wish someone gave me."],
         body=["With 6 months you can go from zero to real conversations about almost anything in your daily life.",
               "Months 1 and 2: the base. Sounds, the 1,000 most common words, present tense, and one magic structure: 'voy a' plus a verb, to talk about the future.",
               "Months 3 and 4: speaking. A tutor twice a week, a language exchange once a week. Past tenses. Podcasts on your commute.",
               "Months 5 and 6: living in Spanish. Your phone in Spanish. Series without English subtitles. Think in Spanish when you're alone: 'now I'm cooking, now I'm going to the store.'",
               "The secret isn't the plan. It's not breaking the chain. A bad 15-minute day still counts."],
         screen=["MONTHS 1-2 · THE BASE", "MONTHS 3-4 · SPEAKING", "MONTHS 5-6 · LIVE IN SPANISH", "DON'T BREAK THE CHAIN"],
         cta="Comment ROADMAP and I'll send you the plan for 3, 6 and 12 months.",
         note="Serie: grabá 3, 6 y 12 meses el mismo día, misma ropa y luz. Publicalos en días seguidos y referenciá el anterior ('ayer te di el de 3 meses')."),
    dict(pillar=P_METHOD, title="Fluent in Spanish in 1 Year: The Real Plan", edit="Glass explainer", length="50-60 s", kw="ROADMAP",
         hook="One year is enough to get fluent in Spanish. If you do it like this.",
         alts=["Fluent in a year isn't a dream. It's math.",
               "Here's what one year of Spanish looks like when you do it right."],
         body=["One hour a day for a year is about 365 hours. Add the music, the series and the podcasts and you're way past that.",
               "Quarter 1: the base. Sounds, the most common words, present and future.",
               "Quarter 2: speaking. Tutor, language exchange, past tenses. You'll feel stupid. Good. That's the phase where most people quit.",
               "Quarter 3: volume. Series, podcasts, books for learners. Start the subjunctive, slowly.",
               "Quarter 4: real life. A trip, a Spanish-speaking friend, a job, a class in Spanish about something you love, like cooking or salsa.",
               "Fluent doesn't mean perfect. It means you can live your life in Spanish. And a year is enough."],
         screen=["365 DAYS × 1 HOUR", "Q1 BASE · Q2 SPEAK · Q3 VOLUME · Q4 REAL LIFE", "FLUENT ≠ PERFECT"],
         cta="Comment ROADMAP and I'll send you the full one-year plan.",
         note="Remarcá el 'Q2 es donde la gente abandona': genera identificación y comentarios."),
    dict(pillar=P_METHOD, title="If I Started From Zero Today: Week 1", edit="Explainer panel", length="45-55 s", kw="ROADMAP",
         hook="If I had to start Spanish from zero today, this is what I'd do this week.",
         alts=["Day 1 of Spanish. Do this, not Duolingo.",
               "Your first week of Spanish, done right."],
         body=["Day 1: the 5 vowels. A, E, I, O, U. In Spanish they always sound the same. That alone fixes half your accent.",
               "Day 2: greetings and the 20 words you'll use every day. Hola, gracias, por favor, quiero, tengo, ¿dónde está…?",
               "Day 3: 'quiero' plus anything. Quiero un café. Quiero ir. Quiero aprender español. One verb, a hundred sentences.",
               "Day 4: watch 20 minutes of Spanish for beginners. Understand 10%? Perfect.",
               "Day 5: say 10 sentences out loud about yourself. Record them.",
               "Day 6 and 7: repeat everything. And change your phone to Spanish.",
               "One week. You already speak more Spanish than after a semester of school."],
         screen=["A · E · I · O · U", "QUIERO + ___", "PHONE → ESPAÑOL"],
         cta="Comment ROADMAP and I'll send you weeks 2, 3 and 4.",
         note="Pronunciá bien cada vocal con pausa; poné el texto grande. Que se pueda guardar: decí 'guardalo para el lunes'."),
    dict(pillar=P_METHOD, title="Stop Studying Grammar First", edit="Fitted stacked captions", length="30-40 s", kw="ZERO",
         hook="If you're starting Spanish with grammar, you're doing it backwards.",
         alts=["Grammar first is why you quit Spanish last time.",
               "Kids don't learn grammar. They learn to talk. Then grammar."],
         body=["Nobody learned their first language with a conjugation chart.",
               "You heard it thousands of times, you understood a little more every day, and one day you started talking.",
               "With Spanish, do the same: first understand a lot, then speak, then use grammar to fix what you already say.",
               "Grammar is a map. But you need to have walked the city first, or the map means nothing.",
               "I'm not saying ignore it. I'm saying put it in third place."],
         screen=["1 · UNDERSTAND", "2 · SPEAK", "3 · GRAMMAR"],
         cta="Follow me if you want to learn Spanish the way you learned your first language.",
         note="Opinión fuerte = comentarios a favor y en contra. Respondé los que discuten con un video."),
    dict(pillar=P_METHOD, title="Talk About the Future With One Trick", edit="Fitted stacked captions", length="25-35 s", kw="ROADMAP",
         hook="Here's a Spanish cheat code nobody teaches you in week one.",
         alts=["Skip the future tense. Use this instead.",
               "Learn this and you can talk about your whole week in Spanish."],
         body=["The future tense in Spanish has its own conjugations. You don't need them yet.",
               "Just use 'voy a' plus any verb. Exactly like 'I'm going to' in English.",
               "Voy a comer. I'm going to eat. Voy a viajar. I'm going to travel. Voy a aprender español. I'm going to learn Spanish.",
               "Change who's doing it: vas a, va a, vamos a, van a.",
               "Vamos a ver. We're going to see. Natives say that all the time.",
               "One structure, and you can talk about everything you're going to do."],
         screen=["VOY A + VERB = I'M GOING TO", "VOY A COMER · I'M GOING TO EAT", "VAMOS A VER · WE'LL SEE"],
         cta="Comment 'voy a' plus what you're going to do this weekend. In Spanish. I'll correct you.",
         note="CTA de práctica: comentarios en español. Respondé a muchos con corrección amable: el algoritmo lo premia y la gente vuelve."),

    # ---------------- APPS ----------------
    dict(pillar=P_APPS, title="Ranking Every App to Learn Spanish", edit="Ranking format", length="45-60 s", kw="APPS",
         hook="I ranked the apps to learn Spanish from useless to life-changing.",
         alts=["The apps I used to learn 3 languages, ranked.",
               "Duolingo is NOT number one. Here's my ranking."],
         body=["[AJUSTAR: confirmá cuáles usaste vos y reordená según tu experiencia real]",
               "Number 6: Duolingo. Great to build the habit, terrible to actually speak. Use it as a warm-up, not as your method.",
               "Number 5: HelloTalk or Tandem. Free chats with natives. Amazing once you know the basics.",
               "Number 4: Language Reactor. Netflix and YouTube with two subtitles at the same time. Click any word and get the translation.",
               "Number 3: Anki. Flashcards that show you a word right before you forget it. Boring. It works.",
               "Number 2: Dreaming Spanish. Hours of videos in easy Spanish, by level. This is where you learn to understand.",
               "Number 1: a real tutor on italki or Preply. Thirty minutes of talking beat ten hours of apps. Speaking is the skill, and only speaking trains it."],
         screen=["6 DUOLINGO", "5 HELLOTALK / TANDEM", "4 LANGUAGE REACTOR", "3 ANKI", "2 DREAMING SPANISH", "1 A REAL TUTOR"],
         cta="Comment APPS and I'll send you how I'd combine them in a daily routine.",
         note="Usá el skill de ranking-format. Mostrá cada app en pantalla (grabación del celu). Antes de publicar verificá que cada app siga existiendo y con ese nombre."),
    dict(pillar=P_APPS, title="Duolingo Won't Make You Fluent (Use It Like This)", edit="Split reel", length="30-40 s", kw="APPS",
         hook="I have to tell you something about your 400-day Duolingo streak.",
         alts=["Duolingo won't make you fluent. But it can help, if you do this.",
               "Why you have a huge streak and still can't talk."],
         body=["Duolingo is great at one thing: making you open the app every day. That's valuable.",
               "But tapping words on a screen isn't speaking. And it's not listening to real people talking fast.",
               "So keep it, but change its job. Five minutes of Duolingo as a warm-up.",
               "Then 20 minutes of real Spanish you enjoy. And at least once a week, a real conversation.",
               "Your streak shows discipline. Now point that discipline at the right thing."],
         screen=["STREAK ≠ SPEAKING", "5 MIN DUOLINGO", "20 MIN REAL SPANISH", "1 CONVERSATION/WEEK"],
         cta="Comment your streak. I'll tell you what to add to it.",
         note="Arriba: animación de racha que se rompe; abajo vos. No le pegues a la app: el tono es 'cambiale el rol'."),
    dict(pillar=P_APPS, title="How to Learn Spanish With Netflix (The Right Way)", edit="Split reel", length="40-50 s", kw="SERIES",
         hook="Watching Netflix in Spanish won't teach you anything. Unless you do it like this.",
         alts=["The right way to learn Spanish with series.",
               "I learned [AJUSTAR: inglés/italiano] with series. Here's the method."],
         body=["If you put on a series in Spanish with English subtitles, you're reading English. Not learning Spanish.",
               "Step 1: pick something you've already seen in English. You know the story, so you can focus on the words.",
               "Step 2: Spanish audio, Spanish subtitles. Use Language Reactor to see the translation only when you need it.",
               "Step 3: pause when you hear something useful and repeat it out loud. Same speed, same tone.",
               "Shows I'd start with: La casa de papel for Spain, Club de Cuervos for Mexico, and El Eternauta for Argentina.",
               "One episode a day, done like this, beats a whole season binged in English."],
         screen=["ENGLISH SUBS ✗", "SPANISH AUDIO + SPANISH SUBS ✓", "PAUSE · REPEAT", "🇪🇸 LA CASA DE PAPEL · 🇲🇽 CLUB DE CUERVOS · 🇦🇷 EL ETERNAUTA"],
         cta="Comment SERIES and I'll send you my list of the best series by level.",
         note="Mostrá Language Reactor en pantalla. Confirmá que las series sigan en Netflix en EE. UU. antes de publicar."),

    # ---------------- MINI CLASES ----------------
    dict(pillar=P_LESSON, title="Spanish Mistakes That Make Natives Laugh", edit="B-roll + stacked text", length="35-45 s", kw="ERRORES",
         hook="Five Spanish mistakes English speakers make, and number 2 is dangerous.",
         alts=["Please don't say 'estoy caliente'.",
               "These words look like English. They're a trap."],
         body=["One: 'estoy embarazada' doesn't mean embarrassed. It means pregnant. Say 'me da vergüenza'.",
               "Two: 'estoy caliente' for 'I'm hot'. That means you're… in the mood. Say 'tengo calor'.",
               "Three: 'realizar' is not 'to realize'. It means to carry out. 'I realized' is 'me di cuenta'.",
               "Four: 'actualmente' is not 'actually'. It means currently. 'Actually' is 'en realidad'.",
               "Five: 'estoy excitado'. Same problem as number two. Say 'estoy emocionado'.",
               "Save this before you embarrass yourself. I mean… before 'te da vergüenza'."],
         screen=["EMBARAZADA = PREGNANT", "ESTOY CALIENTE ✗ → TENGO CALOR ✓", "REALIZE = DARSE CUENTA", "ACTUALLY = EN REALIDAD", "EXCITED = EMOCIONADO"],
         cta="Follow for part 2. I've got 20 more of these.",
         note="Formato con más potencial viral de la lista. Cara de sorpresa en el número 2. Hacé partes 2, 3, 4 si funciona."),
    dict(pillar=P_LESSON, title="Ser vs. Estar in 30 Seconds", edit="Fitted stacked captions", length="25-35 s", kw="ZERO",
         hook="Get ser and estar wrong and you'll insult someone. Watch.",
         alts=["Ser vs estar, the only explanation you need.",
               "One letter changes 'I'm bored' into 'I'm boring'."],
         body=["'Soy aburrido' means I'm a boring person. 'Estoy aburrido' means I'm bored right now.",
               "'Es listo' means he's smart. 'Está listo' means he's ready.",
               "'Es rico' means he's rich. 'Está rico' means it's delicious. Please don't mix those up at dinner.",
               "Easy rule to start: ser is what something is. Estar is how it is right now.",
               "It's not perfect, but it'll get you right most of the time."],
         screen=["SOY ABURRIDO = I'M BORING", "ESTOY ABURRIDO = I'M BORED", "ES RICO = HE'S RICH", "ESTÁ RICO = IT'S DELICIOUS", "SER = WHAT IT IS · ESTAR = HOW IT IS NOW"],
         cta="Comment one sentence with ser and one with estar. I'll correct them.",
         note="Gestos exagerados en cada par. Pocas palabras en pantalla, grandes."),
    dict(pillar=P_LESSON, title="Things Textbooks Teach That Natives Never Say", edit="Split reel", length="30-40 s", kw="NATIVO",
         hook="Your Spanish textbook is making you sound like a robot.",
         alts=["Nobody talks like your Spanish textbook.",
               "Textbook Spanish vs. real Spanish."],
         body=["Textbook: 'Estoy bien, gracias, ¿y usted?' Real life: 'Todo bien, ¿y vos?' or '¿y tú?'",
               "Textbook: '¿Cómo estás?' Real life: '¿Qué tal?', '¿Todo bien?', '¿Qué onda?'",
               "Textbook: 'Muy bien.' Real life: 'Dale', 'Vale', 'Perfecto'. 'Vale' in Spain, 'dale' in Argentina.",
               "Textbook: 'No tengo problema.' Real life: 'No pasa nada.'",
               "Learn the textbook version to be correct. Learn this version to sound human."],
         screen=["📕 ESTOY BIEN, ¿Y USTED?", "🗣️ TODO BIEN, ¿Y VOS?", "📕 MUY BIEN → 🗣️ DALE / VALE", "📕 NO TENGO PROBLEMA → 🗣️ NO PASA NADA"],
         cta="Comment NATIVO and I'll send you 30 more phrases natives actually use.",
         note="Arriba: hoja de libro vieja vs. chat de WhatsApp. Actuá los dos personajes (robot vs. vos)."),
    dict(pillar=P_LESSON, title="Argentine Spanish Explained in 40 Seconds", edit="Cutout backdrop", length="35-45 s", kw="ARGENTINA",
         hook="This is Spanish. But if you learned it in school, you won't understand a word.",
         alts=["Why Argentines sound different from every other Spanish speaker.",
               "I'm Argentine. Let me explain our Spanish."],
         body=["One: we say 'vos' instead of 'tú'. Not '¿tú tienes?', it's '¿vos tenés?'",
               "Two: the 'll' and the 'y' sound like 'sh'. 'Yo me llamo' sounds like 'sho me shamo'.",
               "Three: 'che'. It means 'hey'. We put it everywhere. '¿Che, venís?'",
               "Four: 're'. It means 'very'. 'Re bueno', 're lindo', 're cansado'.",
               "Five: 'dale'. OK, let's go, sure, deal. One word, a thousand uses.",
               "Should you learn Argentine Spanish first? Probably not. Learn neutral Spanish, then pick an accent you love. But if you fall in love with this one, I'm here."],
         screen=["TÚ → VOS", "LL / Y → 'SH'", "CHE = HEY", "RE = VERY", "DALE = OK"],
         cta="Comment ARGENTINA if you want a full series on our Spanish.",
         note="Fondos: Buenos Aires, mate, fútbol, asado. Este es tu diferencial: nadie lo puede contar como vos. Serie propia."),
    dict(pillar=P_LESSON, title="You Already Know Hundreds of Spanish Words", edit="Fitted stacked captions", length="25-35 s", kw="ZERO",
         hook="If you speak English, you already know hundreds of Spanish words. You just don't know it yet.",
         alts=["Learn this one trick and your Spanish vocabulary explodes.",
               "English words that turn into Spanish with one change."],
         body=["Words that end in '-tion' in English usually end in '-ción' in Spanish. Nation, nación. Information, información. Conversation, conversación.",
               "'-ty' becomes '-dad'. City, ciudad. University, universidad. Reality, realidad.",
               "'-ly' becomes '-mente'. Rapidly, rápidamente. Exactly, exactamente.",
               "It doesn't work every time, but it works a lot.",
               "So no, you're not starting from zero. You're starting with a head start."],
         screen=["-TION → -CIÓN", "-TY → -DAD", "-LY → -MENTE", "YOU'RE NOT AT ZERO"],
         cta="Comment a '-tion' word in Spanish. Let's see how many we get.",
         note="Mensaje motivador: baja la barrera de entrada para el que nunca empezó. Bueno para anuncios también."),
    dict(pillar=P_LESSON, title="5 Phrases That Make You Sound Native", edit="B-roll + stacked text", length="30-40 s", kw="NATIVO",
         hook="Say these 5 phrases and people will think you've lived in Latin America.",
         alts=["5 tiny phrases natives use all day.",
               "Want to sound less like a student? Use these."],
         body=["'No pasa nada.' No problem, it's fine. Someone apologizes? 'No pasa nada.'",
               "'¿En serio?' Seriously? Use it with drama.",
               "'Me da igual.' I don't mind, either way.",
               "'Qué lástima.' What a shame.",
               "'Ya está.' Done, that's it. You finish something, you say 'ya está'.",
               "Pick one today and use it five times. Tomorrow, the next one."],
         screen=["NO PASA NADA", "¿EN SERIO?", "ME DA IGUAL", "QUÉ LÁSTIMA", "YA ESTÁ"],
         cta="Comment NATIVO and I'll send you the full list of 30.",
         note="Cada frase con mini escena actuada (B-roll tuyo). Ritmo rápido."),

    # ---------------- 4 IDIOMAS ----------------
    dict(pillar=P_POLY, title="'I Love You' in the 4 Languages I Speak", edit="Cutout grid (4 flags)", length="25-35 s", kw="ZERO",
         hook="I speak four languages. Here's how 'I love you' changes in each one.",
         alts=["One sentence, four languages, four different feelings.",
               "Spanish has two ways to say 'I love you'. Use the wrong one and it's awkward."],
         body=["English: I love you. One phrase for your partner, your mom and pizza.",
               "French: Je t'aime. Careful, add 'bien' and it gets weaker: 'je t'aime bien' is more like 'I like you'.",
               "Italian: Ti amo for your partner. Ti voglio bene for family and friends.",
               "Spanish does the same thing: 'te amo' is deep, romantic love. 'Te quiero' is for family, friends, and the start of a relationship.",
               "Say 'te amo' on the second date and… good luck."],
         screen=["🇺🇸 I LOVE YOU", "🇫🇷 JE T'AIME", "🇮🇹 TI AMO · TI VOGLIO BENE", "🇦🇷 TE AMO · TE QUIERO"],
         cta="Follow me. Next: the same sentence in 4 languages, and which one is the hardest.",
         note="Formato serie: 'Same sentence in 4 languages'. Repetilo con 'I'm hungry', 'I miss you', insultos suaves, etc. Grilla con 4 banderas."),
    dict(pillar=P_POLY, title="Which of My 4 Languages Is Easiest for English Speakers?", edit="Cutout grid (4 flags)", length="35-45 s", kw="ZERO",
         hook="I speak four languages. Here's the easiest one for English speakers. It's not French.",
         alts=["Easiest language to learn if you speak English? I speak 4. Here's my answer.",
               "Spanish vs French vs Italian: which one should you learn?"],
         body=["French: beautiful, but you write 'eau' and say 'o'. Half the letters are silent. Hard to read out loud.",
               "Italian: great pronunciation, but fewer speakers and fewer places to practice.",
               "Spanish: you say it exactly how it's written. Five vowels, always the same sound.",
               "Thousands of words you already know from English. Around 500 million native speakers, and in the US you'll hear it everywhere.",
               "Easy to read, useful to speak, and somebody to practice with in every city. That's Spanish."],
         screen=["🇫🇷 HARD TO READ", "🇮🇹 FEWER SPEAKERS", "🇪🇸 SAY IT HOW IT'S WRITTEN", "~500M NATIVE SPEAKERS"],
         cta="Follow and I'll show you how to start this week.",
         note="Opinión de alguien que habla los 4 = autoridad. Esperá debate en comentarios (franceses ofendidos = alcance)."),
    dict(pillar=P_POLY, title="Learn Spanish, Get Italian (Almost) Free", edit="Split reel", length="30-40 s", kw="ZERO",
         hook="Learn Spanish and you get half of Italian for free. I'm the proof.",
         alts=["Why my third and fourth languages were so much faster.",
               "The hidden bonus of learning Spanish."],
         body=["When I learned Italian, I already had Spanish. And a lot of it was the same.",
               "'Tengo hambre' in Spanish. 'Ho fame' in Italian. 'J'ai faim' in French. Same idea: you 'have' hunger.",
               "'La casa', 'la casa'. 'Bueno', 'buono'. 'Mañana', 'domani'… OK, not all of them.",
               "Spanish, Italian, French and Portuguese all come from Latin. Learn one well, and the next one is way faster.",
               "So Spanish isn't just one language. It's a door to four."],
         screen=["TENGO HAMBRE · HO FAME · J'AI FAIM", "BUENO → BUONO", "1 LANGUAGE → 4 DOORS"],
         cta="Comment which language you'd learn after Spanish.",
         note="Decí las frases con acento de cada idioma; ese cambio de voz es el gancho visual."),
]

# ---------------- HTML / PDF ----------------
def esc(s): return html.escape(s, quote=False)
N = len(S)
cover = f'''<section class="page cover">
  <div class="eyebrow">NAHUEL CASARTELLI · SPANISH ACCOUNT · [AJUSTAR @HANDLE]</div>
  <h1>Learn Spanish<br><span>con Nahuel</span></h1>
  <p class="lead">{N} guiones listos para grabar. Se hablan en inglés, el español va en pantalla. Cada uno trae hook, 2 hooks alternativos, cuerpo, texto en pantalla, CTA y el estilo de edición del repo que le corresponde.</p>
  <div class="facts">
    <div><span>MI HISTORIA</span><b>{sum(s["pillar"]==P_STORY for s in S)} guiones</b></div>
    <div><span>EL MÉTODO</span><b>{sum(s["pillar"]==P_METHOD for s in S)} guiones</b></div>
    <div><span>APPS</span><b>{sum(s["pillar"]==P_APPS for s in S)} guiones</b></div>
    <div><span>MINI CLASES</span><b>{sum(s["pillar"]==P_LESSON for s in S)} guiones</b></div>
  </div>
  <div class="box"><div class="bh"><em>!</em>ANTES DE GRABAR</div><div class="core">
    <p>Todo lo marcado <b class="kw">[AJUSTAR]</b> es un dato tuyo (años, orden de los idiomas, apps que usaste, tu error más vergonzoso). Reemplazalo por lo real: la historia verdadera es lo que hace viral a este tipo de cuenta.</p>
    <p>No lo leas palabra por palabra. Aprendete el hook exacto y los puntos; el resto decilo con tus palabras.</p>
    <p>Las palabras clave (ROADMAP, APPS, SERIES, NATIVO, ARGENTINA, ERRORES) se responden por DM con ManyChat. ROADMAP es el imán principal: un PDF con el plan de 3, 6 y 12 meses.</p>
  </div></div>
  <div class="foot"><span>LEARN SPANISH CON NAHUEL · GUIONES</span><span>00 / {N:02d}</span></div>
</section>'''
pages = [cover]
for i, s in enumerate(S):
    cta_html = esc(s["cta"]).replace(s["kw"], f'<span class="kw">{s["kw"]}</span>', 1)
    body = "".join(f"<p>{esc(p)}</p>" for p in s["body"]).replace("[AJUSTAR", '<b class="adj">[AJUSTAR').replace("]</p>", "]</b></p>")
    scr = "".join(f"<i>{esc(t)}</i>" for t in s["screen"])
    pages.append(f'''<section class="page">
  <div class="eyebrow">NAHUEL CASARTELLI · LEARN SPANISH</div>
  <div class="top"><span class="sc"><i></i>SCRIPT {i+1} OF {N}</span><span class="tag">{esc(s["pillar"])}</span></div>
  <h2>{esc(s["title"])}</h2>
  <div class="facts">
    <div><span>EDICIÓN</span><b>{esc(s["edit"])}</b></div>
    <div><span>DURACIÓN</span><b>{s["length"]}</b></div>
    <div><span>IDIOMA</span><b>Inglés + ES en pantalla</b></div>
    <div><span>KEYWORD</span><b class="kw">{s["kw"]}</b></div>
  </div>
  <div class="box"><div class="bh"><em>01</em>HOOK · 0-3 S</div><p class="hook">“{esc(s["hook"])}”</p>
    <div class="alts"><span>HOOKS ALTERNATIVOS · PROBÁ LOS 3</span>{"".join(f"<p>“{esc(h)}”</p>" for h in s["alts"])}</div></div>
  <div class="box"><div class="bh"><em>02</em>CUERPO</div><div class="core">{body}</div></div>
  <div class="box"><div class="bh"><em>03</em>TEXTO EN PANTALLA</div><div class="scr">{scr}</div></div>
  <div class="box cta"><div class="bh"><em>04</em>CTA</div><p class="hook">“{cta_html}”</p></div>
  <div class="box note"><div class="bh"><em>✎</em>DIRECCIÓN</div><p>{esc(s["note"])}</p></div>
  <div class="foot"><span>LEARN SPANISH CON NAHUEL · {esc(s["pillar"])}</span><span>{i+1:02d} / {N:02d}</span></div>
</section>''')

CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #0b0d12; font-family: Inter, Arial, sans-serif; color: #f4f5f8; }
.page { width: 8.5in; height: 11in; padding: 0.55in 0.6in 0.6in; position: relative; overflow: hidden; break-after: page; background: #0b0d12; }
.page:last-child { break-after: auto; }
.eyebrow { font-size: 8pt; font-weight: 700; letter-spacing: .1em; color: #74acdf; }
.foot { position: absolute; left: .6in; right: .6in; bottom: .38in; display: flex; justify-content: space-between; border-top: .75pt solid #1e222c; padding-top: 9pt; font-size: 7pt; letter-spacing: .06em; color: #646a78; }
.tag { font-size: 7.3pt; font-weight: 700; letter-spacing: .1em; padding: 3pt 9pt; border-radius: 10pt; color: #f6b40e; background: rgba(246,180,14,.14); }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 14pt; }
.sc { font-size: 8pt; font-weight: 700; letter-spacing: .08em; color: #74acdf; display: flex; align-items: center; gap: 8pt; }
.sc i { width: 14pt; height: 1.5pt; background: #74acdf; display: inline-block; }
h1 { font-size: 46pt; font-weight: 800; line-height: 1.05; margin-top: 1.4in; }
h1 span { color: #74acdf; font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-weight: 600; }
.lead { font-size: 12pt; color: #a7adbb; line-height: 1.6; margin-top: 18pt; max-width: 6in; }
.cover .facts { margin-top: 28pt; }
.cover .box { margin-top: 22pt; }
h2 { font-size: 19pt; font-weight: 800; margin-top: 8pt; line-height: 1.2; }
.facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7pt; margin-top: 12pt; }
.facts div { background: #13161d; border: .75pt solid #222733; border-radius: 6pt; padding: 9pt 10pt 10pt; }
.facts span { display: block; font-size: 6.8pt; letter-spacing: .06em; color: #646a78; margin-bottom: 6pt; }
.facts b { font-size: 9.2pt; font-weight: 700; }
.kw { color: #74acdf; font-weight: 700; }
.adj { color: #f6b40e; font-weight: 600; }
.box { background: #13161d; border: .75pt solid #222733; border-radius: 7pt; padding: 10pt 12pt; margin-top: 8pt; }
.bh { font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; color: #646a78; margin-bottom: 6pt; }
.bh em { font-style: normal; color: #74acdf; font-size: 9.6pt; margin-right: 7pt; }
.hook { font-size: 10.4pt; font-weight: 700; line-height: 1.42; }
.core p { font-size: 8.6pt; color: #b3b8c4; line-height: 1.6; }
.core p + p { margin-top: 4pt; }
.scr { display: flex; flex-wrap: wrap; gap: 5pt; }
.scr i { font-style: normal; font-size: 7.6pt; font-weight: 700; letter-spacing: .03em; padding: 3pt 7pt; border-radius: 4pt; background: rgba(116,172,223,.12); color: #a9cdee; }
.box.cta { background: #0f1a2a; border-color: #29507a; }
.alts { margin-top: 7pt; padding-top: 7pt; border-top: .75pt solid #222733; }
.alts span { display: block; font-size: 6.6pt; font-weight: 700; letter-spacing: .08em; color: #646a78; margin-bottom: 3pt; }
.alts p { font-size: 8.5pt; color: #b3b8c4; line-height: 1.5; }
.box.note p { font-size: 8.1pt; color: #a7adbb; font-style: italic; line-height: 1.6; }
"""

doc = f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Learn Spanish con Nahuel</title><style>{FONTS}</style><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
src = HERE / "_tmp.html"; src.write_text(doc)
pdf = HERE / "NahuelCasartelli_LearnSpanish_Guiones.pdf"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", str(src)], check=True, stderr=subprocess.DEVNULL)
src.unlink()

# misma data en markdown, para leer desde el celular
md = ["# Learn Spanish con Nahuel · Guiones", "",
      f"{N} guiones. Se hablan en inglés; el español va en pantalla. `[AJUSTAR]` = dato tuyo a confirmar.", ""]
for i, s in enumerate(S):
    md += [f"## {i+1}. {s['title']}", "",
           f"**Pilar:** {s['pillar']} · **Edición:** {s['edit']} · **Duración:** {s['length']} · **Keyword:** `{s['kw']}`", "",
           f"**Hook (0-3 s):** \"{s['hook']}\"", "", "**Hooks alternativos:**"] + [f"- \"{h}\"" for h in s["alts"]] + \
          ["", "**Cuerpo:**", ""] + [f"> {p}\n>" for p in s["body"]] + \
          ["", "**Texto en pantalla:** " + " · ".join(f"`{t}`" for t in s["screen"]), "",
           f"**CTA:** \"{s['cta']}\"", "", f"*Dirección: {s['note']}*", "", "---", ""]
(HERE / "guiones.md").write_text("\n".join(md))
print(pdf)
