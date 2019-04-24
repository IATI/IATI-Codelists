IATI Codelists
^^^^^^^^^^^^^^

.. image:: https://travis-ci.org/IATI/IATI-Codelists.svg?branch=version-2.01
    :target: https://travis-ci.org/IATI/IATI-Codelists
.. image:: https://requires.io/github/IATI/IATI-Codelists/requirements.svg?branch=version-2.01
    :target: https://requires.io/github/IATI/IATI-Codelists/requirements/?branch=version-2.01
    :alt: Requirements Status
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/IATI/IATI-Codelists/blob/version-2.01/LICENSE

Introduction
------------

This repository contains the codelists for the IATI Standard, and is part of the Single Source of Truth (SSOT). For more information about the SSOT, please see http://iatistandard.org/201/developer/ssot/ 

The Codelists
=============

The source codelists can be found in the `xml/` directory. 

Core vs Non-Core Codelists
=================================

This repository contains only codelists that are core to the IATI Standard. Core means that IATI is directly responsible for them, and any changes to them need to go through the same change control process as other changes to the standard.

Those codelists that are not core can be found in a seperate repository at `<https://github.com/IATI/IATI-Codelists-NonEmbedded/>`_. These lists are typically maintained by other organisations that IATI has no control over but which IATI data relies on such as country codes, language codes and so on. The aspiration for these codelists is to have them pulled from their external sources regularly and automatically.

Codelist XML Format
===============

The codelist are in an XML format described by the  ``codelist.xsd`` schema. 
This format has been chosen for the single source of truth as it has a number of advantages over the previous format used by IATI.
 
* the codelists no longer include the element name as a tag name,
* all have language information described the same way as IATI XML 
* as there is a codelist schema we can validate all the source XML 
* more metadata, including a description, is now included in the codesists

Codelists in Other Formats (.json, .csv)
========================================

``gen.sh`` (which calls ``gen.py``) can be used to convert the Codelists to JSON and CSV format. Converted coedlists are availible on dev.iatistandard.org

To do the conversion yourself, you will need BASH, Python and python-lxml. Then simply run ``gen.sh``. The generated codelists will be in the ``out`` folder.

Codelist Mapping
================

`mapping.xml <https://github.com/IATI/IATI-Codelists/blob/version-2.02/mapping.xml>`__ relates codelists to an XML path in the standard. This should make it easier for users to work out which codelists go with which element and vice versa.

It's structured as a list of `mapping` elements, which each have a `path` element that describes the relevant attribute, and a `codelist@ref` attribute which is the same ref as used in the codelist filenames. An optional `condition` element is an xpath expression which limits the scope of the given codelist - e.g. it only applies if a certain vocabulary is being used. A sample of the XML is as follows:

.. code-block:: xml

    <mappings>
        <mapping>
            <path>//iati-activity/@default-currency</path>
            <codelist ref="Currency" />
        </mapping>
        <mapping>
            <path>//iati-activity/country-budget-items/budget-item/@code</path>
            <codelist ref="BudgetIdentifier" />
            <condition>@vocabulary = '1'</condition>
        </mapping>
        ...
    </mappings>

A `JSON version <http://iatistandard.org/201/codelists/downloads/clv1/mapping.json>`__ is also available.

Testing Compliance Against Codelists
===================================

``testcodelists.py`` can be run against an IATI Activity XML to check that it is using the correct codelists values. Only codelists that are complete will be tested (see next section).

Extra Metadata
==============

`complete` - boolean that describes whether the codelist is 'complete' ie. having a value not on the codelist is definitely invalid. An example of an incomplete codelist is country codes, where extra codes may exist for disputed countries.
