import copy
import json
import pathlib
from pathlib import Path
from typing import Any, Generator

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets.compose import get_compose
from OpenStudioLandscapes.engine.common_assets.constants import get_constants
from OpenStudioLandscapes.engine.common_assets.docker_compose_graph import (
    get_docker_compose_graph,
)
from OpenStudioLandscapes.engine.common_assets.docker_config import get_docker_config
from OpenStudioLandscapes.engine.common_assets.docker_config_json import (
    get_docker_config_json,
)
from OpenStudioLandscapes.engine.common_assets.env import get_env
from OpenStudioLandscapes.engine.common_assets.feature_out import get_feature_out
from OpenStudioLandscapes.engine.common_assets.group_in import get_group_in
from OpenStudioLandscapes.engine.common_assets.group_out import get_group_out
from OpenStudioLandscapes.engine.constants import *
from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *

from OpenStudioLandscapes.filebrowser.constants import *

constants = get_constants(
    ASSET_HEADER=ASSET_HEADER,
)


docker_config = get_docker_config(
    ASSET_HEADER=ASSET_HEADER,
)


group_in = get_group_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_PARENT=ASSET_HEADER_BASE,
    input_name=str(GroupIn.BASE_IN),
)


env = get_env(
    ASSET_HEADER=ASSET_HEADER,
)


group_out = get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph = get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose = get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out = get_feature_out(
    ASSET_HEADER=ASSET_HEADER,
    feature_out_ins={
        "env": dict,
        "compose": dict,
        "group_in": dict,
    },
)


docker_config_json = get_docker_config_json(
    ASSET_HEADER=ASSET_HEADER,
)


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None
]:

    compose_network_mode = ComposeNetworkMode.DEFAULT

    if compose_network_mode == ComposeNetworkMode.DEFAULT:
        docker_dict = {
            "networks": {
                # "mongodb": {
                #     "name": "network_mongodb-10-2",
                # },
                "repository": {
                    "name": "network_repository-10-2",
                },
                # "ayon": {
                #     "name": "network_ayon-10-2",
                # },
            },
        }

    else:
        docker_dict = {
            "network_mode": compose_network_mode.value,
        }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
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
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    filebrowser_json: pathlib.Path,  # pylint: disable=redefined-outer-name
    filebrowser_db: pathlib.Path,  # pylint: disable=redefined-outer-name
    shared_directory: pathlib.Path,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {"networks": list(compose_networks.get("networks", {}).keys())}
        ports_dict = {
            "ports": [
                f"{env.get('FILEBROWSER_PORT_HOST')}:{env.get('FILEBROWSER_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {"network_mode": compose_networks.get("network_mode")}

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
            path_src=pathlib.Path(env["DOCKER_COMPOSE"]),
            path_dst=pathlib.Path(host),
            path_common_root=pathlib.Path(env["DOT_LANDSCAPES"]),
        )

        _volume_relative.append(
            f"{volume_dir_host_rel_path.as_posix()}:{container}",
        )

    volumes_dict = {
        "volumes": [
            f"{shared_directory.as_posix()}:/shared:{env.get('FILEBROWSER_ROOT_PERMISSION')}",
            *_volume_relative,
        ]
    }

    service_name = "filebrowser"
    container_name = "--".join([service_name, env.get("LANDSCAPE", "default")])
    host_name = ".".join([service_name, env["ROOT_DOMAIN"]])

    docker_dict = {
        "services": {
            service_name: {
                "image": "docker.io/filebrowser/filebrowser",
                "container_name": container_name,
                "hostname": host_name,
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
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
        "env": AssetIn(
            AssetKey([*ASSET_HEADER["key_prefix"], "env"]),
        ),
    },
)
def filebrowser_db(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Path] | AssetMaterialization | Any, None, None]:

    filebrowser_db_dir = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE", "default"),
        f"{ASSET_HEADER['group_name']}__{'__'.join(ASSET_HEADER['key_prefix'])}",
        "configs",
        "filebrowser_db",
    ).expanduser()

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
