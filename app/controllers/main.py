
import re
from flask import current_app, render_template, url_for

def main():
    uuid_regex = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"

    return render_template(
        "main.html",
        uuid_regex=uuid_regex,
        user_url_regex=re.escape(
            current_app.config["BASE_URL"] + url_for(endpoint="show_user", user_id="")
        ).replace("/", "\\/") + uuid_regex
    )
