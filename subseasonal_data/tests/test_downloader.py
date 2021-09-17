import io
import unittest
from contextlib import redirect_stdout
from subseasonal_data import downloader


class TestDownloader(unittest.TestCase):
    """Basic tests for downloder methods."""

    def test_download_file(self):
        """Smoke test for downloading one file."""
        data_subdir = "masks"
        fname = "fcstrodeo_mask.nc"
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            downloader.download_file(data_subdir=data_subdir, filename=fname)
        print("Downloading a test file was successful.")

    def test_get_local_file_path(self):
        """Smoke test for getting the local path of a file."""
        data_subdir = "masks"
        fname = "fcstrodeo_mask.nc"
        downloader.get_local_file_path(
            data_subdir=data_subdir, fname=fname, sync=False)
        print("Getting local paths for downloaded files was successful.")

    def test_check_azcopy_install(self):
        """Smoke test that checks azcopy installation."""
        downloader.check_azcopy_install()
        print("AzCopy is successfully installed.")

    def test_list_subdir_files(self):
        """Smoke test for listing files at origin."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            downloader.list_subdir_files(data_subdir="combined_dataframes")
        print("Listing files at origin was successful.")
