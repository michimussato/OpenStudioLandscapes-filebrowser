from dagster import (
    Definitions,
    load_assets_from_modules,
    AssetSpec,
    AssetKey,
)

import OpenStudioLandscapes.filebrowser.assets

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.filebrowser.assets],
)


# AssetSpecs

GROUP_BASE = "OpenStudioLandscapes_Base"
KEY_BASE = [GROUP_BASE]

ASSET_HEADER_BASE = {
    "group_name": GROUP_BASE,
    "key_prefix": KEY_BASE,
}
group_out_base = AssetSpec(
    key=AssetKey(
        [
            *ASSET_HEADER_BASE["key_prefix"],
            "single_asset"
        ],
    ),
    group_name=ASSET_HEADER_BASE["group_name"],
    description="Entry point for `OpenStudioLandscapes.engine.group_out_base` asset.",
)
assets.append(group_out_base)


defs = Definitions(
    assets=[
        *assets,
    ],
)
