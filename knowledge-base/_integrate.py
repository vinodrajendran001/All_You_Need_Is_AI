import os, re, sys, io

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
WIKI = "wiki"

_idx = {}
for r, d, fs in os.walk(WIKI):
    for f in fs:
        if f.endswith(".md"):
            _idx[f[:-3]] = os.path.join(r, f)


def integrate(page, new_ids, heading, body, related=(), updated="2026-09-04"):
    fp = _idx[page]
    t = io.open(fp, encoding="utf-8").read()
    head, fm, rest = t.split("---", 2)

    # 1. source_ids
    for sid in new_ids:
        if sid not in fm:
            m = re.search(r"^source_ids:\n((?:  - \S+\n)+)", fm, re.M)
            if m:
                fm = fm[: m.end(1)] + "  - %s\n" % sid + fm[m.end(1):]
            else:
                raise SystemExit("no source_ids list in " + page)

    # 2. updated
    if re.search(r"^updated:", fm, re.M):
        fm = re.sub(r"^updated:.*$", "updated: " + updated, fm, count=1, flags=re.M)
    else:
        fm = re.sub(r"^(created:.*)$", r"\1\nupdated: " + updated, fm, count=1, flags=re.M)

    # 3. insert section before Open questions, else before Related pages
    sec = "## %s\n\n%s\n\n" % (heading, body.strip())
    m = re.search(r"^## Open questions\s*$", rest, re.M)
    if not m:
        m = re.search(r"^## Related pages\s*$", rest, re.M)
    if not m:
        raise SystemExit("no anchor in " + page)
    rest = rest[: m.start()] + sec + rest[m.start():]

    # 4. related links appended
    m = re.search(r"^## Related pages\s*$", rest, re.M)
    tail = rest[m.end():]
    add = [l for l in related if ("[[%s]]" % l) not in tail]
    if add:
        rest = rest.rstrip("\n") + "\n" + "\n".join("- [[%s]]" % l for l in add) + "\n"

    io.open(fp, "w", encoding="utf-8").write(head + "---" + fm + "---" + rest)
    print("integrated:", page)
