head = r"""
        <title>Absicht & Szenario & Anmerkung</title>
        <script>
            function input_absicht_szenario_2() {
                const form_absicht_szenario = document.getElementById("form_absicht_szenario");
                const absicht_szenario_anmerkung_text = form_absicht_szenario.elements["absicht_szenario_anmerkung_text"].value;
                if (absicht_szenario_anmerkung_text) {
                    const absicht_szenario_anmerkung_radio = form_absicht_szenario.elements["absicht_szenario_anmerkung_radio"].value;
                    if (absicht_szenario_anmerkung_radio === "absicht") {
                        window.pywebview.api.add_absicht(absicht_szenario_anmerkung_text).then(response => {
                            form_absicht_szenario.elements["absicht_szenario_anmerkung_text"].value = '';
                            load_absicht_2();
                            information_bar(response);
                        });
                    } else if(absicht_szenario_anmerkung_radio === "szenario") {
                        window.pywebview.api.add_szenario(absicht_szenario_anmerkung_text).then(response => {
                            form_absicht_szenario.elements["absicht_szenario_anmerkung_text"].value = '';
                            load_szenario_2();
                            information_bar(response);
                        });
                    } else if(absicht_szenario_anmerkung_radio === "anmerkung") {
                        window.pywebview.api.add_anmerkung(absicht_szenario_anmerkung_text).then(response => {
                            form_absicht_szenario.elements["absicht_szenario_anmerkung_text"].value = '';
                            load_anmerkung_2();
                            information_bar(response);
                        });
                    }
                }else{
                    information_bar("es muss etwas ausgefüllt werden");
                }
            }

            function load_anmerkung_2() {
                window.pywebview.api.show_anmerkung().then(results => {
                    const anmerkung_list = document.getElementById('anmerkung_list');
                    anmerkung_list.innerHTML = '';
                    results = JSON.parse(results)
                    results.forEach(result => {
                        const li = document.createElement('li');
                        li.textContent = result.anmerkung;
                        anmerkung_list.appendChild(li);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.onclick = () => delete_anmerkung_2(result.anmerkung_id);
                        anmerkung_list.appendChild(delete_btn);
                    });
                });
            }

            function load_absicht_2() {
                window.pywebview.api.show_absicht().then(results => {
                    const absicht_list = document.getElementById('absicht_list');
                    absicht_list.innerHTML = '';
                    results = JSON.parse(results)
                    results.forEach(result => {
                        const li = document.createElement('li');
                        li.textContent = result.absicht;
                        absicht_list.appendChild(li);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.onclick = () => delete_absicht_2(result.absicht_id);
                        absicht_list.appendChild(delete_btn);
                    });
                });
            }

            function load_szenario_2() {
                window.pywebview.api.show_szenario().then(results => {
                    const szenario_list = document.getElementById('szenario_list');
                    szenario_list.innerHTML = '';
                    results = JSON.parse(results)
                    results.forEach(result => {
                        const li = document.createElement('li');
                        li.textContent = result.szenario;
                        szenario_list.appendChild(li);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.onclick = () => delete_szenario_2(result.szenario_id);
                        szenario_list.appendChild(delete_btn);
                    });
                });
            }

            function start_init_2(){
                //information_bar("response2");
                load_absicht_2();
                load_szenario_2();
                load_anmerkung_2();
            }

            function delete_anmerkung_2(anmerkung_id){
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + anmerkung_id);
                window.pywebview.api.delete_anmerkung(anmerkung_id).then(response => {
                    load_anmerkung_2();
                    information_bar(response);
                });
            }

            function delete_szenario_2(szenario_id){
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + szenario_id);
                window.pywebview.api.delete_szenario(szenario_id).then(response => {
                    load_szenario_2();
                    information_bar(response);
                });
            }

            function delete_absicht_2(absicht_id){
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + absicht_id);
                window.pywebview.api.delete_absicht(absicht_id).then(response => {
                    load_absicht_2();
                    information_bar(response);
                });
            }

            window.onload = function() {
                setTimeout(start_init_2, 100);
            };
        </script>
    """

body = r"""
        <h1>Absicht & Szenario & Anmerkung</h1>

        <form id="form_absicht_szenario" onsubmit="event.preventDefault(); input_absicht_szenario_2();">
            <input type="text" name="absicht_szenario_anmerkung_text" placeholder="Absicht / Szenario / Absicht" required>

            <div>
                <input type="radio" name="absicht_szenario_anmerkung_radio" value="absicht" checked>
                <label for="absicht">Absicht</label>

                <input type="radio" name="absicht_szenario_anmerkung_radio" value="szenario">
                <label for="szenario">Szenario</label>

                <input type="radio" name="absicht_szenario_anmerkung_radio" value="anmerkung">
                <label for="szenario">Anmerkung</label>
            </div>

            <button type="submit">Add</button>
        </form>

        <button onclick="goToPage(1)">züruck</button>

        <div style="display:flex; gap:50px">
            <div>
                <h2>Absicht List</h2>
                <ol id="absicht_list"></ol>
            </div>
            <div>
                <h2>Szenario List</h2>
                <ol id="szenario_list"></ol>
            </div>
            <div>
                <h2>Anmerkung List</h2>
                <ol id="anmerkung_list"></ol>
            </div>
        <div>
    """