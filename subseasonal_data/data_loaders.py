import os
import pandas as pd
import itertools
import sys
from .utils import (printf, createmaskdf, load_measurement,
                    get_measurement_variable, shift_df, load_forecast_from_file,
                    get_combined_data_filename, print_missing_cols_func, year_slice, df_merge)
from .downloader import get_subseasonal_data_path, download_file, get_local_file_path

# Globals
# Forecast id to file name
FORECASTID_TO_FILENAME = {
    "subx_cfsv2-precip": "subx-cfsv2-precip-all_leads-8_periods_avg",
    "subx_cfsv2-tmp2m": "subx-cfsv2-tmp2m-all_leads-8_periods_avg",
    "subx_geos_v2p1-precip": "subx-geos_v2p1-precip-all_leads-4_periods_avg",
    "subx_geos_v2p1-tmp2m": "subx-geos_v2p1-tmp2m-all_leads-4_periods_avg",
    "subx_nesm-precip": "subx-nesm-precip-all_leads-4_periods_avg",
    "subx_nesm-tmp2m": "subx-nesm-tmp2m-all_leads-4_periods_avg",
    "subx_ccsm4-precip": "subx-ccsm4-precip-all_leads-4_periods_avg",
    "subx_ccsm4-tmp2m": "subx-ccsm4-tmp2m-all_leads-4_periods_avg",
    "subx_cfsv2-precip-us": "subx-cfsv2-precip-all_leads-8_periods_avg-us",
    "subx_cfsv2-tmp2m-us": "subx-cfsv2-tmp2m-all_leads-8_periods_avg-us",
    "subx_geos_v2p1-precip-us": "subx-geos_v2p1-precip-all_leads-4_periods_avg-us",
    "subx_geos_v2p1-tmp2m-us": "subx-geos_v2p1-tmp2m-all_leads-4_periods_avg-us",
    "subx_nesm-precip-us": "subx-nesm-precip-all_leads-4_periods_avg-us",
    "subx_nesm-tmp2m-us": "subx-nesm-tmp2m-all_leads-4_periods_avg-us",
    "subx_ccsm4-precip-us": "subx-ccsm4-precip-all_leads-4_periods_avg-us",
    "subx_ccsm4-tmp2m-us": "subx-ccsm4-tmp2m-all_leads-4_periods_avg-us",
    "iri_ccsm4-precip-us1_5": "iri-ccsm4-precip-all-us1_5",
    "iri_ccsm4-tmp2m-us1_5": "iri-ccsm4-tmp2m-all-us1_5",
    "iri_cfsv2-precip-us1_5": "iri-cfsv2-precip-all-us1_5-ensembled",
    "iri_cfsv2-tmp2m-us1_5": "iri-cfsv2-tmp2m-all-us1_5-ensembled",
    "iri_fimr1p1-precip-us1_5": "iri-fimr1p1-precip-all-us1_5",
    "iri_fimr1p1-tmp2m-us1_5": "iri-fimr1p1-tmp2m-all-us1_5",
    "iri_gefs-precip-us1_5": "iri-gefs_combo-precip-all-us1_5",
    "iri_gefs-tmp2m-us1_5": "iri-gefs_combo-tmp2m-all-us1_5",
    "iri_geos_v2p1-precip-us1_5": "iri-geos_v2p1-precip-all-us1_5",
    "iri_geos_v2p1-tmp2m-us1_5": "iri-geos_v2p1-tmp2m-all-us1_5",
    "iri_gem-precip-us1_5": "iri-gem_combo-precip-all-us1_5",
    "iri_gem-tmp2m-us1_5": "iri-gem_combo-tmp2m-all-us1_5",
    "iri_nesm-precip-us1_5": "iri-nesm-precip-all-us1_5",
    "iri_nesm-tmp2m-us1_5": "iri-nesm-tmp2m-all-us1_5",
    "iri_subx_mean-tmp2m_12w-us1_5": "iri-subx_mean-tmp2m_12w-all-us1_5",
    "iri_subx_mean-tmp2m_34w-us1_5": "iri-subx_mean-tmp2m_34w-all-us1_5",
    "iri_subx_mean-tmp2m_56w-us1_5": "iri-subx_mean-tmp2m_56w-all-us1_5",
    "iri_subx_mean-precip_12w-us1_5": "iri-subx_mean-precip_12w-all-us1_5",
    "iri_subx_mean-precip_34w-us1_5": "iri-subx_mean-precip_34w-all-us1_5",
    "iri_subx_mean-precip_56w-us1_5": "iri-subx_mean-precip_56w-all-us1_5",
    "ecmwf-tmp2m-us1_5-pf-forecast": "iri-ecmwf-tmp2m-all-us1_5-pf-forecast",
    "ecmwf-tmp2m-us1_5-cf-forecast": "iri-ecmwf-tmp2m-all-us1_5-cf-forecast",
    "ecmwf-tmp2m-us1_5-ef-forecast": "iri-ecmwf-tmp2m-all-us1_5-ef-forecast",
    "ecmwf-tmp2m-us1_5-pf-reforecast": "iri-ecmwf-tmp2m-all-us1_5-pf-reforecast",
    "ecmwf-tmp2m-us1_5-cf-reforecast": "iri-ecmwf-tmp2m-all-us1_5-cf-reforecast",
    "ecmwf-tmp2m-us1_5-ef-reforecast": "iri-ecmwf-tmp2m-all-us1_5-ef-reforecast",
    "ecmwf-precip-us1_5-pf-forecast": "iri-ecmwf-precip-all-us1_5-pf-forecast",
    "ecmwf-precip-us1_5-cf-forecast": "iri-ecmwf-precip-all-us1_5-cf-forecast",
    "ecmwf-precip-us1_5-ef-forecast": "iri-ecmwf-precip-all-us1_5-ef-forecast",
    "ecmwf-precip-us1_5-pf-reforecast": "iri-ecmwf-precip-all-us1_5-pf-reforecast",
    "ecmwf-precip-us1_5-cf-reforecast": "iri-ecmwf-precip-all-us1_5-cf-reforecast",
    "ecmwf-precip-us1_5-ef-reforecast": "iri-ecmwf-precip-all-us1_5-ef-reforecast",
    "ecmwf-tmp2m_p1-global1_5-reforecast": "iri-ecmwf-tmp2m-all-global1_5-p1-reforecast",
    "ecmwf-tmp2m_p3-global1_5-reforecast": "iri-ecmwf-tmp2m-all-global1_5-p3-reforecast",
    "ecmwf-precip_p1-global1_5-reforecast": "iri-ecmwf-precip-all-global1_5-p1-reforecast",
    "ecmwf-precip_p3-global1_5-reforecast": "iri-ecmwf-precip-all-global1_5-p3-reforecast",
    "ecmwf-tmp2m_p1-global1_5-forecast": "iri-ecmwf-tmp2m-all-global1_5-p1-forecast",
    "ecmwf-tmp2m_p3-global1_5-forecast": "iri-ecmwf-tmp2m-all-global1_5-p3-forecast",
    "ecmwf-precip_p1-global1_5-forecast": "iri-ecmwf-precip-all-global1_5-p1-forecast",
    "ecmwf-precip_p3-global1_5-forecast": "iri-ecmwf-precip-all-global1_5-p3-forecast",
}
FORECASTID_TO_FILENAME.update({
    f"ecmwf-{gt}-us1_5-pf{ii}-forecast": f"iri-ecmwf-{gt}-all-us1_5-pf{ii}-forecast"
    for gt in ["tmp2m", "precip"] for ii in range(1,51) 
})

def get_contest_mask(sync=True, allow_write=False):
    """Return forecast rodeo contest mask as a dataframe.

    This corresponds to the Western US region.

    Columns of dataframe are lat, lon, and mask, where mask is a {0,1} variable
    indicating whether the grid point should be included (1) or excluded (0).

    Parameters
    ----------
    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    mask: pd.DataFrame
        Contest mask to be applied to other data files.
    """
    file_path = get_local_file_path(
        data_subdir="masks", fname="fcstrodeo_mask.nc", sync=sync, allow_write=allow_write)
    return createmaskdf(file_path)


def get_us_mask(sync=True,  fname="us_mask.nc", allow_write=False):
    """Return contiguous U.S. mask as a dataframe.

    Columns of dataframe are lat, lon, and mask, where mask is a {0,1} variable
    indicating whether the grid point should be included (1) or excluded (0).

    Parameters
    ----------
    sync: bool (default=True)
        Whether to download/sync the source files.
    fname: string, (default="us_mask.nc")
        Name of US mask file
    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    mask: pd.DataFrame
        U.S. mask to be applied to other data files.
    """
    file_path = get_local_file_path(
        data_subdir="masks", fname=fname, sync=sync, allow_write=allow_write)
    return createmaskdf(file_path)


def get_climatology(gt_id, mask_df=None, sync=True, allow_write=False):
    """Return climatology data as a dataframe.

    Parameters
    ----------
    gt_id: string, {'contest_tmp2m', 'contest_precip', 'us_tmp2m', 'us_precip'}
        Ground truth ID given by [region]_[variable], where region is {'contest', 'us'}
        (see :func:`~subseasonal_data.data_loaders.get_contest_mask`,
        :func:`~subseasonal_data.data_loaders.get_us_mask`) and variable is 'tmp2m' (temperature in deg&;C)
        or `precip` (precipitation in mm).

    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, default=False
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    clim_df: pd.DataFrame
        Climatology dataframe.
    """
    # Load global climatology if US climatology requested
    file_path = get_local_file_path(
        data_subdir="dataframes", fname="official_climatology-"+gt_id+".h5", sync=sync, allow_write=allow_write)
    return load_measurement(file_path, mask_df)

