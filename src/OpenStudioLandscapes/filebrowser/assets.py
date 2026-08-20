# pylint: disable=line-too-long,invalid-name
import copy
import enum
import pathlib
from typing import Dict, Generator, List, Union

import yaml
from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    AssetsDefinition,
    MetadataValue,
    Output,
    asset,
)
from OpenStudioLandscapes.engine.common_assets import (
    cmd,
    compose,
    docker_compose_graph,
    feature,
    feature_out,
    group_in,
    group_out,
)
from OpenStudioLandscapes.engine.config.models import ConfigEngine
from OpenStudioLandscapes.engine.constants import (
    ASSET_HEADER_BASE,
    ConfigParent,
)
from OpenStudioLandscapes.engine.enums import (
    DockerComposePolicies,
)
from OpenStudioLandscapes.engine.utils import (
    get_docker_compose_names,
    get_relative_path_via_common_root,
)
from OpenStudioLandscapes.engine.utils.docker.compose_dicts import (
    get_network_dicts,
)

from OpenStudioLandscapes.filebrowser.constants import (
    ASSET_HEADER,
    LOGGER,
    dist,
)
from OpenStudioLandscapes.filebrowser.config import models

# https://github.com/yaml/pyyaml/issues/722#issuecomment-1969292770
yaml.SafeDumper.add_multi_representer(
    data_type=enum.Enum,
    representer=yaml.representer.SafeRepresenter.represent_str,
)


cmd: AssetsDefinition = cmd.get_feature__cmd(
    ASSET_HEADER=ASSET_HEADER,
)

CONFIG: AssetsDefinition = feature.get_feature__CONFIG(
    ASSET_HEADER=ASSET_HEADER,
    CONFIG_STR=models.CONFIG_STR,
    search_model_of_type=models.Config,
)

feature_in: AssetsDefinition = group_in.get_feature_in(
    ASSET_HEADER=ASSET_HEADER,
    ASSET_HEADER_BASE=ASSET_HEADER_BASE,
    ASSET_HEADER_FEATURE_IN={},
)

group_out: AssetsDefinition = group_out.get_group_out(
    ASSET_HEADER=ASSET_HEADER,
)


docker_compose_graph: AssetsDefinition = docker_compose_graph.get_docker_compose_graph(
    ASSET_HEADER=ASSET_HEADER,
)


compose: AssetsDefinition = compose.get_compose(
    ASSET_HEADER=ASSET_HEADER,
)


feature_out_v2: AssetsDefinition = feature_out.get_feature_out_v2(
    ASSET_HEADER=ASSET_HEADER,
)


# Produces
# - feature_in_parent
# - CONFIG_PARENT
# if ConfigParent is or type FeatureBaseModel
feature_in_parent: Union[AssetsDefinition, None] = group_in.get_feature_in_parent(
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
    CONFIG: models.Config,  # pylint: disable=redefined-outer-name
) -> Generator[
    Output[Dict[str, Dict[str, Dict[str, str]]]] | AssetMaterialization, None, None
]:

    env: Dict = CONFIG.env

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
    },
)
def compose_filebrowser(
    context: AssetExecutionContext,
    CONFIG: models.Config,  # pylint: disable=redefined-outer-name
    compose_networks: Dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[Dict] | AssetMaterialization, None, None]:
    """"""

    env: Dict = CONFIG.env

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

    db_dir: pathlib.Path = CONFIG.filebrowser_db_dir_expanded
    db_dir.mkdir(parents=True, exist_ok=True)

    shared_directory: pathlib.Path = CONFIG.filebrowser_shared_dir_host_expanded
    shared_directory.mkdir(parents=True, exist_ok=True)

    volumes_dict = {
        "volumes": [
            f"{db_dir.as_posix()}:/database",
            f"{shared_directory.as_posix()}:{CONFIG.filebrowser_shared_dir_container.as_posix()}:{CONFIG.filebrowser_shared_dir_permission}",
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
        "volumes": list(
            {
                *_volume_relative,
                *config_engine.global_bind_volumes,
                *CONFIG.local_bind_volumes,
            }
        )
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

    cmd_ = [
        "--database",
        "/database/filebrowser.db",
        "--username",
        CONFIG.default_username,
        "--password",
        CONFIG.default_password_hashed,
        "--root",
        CONFIG.filebrowser_shared_dir_container.as_posix(),
        "--port",
        str(CONFIG.filebrowser_port_container),
        "--baseURL",
        "",
        "--address",
        "",
        "--log",
        "stdout",
    ]

    if CONFIG.filebrowser_noauth:
        cmd_.append("--noauth")

    docker_dict = {
        "services": {
            service_name: {
                "image": "docker.io/filebrowser/filebrowser",
                "container_name": container_name,
                "hostname": host_name,
                "domainname": config_engine.openstudiolandscapes__domain_lan,
                "restart": DockerComposePolicies.RESTART_POLICY.ALWAYS.value,
                # from https://hub.docker.com/r/filebrowser/filebrowser/tags?name=latest
                # - ENTRYPOINT ["tini" "--" "/init.sh"]
                "command": cmd_,
                "environment": {
                    "TZ": config_engine.tz,
                    **config_engine.global_environment_variables,
                    **CONFIG.local_environment_variables,
                    # - PUID=$(id -u)
                    # - PGID=$(id -g)
                },
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
) -> Generator[Output[List[Dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )
