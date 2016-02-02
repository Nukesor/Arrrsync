import re


def escape(string):
    string = string.replace(' ', '\ ')
    string = string.replace('&', '\&')
    string = string.replace('(', '\(')
    string = string.replace(')', '\)')
    string = string.replace('[', '\[')
    string = string.replace(']', '\]')
    string = string.replace('{', '\{')
    string = string.replace('}', '\}')
    string = string.replace("'", "\'")

    return string


def unescape(string):
    string = string.replace('\ ', ' ')
    string = string.replace('\&', '&')
    string = string.replace('\(', '(')
    string = string.replace('\)', ')')
    string = string.replace('\[', '[')
    string = string.replace('\]', ']')
    string = string.replace('\{', '{')
    string = string.replace('\}', '}')
    string = string.replace("\'", "'")

    return string


def reassemble_command(command_list):
    splitted = re.split(r"((?<!\\)\s)", command_list)
    fixed = filter(lambda a: a != ' ', splitted)

    return list(fixed)
