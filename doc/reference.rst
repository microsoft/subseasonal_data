Module Reference
================

Data Download
-------------

.. autosummary::
    :toctree: _autosummary

    subseasonal_data.downloader.download
    subseasonal_data.downloader.download_file
    subseasonal_data.downloader.get_subseasonal_data_path
    subseasonal_data.downloader.get_local_file_path
    subseasonal_data.downloader.check_azcopy_install
    subseasonal_data.downloader.list_subdir_files

Data Loaders
------------

.. autosummary::
    :toctree: _autosummary

    subseasonal_data.data_loaders.get_contest_mask
    subseasonal_data.data_loaders.get_us_mask
    subseasonal_data.data_loaders.get_climatology
    subseasonal_data.data_loaders.get_ground_truth
    subseasonal_data.data_loaders.get_ground_truth_anomalies
    subseasonal_data.data_loaders.get_forecast
    subseasonal_data.data_loaders.get_lat_lon_gt
    subseasonal_data.data_loaders.load_combined_data
    subseasonal_data.data_loaders.get_date_features
    subseasonal_data.data_loaders.get_lat_lon_date_features
    subseasonal_data.data_loaders.get_lat_lon_features

Utils
-----

.. autosummary::
    :toctree: _autosummary

    subseasonal_data.utils.load_measurement
    subseasonal_data.utils.subsetmask
    subseasonal_data.utils.shift_df
    subseasonal_data.utils.load_forecast_from_file
    subseasonal_data.utils.get_measurement_variable

