from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.filebrowser.assets
import OpenStudioLandscapes.filebrowser.constants

assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.filebrowser.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.filebrowser.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
