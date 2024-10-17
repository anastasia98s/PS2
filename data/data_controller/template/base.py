def call_base(head, body):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script>
                function goToPage(site) {{
                    window.pywebview.api.showPage(site).then(html => {{
                        document.open();
                        document.write(html);
                        document.close();
                    }});
                }}

                function information_bar(text){{
                    const information_container = document.getElementById("information_container");
                    information_container.textContent = text;
                }}
            </script>
            {head}
        </head>
        <body>
            <div id="information_container"></div>
            {body}
        </body>
        </html>
    """