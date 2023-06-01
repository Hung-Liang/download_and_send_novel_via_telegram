from opencc import OpenCC


def translate_simp_to_trad(lines):
    """Translate the text from simplified Chinese to traditional Chinese.

    Args:
        `lines`: The text to be translated.

    Returns:
        `result`: The translated text.
    """

    cc = OpenCC('s2t')

    result = [cc.convert(line) for line in lines]

    return result
