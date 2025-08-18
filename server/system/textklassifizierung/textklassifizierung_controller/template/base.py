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

                function scrollToTop() {{
                    window.scrollTo({{
                        top: 0,
                        behavior: 'smooth' // Smooth scrolling
                    }});
                }}

                function scrollToBottom() {{
                    window.scrollTo({{
                        top: document.body.scrollHeight,
                        behavior: 'smooth' // Smooth scrolling
                    }});
                }}

                function popup_schliessen() {{
                    const popup_container = document.getElementById('popup_container');
                    const overlay_container = document.getElementById('overlay_container');
                    popup_container.style.display = 'none';
                    overlay_container.style.display = 'none';
                }}
            </script>
            <style>
                body{{
                    font-family: Arial, Helvetica, sans-serif;
                    background-color: rgb(216, 209, 196)
                }}

                .scroll_btn_container {{
                    position: fixed;
                    right: 5px;
                    z-index: 1000;
                    bottom: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                }}
                .scroll_btn{{
                    background: #523750;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1.3rem;
                    padding: 5px 10px;
                    font-weight: 900;
                }}

                #popup_container {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 10px;
                    z-index: 1001;
                }}

                #overlay_container {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 1000;
                }}
            </style>
            {head}
        </head>
        <body>
            <div id="information_container"></div>
            {body}
            <div class="scroll_btn_container">
                <button class="scroll_btn" onclick="scrollToTop()">↑</button>
                <button class="scroll_btn" onclick="scrollToBottom()">↓</button>
            </div>

            <div id="overlay_container" style="
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1001;
            ">
                <div id="popup_container" style="
                    display: none;
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 80%;
                    max-width: 400px;
                    height: 60%;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    z-index: 1000;
                    overflow: hidden;
                ">
                    <button onclick="popup_schliessen()">Schließen</button>
                    <div id="popup_inhalt_container" style="display:flex; flex-direction: column; padding: 25px 50px;"></div>
                </div>
            </div>
        </body>
        </html>
    """