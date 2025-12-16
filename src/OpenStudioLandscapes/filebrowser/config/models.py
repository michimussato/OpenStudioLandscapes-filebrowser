import enum
import pathlib

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel

from OpenStudioLandscapes.filebrowser import dist

config_default = pathlib.Path(__file__).parent.joinpath("config_default.yml")
CONFIG_STR = config_default.read_text()


class FilebrowerRootPermission(enum.StrEnum):
    rw = "rw"
    ro = "ro"


class Config(FeatureBaseModel):
    feature_name: str = dist.name

    definitions: str = "OpenStudioLandscapes.filebrowser.definitions"

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

    filebrowser_root_permission: FilebrowerRootPermission = Field(
        default="rw",
        description="The filebrowser root permission.",
        examples=["rw", "ro"],
    )

    filebrowser_db_dir: pathlib.Path = Field()

    # EXPANDABLE PATHS
    @property
    def filebrowser_db_dir_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")

        LOGGER.debug(f"Expanding {self.filebrowser_db_dir}...")
        ret = pathlib.Path(
            self.filebrowser_db_dir.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret