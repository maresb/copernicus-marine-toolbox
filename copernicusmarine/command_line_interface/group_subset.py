import logging
import pathlib
from typing import List, Optional

import click

from copernicusmarine.command_line_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicusmarine.command_line_interface.utils import (
    assert_cli_args_are_not_set_except_create_template,
    force_dataset_part_option,
    force_dataset_version_option,
    tqdm_disable_option,
)
from copernicusmarine.core_functions import documentation_utils
from copernicusmarine.core_functions.deprecated import (
    DeprecatedClickOptionsCommand,
)
from copernicusmarine.core_functions.models import (
    DEFAULT_COORDINATES_SELECTION_METHOD,
    DEFAULT_COORDINATES_SELECTION_METHODS,
    DEFAULT_FILE_FORMAT,
    DEFAULT_FILE_FORMATS,
    DEFAULT_VERTICAL_DIMENSION_OUTPUT,
    DEFAULT_VERTICAL_DIMENSION_OUTPUTS,
    CoordinatesSelectionMethod,
    FileFormat,
    VerticalDimensionOutput,
)
from copernicusmarine.core_functions.subset import (
    create_subset_template,
    subset_function,
)
from copernicusmarine.core_functions.utils import (
    OVERWRITE_LONG_OPTION,
    OVERWRITE_OPTION_HELP_TEXT,
    OVERWRITE_SHORT_OPTION,
    datetime_parser,
)

logger = logging.getLogger("copernicusmarine")
blank_logger = logging.getLogger("copernicusmarine_blank_logger")


@click.group()
def cli_subset() -> None:
    pass


