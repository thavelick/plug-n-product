from flask import request, session, render_template
from jinja2_fragments.flask import render_block


def oob_block_tag(template, block, tag_name, tag_id, **kwargs):
    content = render_block(template, block, **kwargs)
    return f'<{tag_name} id="{tag_id}" hx-swap-oob="true">{content}</{tag_name}>'


def render_htmx_template(template, block, **kwargs):
    if request.headers.get("HX-Request"):
        blocks = [
            render_block(template, block, **kwargs),
            oob_block_tag(
                template, block="title", tag_name="title", tag_id="title", **kwargs
            ),
            oob_block_tag(
                "base.html",
                block="flash_messages",
                tag_name="div",
                tag_id="flash_messages",
                **kwargs,
            ),
        ]
        if "top_nav" in session.get("oob_updates", []):
            blocks.append(
                oob_block_tag(
                    "base.html",
                    block="top_nav",
                    tag_name="nav",
                    tag_id="top_nav",
                    **kwargs,
                )
            )
        session.pop("oob_updates", None)
        return " ".join(blocks)

    return render_template(template, **kwargs)
