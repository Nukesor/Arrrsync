import re


def escape(unescaped):
    if isinstance(unescaped, list):
        escaped = []
        for item in unescaped:
            escaped.append(unescape(item))
    elif isinstance(unescaped, str):
        escaped = unescaped.replace(' ', '\ ')
        escaped = escaped.replace('&', '\&')
        escaped = escaped.replace('(', '\(')
        escaped = escaped.replace(')', '\)')
        escaped = escaped.replace('[', '\[')
        escaped = escaped.replace(']', '\]')
        escaped = escaped.replace('{', '\{')
        escaped = escaped.replace('}', '\}')
        escaped = escaped.replace("'", "\'")

    return escaped


def unescape(escaped):
    if isinstance(escaped, list):
        unescaped = []
        for item in escaped:
            unescaped.append(unescape(item))
    elif isinstance(escaped, str):
        unescaped = escaped.replace('\ ', ' ')
        unescaped = unescaped.replace('\&', '&')
        unescaped = unescaped.replace('\(', '(')
        unescaped = unescaped.replace('\)', ')')
        unescaped = unescaped.replace('\[', '[')
        unescaped = unescaped.replace('\]', ']')
        unescaped = unescaped.replace('\{', '{')
        unescaped = unescaped.replace('\}', '}')
        unescaped = unescaped.replace("\'", "'")

    return unescaped


def argsplit(command_list):
    splitted = re.split(r"((?<!\\)\s)", command_list)
    fixed = filter(lambda a: a != ' ', splitted)
    return list(fixed)
