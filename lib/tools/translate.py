from opencc import OpenCC


def translate_simp_to_trad(lines):

    cc = OpenCC('s2t')

    result = [cc.convert(line) for line in lines]

    return result