@cli_subset.command(
    "subset",
    cls=DeprecatedClickOptionsCommand,
    short_help="Download subsets of datasets as NetCDF files or Zarr stores.",
    help="""
    Download subsets of datasets as NetCDF files or Zarr stores.

    The ``--dataset-id`` is required (can be found via the "describe" command). The argument values passed individually through the CLI take precedence over the values from the ``--motu-api-request`` option, which takes precedence over the ones from the ``--request-file`` option.
    """,  # noqa
    epilog="""
    .. code-block:: bash

        copernicusmarine subset
        --dataset-id cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i
        --variable thetao
        --start-datetime 2022-01-01T00:00:00
        --end-datetime 2022-12-31T23:59:59
        --minimum-longitude -6.17
        --maximum-longitude -5.08
        --minimum-latitude 35.75
        --maximum-latitude 36.30
        --minimum-depth 0.0
        --maximum-depth 5.0

    Equivalent to:

    .. code-block:: bash

        copernicusmarine subset -i cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i -v thetao -t 2022-01-01T00:00:00 -T 2022-12-31T23:59:59 -x -6.17 -X -5.08 -y 35.75 -Y 36.30 -z 0.0 -Z 5.0
    """,  # noqa
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    default=None,
    help=documentation_utils.SUBSET_HELP["DATASET_ID_HELP"],
)
@force_dataset_version_option
@force_dataset_part_option
@click.option(
    "--username",
    type=str,
    default=None,
    help=documentation_utils.SUBSET_HELP["USERNAME_HELP"],
)
@click.option(
    "--password",
    type=str,
    default=None,
    help=documentation_utils.SUBSET_HELP["PASSWORD_HELP"],
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help=documentation_utils.SUBSET_HELP["VARIABLE_HELP"],
    multiple=True,
)
@click.option(
    "--minimum-longitude",
    "-x",
    type=float,
    help=documentation_utils.SUBSET_HELP["MINIMUM_LONGITUDE_HELP"],
)
@click.option(
    "--maximum-longitude",
    "-X",
    type=float,
    help=documentation_utils.SUBSET_HELP["MAXIMUM_LONGITUDE_HELP"],
)
@click.option(
    "--minimum-latitude",
    "-y",
    type=click.FloatRange(min=-90, max=90),
    help=documentation_utils.SUBSET_HELP["MINIMUM_LATITUDE_HELP"],
)
@click.option(
    "--maximum-latitude",
    "-Y",
    type=click.FloatRange(min=-90, max=90),
    help=documentation_utils.SUBSET_HELP["MAXIMUM_LATITUDE_HELP"],
)
@click.option(
    "--minimum-depth",
    "-z",
    type=click.FloatRange(min=0),
    help=documentation_utils.SUBSET_HELP["MINIMUM_DEPTH_HELP"],
)
@click.option(
    "--maximum-depth",
    "-Z",
    type=click.FloatRange(min=0),
    help=documentation_utils.SUBSET_HELP["MAXIMUM_DEPTH_HELP"],
)
@click.option(
    "--vertical-dimension-output",
    "-V",
    type=click.Choice(DEFAULT_VERTICAL_DIMENSION_OUTPUTS),
    default=DEFAULT_VERTICAL_DIMENSION_OUTPUT,
    help=documentation_utils.SUBSET_HELP["VERTICAL_DIMENSION_OUTPUT_HELP"],
)
@click.option(
    "--start-datetime",
    "-t",
    type=str,
    help=documentation_utils.SUBSET_HELP["START_DATETIME_HELP"],
)
@click.option(
    "--end-datetime",
    "-T",
    type=str,
    help=documentation_utils.SUBSET_HELP["END_DATETIME_HELP"],
)
@click.option(
    "--coordinates-selection-method",
    type=click.Choice(DEFAULT_COORDINATES_SELECTION_METHODS),
    default=DEFAULT_COORDINATES_SELECTION_METHOD,
    help=documentation_utils.SUBSET_HELP["COORDINATES_SELECTION_METHOD_HELP"],
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(path_type=pathlib.Path),
    help=documentation_utils.SUBSET_HELP["OUTPUT_DIRECTORY_HELP"],
)
@click.option(
    "--credentials-file",
    type=click.Path(path_type=pathlib.Path),
    help=documentation_utils.SUBSET_HELP["CREDENTIALS_FILE_HELP"],
)
@click.option(
    "--output-filename",
    "-f",
    type=str,
    help=documentation_utils.SUBSET_HELP["OUTPUT_FILENAME_HELP"],
)
@click.option(
    "--file-format",
    type=click.Choice(DEFAULT_FILE_FORMATS),
    default=DEFAULT_FILE_FORMAT,
    help=documentation_utils.SUBSET_HELP["FILE_FORMAT_HELP"],
)
@click.option(
    "--force-download",
    is_flag=True,
    default=False,
    help=documentation_utils.SUBSET_HELP["FORCE_DOWNLOAD_HELP"],
)
@click.option(
    OVERWRITE_LONG_OPTION,
    OVERWRITE_SHORT_OPTION,
    is_flag=True,
    default=False,
    help=OVERWRITE_OPTION_HELP_TEXT,
)
@click.option(
    "--service",
    "-s",
    type=str,
    help=documentation_utils.SUBSET_HELP["SERVICE_HELP"],
)
@click.option(
    "--create-template",
    type=bool,
    is_flag=True,
    default=False,
    help=documentation_utils.SUBSET_HELP["CREATE_TEMPLATE_HELP"],
)
@click.option(
    "--request-file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help=documentation_utils.SUBSET_HELP["REQUEST_FILE_HELP"],
)
@click.option(
    "--motu-api-request",
    type=str,
    help=documentation_utils.SUBSET_HELP["MOTU_API_REQUEST_HELP"],
)
@click.option(
    "--dry-run",
    type=bool,
    is_flag=True,
    default=False,
    help=documentation_utils.SUBSET_HELP["DRY_RUN_HELP"],
)
@tqdm_disable_option
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=documentation_utils.SUBSET_HELP["LOG_LEVEL_HELP"],
)
@click.option(
    "--staging",
    type=bool,
    default=False,
    is_flag=True,
    hidden=True,
)
@click.option(
    "--netcdf-compression-enabled",
    type=bool,
    default=False,
    is_flag=True,
    help=documentation_utils.SUBSET_HELP["NETCDF_COMPRESSION_ENABLED_HELP"],
)
@click.option(
    "--netcdf-compression-level",
    type=click.IntRange(0, 9),
    help=documentation_utils.SUBSET_HELP["NETCDF_COMPRESSION_LEVEL_HELP"],
)
@click.option(
    "--netcdf3-compatible",
    type=bool,
    default=False,
    is_flag=True,
    help=documentation_utils.SUBSET_HELP["NETCDF_COMPATIBLE_HELP"],
)
@log_exception_and_exit
def subset(
    dataset_id: str,
    dataset_version: Optional[str],
    dataset_part: Optional[str],
    username: Optional[str],
    password: Optional[str],
    variables: Optional[List[str]],
    minimum_longitude: Optional[float],
    maximum_longitude: Optional[float],
    minimum_latitude: Optional[float],
    maximum_latitude: Optional[float],
    minimum_depth: Optional[float],
    maximum_depth: Optional[float],
    vertical_dimension_output: VerticalDimensionOutput,
    start_datetime: Optional[str],
    end_datetime: Optional[str],
    coordinates_selection_method: CoordinatesSelectionMethod,
    output_filename: Optional[str],
    file_format: FileFormat,
    netcdf_compression_enabled: bool,
    netcdf_compression_level: Optional[int],
    netcdf3_compatible: bool,
    service: Optional[str],
    create_template: bool,
    request_file: Optional[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    motu_api_request: Optional[str],
    force_download: bool,
    overwrite_output_data: bool,
    dry_run: bool,
    disable_progress_bar: bool,
    log_level: str,
    staging: bool = False,
):
    if log_level == "QUIET":
        logger.disabled = True
        logger.setLevel(level="CRITICAL")
    else:
        logger.setLevel(level=log_level)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("DEBUG mode activated")

    if create_template:
        assert_cli_args_are_not_set_except_create_template(
            click.get_current_context()
        )
        create_subset_template()
        return

    response = subset_function(
        dataset_id=dataset_id,
        force_dataset_version=dataset_version,
        force_dataset_part=dataset_part,
        username=username,
        password=password,
        variables=variables,
        minimum_longitude=minimum_longitude,
        maximum_longitude=maximum_longitude,
        minimum_latitude=minimum_latitude,
        maximum_latitude=maximum_latitude,
        minimum_depth=minimum_depth,
        maximum_depth=maximum_depth,
        vertical_dimension_output=vertical_dimension_output,
        start_datetime=(
            datetime_parser(start_datetime) if start_datetime else None
        ),
        end_datetime=datetime_parser(end_datetime) if end_datetime else None,
        coordinates_selection_method=coordinates_selection_method,
        output_filename=output_filename,
        file_format=file_format,
        force_service=service,
        request_file=request_file,
        output_directory=output_directory,
        credentials_file=credentials_file,
        motu_api_request=motu_api_request,
        force_download=force_download,
        overwrite_output_data=overwrite_output_data,
        dry_run=dry_run,
        disable_progress_bar=disable_progress_bar,
        staging=staging,
        netcdf_compression_enabled=netcdf_compression_enabled,
        netcdf_compression_level=netcdf_compression_level,
        netcdf3_compatible=netcdf3_compatible,
    )
    blank_logger.info(response.model_dump_json(indent=2))
