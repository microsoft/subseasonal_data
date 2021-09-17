import io
import unittest
from contextlib import redirect_stdout
from subseasonal_data import data_loaders


def _quiet_test(f):
    def wrapper(*args, **kwargs):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            f(*args, **kwargs)
        print(f"Calling '{f.__name__[5:]}' was successful.")
    return wrapper


class TestDataLoaders(unittest.TestCase):
    """Basic tests for data loaders."""

    @_quiet_test
    def test_get_contest_mask(self):
        """Smoke test for 'get_contest_mask' data loader."""
        data_loaders.get_contest_mask()

    @_quiet_test
    def test_get_us_mask(self):
        """Smoke test for 'get_us_mask' data loader."""
        data_loaders.get_us_mask()

    @_quiet_test
    def test_get_climatology(self):
        """Smoke test for 'get_climatology' data loader."""
        gt_id = "us_tmp2m"
        data_loaders.get_climatology(gt_id=gt_id)

    @_quiet_test
    def test_get_ground_truth(self):
        """Smoke test for 'get_ground_truth' data loader."""
        gt_id = "us_precip"
        data_loaders.get_ground_truth(gt_id=gt_id)

    @_quiet_test
    def test_get_ground_truth_anomalies(self):
        """Smoke test for 'get_ground_truth_anomalies' data loader."""
        gt_id = "us_tmp2m"
        data_loaders.get_ground_truth_anomalies(gt_id=gt_id)

    @_quiet_test
    def test_get_forecast(self):
        """Smoke test for 'get_forecast' data loader."""
        forecast_id = "subx_cfsv2-tmp2m-us"
        data_loaders.get_forecast(forecast_id=forecast_id)

    @_quiet_test
    def test_get_lat_lon_gt(self):
        """Smoke test for 'get_lat_lon_gt' data loader."""
        gt_id = "elevation"
        data_loaders.get_lat_lon_gt(gt_id=gt_id)

    @_quiet_test
    def test_load_combined_data(self):
        """Smoke test for 'load_combined_data' data loader."""
        file_id = "all_data"
        gt_id = "contest_precip"
        target_horizon = "34w"
        data_loaders.load_combined_data(
            file_id=file_id, gt_id=gt_id, target_horizon=target_horizon)

    @_quiet_test
    def test_get_date_features(self):
        """Smoke test for 'get_date_features' data loader."""
        gt_ids = ["contest_tmp2m", "contest_precip"]
        data_loaders.get_date_features(gt_ids=gt_ids)

    @_quiet_test
    def test_get_lat_lon_date_features(self):
        """Smoke test for 'get_lat_lon_date_features' data loader."""
        gt_ids = ["contest_tmp2m", "contest_precip"]
        data_loaders.get_lat_lon_date_features(gt_ids=gt_ids)

    @_quiet_test
    def test_get_lat_lon_features(self):
        """Smoke test for 'get_lat_lon_features' data loader."""
        gt_ids = ["elevation", "climate_regions"]
        data_loaders.get_lat_lon_features(gt_ids=gt_ids)
