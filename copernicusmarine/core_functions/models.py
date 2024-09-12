import pathlib
from typing import Literal, Optional, get_args

from pydantic import BaseModel, model_serializer

FileFormat = Literal["netcdf", "zarr"]
DEFAULT_FILE_FORMAT: FileFormat = "netcdf"
DEFAULT_FILE_FORMATS = list(get_args(FileFormat))

FileExtension = Literal[".nc", ".zarr"]
DEFAULT_FILE_EXTENSION: FileExtension = ".nc"
DEFAULT_FILE_EXTENSIONS = list(get_args(FileExtension))

SubsetMethod = Literal["nearest", "strict"]
DEFAULT_SUBSET_METHOD: SubsetMethod = "nearest"
DEFAULT_SUBSET_METHODS = list(get_args(SubsetMethod))

BoundingBoxMethod = Literal["inside", "nearest", "outside"]
DEFAULT_BOUNDING_BOX_METHOD: BoundingBoxMethod = "inside"
DEFAULT_BOUNDING_BOX_METHODS = list(get_args(BoundingBoxMethod))


class FileGet(BaseModel):
    #: Full url of the location of the file server side.
    url: str
    #: Size of the file in MB.
    size: float
    #: Last modified date.
    last_modified: str
    #: Path to the local downloaded file
    output: pathlib.Path


class ResponseGet(BaseModel):
    """Metadata returned when using :func:`~copernicusmarine.get`"""

    #: Description of the files concerned by the query
    files: list[FileGet]


class GeographicalExtent(BaseModel):
    """Interval for geographical coordinates."""

    minimum: Optional[float]
    maximum: Optional[float]


class TimeExtent(BaseModel):
    """Interval for time coordinate."""

    minimum: Optional[str]
    maximum: Optional[str]


class DatasetCoordinatesExtent(BaseModel):
    #: Longitude Interval of the subsetted data.
    longitude: GeographicalExtent
    #: Latitude Interval of the subsetted data.
    latitude: GeographicalExtent
    #: Time Interval of the subsetted data in iso8601 string
    time: TimeExtent
    #: Depth Interval of the subsetted data.
    depth: Optional[GeographicalExtent] = None
    #: Elevation Interval of the subsetted data.
    #: Is relevant if data are requested for elevation
    #: instead of depth
    elevation: Optional[GeographicalExtent] = None

    @model_serializer(mode="wrap")
    def _serialize(self, handler):
        d = handler(self)
        if not self.depth:
            del d["depth"]
        if not self.elevation:
            del d["elevation"]
        return d


class ResponseSubset(BaseModel):
    """Metadata returned when using :func:`~copernicusmarine.subset`"""

    #: Path to the result file.
    output: pathlib.Path
    #: Estimation of the size of the final result file in MB.
    size: Optional[float]
    #: Estimation of the maximum amount of data needed to
    #: get the final result in MB.
    data_needed: Optional[float]
    #: The bounds of the subsetted dataset.
    coodinates_extent: DatasetCoordinatesExtent
