IATI Codelists
^^^^^^^^^^^^^^

This repository contains the codelists for the IATI Standard, and is part of the Single Source of Truth (SSOT). For more information about the SSOT, please see https://github.com/IATI/IATI-Standard-SSOT/blob/master/meta-docs/index.rst 

This repository is currently under development, and does not necessarily represent any current or future version of the IATI standard.

The Codelists
=============

The source codelists can be found in the `xml/` directory. These are in a new XML format described by the  ``codelist.xsd`` schema.


Embedded vs NonEmbedded Codelists
=================================

This repository contains only codelists that are embedded in the in the IATI Standard. Embedded means that IATI is directly responsible for them, and any changes to them need to go through the same change control process as other changes to the standard.

Those codelists that are not Embedded can be found in a seperate repository at `<https://github.com/IATI/IATI-Codelists-NonEmbedded/>`_. The aspiration for these codelists is to have them pulled from their external sources regularly and automatically.

Codelists in Other Formats
==========================

``gen.sh`` (which calls ``gen.py``) can be used to convert the Codelists to JSON and CSV format. Converted coedlists are availible on dev.iatistandard.org

To do the conversion yourself, you will need BASH, Python and python-lxml. Then simply run ``gen.sh``. The generated codelists will be in the ``out`` folder.

Codelist Mapping
================

``mapping.xml`` relates codelists to an XML path in the standard.

Testing Complians Against Codelists
===================================

``testcodelists.py`` can be used to test an XML file against the codelists.

Extra Metadata
==============

`complete` - boolean that describes whether the codelist is 'complete' ie. having a value not on the codelist is definitely invalid. An example of an incomplete codelist is country codes, where extra codes may exist for disputed countries.
