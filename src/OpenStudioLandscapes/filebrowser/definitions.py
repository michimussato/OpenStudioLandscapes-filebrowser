from dagster import (
    Definitions,
    load_assets_from_modules,
)

from OpenStudioLandscapes.filebrowser import assets, assets_external

assets = load_assets_from_modules(
    modules=[
        assets,
    ],
)

assets_external = load_assets_from_modules(
    modules=[
        assets_external,
    ],
    include_specs=True,
)

defs = Definitions(
    assets=[
        *assets,
        *assets_external,
    ],
)
