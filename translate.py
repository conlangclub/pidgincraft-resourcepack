import csv
import json
import datetime

MC_ENGLISH_FILE = 'en_us.json' # English translation file from minecraft.jar/assets/lang
VOCAB_CSV = 'vocab.csv'
RESOURCE_PACK_ROOT = 'scc_resourcepack'
MC_PIDGIN_FILE_OUT = RESOURCE_PACK_ROOT + '/assets/pidgincraft/lang/pidgin_scc.json'

PACK_MCMETA = RESOURCE_PACK_ROOT + '/pack.mcmeta'
METADATA_DESC = 'Seattle Conlang Club PidginCraft translation resource pack'

STOP_WORDS = ['in', 'at', 'on', 'to', 'is', 'be', 'yes', 'no']

mc_lang_en = json.load(open(MC_ENGLISH_FILE))

# Load in the Pidgin dictionary CSV

dict_eng_pidgin = {} # eng to pidgin dictionary

for word in csv.DictReader(open(VOCAB_CSV)):
    for sense in word['English definition'].replace(';', ',').split(','):
        sense = sense.lower().strip()
        if sense not in dict_eng_pidgin:
            dict_eng_pidgin[sense] = word['Pidgin word']
        else:
            dict_eng_pidgin[sense] += '/' + word['Pidgin word']

del dict_eng_pidgin['?'] # The English translation of an ambiguous pidgin word is always '?'

# Build the MC translation JSON for the pidgin

mc_lang_pidgin = {}

for [key, translation] in mc_lang_en.items():
    translation = translation.lower().strip()
    if translation == "crafting table":
        print("a")

    if (
        key.startswith('menu.') or
        key.startswith('options.') or
        key.startswith('pack.') or
        key.startswith('chat.')
    ): # do not touch menu/option strings
        mc_lang_pidgin[key] = mc_lang_en[key]
    elif translation in dict_eng_pidgin:
        mc_lang_pidgin[key] = dict_eng_pidgin[translation]
    else:
        pidgin_words = []
        for token in translation.split():
            if token.startswith("%"): # Minecraft uses tokens starting with % to interpolate values, like tool durability
                pidgin_words.append(token)
            elif token in dict_eng_pidgin and token not in STOP_WORDS:
                pidgin_words.append(dict_eng_pidgin[token])

        if len(pidgin_words) > 0:
            mc_lang_pidgin[key] = '? ' + ' '.join(pidgin_words) + ' ?'
        else:
            mc_lang_pidgin[key] = '???'

json.dump(mc_lang_pidgin, open(MC_PIDGIN_FILE_OUT, 'w'), indent=2)

# Update pack.mcmeta with date of creation
with open(PACK_MCMETA) as pack_mcmeta_file:
    metadata = json.load(pack_mcmeta_file)
metadata['pack']['description'] = METADATA_DESC + ' ' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d UTC')
json.dump(metadata, open(PACK_MCMETA, 'w'), indent=2)

print("Finished creating MC translation file")