def get_tercile(gt_id, tercile=1, first_year=1981, last_year=2010,
                mask_df=None, sync=True, allow_write=False):
    """Return climatological tercile data as a dataframe.

    Parameters
    ----------
    gt_id: string, {'contest_tmp2m', 'contest_precip', 'us_tmp2m', 'us_precip', 'us_tmp2m_1.5x1.5', 'us_precip_1.5x1.5'}
        Ground truth ID given by [region]_[variable], where region is {'contest', 'us'}
        (see :func:`~subseasonal_data.data_loaders.get_contest_mask`,
        :func:`~subseasonal_data.data_loaders.get_us_mask`) and variable is 'tmp2m' (temperature in deg&;C)
        or `precip` (precipitation in mm).
        
    tercile: integer, {1, 2} (default=1)
        Which tercile to return.
    
    first_year: integer (default=1981)
        First year of climatological period.

    last_year: integer (default=2010)
        Last year of climatological period.
        
    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, default=False
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    tercile_df: pd.DataFrame
        Tercile dataframe.
    """
    file_path = get_local_file_path(
        data_subdir="dataframes", 
        fname=f"tercile{tercile}_{first_year}_{last_year}-{gt_id}.h5", 
        sync=sync, allow_write=allow_write)
    return load_measurement(file_path, mask_df)


def get_ground_truth(gt_id, mask_df=None, shift=None, sync=True, allow_write=False):
    """Return ground truth data as a dataframe.

    Parameters
    ----------
    gt_id: string
        Ground truth ID. Valid choices are "global_precip", "global_tmp2m", "us_precip",
         "contest_precip", "contest_tmp2m", "contest_tmin", "contest_tmax",
         "contest_sst", "contest_icec", "contest_sce",
         "pca_tmp2m", "pca_precip", "pca_sst", "pca_icec", "mei", "mjo",
         "pca_hgt_{}", "pca_uwnd_{}", "pca_vwnd_{}",
         "pca_sst_2010", "pca_icec_2010", "pca_hgt_10_2010",
         "contest_rhum.sig995", "contest_pres.sfc.gauss", "contest_pevpr.sfc.gauss",
         "wide_contest_sst", "wide_hgt_{}", "wide_uwnd_{}", "wide_vwnd_{}",
         "us_tmp2m", "us_tmin", "us_tmax", "us_sst", "us_icec", "us_sce",
         "us_rhum.sig995", "us_pres.sfc.gauss", "us_pevpr.sfc.gauss"

    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).
        Masks can be created using :func:`subseasonal_data.utils.subsetmask`.

    shift: int, optional (default=None)
        Number of days by which ground truth measurements should be shifted forward.
        The date index will be extended upon shifting.

    sync: bool, optional (default=True)
        Whether to download/sync the source file.

    allow_write: bool, default=False
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    gt_df: pd.DataFrame
        Ground truth dataframe.
    """
    gt_file = get_local_file_path(
        data_subdir="dataframes", fname="gt-"+gt_id+"-14d.h5", sync=sync, allow_write=allow_write)
    if gt_id.endswith("mei"):
        # MEI does not have an associated number of days
        gt_file = gt_file.replace("-14d", "")
    if gt_id.endswith("mjo"):
        # MJO is not aggregated to a 14-day period
        gt_file = gt_file.replace("14d", "1d")
    printf(f"Loading {gt_file}")
    return load_measurement(gt_file, mask_df, shift)


