#!/usr/bin/env python3

import collections
import graphlib
from pathlib import Path
import pprint

class trie_node(dict):
    name = None

    def __missing__(self, key):
        self[key] = trie_node()
        self[key][''] = 0
        return self[key]

    @property
    def key(self):
        return tuple(sorted(self.items()))

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

emoji = trie_node()

LEVEL = {
    "unqualified" : 1,
    "component" : 2,
    "minimally-qualified" : 3,
    "fully-qualified" : 4,
}

def load():
    """
    Load the emoji.
    """

    emoji_test_text = Path(__file__).parent / "emoji-test.txt"
    lines = emoji_test_text.read_text().splitlines()

    for l in lines:
        l = l.partition("#")[0].strip()
        if not l:
            continue

        codepoints, qualifier = l.split(";")

        level = LEVEL[qualifier.strip()]

        d = emoji

        for i in codepoints.strip().split():
            i = chr(int(i, 16))
            d = d[i]

        d[''] = level

    emoji[''] = 0


def merge(d):
    """
    Merge tries with identical subtrees.
    """

    unique_tries = { }

    def pass1(d):
        unique_tries[d] = d
        for v in d.values():
            if type(v) is not int:
                pass1(v)

    def pass2(d):
        d = unique_tries[d]

        for k, v in d.items():
            if type(v) is not int:
                d[k] = pass2(v)

        return d

    pass1(d)
    return pass2(d)

dict_by_name = { }

def assign_names(d):
    """
    Assigns a unique name to each trie node.
    """

    serial = 0

    def assign(d):
        if type(d) is int or type(d) is str:
            return

        if d.name is not None:
            return

        nonlocal serial
        d.name = f"e{serial}"
        dict_by_name[d.name] = d
        serial += 1

        for v in d.values():
            assign(v)

    assign(d)
    d.name = "emoji"
    dict_by_name[d.name] = d

order = [ ]

def sort():
    """
    Sorts the dicts into dependency order.
    """

    graph = { }

    def add(d):
        graph[d.name] = {v.name for v in d.values() if type(v) is not int}

        for v in d.values():
            if type(v) is not int:
                add(v)

    add(emoji)

    ts = graphlib.TopologicalSorter(graph)

    global order
    order = list(ts.static_order())

def generate(f, d):
    """
    Generates Python code for a trie node.
    """

    l = [ f"{d.name} = {{" ]

    for k in sorted(d.keys()):
        v = d[k]
        if type(v) is int:
            l.append(f"'{k}': {v},")
        else:
            l.append(f"'{k}': {v.name},")

    l.append("}")

    print(" ".join(l), file=f)


def main():

    dest = Path(__file__).parent.parent.parent / "renpy"/ "text"/ "emoji_trie.py"

    with open(dest, "w") as f:

        print("""\
# This file is generated by module/emoji/make_emoji_trie.py. Do not
# edit it directly.
#
# Emoji trie data.
#
#
# It contains a data structure that can be used to determine if a
# sequence of codepoints is an emoji and if it should be rendered
# in an emoji font.
#
# Each trie node is a dictionary mapping codepoints to other dictionaries.
# If a codepoint is not present in the dictionarly, look up the '' key
# in the dictionary to find what it maps to. (It will be one of the constants
# below.
#
# The top-level dictionary is named emoji.

# The codepoint is not an emoji.
NOT_EMOJI = 0

# The codepoints are an emoji, but it may or may not be rendered in an emoji font.
UNQUALIFIED = 1

# The codepoints are part of a larger emoji sequence, and should be rendered
# in an emoji font when standing alone.
COMPONENT = 2

# The codepoints are an emoji, and should be rendered in an emoji font, but
# aren't fully qualified.
MINIMALLY_QUALIFIED = 3

# The codepoints are an emoji, and should be rendered in an emoji font.
QUALIFIED = 4

""", file=f)

        global emoji

        load()
        emoji = merge(emoji)
        assign_names(emoji)
        sort()

        for name in order:
            generate(f, dict_by_name[name])

if __name__ == "__main__":
    main()
