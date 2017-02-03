#!/usr/bin/env python

import sys

from cdrouter import CDRouter
from cdrouter.filters import Field as field
from cdrouter.annotations import Annotation
from cdrouter.highlights import Highlight

if len(sys.argv) < 4:
    print('usage: <base_url> <token> <result-id> [<color> <filter>]...')
    sys.exit(1)

colors = ['yellow', 'blue', 'red', 'green']

base = sys.argv[1]
token = sys.argv[2]
result_id = int(sys.argv[3])
color_filter_pairs = []
if len(sys.argv) > 4:
    color_filter_pairs = sys.argv[4:]

c = CDRouter(base, token=token)

r = c.results.get(result_id)

# unstar the result
r.starred = False
c.results.edit(r)

# loop over all tests in the result
for tr in c.tests.iter_list(result_id):
    # some tests don't have a logfile, skip them
    if len(tr.log) == 0:
        continue

    # delete any existing comments/highlights
    for ann in c.annotations.list(tr.id, tr.seq):
        c.annotations.delete(tr.id, tr.seq, ann.line)
    for h in c.highlights.list(tr.id, tr.seq):
        c.highlights.delete(tr.id, tr.seq, h.line)

    # clear the test's flag
    tr.flagged = False
    c.tests.edit(tr.id, tr)

    # loop over the test's capture files
    for cap in c.captures.list(tr.id, tr.seq):
        iterator = iter(color_filter_pairs)

        # loop over each color-filter pair
        for color in iterator:
            pcap_filter = next(iterator)
            if color not in colors:
                print('Invalid color {}, must be one of: {}'.format(color, ', '.join(colors)))
                sys.exit(1)

            # get list of packets matching filter
            summ = c.captures.summary(tr.id, tr.seq, cap.interface, inline=True, filter=pcap_filter)
            if summ.summaries is None or summ.summaries[0].sections is None:
                continue

            # build list of frame numbers of matching packets
            # (first summary column is frame number)
            frames = [s.sections[0].value for s in summ.summaries]

            # add highlight and comment in the logfile for matching packets
            for frame in frames:
                logs = c.tests.list_log(tr.id, tr.seq, filter=[field('interface').eq(cap.interface),
                                                               field('packet').eq(frame)])
                if len(logs.lines) == 0:
                    continue
                l = logs.lines[0]

                print('{}: {} ({}): line {}: {}'.format(tr.id, tr.name, tr.seq, l.line, l.raw))

                # flag the test and star the result
                r.starred = True
                tr.flagged = True

                c.annotations.create_or_edit(result_id, tr.seq, Annotation(line=l.line, comment=pcap_filter))
                c.highlights.create_or_edit(result_id, tr.seq, Highlight(line=l.line, color=color))

    if r.starred:
        c.results.edit(r)
    if tr.flagged:
        c.tests.edit(tr.id, tr)
