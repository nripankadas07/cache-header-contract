"""Audit captured response headers against explicit deployment expectations."""
import argparse
import json
import re
from pathlib import Path

TOKEN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
NUMERIC = {"max-age", "s-maxage", "stale-while-revalidate", "stale-if-error"}


def split_directives(text):
    parts, start, quoted, escaped = [], 0, False, False
    for i, c in enumerate(text):
        if escaped:
            escaped = False
        elif c == "\\" and quoted:
            escaped = True
        elif c == '"':
            quoted = not quoted
        elif c == "," and not quoted:
            parts.append(text[start:i]); start = i + 1
    if quoted or escaped:
        raise ValueError("unterminated quoted directive")
    return parts + [text[start:]]


def parse(text):
    if not isinstance(text, str) or any(c in text for c in "\r\n"):
        raise ValueError("header must be a single-line string")
    values, duplicates = {}, []
    for part in split_directives(text):
        part = part.strip()
        if not part:
            continue
        name, sep, value = part.partition("="); name = name.strip().lower(); value = value.strip()
        if not TOKEN.fullmatch(name):
            raise ValueError("invalid directive name")
        if sep:
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif not TOKEN.fullmatch(value):
                raise ValueError("invalid unquoted directive value")
        else:
            value = None
        if name in NUMERIC and (value is None or not re.fullmatch(r"[0-9]{1,12}", value)):
            raise ValueError("invalid bounded delta-seconds for " + name)
        if name in values:
            duplicates.append(name)
        else:
            values[name] = value
    return values, sorted(set(duplicates))


def check(headers, contract):
    if not isinstance(headers, list) or not all(isinstance(h, list) and len(h) == 2 and all(isinstance(z, str) for z in h) for h in headers):
        raise ValueError("headers must be ordered [name,value] pairs; repeated fields preserved")
    if not isinstance(contract, dict) or set(contract) - {"require", "forbid", "max_shared_ttl", "vary"}:
        raise ValueError("unknown contract option")
    required, forbidden, vary_expected = contract.get("require", []), contract.get("forbid", []), contract.get("vary", [])
    for xs in (required, forbidden, vary_expected):
        if not isinstance(xs, list) or not all(isinstance(x, str) and TOKEN.fullmatch(x) for x in xs):
            raise ValueError("contract directive/header lists must contain tokens")
    required, forbidden, vary_expected = [set(x.lower() for x in xs) for xs in (required, forbidden, vary_expected)]
    cap = contract.get("max_shared_ttl")
    if cap is not None and (type(cap) is not int or cap < 0):
        raise ValueError("max_shared_ttl must be a nonnegative integer")
    fields = {}
    for name, value in headers:
        if not TOKEN.fullmatch(name) or any(c in value for c in "\r\n"):
            raise ValueError("invalid captured header")
        fields.setdefault(name.lower(), []).append(value)
    directives, duplicates = parse(",".join(fields.get("cache-control", [])))
    findings = [{"code": "duplicate_directive", "directive": x} for x in duplicates]
    findings += [{"code": "missing_directive", "directive": x} for x in sorted(required - directives.keys())]
    findings += [{"code": "forbidden_directive", "directive": x} for x in sorted(forbidden & directives.keys())]
    if "private" in directives and "public" in directives:
        findings.append({"code": "conflicting_scope"})
    ttl_source = "s-maxage" if "s-maxage" in directives else "max-age" if "max-age" in directives else None
    ttl = int(directives[ttl_source]) if ttl_source and ttl_source not in duplicates else None
    if cap is not None and (ttl is None or ttl > cap):
        findings.append({"code": "shared_ttl_missing_or_exceeds_cap"})
    vary = {x.strip().lower() for v in fields.get("vary", []) for x in v.split(",") if x.strip()}
    if vary_expected - vary:
        findings.append({"code": "missing_vary", "headers": sorted(vary_expected - vary)})
    return {"ok": not findings, "directives": directives, "shared_ttl": ttl, "ttl_source": ttl_source, "vary": sorted(vary), "findings": findings}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("capture"); p.add_argument("contract"); a = p.parse_args()
    try:
        r = check(json.loads(Path(a.capture).read_text(encoding="utf-8")), json.loads(Path(a.contract).read_text(encoding="utf-8")))
        print(json.dumps(r, sort_keys=True)); return 0 if r["ok"] else 1
    except (ValueError, OSError) as e:
        print(json.dumps({"error": str(e)})); return 2


if __name__ == "__main__":
    raise SystemExit(main())
