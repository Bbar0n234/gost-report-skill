"""CI-раннер: собирает тестовые документы и проверяет результат.

Использование:
    python tests/ci_check.py --expect-toc       # LibreOffice есть: СОДЕРЖАНИЕ должно быть посчитано
    python tests/ci_check.py --expect-degraded  # LibreOffice нет: сборка обязана пройти с честным warning'ом

Собирает tests/lab_test.md и tests/course_test.md, гоняет scripts/verify.py по обоим,
затем проверяет режим TOC. Выход 0 — всё прошло, 1 — есть провалы.
"""

import subprocess
import sys
import zipfile
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = TESTS_DIR.parent / "gost-lab-report"
BUILD = SKILL_DIR / "scripts" / "build.py"
VERIFY = SKILL_DIR / "scripts" / "verify.py"
OUT_DIR = TESTS_DIR / "out"


def run(args, **kw):
    print(f"\n$ {' '.join(str(a) for a in args)}", flush=True)
    proc = subprocess.run(
        [sys.executable, *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=TESTS_DIR, **kw,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc


def document_xml(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        return z.read("word/document.xml").decode("utf-8", errors="replace")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("--expect-toc", "--expect-degraded"):
        print(__doc__)
        return 1

    expect_toc = sys.argv[1] == "--expect-toc"
    OUT_DIR.mkdir(exist_ok=True)
    failures = []

    builds = {}
    for name in ("lab_test", "course_test"):
        out = OUT_DIR / f"{name}.docx"
        proc = run([BUILD, TESTS_DIR / f"{name}.md", out])
        builds[name] = proc
        if proc.returncode != 0:
            failures.append(f"build {name}: exit {proc.returncode}")
            continue
        vproc = run([VERIFY, out])
        if vproc.returncode != 0:
            failures.append(f"verify {name}: exit {vproc.returncode}")

    course_out = OUT_DIR / "course_test.docx"
    if course_out.exists():
        xml = document_xml(course_out)
        # LibreOffice пишет посчитанный TOC гиперссылками на якоря __RefHeading___Toc…;
        # PAGEREF — на случай, если содержание посчитал Word
        toc_computed = "__RefHeading" in xml or "PAGEREF" in xml
        course_log = builds["course_test"].stdout + builds["course_test"].stderr
        if expect_toc:
            if not toc_computed:
                failures.append("TOC: маркеры не найдены — СОДЕРЖАНИЕ не посчитано, хотя LibreOffice ожидался")
        else:
            if toc_computed:
                failures.append("TOC: содержание посчитано — ожидалась деградация без LibreOffice")
            if "LibreOffice" not in course_log:
                failures.append("degradation: сборка без LibreOffice не предупредила пользователя (нет warning'а)")
    elif expect_toc or "course_test" not in [f.split()[1].rstrip(":") for f in failures]:
        pass  # провал сборки уже зафиксирован выше

    print("\n=== CI SUMMARY ===")
    if failures:
        for f in failures:
            print(f"[FAIL] {f}")
        return 1
    mode = "TOC computed" if expect_toc else "degraded honestly (warning shown)"
    print(f"[PASS] builds + verify + mode: {mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
