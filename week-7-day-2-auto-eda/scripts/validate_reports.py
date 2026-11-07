from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"

REPORTS = [
    REPORT_DIR / "profile_report.html",
    REPORT_DIR / "sweetviz_report.html",
]


def validate():
    failed = False

    for report in REPORTS:
        if not report.is_file():
            print(f"FAILED: Missing {report.name}")
            failed = True
            continue

        size_kb = report.stat().st_size / 1024
        if size_kb < 10:
            print(f"WARNING: {report.name} is only {size_kb:.1f} KB")
            failed = True
        else:
            print(f"PASSED: {report.name} - {size_kb:.1f} KB")

    if failed:
        print("\nReport validation failed.")
        return False

    print("\nAll reports passed validation.")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if validate() else 1)
