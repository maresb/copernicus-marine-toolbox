import pathlib
from datetime import datetime
from typing import List, Optional, Union

import pandas

from copernicusmarine.catalogue_parser.request_structure import LoadRequest
from copernicusmarine.core_functions.deprecated import (
    deprecated_python_option,
    log_deprecated_message,
)
from copernicusmarine.core_functions.deprecated_options import (
    DEPRECATED_OPTIONS,
)
from copernicusmarine.core_functions.models import (
    DEFAULT_BOUNDING_BOX_METHOD,
    DEFAULT_SUBSET_METHOD,
    BoundingBoxMethod,
    SubsetMethod,
)
from copernicusmarine.download_functions.download_arco_series import (
    read_dataframe_from_arco_series,
)
from copernicusmarine.download_functions.subset_parameters import (
    DepthParameters,
    GeographicalParameters,
    LatitudeParameters,
    LongitudeParameters,
    TemporalParameters,
)
from copernicusmarine.python_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicusmarine.python_interface.load_utils import (
    load_data_object_from_load_request,
)
from copernicusmarine.python_interface.utils import homogenize_datetime


@log_exception_and_exit
def load_pandas_dataframe(*args, **kwargs):
    """
    Deprecated function, use 'read_dataframe' instead.
    """
    log_deprecated_message("load_pandas_dataframe", "read_dataframe")
    return read_dataframe(*args, **kwargs)


@deprecated_python_option(**DEPRECATED_OPTIONS.dict_old_names_to_new_names)
@log_exception_and_exit
def read_dataframe(
    dataset_id: str,
    dataset_version: Optional[str] = None,
    dataset_part: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    variables: Optional[List[str]] = None,
    minimum_longitude: Optional[float] = None,
    maximum_longitude: Optional[float] = None,
    minimum_latitude: Optional[float] = None,
    maximum_latitude: Optional[float] = None,
    minimum_depth: Optional[float] = None,
    maximum_depth: Optional[float] = None,
    vertical_dimension_as_originally_produced: bool = True,
    start_datetime: Optional[Union[datetime, str]] = None,
    end_datetime: Optional[Union[datetime, str]] = None,
    bounding_box_method: BoundingBoxMethod = DEFAULT_BOUNDING_BOX_METHOD,
    subset_method: SubsetMethod = DEFAULT_SUBSET_METHOD,
    force_service: Optional[str] = None,
    credentials_file: Optional[Union[pathlib.Path, str]] = None,
) -> pandas.DataFrame:
    """
    Immediately loads a Pandas DataFrame into memory from a specified dataset.

    Unlike "lazy-loading," the data is loaded as soon as this function is executed,
    which may be preferable when rapid access to the entire dataset is required,
    but may require careful memory management.

    Parameters
    ----------
    dataset_id : str, optional
        The identifier of the dataset.
    dataset_version : str, optional
        Force a specific dataset version.
    dataset_part : str, optional
        Force a specific dataset part.
    username : str, optional
        Username for authentication.
    password : str, optional
        Password for authentication.
    variables : List[str], optional
        List of variable names to load.
    minimum_longitude : float, optional
        Minimum longitude for spatial subset.
    maximum_longitude : float, optional
        Maximum longitude for spatial subset.
    minimum_latitude : float, optional
        Minimum latitude for spatial subset.
    maximum_latitude : float, optional
        Maximum latitude for spatial subset.
    minimum_depth : float, optional
        Minimum depth for vertical subset.
    maximum_depth : float, optional
        Maximum depth for vertical subset.
    vertical_dimension_as_originally_produced : bool, optional
        If True, use the vertical dimension as originally produced.
    start_datetime : datetime, optional
        Start datetime for temporal subset.
    end_datetime : datetime, optional
        End datetime for temporal subset.
    bounding_box_method : str, optional
        The bounding box method when requesting the dataset. If 'inside' (by default),
        it will return the inside interval. If 'nearest', the limits of the requested
        interval will be the nearest points of the dataset. If 'outside', it will return
        all the data such that the requested interval is fully included. Check the documentation
        for more details.
    subset_method : str, optional
        The subset method ('nearest' or 'strict') when requesting the dataset.
        If strict, you can only request dimensions strictly inside the dataset.
    force_service : str, optional
        Force a specific service for data download.
    credentials_file : Union[pathlib.Path, str], optional
        Path to a credentials file for authentication.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the loaded Copernicus Marine data.
    """  # noqa

    start_datetime = homogenize_datetime(start_datetime)
    end_datetime = homogenize_datetime(end_datetime)
    credentials_file = (
        pathlib.Path(credentials_file) if credentials_file else None
    )
    load_request = LoadRequest(
        dataset_id=dataset_id,
        force_dataset_version=dataset_version,
        force_dataset_part=dataset_part,
        username=username,
        password=password,
        variables=variables,
        geographical_parameters=GeographicalParameters(
            latitude_parameters=LatitudeParameters(
                minimum_latitude=minimum_latitude,
                maximum_latitude=maximum_latitude,
            ),
            longitude_parameters=LongitudeParameters(
                minimum_longitude=minimum_longitude,
                maximum_longitude=maximum_longitude,
            ),
        ),
        temporal_parameters=TemporalParameters(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        ),
        subset_method=subset_method,
        depth_parameters=DepthParameters(
            minimum_depth=minimum_depth,
            maximum_depth=maximum_depth,
            vertical_dimension_as_originally_produced=vertical_dimension_as_originally_produced,  # noqa
        ),
        bounding_box_method=bounding_box_method,
        force_service=force_service,
        credentials_file=credentials_file,
    )
    dataset = load_data_object_from_load_request(
        load_request,
        read_dataframe_from_arco_series,
    )
    return dataset