def get_ground_truth_anomalies(gt_id, mask_df=None, shift=None, sync=True, allow_write=False):
    """Return ground truth data, climatology, and ground truth anomalies
    as a dataframe.

    Parameters
    ----------
        gt_id: string, {'contest_tmp2m', 'contest_precip', 'us_tmp2m', 'us_precip'}
        Ground truth ID given by [region]_[variable], where region is {'contest', 'us'}
        and variable is 'tmp2m' (temperature in deg&;C) or `precip` (precipitation in mm).

    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).

    shift: int, optional (default=None)
        Number of days by which ground truth measurements should be shifted forward.
        The date index will be extended upon shifting.

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, default=False
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    gt_anom: pd.DataFrame
        Dataframe containing ground truth, climatology and anomalies.
    """
    date_col = "start_date"
    # Get shifted ground truth column names
    gt_col = get_measurement_variable(gt_id, shift=shift)
    # Load unshifted ground truth data
    gt = get_ground_truth(gt_id, mask_df=mask_df,
                          sync=sync, allow_write=allow_write)
    printf("Merging climatology and computing anomalies")
    # Load associated climatology
    climatology = get_climatology(
        gt_id, mask_df=mask_df, sync=sync, allow_write=allow_write)
    if shift is not None and shift != 0:
        # Rename unshifted gt columns to reflect shifted data name
        cols_to_shift = gt.columns.drop(
            ['lat', 'lon', date_col], errors='ignore')
        gt.rename(columns=dict(
            list(zip(cols_to_shift, [col+"_shift"+str(shift) for col in cols_to_shift]))),
            inplace=True)
        unshifted_gt_col = get_measurement_variable(gt_id)
        # Rename unshifted climatology column to reflect shifted data name
        climatology.rename(columns={unshifted_gt_col: gt_col},
                           inplace=True)
    # Merge climatology into dataset
    gt = pd.merge(gt, climatology[[gt_col]],
                  left_on=['lat', 'lon', gt[date_col].dt.month,
                           gt[date_col].dt.day],
                  right_on=[climatology.lat, climatology.lon,
                            climatology[date_col].dt.month,
                            climatology[date_col].dt.day],
                  how='left', suffixes=('', '_clim')).drop(['key_2', 'key_3'], axis=1)
    clim_col = gt_col+"_clim"
    # Compute ground-truth anomalies
    anom_col = gt_col+"_anom"
    gt[anom_col] = gt[gt_col] - gt[clim_col]
    printf("Shifting dataframe")
    # Shift dataframe without renaming columns
    gt = shift_df(gt, shift=shift, rename_cols=False)
    return gt


def get_forecast(forecast_id, mask_df=None, shift=None, sync=True, allow_write=False):
    """Return CFSv2 forecast data as a dataframe.

    Forecast data from the following available models:
        * SubX models: `Subseasonal Experiment <https://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/>`_

    Parameters
    ----------
    forecast_id: string
        Forecast identifier recognized by the dictionary FORECASTID_TO_FILENAME

    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).

    shift: int, optional (default=None)
        Number of days by which ground truth measurements should be shifted forward.
        The date index will be extended upon shifting.

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    forecast_df: pd.DataFrame
        Dataframe with forecasts for each available (start_date, lat, lon) triplet.
    """
    forecast_file = get_local_file_path(
        data_subdir="dataframes", fname=FORECASTID_TO_FILENAME[forecast_id]+".h5", sync=sync)
    printf(f"Loading {forecast_file}")
    forecast = load_forecast_from_file(forecast_file, mask_df)

    return shift_df(forecast, shift=shift,
                    groupby_cols=['lat', 'lon'])


