import textwrap

import snakemd

from OpenStudioLandscapes.filebrowser.config.models import Config

def readme_feature(
    doc: snakemd.Document,
    main_header: str,
) -> snakemd.Document:

    # Some Specific information

    doc.add_heading(
        text=main_header,
        level=1,
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent("""\
                Logo filebrowser\
                """),
            image="https://raw.githubusercontent.com/filebrowser/filebrowser/master/branding/banner.png",
            link="https://filebrowser.org/index.html",
        ).__str__()
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            filebrowser is - as the name suggests - a web based file browser.\
            """))

    doc.add_heading(
        text="Official Documentation",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[Website](https://filebrowser.org/)",
            "[Docs](https://filebrowser.org/installation.html)",
            "[GitHub](https://github.com/filebrowser/filebrowser)",
        ]
    )

    doc.add_heading(
        text="Authentication",
        level=3,
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            The default OpenStudioLandscapes-filebrowser credentials
            are set to:\
            """))

    doc.add_unordered_list(
        [
            f"`username`: `{Config().default_username}`",
            f"`password`: `{Config().default_password}`",
        ]
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            To disable user based authentication entirely, set `filebrowser_noauth` in `config.yaml`
            to `true`.\
            """))

    doc.add_paragraph(text=textwrap.dedent("""\
            filebrowser offers several different authentication methods. 
            More information can be found [here](https://filebrowser.org/authentication.html#authentication).\
            """))

    doc.add_heading(
        text="Known Issues",
        level=2,
    )

    doc.add_heading(
        text="Error: open /database/filebrowser.db: permission denied",
        level=3,
    )

    doc.add_code(
        code=textwrap.dedent("""\
        filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 Using config file: /config/settings.json    
        filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 WARNING: filebrowser.db can't be found. Initialing in /database/
        filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | 2026/02/09 09:12:48 Using database: /database/filebrowser.db
        filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend  | Error: open /database/filebrowser.db: permission denied
        filebrowser.2026-02-09_09-42-23__highly-merciful-imaginary-legend exited with code 1 (restarting)\
        """),
        lang="generic",
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            This error is usually caused if the database file does not exist
            when using bind mounts. Make sure the file exists (empty).\
            """))

    doc.add_paragraph(text=textwrap.dedent("""\
            References:\
            """))

    doc.add_unordered_list(
        [
            "[Deploying Filebrowser](https://docs.techdox.nz/filebrowser/#deploying-filebrowser)",
        ]
    )

    doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
