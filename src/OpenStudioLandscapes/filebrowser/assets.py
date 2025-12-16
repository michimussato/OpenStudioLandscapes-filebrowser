import copy
import enum
import json
import pathlib
from pathlib import Path
from typing import Any, Generator, Union

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset, AssetsDefinition,
)
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
# from OpenStudioLandscapes.engine.common_assets.constants import get_constants

from OpenStudioLandscapes.engine.common_assets.compose_scope import get_compose_scope_group__cmd
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
# from OpenStudioLandscapes.engine.common_assets.docker_config import get_docker_config
# from OpenStudioLandscapes.engine.common_assets.docker_config_json import (
#     get_docker_config_json,
# )
# from OpenStudioLandscapes.engine.common_assets.env import get_env

from OpenStudioLandscapes.engine.common_assets.feature import get_feature__CONFIG
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out, get_feature_out_v2
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in, get_feature_in, get_feature_in_parent
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.config.models import ConfigEngine
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import *

from OpenStudioLandscapes.filebrowser import dist
from OpenStudioLandscapes.filebrowser.config.models import CONFIG_STR, Config
from OpenStudioLandscapes.filebrowser.constants import *

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
yaml.SafeDumper.add_multi_representer(
    data_type=enum.Enum,
    representer=yaml.representer.SafeRepresenter.represent_str,
)


compose_scope_group__cmd: AssetsDefinition = get_compose_scope_group__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=CONFIG_STR,
    search_model_of_type=Config,
)

feature_in: AssetsDefinition = get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)

group_out: AssetsDefinition = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = get_feature_in_parent(
    ASSET_HEADER=ASSET_HEADER,
    config_parent=ConfigParent,
)


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def compose_networks(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None
]:

    env: dict = CONFIG.env

    compose_network_mode = DockerComposePolicies.NETWORK_MODE.BRIDGE

    docker_dict = get_network_dicts(
        context=context,
        compose_network_mode=compose_network_mode,
        env=env,
    )

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_networks"]),
        ),
        "filebrowser_json": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "filebrowser_json"]),
        ),
        "filebrowser_db": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "filebrowser_db"]),
        ),
        "shared_directory": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "shared_directory"]),
        ),
    },
)
def compose_filebrowser(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    filebrowser_json: pathlib.Path,  # pylint: disable=redefined-outer-name
    filebrowser_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    shared_directory: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """"""

    env: dict = CONFIG.env

    config_engine: ConfigEngine = CONFIG.config_engine

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{CONFIG.filebrowser_port_host}:{CONFIG.filebrowser_port_container}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks["network_mode"]}

    volumes_dict = {
        "volumes": [
            f"{filebrowser_json.as_posix()}:/config/settings.json:ro",
            f"{filebrowser_db.as_posix()}:/database:rw",
        ]
    }

    # For portability, convert absolute volume paths to relative paths

    _volume_relative = []

    for v in volumes_dict["volumes"]:

        host, container = v.split(":", maxsplit=1)

        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=CONFIG.docker_compose_expanded,
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            f"{shared_directory.as_posix()}:/shared:{env['FILEBROWSER_ROOT_PERMISSION']}",
            *_volume_relative,
        ]
    }

    service_name = "filebrowser"
    container_name, host_name = get_docker_compose_names(
        context=context,
        service_name=service_name,
        landscape_id=env.get("LANDSCAPE", "default"),
        domain_lan=config_engine.openstudiolandscapes__domain_lan,
    )
    # container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    # host_name = ".".join(
    #     [service_name, env["OPENSTUDIOLANDSCAPES__DOMAIN_LAN"]]
    # )

    docker_dict = {
        "services": {
            service_name: {
                "image": "docker.io/filebrowser/filebrowser",
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict),
                **copy.deepcopy(volumes_dict),
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_filebrowser": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "compose_filebrowser"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list[dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
        # "shared_directory": AssetIn(
        #     AssetKey([*ASSET_HEADER["key_prefix"], "shared_directory"]),
        # ),
    },
)
def filebrowser_json(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    # shared_directory: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Path] | AssetMaterialization | Any, None, None]:

    filebrowser_dict = {
        "port": 80,
        "baseURL": "",
        "address": "",
        "log": "stdout",
        "database": "/database/filebrowser.db",
        "root": "/shared",
        "noauth": True,
    }

    filebrowser_json_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
        "configs",
        "filebrowser.json",
    ).expanduser()

    filebrowser_json_file.parent.mkdir(parents=True, exist_ok=True)

    with open(filebrowser_json_file, "w") as fw:
        json.dump(
            filebrowser_dict,
            fw,
            ensure_ascii=True,
            indent=4,
        )

    yield Output(filebrowser_json_file)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(
                filebrowser_json_file
            ),
            "filebrowser_dict": MetadataValue.json(filebrowser_dict),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "CONFIG": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "CONFIG"]),
        ),
    },
)
def filebrowser_db(
    context: AssetExecutionContext,
    CONFIG: Config,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Path] | AssetMaterialization | Any, None, None]:

    filebrowser_db_dir = CONFIG.filebrowser_db_dir_expanded

    filebrowser_db_dir.mkdir(parents=True, exist_ok=True)

    yield Output(filebrowser_db_dir)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(filebrowser_db_dir),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
    },
)
def shared_directory(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Path] | AssetMaterialization | Any, None, None]:

    root = env.get("FILEBROWSER_ROOT", "")

    if bool(root):
        root = pathlib.Path(root).expanduser()

        if not root.exists():
            raise FileNotFoundError(
                f"Directory {root.as_posix()} does not exist. "
                f"Please create it manually first."
            )

    else:
        shared_directory = pathlib.Path(
            env["DOT_LANDSCAPES"],
            env.get("LANDSCAPE", "default"),
            f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
            "shared_directory",
        ).expanduser()

        shared_directory.mkdir(parents=True, exist_ok=True)

        # For portability, convert absolute volume paths to relative paths
        volume_dir_host_rel_path = get_relative_path_via_common_root(
            context=context,
            path_src=pathlib.Path(env["DOCKER_COMPOSE"]),
            path_dst=shared_directory,
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )
        root = volume_dir_host_rel_path

    yield Output(root)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.path(root),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_extend(
    context: AssetExecutionContext,
) -> Generator[Output[list[Any]] | AssetMaterialization | Any, Any, None]:

    ret = []

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={},
)
def cmd_append(
    context: AssetExecutionContext,
) -> Generator[Output[dict[str, list[Any]]] | AssetMaterialization | Any, Any, None]:

    ret = {"cmd": [], "exclude_from_quote": []}

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