def get_lat_lon_gt(gt_id, mask_df=None, sync=True, allow_write=False):
    """Return dataframe with lat_lon feature gt_id.

    Parameters
    ----------
    gt_id: string, {"elevation", "climate_regions"}
        Ground truth ID data string; either "elevation" or "climate_regions".

    mask_df: pd.DataFrame, optional (default=None)
        Mask to use for filtering the data. Columns of dataframe should be lat, lon, and mask,
        where mask is a {0,1} variable indicating whether the grid point should be included (1) or excluded (0).

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    lat_lon_gt_df: pd.DataFrame
        Lat_lon data dataframe.
    """
    gt_file = get_local_file_path(
        data_subdir="dataframes", fname="gt-{}.h5".format(gt_id), sync=sync, allow_write=allow_write)
    df = load_measurement(gt_file, mask_df)
    return df


def load_combined_data(file_id, gt_id,
                       target_horizon,
                       target_date_obj=None,
                       columns=None, sync=True,
                       allow_write=False):
    """Load and return a previously saved combined data dataset.

    Parameters
    ----------
    file_id: string
        Identifier defining data file of interest.
        Valid values include {"lat_lon_date_data", "lat_lon_data", "date_data", "all_data", "all_data_no_NA"}

    gt_id: string {"contest_precip", "contest_tmp2m", "us_precip", "us_tmp2m"}
        Ground truth ID.

    target_horizon: string {"34w", "56w"}
        Target horizon for prediction, "34w" and "56w" corresponding
        to 3-4 weeks and 5-6 weeks, respectively.

    target_date_obj: string (default=None)
        If not None, print any columns in loaded data that are
        missing on this date in datetime format

    columns: list of string (default=None)
        Column names to load or None to load all.

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    combined_data_df: pd.DataFrame
        Combined data dataframe.
    """
    data_file = get_combined_data_filename(
        file_id, gt_id, target_horizon, sync=sync, allow_write=allow_write)

    # ---------------
    # Read data_file from disk
    # ---------------
    col_arg = "all columns" if columns is None else columns
    printf(f"Reading {col_arg} from file {data_file}")
    data = pd.read_feather(data_file, columns=columns)
    # Print any data columns missing on target date
    if target_date_obj is not None:
        print_missing_cols_func(data, target_date_obj, True)
    return data


def get_date_features(gt_ids=[], gt_masks=None, gt_shifts=None, first_year=None, sync=True, allow_write=False):
    """Return dataframe of features associated with start_date values.

    If any of the input dataframes contains columns (lat, lon), it is converted
    to wide format, with one column for each (lat, lon) grid point.

    Parameters
    ----------
    gt_ids: list of string (default=[])
        Ground-truth variable identifiers to include as features, choose from
        {"contest_tmp2m", "pca_tmp2m", "contest_precip",
        "pca_precip", "contest_sst", "pca_sst", "contest_icec", "pca_icec",
        "mei", "mjo", "pca_sst_2010", "pca_icec_2010", "pca_hgt_{}",
        "pca_uwnd_{}", "pca_vwnd_{}", "us_tmp2m", "us_precip", "us_sst", "us_icec"}

    gt_masks: pd.DataFrame or list of pd.DataFrame (default=None)
        A mask dataframe, the value None, or list of masks that should
        be applied to each ground-truth feature.

    gt_shifts: int or list of int (default=None)
        Shift in days, the value None, or list of shifts that should
        be used to shift each ground truth time series forward to produce features.

    first_year: int (default=None)
        Only include rows with year >= first_year; if None, do
        not prune rows by year.

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    date_features_df: pd.DataFrame
        Data dataframe containing chosen date features.
    """
    # If particular arguments aren't lists, replace with repeating iterators
    if not isinstance(gt_masks, list):
        gt_masks = itertools.repeat(gt_masks)
    if not isinstance(gt_shifts, list):
        gt_shifts = itertools.repeat(gt_shifts)

    # Add each ground truth feature to dataframe
    df = None
    for gt_id, gt_mask, gt_shift in zip(gt_ids, gt_masks, gt_shifts):
        # Load ground truth data
        printf("\nGetting {}_shift{}".format(gt_id, gt_shift))
        gt = get_ground_truth(gt_id, gt_mask, gt_shift,
                              sync=sync, allow_write=allow_write)
        # Discard years prior to first_year
        printf(f"Discarding years prior to {first_year}")
        gt = year_slice(gt, first_year=first_year)
        # If lat, lon columns exist, pivot to wide format
        if 'lat' in gt.columns and 'lon' in gt.columns:
            if gt_shift is None:
                measurement_variable = get_measurement_variable(gt_id)
            else:
                measurement_variable = get_measurement_variable(
                    gt_id)+'_shift'+str(gt_shift)
            printf("Transforming to wide format")
            gt = gt.set_index(['lat', 'lon', 'start_date']
                              ).unstack(['lat', 'lon'])
            gt = pd.DataFrame(gt.to_records())

        # Use outer merge to include union of start_date values across all features
        # combinations across all features
        printf("Merging")
        df = df_merge(df, gt, on="start_date")

    return df


