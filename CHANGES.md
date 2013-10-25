# Changes compared to previous codelists

## Initial import and cleanup

Each codelist has been given consistently named XML elements (rather than elements based on the codelist name). This was automated by running:

    for f in *.xml; do sed -i "s/`basename $f .xml`>/codelist-item>/g" $f; done
    # These two lines required because these codelists weren't consistent
    sed -i "s/OrganisationalIdentifier>/codelist-item>/g" ./OrganisationIdentifier.xml
    sed -i "s/TransactionType>/codelist-item>/g" ./ValueType.xml

Futher, all instances of the `date-last-modifed` attribute were replaced with `date-last-modified`. And the extra `last-modified` attribute in `SectorCategory` was removed.
    sed -i s/date-last-modifed/date-last-modified/g *.xml

An [xsd schema](https://github.com/Bjwebb/IATI-Codelists/blob/74cb1a5371b60272646ed32802c2968c180b968f/codelist.xsd) was written for these updated files.

The codelist list was stripped down to simply reference the codelists, and the descriptions moved to the individual codelist files.

## Transition to GitHub for versioning

Since GitHub is now used for version tracking the @version and @date-last-modified attributes are no longer needed, so have been removed.

## Language changes

The language element has been removed
