
#   Copyright (c) 2015 Martin F. Falatic
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
Typical names for segments:

    /-----------\   /-----------\
   ||    'a'    || ||    'b'    ||
    \-----------/   \-----------/
   /-\ /--\      /-\      /--\ /-\
  |   |\   \    |   |    /   /|   |
  |   | \   \   |   |   /   / |   |
  |'h'|  \'k'\  |'m'|  /'n'/  |'c'|
  |   |   \   \ |   | /   /   |   |
  |   |    \   \|   |/   /    |   |
   \-/      \--/ \-/ \--/      \-/
    /-----------\   /-----------\
   ||    'u'    || ||    'p'    ||
    \-----------/   \-----------/
   /-\      /--\ /-\ /--\      /-\
  |   |    /   /|   |\   \    |   |
  |   |   /   / |   | \   \   |   |
  |'g'|  /'t'/  |'s'|  \'r'\  |'d'|
  |   | /   /   |   |   \   \ |   |
  |   |/   /    |   |    \   \|   |
   \-/ \--/      \-/      \--/ \-/
    /-----------\   /-----------\
   ||    'f'    || ||    'e'    ||
    \-----------/   \-----------/

Bit as int hex pos/bit values:

    /-----------\   /-----------\
   ||    1-1    || ||    3-1    ||
    \-----------/   \-----------/
   /-\ /--\      /-\      /--\ /-\
  |   |\   \    |   |    /   /|   |
  |   | \   \   |   |   /   / |   |
  |1-2|  \1-4\  |3-8|  /3-4/  |3-2|
  |   |   \   \ |   | /   /   |   |
  |   |    \   \|   |/   /    |   |
   \-/      \--/ \-/ \--/      \-/
    /-----------\   /-----------\
   ||    1-8    || ||    2-8    ||
    \-----------/   \-----------/
   /-\      /--\ /-\ /--\      /-\
  |   |    /   /|   |\   \    |   |
  |   |   /   / |   | \   \   |   |
  |0-2|  /0-4/  |0-8|  \2-4\  |2-2|
  |   | /   /   |   |   \   \ |   |
  |   |/   /    |   |    \   \|   |
   \-/ \--/      \-/      \--/ \-/
    /-----------\   /-----------\
   ||    0-1    || ||    2-1    ||
    \-----------/   \-----------/

