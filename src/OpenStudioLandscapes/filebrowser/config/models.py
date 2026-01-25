import enum
import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from OpenStudioLandscapes.engine.config.str_gen import get_config_str

from OpenStudioLandscapes.filebrowser import constants, dist


class FilebrowerRootPermission(enum.StrEnum):
    rw = "rw"
    ro = "ro"


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    filebrowser_port_container: PositiveInt = Field(
        default=80,
        description="The filebrowser container port.",
        frozen=True,
    )
    filebrowser_port_host: PositiveInt = Field(
        default=8080,
        description="The Kitsu host port.",
        frozen=False,
    )

    filebrowser_docker_image: str = Field(
        default="docker.io/filebrowser/filebrowser",
    )

    filebrowser_shared_dir_permission: FilebrowerRootPermission = Field(
        default=FilebrowerRootPermission.rw,
        description="The filebrowser root permission.",
        examples=[i.name for i in FilebrowerRootPermission],
    )

    filebrowser_db_dir: pathlib.Path = Field(
        default=pathlib.Path(
            "{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/configs/filebrowser_db"
        ),
        description="Where on the host to store the database.",
    )

    filebrowser_shared_dir: pathlib.Path = Field(
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/shared"),
        description="Set the shared directory on the host. If you want this "
        "to be absolut path on the system outside of the Landscape, "
        "say `/root/data`, make sure `shared` is a symbolic link "
        "pointing to `/root/data`.",
    )

    filebrowser_json: pathlib.Path = Field(
        default=pathlib.Path(
            "{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/configs/filebrowser.json"
        ),
        description="Where on the host to store the configuration file.",
    )

    # EXPANDABLE PATHS
    @property
    def filebrowser_db_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.filebrowser_db_dir}...")
        ret = pathlib.Path(
            self.filebrowser_db_dir.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def filebrowser_shared_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.filebrowser_shared_dir}...")
        ret = pathlib.Path(
            self.filebrowser_shared_dir.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret

    @property
    def filebrowser_json_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.filebrowser_json}...")
        ret = pathlib.Path(
            self.filebrowser_json.expanduser()  # pylint: disable=E1101
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = get_config_str(
    Config=Config,
)
