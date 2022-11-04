IATI Codelists
^^^^^^^^^^^^^^

.. image:: https://github.com/IATI/IATI-Codelists/workflows/CI/badge.svg
   :target: https://github.com/IATI/IATI-Codelists/actions
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/IATI/IATI-Codelists/blob/version-2.03/LICENSE

Introduction
------------

This repository contains the codelists for the IATI Standard, and is part of the Single Source of Truth (SSOT). For more information about the SSOT, please see https://iatistandard.org/203/developer/ssot/ 

The Codelists
=============

The source codelists can be found in the `xml/` directory. 

Core vs Non-Core Codelists
=================================

This repository contains only codelists that are core to the IATI Standard. Core means that IATI is directly responsible for them, and any changes to them need to go through the same change control process as other changes to the standard.

Those codelists that are not core can be found in a separate repository at `<https://github.com/IATI/IATI-Codelists-NonEmbedded/>`_. These lists are typically maintained by other organisations that IATI has no control over but which IATI data relies on such as country codes, language codes and so on. The aspiration for these codelists is to have them pulled from their external sources regularly and automatically.

Codelist XML Format
===================

The codelist are in an XML format described by the  ``codelist.xsd`` schema. 
This format has been chosen for the single source of truth as it has a number of advantages over the previous format used by IATI.
 
* the codelists no longer include the element name as a tag name,
* all have language information described the same way as IATI XML 
* as there is a codelist schema we can validate all the source XML 
* more metadata, including a description, is now included in the codelists

Codelists in Other Formats (.json, .csv)
========================================

``gen.sh`` (which calls ``gen.py``) can be used to convert the Codelists to JSON and CSV format. Converted codelists are available on https://iatistandard.org/en/iati-standard/203/codelists

To do the conversion yourself, you will need BASH, Python and python-lxml. Then simply run ``gen.sh``. The generated codelists will be in the ``out`` folder.

Codelist Mapping
================

`mapping.xml <https://github.com/IATI/IATI-Codelists/blob/version-2.03/mapping.xml>`__ relates codelists to an XML path in the standard. This should make it easier for users to work out which codelists go with which element and vice versa.

It's structured as a list of `mapping` elements, which each have a `path` element that describes the relevant attribute, and a `codelist@ref` attribute which is the same ref as used in the codelist filenames. An optional `condition` element is an xpath expression which limits the scope of the given codelist - e.g. it only applies if a certain vocabulary is being used. A sample of the XML is as follows:

.. code-block:: xml

    <mappings>
        <mapping>
            <path>//iati-activity/transaction/recipient-country/@code</path>
            <codelist ref="Country" />
        </mapping>
        <mapping>
            <path>//iati-activity/transaction/recipient-region/@code</path>
            <codelist ref="Region" />
            <condition>@vocabulary = '1'</condition>
        </mapping>
        ...
    </mappings>

A `JSON version <http://iatistandard.org/203/codelists/downloads/clv1/mapping.json>`__ is also available.

Testing Compliance Against Codelists
===================================

``testcodelists.py`` can be run against an IATI Activity XML to check that it is using the correct codelists values. Only codelists that are complete will be tested (see next section).

Extra Metadata
==============

``complete`` - boolean that describes whether the codelist is 'complete' ie. having a value not on the codelist is definitely invalid. An example of an incomplete codelist is country codes, where extra codes may exist for disputed countries.

Translation script
==================

``translations_csv_to_xml.py`` can be run to output XML codelists with translated elements, the expected format of the CSV files is that they must have ``code`` and ``name (<language iso code>)`` columns, and they can have ``description (<language iso code>)`` as well. The python script must be modified to include ``OUTPUTDIR``, ``PATH_TO_CSV``, ``PATH_TO_XML`` and ``LANG``. 

Add metadata categories
=======================

``category_csv_to_xml.py`` can be run to output XML codelists with ``metadata/category`` elements, the expected format of the CSV files is that they must have ``Codelist``, ``Type_version <version number>`` and ``New Type`` columns. The python script must be modified to include the output directories, ``VERSION``, ``PATH_TO_XML`` and ``CSV_FILE``. 

Information for developers
==========================

This tool supports Python 3.x. To use this script, we recommend the use of a virtual environment::

    python3 -m venv pyenv
    source pyenv/bin/activate
    pip install -r requirements.txt

Downstream Updates
==================

IATI Standard Website
---------------------

- The `IATI/IATI-Reference-Generator <https://github.com/IATI/IATI-Reference-Generator>`__ repo should be used to rebuild the SSOT documentation and upload to the website following that process. 
- This will ensure the updates to the codelists are reflected on the IATI Standard website.

IATI Validator
--------------

- The `Validator <https://iativalidator.iatistandard.org>`__ utilises a transformed version of the Codelists stored in `IATI/IATI-Validator-Codelists <https://github.com/IATI/IATI-Validator-Codelists>`__. 
- When changes are pushed to a version branch, the `call-update-validator-codelists` job in `.github/workflows/CI.yml` triggers a GitHub action in `IATI/IATI-Validator-Codelists <https://github.com/IATI/IATI-Validator-Codelists>`__. 
- Follow the `Update Process <https://github.com/IATI/IATI-Validator-Codelists#update-process>`__ as documented in the IATI-Validator-Codelists repo

IATI Datastore
--------------

- The `Datastore Search <https://datastore.iatistandard.org>`__ utilises a transformed version of the Codelists stored in `IATI/dss-filters <https://github.com/IATI/dss-filters>`__
- When changes are pushed to a version-2.03 branch, the `call-update-dss-filters` job in `.github/workflows/CI.yml` triggers a GitHub action in `IATI/dss-filters <https://github.com/IATI/dss-filters>`__.
- See `IATI/dss-filters <https://github.com/IATI/dss-filters>`__ for instructions on updating the Codelists used by Datastore Search.