"""

DIGIT_POLYS_ALPHA_16_DP = dict([
    ('f',  {'pts': [ (8,160),   (20,151),  (48,151),  (45,165), (14,165), ]}),
    ('g',  {'pts': [ (6,156),   (2,151),   (14,84),   (21,84),  (26,90),  (15,149), ]}),
    ('t',  {'pts': [ (50,92),   (47,111),  (19,146),  (24,123), ]}),
    ('s',  {'pts': [ (54,92),   (66,92),   (57,148),  (44,148), ]}),

    ('a',  {'pts': [ (42,2),    (74,2),    (71,17),   (44,17),  (37,5), ]}),
    ('h',  {'pts': [ (35,6),    (41,18),   (30,73),   (21,80),  (15,80),  (28,15), ]}),
    ('k',  {'pts': [ (44,22),   (57,52),   (53,72),   (41,42), ]}),
    ('u',  {'pts': [ (25,81),   (33,75),   (61,75),   (58,89),  (31,89), ]}),

    ('e',  {'pts': [ (86,161),  (81,165),  (48,165),  (51,151), (79,151), ]}),
    ('d',  {'pts': [ (103,86),  (108,86),  (95,153),  (89,158), (82,149), (92,94), ]}),
    ('r',  {'pts': [ (70,92),   (82,127),  (78,147),  (66,110), ]}),
    ('p',  {'pts': [ (100,82),  (91,89),   (62,89),   (65,75),  (92,75), ]}),

    ('b',  {'pts': [ (77,2),    (110,2),   (114,5),   (103,17), (74,17), ]}),
    ('c',  {'pts': [ (116,7),   (120,14),  (109,80),  (104,80), (96,73),  (106,18), ]}),
    ('n',  {'pts': [ (98,23),   (94,44),   (72,72),   (76,49), ]}),
    ('m',  {'pts': [ (66,22),   (77,22),   (69,72),   (57,72), ]}),

    ('dp', {'pts': [ (115,147), (117,147), (119,148), (121,149), (123,151), (124,153),
                     (125,155), (125,157), (124,159), (123,161), (121,163), (119,164),
                     (117,165), (115,165), (113,164), (111,163), (109,161), (108,159),
                     (107,157), (107,155), (108,153), (109,151), (111,149), (113,148), ]}),
])

DIGIT_BITMAP_ALPHA_16_DP = dict([
    ('f',  {'block': 2, 'bit': 0}),
    ('g',  {'block': 2, 'bit': 1}),
    ('t',  {'block': 2, 'bit': 2}),
    ('s',  {'block': 2, 'bit': 3}),

    ('a',  {'block': 3, 'bit': 0}),
    ('h',  {'block': 3, 'bit': 1}),
    ('k',  {'block': 3, 'bit': 2}),
    ('u',  {'block': 3, 'bit': 3}),

    ('e',  {'block': 0, 'bit': 0}),
    ('d',  {'block': 0, 'bit': 1}),
    ('r',  {'block': 0, 'bit': 2}),
    ('p',  {'block': 0, 'bit': 3}),

    ('b',  {'block': 1, 'bit': 0}),
    ('c',  {'block': 1, 'bit': 1}),
    ('n',  {'block': 1, 'bit': 2}),
    ('m',  {'block': 1, 'bit': 3}),

    ('dp', {'block': 4, 'bit': 0}),
])

DIGIT_REPR_ALPHA_16_DP = ['dp', '',
                          'm', 'n', 'c', 'b', '',
                          'p', 'r', 'd', 'e', '',
                          'u', 'k', 'h', 'a', '',
                          's', 't', 'g', 'f']

DIGIT_CHARMAP_ALPHA_16_DP = [
    0xBD3D, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #  !""#$%&'
    0x0000, 0x002E, 0x00A0, 0xAA88, 0xB99B, 0xBCCB, 0xD385, 0x0080,  # !"#$%&'
    0x0044, 0x4400, 0xCCCC, 0x8888, 0x0005, 0x8008, 0x0001, 0x0440,  # ()*+,-./
    0x3773, 0x0062, 0x9339, 0x113B, 0xA02A, 0xB11B, 0xB31B, 0x1032,  # 01234567
    0xB33B, 0xB13B, 0x0880, 0x0480, 0x8044, 0x8109, 0x4408, 0x1838,  # 89:;<=>?
    0x33B9, 0xB23A, 0x19BB, 0x3311, 0x19B3, 0xB311, 0xB210, 0x331B,  # @ABCDEFG
    0xA22A, 0x1991, 0x1B90, 0xA244, 0x2301, 0x6262, 0x6226, 0x3333,  # HIJKLMNO
    0xB238, 0x3337, 0xB23C, 0xB11B, 0x1890, 0x2323, 0x2640, 0x2626,  # PQRSTUVW
    0x5555, 0xA828, 0x1551, 0x0891, 0x4004, 0x1980, 0x0404, 0x0101,  # XYZ[\]^_
    0x4000, 0x8B05, 0xA600, 0x8300, 0x0D80, 0x8701, 0x8898, 0xE900,  # `abcdefg
    0xAA00, 0x0800, 0x0980, 0x08C4, 0x0880, 0x8A0A, 0x8A00, 0x8B00,  # hijklmno
    0xE200, 0xE801, 0x8200, 0x000D, 0x8888, 0x0B00, 0x0600, 0x0606,  # pqrstuvw
    0x4444, 0x4840, 0x8500, 0x8891, 0x2200, 0x1988, 0x3030, 0xFFFF,  # xyz{|}~
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
    0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,  #
]
