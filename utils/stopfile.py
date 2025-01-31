stopwords_pt = ["a","à","ao","aos","às","as","da","das","do","dos","duma","dum","dumas","duns","é","ela","elas","ele","eles",
            "em","essa","esse","essas","esses","esta","este","estas","estes","o","os","e","de","que","um","uma","para",
            "não","no","por","mais","como","mas","foi","ao","tem","seu","sua","ser","quando","muito","há","já","está","também",
            "só","pelo","pela","até","isso","entre","depois","sem","mesmo","aos","ter","seus","quem","nas","me","esse","eles",
            "estão","você","tinha","foram","essa","nem","suas","meu","às","minha","têm","numa","pelos","havia","seja","qual",
            "será","nós","tenho","lhe","deles","essas","esses","pelas","este","fosse","dele","tu","te","vocês","vos","lhes",
            "meus","minhas","teu","tua","teus","tuas","nossa","nossos","nossas","delas","esta","estes","estas","aquele","aquela",
            "aqueles","aquelas","isto","aquilo","estou","está","estamos","estão","estive","esteve","estivemos","estiveram","estava",
            "estávamos","estavam","estivera","esteja","estejamos","estejam","estivermos", "eu", "com", "na", "se", "ainda", "nao", "ou"]


stopwords_eng = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
                'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
                'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
                'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
                'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
                'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
                'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
                's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
                'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
                'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
                "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
                'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


commands = ["!acorda", "!vaidormir", "!intensity", "!status", "!get_guild_data", "!get_guild_history", "!clean_data", "!roast",
            "!fortuneteller", "!vocabulary", "!nuke", "!defuse", "!russianroulette", "!hardcoreroulette", "glockroulette",
            "!ak47roulette", "!deathroll", "!highscores", "!mistery", "!huggies", "!sacrifice", "!get_shrekt", "!get_super_shrekt",
            "!list_events", "!stats", "!stats_uset", "!stats_words", "!stats_channel"]

##########################
def validate_word(word: str) -> bool:
    if word in stopwords_pt:
        return False
    
    if word in stopwords_eng:
        return False

    if word in commands:
        return False
    
    return True
