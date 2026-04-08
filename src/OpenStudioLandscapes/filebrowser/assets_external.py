from dagster import (
    AssetKey,
    AssetSpec,
)

from OpenStudioLandscapes.engine.constants import ASSET_HEADER_BASE


group_out_base = AssetSpec(
    key=AssetKey(
        [
            *ASSET_HEADER_BASE["key_prefix"],
            "group_out_base"
        ],
    ),
    group_name=ASSET_HEADER_BASE["group_name"],
    description="Entry point for the `OpenStudioLandscapes.engine.base.assets.group_out_base` asset.",
)
