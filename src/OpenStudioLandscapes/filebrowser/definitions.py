from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.filebrowser.assets

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.filebrowser.assets],
)


defs = Definitions(
    assets=[
        *assets,
    ],
)
