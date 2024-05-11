stopwords = {"a", "à", "ao", "aos", "às","as", "da", "das", "do", "dos", "duma", "dum", "dumas", "duns",
             "é", "ela", "elas", "ele", "eles", "em", "essa", "esse", "essas", "esses",
             "esta", "este", "estas", "estes", "o", "os", "e","de", "que", "um", "uma", "para", "não", "com",
             "no", "por", "mais", "como", "mas", "foi", "ao", "tem", "seu", "sua", "ou", "ser", "quando",
             "muito", "há", "já", "está", "também", "só", "pelo", "pela", "até", "isso", "entre", "depois",
             "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você",
             "tinha", "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos",
             "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas",
             "este", "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua",
             "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas",
             "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão",
             "estive", "esteve", "estivemos", "estiveram", "estava", "estávamos", "estavam", "estivera",
             "esteja", "estejamos", "estejam", "estivermos", 
             }

commands = {"!stats",
            "!stats!user=", 
            "!stats!channel=", 
            "!stats!word=",
            "!vaidormir",
            "!acorda",
            "!intensity=",
            "!nuke",
            "!4,8,15,16,23,42"}


##########################
def validate_word(word):
    if word in stopwords:
        return False
    
    for cmd in commands:
        if cmd in word:
            return False
        
    return True