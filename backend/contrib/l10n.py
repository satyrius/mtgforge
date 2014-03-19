EN = 'en'
RU = 'ru'
TW = 'tw'
CN = 'cn'
DE = 'de'
FR = 'fr'
IT = 'it'
JP = 'jp'
KO = 'ko'
PT = 'pt'
ES = 'es'

LANG_MAP = {
    'English': EN,
    'Russian': RU,
    'Chinese Traditional': TW,
    'Chinese Simplified': CN,
    'German': DE,
    'French': FR,
    'Italian': IT,
    'Japanese': JP,
    'Korean': KO,
    'Portuguese (Brazil)': PT,
    'Portuguese': PT,
    'Spanish': ES,
}

LANG_NAMES = {v: k for k, v in LANG_MAP.items()}


def get_code(name):
    return LANG_MAP[name]


def get_name(code):
    return LANG_NAMES[code]
