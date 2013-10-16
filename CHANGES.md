# Changes compared to previous codelists

Each codelist has been given consistently named XML elements (rather than elements based on the codelist name). This was automated by running:

    for f in *.xml; do sed -i "s/`basename $f .xml`>/codelist-item>/g" $f; done
    # These two lines required because these codelists weren't consistent
    sed -i "s/OrganisationalIdentifier>/codelist-item>/g" ./OrganisationIdentifier.xml
    sed -i "s/TransactionType>/codelist-item>/g" ./ValueType.xml


