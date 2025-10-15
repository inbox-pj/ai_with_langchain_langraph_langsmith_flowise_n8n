#!/bin/bash

# CONFIGURABLES
target_dir="target"
coverage_report_dir="$target_dir/site/jacoco"
coverage_xml="$coverage_report_dir/jacoco.xml"
report_dir="build-breaker"

min_coverage_percent=80
max_critical_allowed=0
max_high_allowed=0
max_medium_allowed=9999
max_low_allowed=9999

mkdir -p "$report_dir"

module_coverage_file="$report_dir/module-coverage-history.json"
file_coverage_history_file="$report_dir/file-coverage-history.json"
fortify_fpr="$report_dir/service.fpr"
fortify_summary="$report_dir/service_summary.xml"

start_time=$(date +"%T")

# 1. CLEANUP
rm -rf "$target_dir" "$coverage_report_dir" "$fortify_fpr" "$fortify_summary"

# 2. BUILD
mvn -DjvmArgs="-Xmx2000m" clean install -DskipTests=true -Dmaven.gitcommitid.skip=true
if [ $? -ne 0 ]; then exit 1; fi

# 3. TEST & COVERAGE
mvn -DjvmArgs="-Xmx2000m" test jacoco:report -Dmaven.gitcommitid.skip=true
if [ $? -ne 0 ]; then exit 1; fi

if [ ! -f "$coverage_xml" ]; then
    echo "Coverage XML not found! Exiting."
    exit 1
fi

# 4. COVERAGE ANALYSIS
python3 -c "import xml.etree.ElementTree as ET; x=ET.parse('$coverage_xml').getroot(); c=x.find('counter[@type=\"LINE\"]'); print(f'{c.get(\"covered\")} {c.get(\"missed\")}')" > "$report_dir/coverage.txt"
read covered missed < "$report_dir/coverage.txt"
total=$((covered + missed))
if [ "$total" -eq 0 ]; then
    coverage_percent=0
else
    coverage_percent=$(python3 -c "print(round((float($covered)/$total)*100,2))")
fi
echo "Overall code coverage: $coverage_percent    ($covered / $total lines covered)"
echo "Overall code coverage: $coverage_percent    ($covered / $total lines covered)" > "$report_dir/SummaryReport.txt"

# COVERAGE THRESHOLD
python3 -c "import sys; sys.exit(0) if float($coverage_percent) >= float($min_coverage_percent) else sys.exit(1)"
err=$?
if [ "$err" -eq 0 ]; then
    echo "Coverage threshold met."
else
    echo "Build failed: Code coverage is below $min_coverage_percent, It is $coverage_percent"
    exit 1
fi

# 5. MODULE-LEVEL COVERAGE
pyfile="$report_dir/module_coverage.py"
cat > "$pyfile" <<EOF
import xml.etree.ElementTree as ET
import json, os
xml = ET.parse(r'$coverage_xml')
root = xml.getroot()
modules = {}
for pkg in root.findall('.//package'):
    name = pkg.get('name')
    covered = missed = 0
    for c in pkg.findall('counter'):
        if c.get('type') == 'LINE':
            covered = int(c.get('covered'))
            missed = int(c.get('missed'))
    total = covered + missed
    percent = round((covered/total)*100, 2) if total else 0
    modules[name] = percent
prev = {}
if os.path.exists(r'$module_coverage_file'):
    prev = json.load(open(r'$module_coverage_file'))
print(f'{"Module":30} {"Previous":15} {"Current":15} {"Remark":10}')
print('-'*70)
for mod, curr in modules.items():
    prev_val = prev.get(mod)
    if prev_val is not None:
        if curr > prev_val: remark = 'Increased'
        elif curr < prev_val: remark = 'Decreased'
        else: remark = 'Same'
    else:
        remark = 'New'
    prev_disp = prev_val if prev_val is not None else 'N/A'
    print(f'{mod:30} {prev_disp:15} {curr:15} {remark:10}')
with open(r'$module_coverage_file', 'w') as f:
    json.dump(modules, f)
EOF
python3 "$pyfile"
rm "$pyfile"

