.. include:: <isonum.txt>

Getting Started with subseasonal_data
===================================================

The ``subseasonal_data`` package provides an API for reading and manipulating subseasonal temperature and precipitation data.
In this context, subseasonality refers to weather forecasts made on a 2-6 weeks weeks horizon. 
Currently, we provide historical data for the continental U.S. on an 1 |deg| x1 |deg| lat-long grid. 

The underlying data is made available through Azure and is updated periodically. To download the data through this package,
you will need to have the Azure Storage CLI `azcopy <https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy>`_ installed on your machine.

**Data composition (on Azure):**
    * Ground truth: historically recorded temperature and precipitation data
    * Climatology: historical averages of temperature and precipitation data
    * Date features: sea surface temperature, wind, El Nino state, etc.
    * NMME: `North American Multi-Model Ensemble <https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/north-american-multi-model-ensemble>`_
    * SubX models: `Subseasonal Experiment <https://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/>`_

**Data directory structure (on Azure):**
    * ``dataframes``: individual dataframes containing ground truth, climatology, etc. data
    * ``combined_dataframes``: lat-lon-day dataframes that merge individual dataframes
    * ``masks``: lat-long filters for Western U.S. and contiguous U.S.

**Package structure:**
    * :mod:`~subseasonal_data.downloader`: methods for manually downloading the data
    * :mod:`~subseasonal_data.data_loaders`: methods for loading the data. By default, these can download data on demand.


Quick Start
-----------

Assuming you have Python already, install ``subseasonal_data`` using ``pip``:

.. code-block:: bash

    pip install subseasonal_data

You can download the entire dataset locally:

.. code-block:: Python

    from subseasonal_data import downloader
    downloader.download()

.. warning::

    By default, the data is downloaded in :envvar:`$HOME`/:const:`subseasonal_data.download.DEFAULT_SUBSEASONAL_DATA_DIR`.

    You can change the default behavior by defining the environment variable :envvar:`$SUBSEASONALDATA_PATH` as the target I/O folder.

.. warning::

    Downloading the entire data requires an estimated 175GB disk space.

If the data was previously downloaded, this command will only download the files that have been updated in the interim.

Alternatively, you can download/sync a file at a time:

.. code-block:: Python

    downloader.download_file(
        data_subdir="combined_dataframes", 
        filename="all_data-us_precip_34w.feather", 
        verbose=True)
    
    downloader.list_subdir_files(data_subdir="combined_dataframes")

.. seealso::

    You can list the files in an Azure directory using :func:`~subseasonal_data.downloader.list_subdir_files`.

The methods in :mod:`~subseasonal_data.data_loaders` also download/sync files on demand if ``sync=True``.

Examples
--------

Load ground truth data:

.. code-block:: Python

    from subseasonal_data import data_loaders

    # Loads into a Pandas dataframe
    df = data_loaders.get_ground_truth("us_precip")

Load combined dataframes. i.e. dataframes with nmultiple features per (lat, lon, start_date) triplet:

.. code-block:: Python

    data_loaders.load_combined_data("all_data", "us_tmp2m", "34w")

Data visualization of average temperatures over the 2010-2019 years.

.. image:: ../usage_example.gif