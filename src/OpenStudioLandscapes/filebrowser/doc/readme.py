import textwrap

import snakemd


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

    doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
