# Dataset Details

The **SubseasonalClimateUSA** dataset houses a diverse collection of ground-truth measurements and model forecasts relevant to forecasting at subseasonal timescales.
It can be viewed as a successor to the [SubseasonalRodeo dataset](https://doi.org/10.7910/DVN/IHBANG) of [Hwang et al. (2019)](https://dl.acm.org/doi/10.1145/3292500.3330674), and we quote both Hwang et al. (2019) and Mouatadid et al. (2021) in this dataset description.

## Organization

The dataset is organized as a collection of [Python Pandas](https://pandas.pydata.org/) DataFrames and Series objects stored in HDF5 format (via pandas.DataFrame.to_hdf or pandas.Series.to_hdf) or feather format (via pandas.DataFrame.to_feather or pandas.Series.to_feather), with one .h5 or .feather file per DataFrame or Series. 

Each HDF5 file contributes data variables (features or target values) falling into one of three categories: (i) spatial (varying with the target grid point but not the target date); (ii) temporal (varying with the target date but not the target grid point); (iii) spatiotemporal (varying with both the target grid point and the target date). 

Unless otherwise noted below, temporal and spatiotemporal variables arising from daily data sources were derived by averaging input values over each 14-day period, and spatial and spatiotemporal variables were derived by interpolating input data to a 1° × 1° latitude-longitude grid using the Climate Data Operators operator remapdis (distance-weighted average interpolation) with target grid r360x181 and retaining only the grid points belonging to the contiguous United States. 

## Data Processing

Here we describe any special data processing that deviates from the standard pattern described above.

### Temperature and Precipitation 

The temperature variable (tmp2m) is an average of daily maximum (tmax) and minimum (tmin) temperature at 2 meters in °C.
The precipitation variable (precip) is reported in mm and aggregated by summing over each 14-day period rather than averaging.

The downloaded temperature variables tmin and tmax, global precipitation variable rain, and U.S. precipitation variable precip were each interpolated to both a fixed 1° × 1° grid (NUM_LAT=181, NUM_LON=360) and a fixed 1.5° × 1.5° (NUM_LAT=121, NUM_LON=240) using the NCAR Command Language function area_hi2lores_Wrap with arguments new_lat = latGlobeF(NUM_LAT, "lat", "latitude", "degrees_north"); new_lon = lonGlobeF(NUM_LON, "lon", "longitude", "degrees_east"); wgt = cos(lat\*pi/180.0) (so that points are weighted by the cosine of the latitude in radians); opt@critpc = 50 (to require only 50% of the values to be present to interpolate); and fiCyclic = True (indicating global data with longitude values that do not quite wrap around the globe). `rain` was then renamed to `precip`.

### Climate Forecasting System, Version 2 (CFSv2) Forecasts at 1ºx1º Resolution

The daily CFSv2 32-member ensemble mean forecasts of temperature and precipitation from the coupled atmosphere-ocean-land dynamical model with 0.5-29.5 day lead times are obtained by

1.  Downloading all six-hourly CFSv2 total precipitation (pr) and 2-meter mean air temperature (tas) hindcast and forecast leads from [SubX](https://doi.org/10.7916/D8PG249H) averaged over the provided model runs and restricted to a 1°×1° latitude-longitude grid in the U.S. bounding box (longitudes 125W-67W and latitudes 25N-50N)
2.  Converting precipitation units to mm and temperature units to °C
3.  For each grid point and issuance time, replacing the recorded forecast for each lead time l, with the average forecast (for temperature) or summed forecast (for precipitation) over the L=14 lead period beginning with lead time l
4.  For each grid point, lead time, and issuance date, averaging the four 6-hourly forecasts from that date
5.  For each issuance date i, lead l, and grid point, replacing the produced forecast with the average of the (issuance date t, lead l) and the (issuance date t-1, lead l+1) forecasts.

### Climate Forecasting System, Version 2 (CFSv2) Forecasts at 1.5ºx1.5º Resolution

Daily CFSv2 predictions for temperature and precipitation, on a 1.5°×1.5° grid, with lead times 0-30 days, are downloaded from IRI already averaged over the four 6-hourly daily predictions, interpolated onto the 1.5x1.5 grid, aggregated over the 2-week period, and with the precipitation units as mm over the 2-week period while temperature is converted to Celsius. Finally, for each issuance date i, lead l, and grid point, the forecast is replaced with the average of the (issuance date t, lead l) and the (issuance date t-1, lead l+1) forecasts.

### European Centre for Medium-Range Weather (ECMWF) Forecasts

Biweekly ECMWF predictions for temperature and precipitation, for both control and perturbed runs, at a 1.5°×1.5° grid, for lead times of 0-32 days, are obtained by downloading the data from IRI already averaged over available model runs and aggregated over 2-week periods. The temperature data is converted to Celsius, while the precipitation data is accumulated to mm over the entire 2-week period. A single dataframe is stored for each weather variable (tmp2m or precip), for each forecast set of runs (control or perturbed) and for each forecast type (reforecast or forecast).

### Madden-Julian Oscillation (MJO)

The MJO is daily measure of tropical convection known to impact subseasonal climate.
We extract daily MJO phase and amplitude but do not average or sum those values over time.

## Data Sources and Citation

If you use any of the **SubseasonalClimateUSA** data in your work, please cite the associated sources and references below.

- **Temperature:** NOAA/OAR/ESRL PSL, CPC global temperature data <ftp://ftp.cdc.noaa.gov/Datasets/cpc_global_temp/>
  - Fan,  Y.  and  Van  den  Dool,  H.  (2008). A  global  monthly  land  surface  air  temperature  analysis  for 1948–present. Journal of Geophysical Research: Atmospheres, 113(D1).
- **Precipitation:** NOAA/OAR/ESRL PSL, CPC global unified precipitation data <ftp://ftp.cdc.noaa.gov/Datasets/cpc_global_precip/.NOAA/OAR/ESRL> and CPC US unified precipitation data <ftp://ftp.cdc.noaa.gov/Datasets/cpc_us_precip/.NOAA/OAR/ESRL>
  - Xie, P., Chen, M., and Shi, W. (2010).  CPC unified gauge-based analysis of global daily precipitation. In Preprints, 24th Conf. on Hydrology, Atlanta, GA, Amer. Meteor. Soc, volume 2.
  - Chen, M., Shi, W., Xie, P., Silva, V. B., Kousky, V. E., Wayne Higgins, R., and Janowiak, J. E. (2008). Assessing objective techniques for gauge-based analyses of global daily precipitation. Journal of Geophysical Research: Atmospheres, 113(D4).
  - Xie, P., Chen, M., Yang, S., Yatagai, A., Hayasaka, T., Fukushima, Y., and Liu, C. (2007). A gauge-based analysis of daily precipitation over east asia. Journal of Hydrometeorology, 8(3):607–626.
- **CFSv2:** SubX data <http://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/>, DOI: <https://doi.org/10.7916/D8PG249H>
  - Saha,  S.,  Moorthi,  S.,  Wu,  X.,  Wang,  J.,  Nadiga,  S.,  Tripp,  P.,  Behringer,  D.,  Hou,  Y.-T.,  Chuang, H.-y., Iredell, M., et al. (2014).   The NCEP climate forecast system version 2. Journal of climate, 27(6):2185–2208.
  - Kirtman,  B.,  Pegion,  K.,  DelSole,  T.,  Tippett,  M.,  Robertson,  A.,  Bell,  M.,  Burgman,  R.,  Lin,  H., Gottschalck, J., Collins, D., et al. (2017).  The subseasonal experiment (SubX). IRI Data Library, 10:D8PG249H.
- **ECMWF**: S2S data <http://iridl.ldeo.columbia.edu/SOURCES/.ECMWF/.S2S/.ECMF/>, DOI: <http://dx.doi.org/10.1175/BAMS-D-16-0017.1>
  - Vitart et al., The Sub-seasonal to Seasonal (S2S) Prediction Project Database. Bull. Amer. Meteor. Soc., 98(1), 163-176
- **Geopotential height (hgt), zonal wind (uwnd), and longitudinal wind (vwnd):** NOAA/OAR/ESRL PSL, NCEP reanalysis data <ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis/surface/>
  - Kalnay, E., Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White,G., Woollen, J., et al. (1996).  The NCEP/NCAR 40-year reanalysis project. Bulletin of the Americanmeteorological Society, 77(3):437–472.
- **Madden-Julian oscillation (MJO):** Australian Bureau of Meteorology, Real-time multivariate Madden Julian Oscillation index <https://iridl.ldeo.columbia.edu/SOURCES/.BoM/.MJO/.RMM/data.nc>
  - Wheeler,  M.  C.  and  Hendon,  H.  H.  (2004). An  all-season  real-time  multivariate  mjo  index:Development of an index for monitoring and prediction. Monthly weather review, 132(8):1917–1932.
- **Multivariate ENSO index (MEI.v2):** NOAA/OAR/ESRL PSL, Multivariate El Niño/Southern Oscillation (ENSO) index  https://psl.noaa.gov/enso/mei/data/meiv2.data.NOAA/OAR/ESRL 
  - Wolter, K. and Timlin, M. S. (1993). Monitoring enso in coads with a seasonally adjusted principal. In Proc. of the 17th Climate Diagnostics Workshop, Norman, OK, NOAA/NMC/CAC, NSSL, Oklahoma Clim. Survey, CIMMS and the School of Meteor., Univ. of Oklahoma, 52, volume 57 
  - Wolter, K. and Timlin, M. S. (1998).  Measuring the strength of enso events: How does 1997/98 rank? Weather, 53(9):315–324.
  - Wolter, K. and Timlin, M. S. (2011). El niño/southern oscillation behaviour since 1871 as diagnosed in an extended multivariate enso index (mei. ext). International Journal of Climatology, 31(7):1074–1087
- **Relative humidity (rhum), sea level pressure (slp), and precipitable water for entire atmosphere (pr_wtr):** NOAA/OAR/ESRL PSL, NCEP reanalysis data <ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis/surface/>
  - Kalnay, E., Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White,G., Woollen, J., et al. (1996).  The NCEP/NCAR 40-year reanalysis project. Bulletin of the Americanmeteorological Society, 77(3):437–472.
- **Pressure at the surface (pres) and potential evaporation (pevpr):** NOAA/OAR/ESRL PSL, NCEP reanalysis data <ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis/surface_gauss/>
  - Kalnay, E., Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White,G., Woollen, J., et al. (1996).  The NCEP/NCAR 40-year reanalysis project. Bulletin of the Americanmeteorological Society, 77(3):437–472.
- **Sea surface temperature and sea ice concentration:** NOAA/OAR/ESRL PSL, NOAA high resolution SST data <ftp://ftp.cdc.noaa.gov/Projects/Datasets/noaa.oisst.v2.highres/>
  - Reynolds, R. W., Smith, T. M., Liu, C., Chelton, D. B., Casey, K. S., and Schlax, M. G. (2007). Daily high-resolution-blended analyses for sea surface temperature. Journal of climate, 20(22):5473–5496.
- **Elevation:** Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010) <https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010\_15n240\_1000deg.nc>
  - Danielson, Jeffrey J., and Dean B. Gesch. Global multi-resolution terrain elevation data 2010 (GMTED2010). US Department of the Interior, US Geological Survey, 2011.
- **Köppen-Geiger climate classification:** World map of Köppen-Geiger climate classification <http://koeppen-geiger.vu-wien.ac.at/data/Koeppen-Geiger-ASCII.zip>
  - Kottek, M., Grieser, J., Beck, C., Rudolf, B., & Rubel, F. (2006). World map of the Köppen-Geiger climate classification updated.

## Data Files

In this section, we describe the individual files comprising the **SubseasonalClimateUSA** dataset.

The filename suffix '-14d' indicates that the file contains temporal variables averaged over 14 days, while the filename suffixes '-7d' and '-1d' indicate that the file contains weekly and daily temporal variables respectively.

Except in the special cases of 'us_icec' and 'us_sst', the filename substring 'us_' or '-us' indicates that the file contains spatial or spatiotemporal variables restricted to the contiguous U.S. latitude-longitude grid cells.  The contiguous U.S. boundary box is defined by latitudes 25° to 50° and longitudes 125°W to 67°W. 
The strings 'us_icec' and 'us_sst' indicate global measurements of sea ice concentration and sea surface temperature respectively on a 1° × 1° grid.  

Except in the special cases of 'contest_icec' and 'contest_sst', the filename substring 'contest_' indicates that spatial variables are restricted to the contiguous western U.S. latitude-longitude grid cells, delimited by latitudes 25° to 50° and longitudes 125°W to 93°W. The strings 'contest_icec-' and 'contest_sst-' indicate measurements of sea ice concentration and sea surface temperature respectively on a 1° × 1° grid restricted to the Pacific basin region (20°S to 65°N, 150°E to 90°W). 

The filename prefixes 'gt-hgt', 'gt-uwnd', and 'gt-vwnd' indicate global spatiotemporal data that has not been interpolated or restricted to any region.

The filename prefix 'gt-wide' indicates that a file contains temporal variables representing a base variable’s measurement at multiple locations on a latitude-longitude grid that need not correspond to contest grid point locations. The temporal variable column names are tuples in the format ('base variable name', latitude, longitude). The base variable measurements underlying the files with the filename prefix 'gt-wide_contest' were first interpolated to a 1° × 1° grid. The measurements underlying the remaining 'gt-wide' files did not undergo interpolation; the original data source grids were instead employed.  

The filename substring 'pca_' indicates that a file contains the top principal components of a data file extracted as described below.
    
- Spatiotemporal variable precipitation:
    - gt-contest\_precip-14d.h5
    - gt-contest\_precip-1d.h5
    - gt-contest\_precip-7d.h5
    - gt-us\_precip-14d.h5
    - gt-us\_precip-1d.h5
    - gt-us\_precip-7d.h5
    - gt-us\_precip\_1.5x1.5-1d.h5	
    - gt-us\_precip\_1.5x1.5-14d.h5 
- Spatial variable precipitation climatology:
  - official\_climatology-contest\_precip.h5
  - official\_climatology-us\_precip.h5
  - official\_climatology-us\_precip\_1.5x1.5.h5
- Spatiotemporal variables temperature at 2m:
    - gt-contest\_tmp2m-14d.h5
    - gt-contest\_tmp2m-7d.h5
    - gt-us\_tmp2m-14d.h5
    - gt-us\_tmp2m-7d.h5
    - gt-us\_tmp2m\_1.5x1.5-14d.h5
- Spatiotemporal variable maximum temperature at 2m:
    - gt-contest\_tmax-14d.h5
    - gt-contest\_tmax-1d.h5
    - gt-contest\_tmax-7d.h5
    - gt-us\_tmax-14d.h5
    - gt-us\_tmax-1d.h5
    - gt-us\_tmax-7d.h5
    - gt-us\_tmax\_1.5x1.5-1d.h5
    - gt-us\_tmax\_1.5x1.5-14d.h5
- Spatiotemporal variable minimum temperature at 2m:
    - gt-contest\_tmin-14d.h5
    - gt-contest\_tmin-1d.h5
    - gt-contest\_tmin-7d.h5
    - gt-us\_tmin-14d.h5
    - gt-us\_tmin-1d.h5
    - gt-us\_tmin-7d.h5
    - gt-us\_tmin\_1.5x1.5-1d.h5
    - gt-us\_tmin\_1.5x1.5-14d.h5
- Spatial variable temperature at 2 meters climatology:
  - official\_climatology-contest\_tmp2m.h5
  - official\_climatology-us\_tmp2m.h5
  - official\_climatology-us\_tmp2m\_1.5x1.5.h5
- Temporal variables MEI (mei), MEI rank (rank), and Niño Index Phase (nip):
  - gt-mei.h5
- Temporal variables MJO phase and amplitude:
  - gt-mjo-1d.h5
- Spatial variable Köppen-Geiger climate classifications:
  - gt-climate\_regions.h5
- Spatial variable elevation:
  - gt-elevation.h5
  - gt-contest\_elevation.h5
- Spatiotemporal variable potential evaporation:
    - gt-contest\_pevpr.sfc.gauss-14d.h5
    - gt-contest\_pevpr.sfc.gauss-1d.h5
    - gt-us\_pevpr.sfc.gauss-14d.h5
    - gt-us\_pevpr.sfc.gauss-1d.h5
- Spatiotemporal variable precipitable water for entire atmosphere:
    - gt-contest\_pr\_wtr.eatm-14d.h5
    - gt-contest\_pr\_wtr.eatm-1d.h5
    - gt-us\_pr\_wtr.eatm-14d.h5
    - gt-us\_pr\_wtr.eatm-1d.h5
- Spatiotemporal variable pressure:
    - gt-contest\_pres.sfc.gauss-14d.h5
    - gt-contest\_pres.sfc.gauss-1d.h5
    - gt-us\_pres.sfc.gauss-14d.h5
    - gt-us\_pres.sfc.gauss-1d.h5
- Spatiotemporal variable relative humidity:
    - gt-contest\_rhum.sig995-14d.h5
    - gt-contest\_rhum.sig995-1d.h5
    - gt-us\_rhum.sig995-14d.h5
    - gt-us\_rhum.sig995-1d.h5
- Spatiotemporal variable sea level pressure:
    - gt-contest\_slp-14d.h5
    - gt-contest\_slp-1d.h5
    - gt-us\_slp-14d.h5
    - gt-us\_slp-1d.h5
- Spatiotemporal variable geopotential height at 10, 100, 500, and 850 millibars:
    - gt-contest\_hgt\_10-14d.h5
    - gt-contest\_hgt\_10-1d.h5
    - gt-contest\_hgt\_100-14d.h5
    - gt-contest\_hgt\_100-1d.h5
    - gt-contest\_hgt\_500-14d.h5
    - gt-contest\_hgt\_500-1d.h5
    - gt-contest\_hgt\_850-14d.h5
    - gt-contest\_hgt\_850-1d.h5
    - gt-hgt\_10-14d.h5
    - gt-hgt\_10-1d.h5
    - gt-hgt\_100-14d.h5
    - gt-hgt\_100-1d.h5
    - gt-hgt\_500-14d.h5
    - gt-hgt\_500-1d.h5
    - gt-hgt\_850-14d.h5
    - gt-hgt\_850-1d.h5
    - gt-us\_hgt\_10-14d.h5
    - gt-us\_hgt\_10-1d.h5
    - gt-us\_hgt\_100-14d.h5
    - gt-us\_hgt\_100-1d.h5
    - gt-us\_hgt\_500-14d.h5
    - gt-us\_hgt\_500-1d.h5
    - gt-us\_hgt\_850-14d.h5
    - gt-us\_hgt\_850-1d.h5
- Temporal variables geopotential height at 10, 100, 500, and 850 millibars for all grid points globally:
    - gt-wide\_hgt\_10-14d.h5
    - gt-wide\_hgt\_100-14d.h5
    - gt-wide\_hgt\_500-14d.h5
    - gt-wide\_hgt\_850-14d.h5
- Temporal variables top principal components of gt-wide_hgt_\*-14d.h5 based on PC loadings from 1948-2010:
    - gt-pca\_hgt\_100\_2010-14d.h5
    - gt-pca\_hgt\_10\_2010-14d.h5
    - gt-pca\_hgt\_500\_2010-14d.h5
    - gt-pca\_hgt\_850\_2010-14d.h5
- Spatiotemporal variable zonal wind at 250 and 925 millibars:
    - gt-contest\_uwnd\_250-14d.h5
    - gt-contest\_uwnd\_250-1d.h5
    - gt-contest\_uwnd\_925-14d.h5
    - gt-contest\_uwnd\_925-1d.h5
    - gt-us\_uwnd\_250-14d.h5
    - gt-us\_uwnd\_250-1d.h5
    - gt-us\_uwnd\_925-14d.h5
    - gt-us\_uwnd\_925-1d.h5
    - gt-uwnd\_250-14d.h5
    - gt-uwnd\_250-1d.h5
    - gt-uwnd\_925-14d.h5
    - gt-uwnd\_925-1d.h5
- Temporal variables longitudinal wind at 250 and 925 millibars for all grid points globally:
    - gt-wide\_uwnd\_250-14d.h5
    - gt-wide\_uwnd\_925-14d.h5
- Temporal variables top principal components of gt-wide_uwnd_\*-14d.h5 based on PC loadings from 1948-2010:
    - gt-pca\_uwnd\_250\_2010-14d.h5
    - gt-pca\_uwnd\_925\_2010-14d.h5
- Spatiotemporal variable longitudinal wind at 250 and 925 millibars:
    - gt-contest\_vwnd\_250-14d.h5
    - gt-contest\_vwnd\_250-1d.h5
    - gt-contest\_vwnd\_925-14d.h5
    - gt-contest\_vwnd\_925-1d.h5
    - gt-us\_vwnd\_250-14d.h5
    - gt-us\_vwnd\_250-1d.h5
    - gt-us\_vwnd\_925-14d.h5
    - gt-us\_vwnd\_925-1d.h5
    - gt-vwnd\_250-14d.h5
    - gt-vwnd\_250-1d.h5
    - gt-vwnd\_925-14d.h5
    - gt-vwnd\_925-1d.h5
- Temporal variables longitudinal wind at 250 and 925 millibars for all grid points globally:
    - gt-wide\_vwnd\_250-14d.h5
    - gt-wide\_vwnd\_925-14d.h5
- Temporal variables top principal components of gt-wide_vwnd_\*-14d.h5 based on PC loadings from 1948-2010:
    - gt-pca\_vwnd\_250\_2010-14d.h5
    - gt-pca\_vwnd\_925\_2010-14d.h5
- Spatiotemporal variable global sea ice concentration:
    - gt-us\_icec-14d.h5
    - gt-us\_icec-1d.h5
- Spatiotemporal variable sea ice concentration in the Pacific basin (20°S to 65°N, 150°E to 90°W):
    - gt-contest\_icec-14d.h5
    - gt-contest\_icec-1d.h5
- Temporal variables sea ice concentration for all grid points:
    - gt-wide\_us\_icec-14d.h5
- Temporal variables sea ice concentration for all grid points in the Pacific basin (20°S to 65°N, 150°E to 90°W):
    - gt-wide\_contest\_icec-14d.h5
- Temporal variables top principal components of gt-wide_us_icec-14d.h5 based on PC loadings from 1981-2010:
    - gt-pca\_us\_icec\_2010-14d.h5
- Temporal variables top principal components of gt-wide_contest_icec-14d.h5 based on PC loadings from 1981-2010:
    - gt-pca\_icec\_2010-14d.h5
- Spatiotemporal variable global sea surface temperature:
    - gt-us\_sst-14d.h5
    - gt-us\_sst-1d.h5
- Spatiotemporal variable sea surface temperature in the Pacific basin (20°S to 65°N, 150°E to 90°W):
    - gt-contest\_sst-14d.h5
    - gt-contest\_sst-1d.h5
- Temporal variables sea surface temperature for all grid points:
    - gt-wide\_us\_sst-14d.h5
- Temporal variables sea surface temperature for all grid points in the Pacific basin (20°S to 65°N, 150°E to 90°W):
    - gt-wide\_contest\_sst-14d.h5
- Temporal variables top principal components of gt-wide_us_sst-14d.h5 based on PC loadings from 1981-2010:
    - gt-pca\_us\_sst\_2010-14d.h5    	
- Temporal variables top principal components of gt-wide_contest_sst-14d.h5 based on PC loadings from 1981-2010:
    - gt-pca\_sst\_2010-14d.h5    	  	
- Spatiotemporal variables CFSv2 ensemble forecasts of US precipitation and temperature:
    - subx-cfsv2-precip-all\_leads-8\_periods\_avg-us.h5
    - subx-cfsv2-tmp2m-all\_leads-8\_periods\_avg-us.h5
- Spatiotemporal variables CFSv2 ensemble forecasts of contest precipitation and temperature:
    - subx-cfsv2-precip-all\_leads-8\_periods\_avg.h5
    - subx-cfsv2-tmp2m-all\_leads-8\_periods\_avg.h5
- Spatiotemporal variables CFSv2 ensemble forecasts of US precipitation and temperature at 1.5°×1.5° resolution:
    - iri-cfsv2-precip-all-us1_5-ensembled.h5
    - iri-cfsv2-tmp2m-all-us1_5-ensembled.h5
- Spatiotemporal variables ECMWF control and perturbed forecasts and reforecasts of US precipitation and temperature at 1.5°×1.5° resolution:
    - iri-ecmwf-precip-all-us1_5-cf-forecast.h5
    - iri-ecmwf-precip-all-us1_5-cf-reforecast.h5
    - iri-ecmwf-precip-all-us1_5-pf-forecast.h5
    - iri-ecmwf-precip-all-us1_5-pf-reforecast.h5
    - iri-ecmwf-tmp2m-all-us1_5-cf-forecast.h5
    - iri-ecmwf-tmp2m-all-us1_5-cf-reforecast.h5
    - iri-ecmwf-tmp2m-all-us1_5-pf-forecast.h5
    - iri-ecmwf-tmp2m-all-us1_5-pf-reforecast.h5
- Combination dataframes containing lagged spatiotemporal variables as features and temperature or precipitation outcome variable
    - lat\_lon\_date\_data-contest\_precip\_34w.feather
    - lat\_lon\_date\_data-contest\_precip\_56w.feather
    - lat\_lon\_date\_data-us\_precip\_34w.feather
    - lat\_lon\_date\_data-us\_precip\_56w.feather
    - lat\_lon\_date\_data-contest\_tmp2m\_34w.feather
    - lat\_lon\_date\_data-contest\_tmp2m\_56w.feather
    - lat\_lon\_date\_data-us\_tmp2m\_34w.feather
    - lat\_lon\_date\_data-us\_tmp2m\_56w.feather    
- Combination dataframes containing lagged temporal variables as features and temperature or precipitation outcome variable:
    - date\_data-contest\_precip\_34w.feather
    - date\_data-contest\_precip\_56w.feather
    - date\_data-us\_precip\_34w.feather
    - date\_data-us\_precip\_56w.feather
    - date\_data-contest\_tmp2m\_34w.feather
    - date\_data-contest\_tmp2m\_56w.feather
    - date\_data-us\_tmp2m\_34w.feather
    - date\_data-us\_tmp2m\_56w.feather
- Combination dataframes containing lagged spatial variables as features and temperature or precipitation outcome variable:
    - lat\_lon\_data-contest\_precip\_34w.feather
    - lat\_lon\_data-contest\_precip\_56w.feather
    - lat\_lon\_data-us\_precip\_34w.feather
    - lat\_lon\_data-us\_precip\_56w.feather
    - lat\_lon\_data-contest\_tmp2m\_34w.feather
    - lat\_lon\_data-contest\_tmp2m\_56w.feather
    - lat\_lon\_data-us\_tmp2m\_34w.feather
    - lat\_lon\_data-us\_tmp2m\_56w.feather
- Combination dataframes containing lagged spatiotemporal, spatial, and temporal variables as features and temperature or precipitation outcome variable:
    - all\_data-contest\_precip\_34w.feather
    - all\_data-contest\_precip\_56w.feather
    - all\_data-us\_precip\_34w.feather
    - all\_data-us\_precip\_56w.feather
    - all\_data-contest\_tmp2m\_34w.feather
    - all\_data-contest\_tmp2m\_56w.feather
    - all\_data-us\_tmp2m\_34w.feather
    - all\_data-us\_tmp2m\_56w.feather
- Combination dataframes containing lagged spatiotemporal, spatial, and temporal variables as features and temperature or precipitation outcome variable with any row containing any missing value dropped:
    - all\_data\_no\_NA-contest\_precip\_34w.feather
    - all\_data\_no\_NA-contest\_precip\_56w.feather
    - all\_data\_no\_NA-us\_precip\_34w.feather
    - all\_data\_no\_NA-us\_precip\_56w.feather
    - all\_data\_no\_NA-contest\_tmp2m\_34w.feather
    - all\_data\_no\_NA-contest\_tmp2m\_56w.feather
    - all\_data\_no\_NA-us\_tmp2m\_34w.feather
    - all\_data\_no\_NA-us\_tmp2m\_56w.feather
    



