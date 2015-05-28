 # -*- coding: utf-8 -*-





def run_filter(text, and_list=[], or_list=[]):
    AND_KEYWORDS = and_list
    OR_KEYWORDS = or_list


    def is_keywords_inside(text):
        if AND_KEYWORDS:
            return is_and_keywords_inside(text, AND_KEYWORDS)

        if OR_KEYWORDS:
            return is_or_keywords_inside(text, OR_KEYWORDS)

        return True

    lines = text.splitlines()
    output_lines = filter(is_keywords_inside, lines)
    return output_lines

def is_and_keywords_inside(text, and_keywords):
    for keyword in and_keywords:
        if keyword not in text:
            return False
    return True


def is_or_keywords_inside(text, or_keywords):
    for keyword in or_keywords:
        if keyword in text:
            return True
    return False

def _print(it):
    print it


if __name__ == '__main__':
    OR_KEYWORDS = []
    AND_KEYWORDS = ['IN', 'rakmod']
    FILE_NAME = '1.txt'

    def main():
        import sys
        with open(FILE_NAME, 'r') as f:
            text = f.read()
        output_lines = run_filter(text, AND_KEYWORDS, OR_KEYWORDS)
        map(_print, output_lines)

    main()