def get_lat_lon_date_features(gt_ids=[], gt_masks=None, gt_shifts=None,
                              forecast_ids=[], forecast_masks=None, forecast_shifts=None,
                              anom_ids=[], anom_masks=None, anom_shifts=None,
                              first_year=None, sync=True, allow_write=False):
    """Return dataframe of features associated with (lat, lon, start_date) values.

    Parameters
    ----------
    gt_ids: list of string (default=[])
        Ground-truth variable identifiers to include as features.
        (see :func:`~subseasonal_data.data_loaders.get_ground_truth`)

    gt_masks: pd.DataFrame or list of pd.DataFrame, optional (default=None)
        A mask dataframe, the value None, or list of masks that should
        be applied to each ground-truth feature.

    gt_shifts: int or list of int, optional (default=None)
        Shift in days, the value None, or list of shifts that should
        be used to shift each ground truth time series forward to produce features.

    forecast_ids: list of string, optional (default=None)
        Forecast identifiers to include as features.
        (see :func:`~subseasonal_data.data_loaders.get_forecast` for available choices)

    forecast_masks: pd.DataFrame or list of pd.DataFrame, optional (default=None)
        A mask dataframe, the value None, or list of masks that
        should be applied to each forecast feature.

    forecast_shifts: int or list of int, optional (default=None)
        Shift in days, the value None, or list of shifts that
        should be used to shift each forecast time series forward to produce
        each forecast feature.

    anom_ids: list of string, optional (default=[])
        For each ground-truth variable identifier in this list,
        returned dataframe will include ground truth, climatology, and
        ground truth anomaly columns with names measurement_variable,
        measurement_variable+"_clim", and measurement_variable+"_anom"
        for measurement_variable = :func:`~subseasonal_data.utils.get_measurement_variable(gt_id)`;
        only applicable to ids ending in "tmp2m" or "precip".

    anom_masks: pd.DataFrame or list of pd.DataFrame, optional (default=None)
        A mask dataframe, the value None, or list of masks that should
        be applied to each feature in anom_ids, as well as to the associated
        climatology.

    anom_shifts: int or list of int, optional (default=None)
        Shift in days, the value None, or list of shifts that should
        be used to shift each ground truth anomaly time series forward to produce feature.

    first_year: int (default=None)
        Only include rows with year >= first_year; if None, do
        not prune rows by year.

    sync: bool (default=True)
        Whether to download/sync the source files.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    lat_lon_date_features_df: pd.DataFrame
        Data dataframe containing (lat, lon, start_date) features.
    """
    # If particular arguments aren't lists, replace with repeating iterators
    if not isinstance(gt_masks, list):
        gt_masks = itertools.repeat(gt_masks)
    if not isinstance(gt_shifts, list):
        gt_shifts = itertools.repeat(gt_shifts)
    if not isinstance(forecast_masks, list):
        forecast_masks = itertools.repeat(forecast_masks)
    if not isinstance(forecast_shifts, list):
        forecast_shifts = itertools.repeat(forecast_shifts)
    if not isinstance(anom_masks, list):
        anom_masks = itertools.repeat(anom_masks)
    if not isinstance(anom_shifts, list):
        anom_shifts = itertools.repeat(anom_shifts)

    # Define canonical name for target start date column
    date_col = "start_date"
    # Function that warns if any lat-lon-date combinations are duplicated

    def warn_if_duplicated(df):
        if df[['lat', 'lon', date_col]].duplicated().any():
            print(
                "Warning: dataframe contains duplicated lat-lon-date combinations", file=sys.stderr)
    # Add each ground truth feature to dataframe
    df = None
    printf("\nAdding ground truth features to dataframe")
    for gt_id, gt_mask, gt_shift in zip(gt_ids, gt_masks, gt_shifts):
        printf(f"\nGetting {gt_id}_shift{gt_shift}")
        # Load ground truth data
        gt = get_ground_truth(gt_id, gt_mask, shift=gt_shift,
                              sync=sync, allow_write=allow_write)
        # Discard years prior to first_year
        gt = year_slice(gt, first_year=first_year)
        # Use outer merge to include union of (lat,lon,date_col)
        # combinations across all features
        df = df_merge(df, gt)
        warn_if_duplicated(df)

    # Add each forecast feature to dataframe
    printf("\nAdding forecast features to dataframe")
    for forecast_id, forecast_mask, forecast_shift in zip(forecast_ids,
                                                          forecast_masks,
                                                          forecast_shifts):
        printf("\nGetting {}_shift{}".format(forecast_id, forecast_shift))
        # Load forecast with years >= first_year
        forecast = get_forecast(
            forecast_id, forecast_mask, shift=forecast_shift, sync=sync, allow_write=allow_write)
        # Discard years prior to first_year
        forecast = year_slice(forecast, first_year=first_year)
        # Use outer merge to include union of (lat,lon,date_col)
        # combinations across all features
        df = df_merge(df, forecast)
        warn_if_duplicated(df)

    # Add anomaly features and climatology last so that climatology
    # is produced for all previously added start dates
    printf("\nAdding anomaly features to dataframe")
    for anom_id, anom_mask, anom_shift in zip(anom_ids, anom_masks, anom_shifts):
        printf("\nGetting {}_shift{} with anomalies".format(anom_id, anom_shift))
        # Add masked ground truth anomalies
        gt = get_ground_truth_anomalies(
            anom_id, mask_df=anom_mask, shift=anom_shift)
        # Discard years prior to first_year
        printf(f"Discarding years prior to {first_year}")
        gt = year_slice(gt, first_year=first_year)
        # Use outer merge to include union of (lat,lon,date_col)
        # combinations across all features
        printf("Merging in features")
        df = df_merge(df, gt)
        printf("Checking for row duplications")
        warn_if_duplicated(df)

    return df


def get_lat_lon_features(gt_ids=[], gt_masks=None, sync=True, allow_write=False):
    """Return dataframe with (lat, lon) features gt_ids.

    Parameters
    ----------
    gt_ids: list of string {"elevation", "climate_regions"}
        List with ground truth data strings; e.g. ["elevation", "climate_regions"].

    gt_masks: pd.DataFrame or list of pd.DataFrame, optional (default=None)
        A mask dataframe, the value None, or list of masks that should
        be applied to each ground-truth feature.

    allow_write: bool, (default=False)
        Whether to give write permissions to all users when syncing files.
        Recommended if working in shared directories. Users must be allowed
        to set permissions.

    Returns
    -------
    lat_lon_features_df: pd.DataFrame
        Data dataframe containing (lat, lon) features.
    """
    # If particular arguments aren't lists, replace with repeating iterators
    if not isinstance(gt_masks, list):
        gt_masks = itertools.repeat(gt_masks)

    df = None
    for gt_id, gt_mask in zip(gt_ids, gt_masks):
        printf("Getting {}".format(gt_id))
        # Load ground truth data
        gt = get_lat_lon_gt(gt_id, gt_mask, sync=sync, allow_write=allow_write)
        # Use outer merge to include union of (lat,lon,date_col)
        # combinations across all features
        df = df_merge(df, gt, on=["lat", "lon"])
    return df
