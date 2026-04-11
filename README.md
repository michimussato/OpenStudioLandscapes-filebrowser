[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-filebrowser](#feature-openstudiolandscapes-filebrowser)
   1. [Brief](#brief)
   2. [Clone](#clone)
      1. [Clone and Install](#clone-and-install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
   4. [Local Development](#local-development)
2. [External Resources](#external-resources)
   1. [Official Documentation](#official-documentation)
   2. [Known Issues](#known-issues)
      1. [Error: open /database/filebrowser.db: permission denied](#error-open-databasefilebrowserdb-permission-denied)
3. [Community](#community)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-filebrowser

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Clone

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-filebrowser.git
deactivate
# Check the resulting console output for installation instructions
```

### Clone and Install

```shell
# cd OpenStudioLandscapes
source .venv/bin/activate
openstudiolandscapes clone-feature --repo=https://github.com/michimussato/OpenStudioLandscapes-filebrowser.git \
    && pip install --editable ./.features/OpenStudioLandscapes-filebrowser
deactivate
```

For more info on `pip` see [VCS Support of `pip`](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Configure

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

> [!TIP]
> 
> To specify a config store location different from
> the default location, check out the OpenStudioLandscapes 
> [CLI Section](https://github.com/michimussato/OpenStudioLandscapes#cli)
> to find out how to do that.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

The following settings are available in `OpenStudioLandscapes-filebrowser` and are based on [`OpenStudioLandscapes-filebrowser/tree/main/OpenStudioLandscapes/filebrowser/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-filebrowser/tree/main/OpenStudioLandscapes/filebrowser/config/models.py).

### Default Configuration

<details open>
<summary><code>config.yml</code></summary>


```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==================
# local_bind_volumes
# ------------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         False
#     Description:
#         Here you can define Feature specific, arbitrary, absolute bind volume mappings.
#     Default value:
#         PydanticUndefined
# Description:
#     Here you can define Feature specific, arbitrary, absolute bind volume mappings.
# Required:
#     False
# Examples:
#     None


# ===========================
# local_environment_variables
# ---------------------------
#
# Type: typing.Dict[str, str]
# Base Class Info:
#     Required:
#         False
#     Description:
#         Here you can define Feature specific, arbitrary environment variables.
#     Default value:
#         PydanticUndefined
# Description:
#     Here you can define Feature specific, arbitrary environment variables.
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Group name. This will represent the group node name. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
group_name: OpenStudioLandscapes_filebrowser


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Asset key prefixes. This will be reflected in the nesting (directory structure) of the Asset. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
key_prefixes:
- OpenStudioLandscapes_filebrowser


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     Whether the Feature is enabled or not.
# Required:
#     False
# Examples:
#     None


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-filebrowser


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# ==========================
# filebrowser_port_container
# --------------------------
#
# Type: <class 'int'>
# Description:
#     The filebrowser container port.
# Required:
#     False
# Examples:
#     None
filebrowser_port_container: 80


# =====================
# filebrowser_port_host
# ---------------------
#
# Type: <class 'int'>
# Description:
#     The Kitsu host port.
# Required:
#     False
# Examples:
#     None
filebrowser_port_host: 8080


# ========================
# filebrowser_docker_image
# ------------------------
#
# Type: <class 'str'>
# Description:
#     None
# Required:
#     False
# Examples:
#     None
filebrowser_docker_image: docker.io/filebrowser/filebrowser


# =================================
# filebrowser_shared_dir_permission
# ---------------------------------
#
# Type: <enum 'FilebrowerRootPermission'>
# Description:
#     The filebrowser root permission.
# Required:
#     False
# Examples:
#     ['rw', 'ro']
filebrowser_shared_dir_permission: rw


# ===========================
# filebrowser_shared_dir_host
# ---------------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Set the shared directory on the host. If you want this to be an absolute path on the system outside of the Landscape, say `/root/data`, make sure `shared` is a symbolic link pointing to `/root/data`.
# Required:
#     False
# Examples:
#     None
filebrowser_shared_dir_host: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/shared'


# ================================
# filebrowser_shared_dir_container
# --------------------------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Set the shared directory on the container. The default is `/shared`.
# Required:
#     False
# Examples:
#     None
filebrowser_shared_dir_container: /shared


# ================
# filebrowser_json
# ----------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     Where on the host to store the configuration file.
# Required:
#     False
# Examples:
#     None
filebrowser_json: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/configs/filebrowser.json'


# ==================
# filebrowser_noauth
# ------------------
#
# Type: <class 'bool'>
# Description:
#     Disable authentication for filebrowser.
# Required:
#     False
# Examples:
#     None
filebrowser_noauth: true
```

</details>


## Local Development

```shell
cd ./.features/OpenStudioLandscapes-filebrowser
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools setuptools_scm wheel
pip install --editable .[dev]
dagster dev --workspace workspace.yaml
```

***

# External Resources

[![Logo filebrowser ](https://raw.githubusercontent.com/filebrowser/filebrowser/master/branding/banner.png)](https://filebrowser.org/index.html)

filebrowser is - as the name suggests - a web based file browser.

## Official Documentation

- [Website](https://filebrowser.org/)
- [Docs](https://filebrowser.org/installation.html)
- [GitHub](https://github.com/filebrowser/filebrowser)

## Known Issues

### Error: open /database/filebrowser.db: permission denied

```generic
filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 Using config file: /config/settings.json    
filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 WARNING: filebrowser.db can't be found. Initialing in /database/
filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 Using database: /database/filebrowser.db
filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | Error: open /database/filebrowser.db: permission denied
filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend exited with code 1 (restarting)        
```

This error is usually caused if the database file does not exist when using bind mounts. Make sure the file exists (empty).

References:

- [Deploying Filebrowser](https://docs.techdox.nz/filebrowser/#deploying-filebrowser)

***

# Community

| Feature                                   | GitHub                                                                                                                                                 | Discord                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| OpenStudioLandscapes                      | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                           | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)              |
| OpenStudioLandscapes-Ayon                 | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                 | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)                 |
| OpenStudioLandscapes-Dagster              | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                           | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)              |
| OpenStudioLandscapes-Deadline-10-2        | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)               | [# openstudiolandscapes-deadline-10-2](https://discord.gg/p2UjxHk4Y3)        |
| OpenStudioLandscapes-Deadline-10-2-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker) | [# openstudiolandscapes-deadline-10-2-worker](https://discord.gg/ttkbfkzUmf) |
| OpenStudioLandscapes-Flamenco             | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)                         | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)             |
| OpenStudioLandscapes-Flamenco-Worker      | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker)           | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p)      |
| OpenStudioLandscapes-Grafana              | [https://github.com/michimussato/OpenStudioLandscapes-Grafana](https://github.com/michimussato/OpenStudioLandscapes-Grafana)                           | [# openstudiolandscapes-grafana](https://discord.gg/gEDQ8vJWDb)              |
| OpenStudioLandscapes-Kitsu                | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                               | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)                |
| OpenStudioLandscapes-LikeC4               | [https://github.com/michimussato/OpenStudioLandscapes-LikeC4](https://github.com/michimussato/OpenStudioLandscapes-LikeC4)                             | [# openstudiolandscapes-likec4](https://discord.gg/qAYYsKYF6V)               |
| OpenStudioLandscapes-OpenCue              | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue](https://github.com/michimussato/OpenStudioLandscapes-OpenCue)                           | [# openstudiolandscapes-opencue](https://discord.gg/3DdCZKkVyZ)              |
| OpenStudioLandscapes-OpenCue-Worker       | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker](https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker)             | [# openstudiolandscapes-opencue-worker](https://discord.gg/n9fxxhHa3V)       |
| OpenStudioLandscapes-RustDeskServer       | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)             | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)       |
| OpenStudioLandscapes-Syncthing            | [https://github.com/michimussato/OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                       | [# openstudiolandscapes-syncthing](https://discord.gg/upb9MCqb3X)            |
| OpenStudioLandscapes-Template             | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)                         | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)             |
| OpenStudioLandscapes-VERT                 | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                                 | [# openstudiolandscapes-vert](https://discord.gg/EPrX5fzBCf)                 |
| OpenStudioLandscapes-filebrowser          | [https://github.com/michimussato/OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                   | [# openstudiolandscapes-filebrowser](https://discord.gg/stzNsZBmwk)          |
| OpenStudioLandscapes-n8n                  | [https://github.com/michimussato/OpenStudioLandscapes-n8n](https://github.com/michimussato/OpenStudioLandscapes-n8n)                                   | [# openstudiolandscapes-n8n](https://discord.gg/yFYrG999wE)                  |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

Last changed: **2026-04-11 01:53:06 UTC**