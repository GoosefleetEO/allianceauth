=======================
Template tags & filters
=======================

The following template tags and filters are available to be used by all apps. To use them just load them into your template like so:

.. code-block:: html+django

    {% load evelinks %}


Template Filters
================

evelinks
--------

Example for using an evelinks filter to render an alliance logo:


.. code-block:: html+django

    <img src="{{ alliance_id|alliance_logo_url }}">


.. automodule:: allianceauth.eveonline.templatetags.evelinks
    :members:
    :undoc-members:
