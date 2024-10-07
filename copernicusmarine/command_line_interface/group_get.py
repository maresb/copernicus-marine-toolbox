import logging
import pathlib
from typing import Optional

import click

from copernicusmarine.command_line_interface.exception_handler import (
    log_exception_and_exit,
)
from copernicusmarine.command_line_interface.utils import (
    MutuallyExclusiveOption,
    assert_cli_args_are_not_set_except_create_template,
    force_dataset_part_option,
    force_dataset_version_option,
    tqdm_disable_option,
)
from copernicusmarine.core_functions import documentation_utils
from copernicusmarine.core_functions.deprecated import (
    DeprecatedClickOptionsCommand,
)
from copernicusmarine.core_functions.get import (
    create_get_template,
    get_function,
)
from copernicusmarine.core_functions.utils import (
    OVERWRITE_LONG_OPTION,
    OVERWRITE_OPTION_HELP_TEXT,
    OVERWRITE_SHORT_OPTION,
)

logger = logging.getLogger("copernicusmarine")
blank_logger = logging.getLogger("copernicusmarine_blank_logger")


@click.group()
def cli_get() -> None:
    pass


@cli_get.command(
    "get",
    cls=DeprecatedClickOptionsCommand,
    short_help="Download originally produced data files.",
    help="""
    Download originally produced data files.

    The ``--dataset-id`` is required (can be found via the "describe" command). The function fetches the files recursively if a folder path is passed as a URL. When provided a dataset ID, all the files in the corresponding folder will be downloaded if none of the ``--filter`` or ``--regex`` options is specified.
    """,  # noqa
    epilog="""
    .. code-block:: bash

        # Example: Download all files from a dataset
        copernicusmarine get -i cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m
    """,  # noqa
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["DATASET_ID_HELP"],
)
@force_dataset_version_option
@force_dataset_part_option
@click.option(
    "--username",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["USERNAME_HELP"],
)
@click.option(
    "--password",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["PASSWORD_HELP"],
)
@click.option(
    "--no-directories",
    "-nd",
    cls=MutuallyExclusiveOption,
    is_flag=True,
    help=documentation_utils.GET_HELP["NO_DIRECTORIES_HELP"],
    default=False,
    mutually_exclusive=["sync"],
)
@click.option(
    "--show-outputnames",
    is_flag=True,
    help=documentation_utils.GET_HELP["SHOW_OUTPUTNAMES_HELP"],
    default=False,
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(path_type=pathlib.Path),
    help=documentation_utils.GET_HELP["OUTPUT_DIRECTORY_HELP"],
)
@click.option(
    "--credentials-file",
    type=click.Path(path_type=pathlib.Path),
    help=documentation_utils.GET_HELP["CREDENTIALS_FILE_HELP"],
)
@click.option(
    "--force-download",
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["FORCE_DOWNLOAD_HELP"],
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
    help=documentation_utils.GET_HELP["SERVICE_HELP"],
)
@click.option(
    "--create-template",
    type=bool,
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["CREATE_TEMPLATE_HELP"],
)
@click.option(
    "--request-file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help=documentation_utils.GET_HELP["REQUEST_FILE_HELP"],
)
@click.option(
    "--filter",
    "--filter-with-globbing-pattern",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["FILTER_WITH_GLOBBING_PATTERN_HELP"],
)
@click.option(
    "--regex",
    "--filter-with-regular-expression",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["FILTER_WITH_REGULAR_EXPRESSION_HELP"],
)
@click.option(
    "--file-list",
    type=pathlib.Path,
    default=None,
    help=documentation_utils.GET_HELP["FILE_LIST_HELP"],
)
@click.option(
    "--create-file-list",
    type=str,
    default=None,
    help=documentation_utils.GET_HELP["CREATE_FILE_LIST_HELP"],
)
@click.option(
    "--sync",
    cls=MutuallyExclusiveOption,
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["SYNC_HELP"],
    mutually_exclusive=["no-directories"],
)
@click.option(
    "--sync-delete",
    cls=MutuallyExclusiveOption,
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["SYNC_DELETE_HELP"],
    mutually_exclusive=["no-directories"],
)
@click.option(
    "--index-parts",
    type=bool,
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["INDEX_PARTS_HELP"],
)
@click.option(
    "--dry-run",
    type=bool,
    is_flag=True,
    default=False,
    help=documentation_utils.GET_HELP["DRY_RUN_HELP"],
)
@click.option(
    "--max-concurrent-requests",
    type=int,
    default=15,
    help=documentation_utils.GET_HELP["MAX_CONCURRENT_REQUESTS_HELP"],
)
@tqdm_disable_option
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=documentation_utils.GET_HELP["LOG_LEVEL_HELP"],
)
@click.option(
    "--staging",
    type=bool,
    default=False,
    is_flag=True,
    hidden=True,
)
@log_exception_and_exit
def get(
    dataset_id: Optional[str],
    dataset_version: Optional[str],
    dataset_part: Optional[str],
    username: Optional[str],
    password: Optional[str],
    no_directories: bool,
    show_outputnames: bool,
    output_directory: Optional[pathlib.Path],
    credentials_file: Optional[pathlib.Path],
    force_download: bool,
    overwrite_output_data: bool,
    create_template: bool,
    request_file: Optional[pathlib.Path],
    service: Optional[str],
    filter: Optional[str],
    regex: Optional[str],
    file_list: Optional[pathlib.Path],
    create_file_list: Optional[str],
    sync: bool,
    sync_delete: bool,
    index_parts: bool,
    dry_run: bool,
    max_concurrent_requests: int,
    disable_progress_bar: bool,
    log_level: str,
    staging: bool,
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
        create_get_template()
        return

    result = get_function(
        dataset_id=dataset_id,
        force_dataset_version=dataset_version,
        force_dataset_part=dataset_part,
        username=username,
        password=password,
        no_directories=no_directories,
        show_outputnames=show_outputnames,
        output_directory=output_directory,
        credentials_file=credentials_file,
        force_download=force_download,
        overwrite_output_data=overwrite_output_data,
        request_file=request_file,
        force_service=service,
        filter=filter,
        regex=regex,
        file_list_path=file_list,
        create_file_list=create_file_list,
        sync=sync,
        sync_delete=sync_delete,
        index_parts=index_parts,
        dry_run=dry_run,
        max_concurrent_requests=max_concurrent_requests,
        disable_progress_bar=disable_progress_bar,
        staging=staging,
    )
    blank_logger.info(result.model_dump_json(indent=2))