# 6. FILE-LEVEL COVERAGE
pyfile="$report_dir/file_coverage.py"
cat > "$pyfile" <<EOF
import xml.etree.ElementTree as ET
import json, os
xml = ET.parse(r'$coverage_xml')
root = xml.getroot()
files = {}
for pkg in root.findall('.//package'):
    name = pkg.get('name')
    for src in pkg.findall('sourcefile'):
        fname = f'{name}/' + src.get('name')
        covered = missed = 0
        for c2 in src.findall('counter'):
            if c2.get('type') == 'LINE':
                covered = int(c2.get('covered'))
                missed = int(c2.get('missed'))
        total = covered + missed
        percent = round((covered/total)*100, 2) if total else 0
        files[fname] = percent
prev = {}
if os.path.exists(r'$file_coverage_history_file'):
    prev = json.load(open(r'$file_coverage_history_file'))
print(f'{"File":60} {"Previous (%)":15} {"Current (%)":15} {"Remark":10}')
print('-'*100)
for fname, curr in files.items():
    prev_val = prev.get(fname)
    if prev_val is not None:
        if curr > prev_val: remark = 'Increased'
        elif curr < prev_val: remark = 'Decreased'
        else: remark = 'Same'
    else:
        remark = 'New'
    prev_disp = prev_val if prev_val is not None else 'N/A'
    print(f'{fname:60} {prev_disp:15} {curr:15} {remark:10}')
with open(r'$file_coverage_history_file', 'w') as f:
    json.dump(files, f)
EOF
python3 "$pyfile"
rm "$pyfile"

# 7. FORTIFY SCAN (if available)
if ! command -v sourceanalyzer &> /dev/null; then
    echo "Fortify SCA not installed, skipping security scan."
    exit 0
fi

if ! command -v ReportGenerator &> /dev/null; then
    echo "Fortify Tools not installed, skipping security scan."
    exit 0
fi

sourceanalyzer -b InitialBuild mvn clean compile -DskipTests=true -Dmaven.gitcommitid.skip=true
if [ $? -ne 0 ]; then
    echo "Fortify translation failed."
    exit 1
fi

sourceanalyzer -b InitialBuild -scan -format fpr -f "$fortify_fpr"
if [ $? -ne 0 ]; then
    echo "Fortify scan failed."
    exit 1
fi

ReportGenerator -format xml -source "$fortify_fpr" -f "$fortify_summary"
if [ $? -ne 0 ]; then
    echo "Fortify report generation failed."
    exit 1
fi

python3 -c "import xml.etree.ElementTree as ET; xml=ET.parse(r'$fortify_summary');root=xml.getroot();sev={'Critical':0,'High':0,'Medium':0,'Low':0};[sev.update({group.findtext('groupTitle'):int(group.get('count',0) or 0)}) for sec in root.findall('.//ReportSection') if sec.findtext('Title')=='Executive Summary' for sub in sec.findall('SubSection') if sub.findtext('Title')=='Issue Summary by Fortify Priority Order' for group in sub.findall('.//GroupingSection') if group.findtext('groupTitle') in sev];print('\n'.join([f'{k}:{sev[k]}' for k in ['Critical','High','Medium','Low']]))" > "$report_dir/fortify_counts.txt"
while IFS=: read k v; do
    eval "sev_$k=$v"
done < "$report_dir/fortify_counts.txt"

fail=0
[ "${sev_Critical:-0}" -gt "$max_critical_allowed" ] && fail=1
[ "${sev_High:-0}" -gt "$max_high_allowed" ] && fail=1
[ "${sev_Medium:-0}" -gt "$max_medium_allowed" ] && fail=1
[ "${sev_Low:-0}" -gt "$max_low_allowed" ] && fail=1

if [ "$fail" -eq 1 ]; then
    echo "Build failed: Vulnerability threshold exceeded! (Critical: ${sev_Critical:-0}, High: ${sev_High:-0}, Medium: ${sev_Medium:-0}, Low: ${sev_Low:-0})"
    exit 1
else
    echo "Build passed: Vulnerabilities within allowed threshold."
fi

end_time=$(date +"%T")
echo "Pipeline started: $start_time"
echo "Pipeline ended: $end_time"
echo "Pipeline started: $start_time" >> "$report_dir/SummaryReport.txt"
echo "Pipeline ended: $end_time" >> "$report_dir/SummaryReport.txt"
