#!/bin/bash
########################################################################
# Validate codelists against codelist.xsd
########################################################################

COLOR_BG=0 # Black
COLOR_FG=7 # White
COLOR_FAIL=1 # Red
COLOR_PASS=2 # Green

count_passed=0
count_failed=0
count_total=0
exitcode=0

function fail {
    ((count_failed++))
    tput setaf $COLOR_FAIL
    echo '[FAIL]' $1
    tput setaf $COLOR_FG
}

function pass {
    ((count_passed++))
    tput setaf $COLOR_PASS
    echo '[PASS]' $1
    tput setaf $COLOR_FG
}

tput setab $COLOR_BG
tput setaf $COLOR_FG

echo "Validating..."
for f in $(find "xml" -name '*.xml' | sort); do
    ((count_total++))
    xmllint -noout --schema "codelist.xsd" $f >/dev/null 2>&1
    valid=$[ $?==0 ]
    if [ $valid == 0 ]; then
        fail $f
        exitcode=1
    else
        pass $f
    fi
done

tput setaf $COLOR_FG;   echo "$count_total codelists checked"
tput setaf $COLOR_PASS; echo "$count_passed passed"
tput setaf $COLOR_FAIL; echo "$count_failed failed"
tput setaf $COLOR_FG;   echo $exitcode

exit $exitcode

# end
