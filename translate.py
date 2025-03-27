import csv
import json
import datetime
import random

MC_ENGLISH_FILE = 'en_us.json' # English translation file from minecraft.jar/assets/lang
VOCAB_CSV = 'vocab.csv'
PHRASES_CSV = 'phrases.csv'
TRANSLATION_OVERRIDES = 'translation_overrides.json'
RESOURCE_PACK_ROOT = 'scc_resourcepack'
MC_PIDGIN_FILE_OUT = RESOURCE_PACK_ROOT + '/assets/pidgincraft/lang/pidgin_scc.json'

PACK_MCMETA = RESOURCE_PACK_ROOT + '/pack.mcmeta'
METADATA_DESC = 'Seattle Conlang Club PidginCraft translation resource pack'

STOP_WORDS = ['in', 'at', 'on', 'to', 'is', 'be', 'yes', 'no']

mc_lang_en = json.load(open(MC_ENGLISH_FILE))

# Load in the Pidgin dictionary CSV

dict_eng_pidgin = {} # eng to pidgin dictionary

def add_word(word_entry):
    for sense in word['English definition'].replace(';', ',').split(','):
        sense = sense.lower().strip()
        if sense not in dict_eng_pidgin:
            dict_eng_pidgin[sense] = word['Pidgin word']
        else:
            dict_eng_pidgin[sense] += '/' + word['Pidgin word']

for word in csv.DictReader(open(VOCAB_CSV)):
    add_word(word)

for word in csv.DictReader(open(PHRASES_CSV)):
    add_word(word)

del dict_eng_pidgin['?'] # The English translation of an ambiguous pidgin word is always '?'

# Build the MC translation JSON for the pidgin

mc_lang_pidgin = {}

for [key, translation] in mc_lang_en.items():
    translation = translation.lower().strip()
    if len(translation) == 0:
        mc_lang_pidgin[key] = ''
        continue

    if (
        key.startswith('menu.') or
        key.startswith('options.') or
        key.startswith('pack.') or
        key.startswith('chat.') or
        key.startswith('chunk.') or
        key.startswith('commands.') or
        key.startswith('addServer.') or
        key.startswith('accessibility.') or
        key.startswith('argument.') or
        key.startswith('arguments.') or
        key.startswith('telemetry') or
        key.startswith('attribute.modifier.') or
        key.startswith('enchantment.level.')
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
            random.shuffle(pidgin_words)
            mc_lang_pidgin[key] = '? ' + ' '.join(pidgin_words) + ' ?'
        else:
            mc_lang_pidgin[key] = '???'

# If translations are explicitly defined in the overrides file, use those
overrides = json.load(open(TRANSLATION_OVERRIDES))
for key, translation in overrides.items():
    mc_lang_pidgin[key] = translation

# Write translations
json.dump(mc_lang_pidgin, open(MC_PIDGIN_FILE_OUT, 'w'), indent=2)

# Update pack.mcmeta with date of creation
with open(PACK_MCMETA) as pack_mcmeta_file:
    metadata = json.load(pack_mcmeta_file)
metadata['pack']['description'] = METADATA_DESC + ' ' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d UTC')
json.dump(metadata, open(PACK_MCMETA, 'w'), indent=2)

print("Finished creating MC translation file")