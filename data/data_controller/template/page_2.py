head = r"""
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
                } else {
                    information_bar("es muss etwas ausgefüllt werden");
                }
            }

            function load_anmerkung_2() {
                window.pywebview.api.show_anmerkung().then(results => {
                    const anmerkung_list = document.getElementById('anmerkung_list');
                    anmerkung_list.innerHTML = '';
                    results = JSON.parse(results);

                    results.forEach(result => {
                        const div = document.createElement('div');
                        div.style.padding = '5px';
                        div.style.border = '1px solid black';
                        div.style.display = 'flex';
                        div.style.flexDirection = 'column';

                        const p = document.createElement('p');
                        p.style.fontWeight = 'bold';
                        p.textContent = result.anmerkung_id + ". " + result.anmerkung;

                        const update_btn = document.createElement('button');
                        update_btn.textContent = "Update";
                        update_btn.style.width = '50%';
                        update_btn.style.backgroundColor = "green";
                        update_btn.style.color = "white";
                        update_btn.style.padding = "5px";
                        update_btn.style.cursor = "pointer";
                        update_btn.onclick = () => popup_update_2("anmerkung", result.anmerkung_id, result.anmerkung);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.style.width = '50%';
                        delete_btn.style.backgroundColor = "red";
                        delete_btn.style.padding = "5px";
                        delete_btn.style.cursor = "pointer";
                        delete_btn.onclick = () => delete_anmerkung_2(result.anmerkung_id);

                        div.appendChild(update_btn);
                        div.appendChild(delete_btn);

                        div.appendChild(p);
                        const div_btn = document.createElement('div');
                        div_btn.style.display = 'flex';
                        div_btn.appendChild(update_btn);
                        div_btn.appendChild(delete_btn);
                        div.appendChild(div_btn);
                        anmerkung_list.appendChild(div);
                    });
                });
            }

            function load_absicht_2() {
                window.pywebview.api.show_absicht().then(results => {
                    const absicht_list = document.getElementById('absicht_list');
                    absicht_list.innerHTML = '';
                    results = JSON.parse(results);

                    results.forEach(result => {
                        const div = document.createElement('div');
                        div.style.padding = '5px';
                        div.style.border = '1px solid black';
                        div.style.display = 'flex';
                        div.style.flexDirection = 'column';

                        const p = document.createElement('p');
                        p.style.fontWeight = 'bold';
                        p.textContent = result.absicht_id + ". " + result.absicht;

                        const update_btn = document.createElement('button');
                        update_btn.textContent = "Update";
                        update_btn.style.width = '50%';
                        update_btn.style.backgroundColor = "green";
                        update_btn.style.color = "white";
                        update_btn.style.padding = "5px";
                        update_btn.style.cursor = "pointer";
                        update_btn.onclick = () => popup_update_2("absicht", result.absicht_id, result.absicht);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.style.width = '50%';
                        delete_btn.style.backgroundColor = "red";
                        delete_btn.style.padding = "5px";
                        delete_btn.style.cursor = "pointer";
                        delete_btn.onclick = () => delete_absicht_2(result.absicht_id);

                        div.appendChild(p);
                        const div_btn = document.createElement('div');
                        div_btn.style.display = 'flex';
                        div_btn.appendChild(update_btn);
                        div_btn.appendChild(delete_btn);
                        div.appendChild(div_btn);
                        absicht_list.appendChild(div);
                    });
                });
            }

            function load_szenario_2() {
                window.pywebview.api.show_szenario().then(results => {
                    const szenario_list = document.getElementById('szenario_list');
                    szenario_list.innerHTML = '';
                    results = JSON.parse(results);

                    results.forEach(result => {
                        const div = document.createElement('div');
                        div.style.padding = '5px';
                        div.style.border = '1px solid black';
                        div.style.display = 'flex';
                        div.style.flexDirection = 'column';

                        const p = document.createElement('p');
                        p.style.fontWeight = 'bold';
                        p.textContent = result.szenario_id + ". " + result.szenario;

                        const update_btn = document.createElement('button');
                        update_btn.textContent = "Update";
                        update_btn.style.width = '50%';
                        update_btn.style.backgroundColor = "green";
                        update_btn.style.color = "white";
                        update_btn.style.padding = "5px";
                        update_btn.style.cursor = "pointer";
                        update_btn.onclick = () => popup_update_2("szenario", result.szenario_id, result.szenario);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.style.width = '50%';
                        delete_btn.style.backgroundColor = "red";
                        delete_btn.style.padding = "5px";
                        delete_btn.style.cursor = "pointer";
                        delete_btn.onclick = () => delete_szenario_2(result.szenario_id);
 
                        div.appendChild(p);
                        const div_btn = document.createElement('div');
                        div_btn.style.display = 'flex';
                        div_btn.appendChild(update_btn);
                        div_btn.appendChild(delete_btn);
                        div.appendChild(div_btn);
                        szenario_list.appendChild(div);
                    });
                });
            }

            function start_init_2() {
                load_absicht_2();
                load_szenario_2();
                load_anmerkung_2();
            }

            function delete_anmerkung_2(anmerkung_id) {
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + anmerkung_id);
                if (confirmDelete) {
                    window.pywebview.api.delete_anmerkung(anmerkung_id).then(response => {
                        load_anmerkung_2();
                        information_bar(response);
                    });
                }
            }

            function delete_szenario_2(szenario_id) {
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + szenario_id);
                if (confirmDelete) {
                    window.pywebview.api.delete_szenario(szenario_id).then(response => {
                        load_szenario_2();
                        information_bar(response);
                    });
                }
            }

            function delete_absicht_2(absicht_id) {
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + absicht_id);
                if (confirmDelete) {
                    window.pywebview.api.delete_absicht(absicht_id).then(response => {
                        load_absicht_2();
                        information_bar(response);
                    });
                }
            }

            function popup_update_2(typ, id, value) {
                const popup_container = document.getElementById('popup_container');
                const overlay_container = document.getElementById('overlay_container');
                popup_container.style.display = 'block';
                overlay_container.style.display = 'block';

                const popup_inhalt_container = document.getElementById('popup_inhalt_container');
                popup_inhalt_container.innerHTML = '';

                const inputElement = document.createElement("input");
                inputElement.placeholder = "Input";
                inputElement.value = value;

                inputElement.style.padding = "5px";
                inputElement.style.width = "100%";
                inputElement.style.marginBottom = "5px";

                const update_ab_sz_an_btn = document.createElement("button");
                update_ab_sz_an_btn.textContent = "Update";

                update_ab_sz_an_btn.style.padding = '10px 20px';
                update_ab_sz_an_btn.style.backgroundColor = 'green';
                update_ab_sz_an_btn.style.color = 'white';
                update_ab_sz_an_btn.style.border = 'none';
                update_ab_sz_an_btn.style.borderRadius = '5px';
                update_ab_sz_an_btn.style.cursor = 'pointer';
                update_ab_sz_an_btn.style.marginTop = '10px';

                update_ab_sz_an_btn.onclick = ()=> {
                    const confirmUpdate = confirm("Möchten Sie diesen Eintrag wirklich ändern?");
                    if (confirmUpdate) {
                        const update_value = inputElement.value.trim().replace(/\s+/g, ' ');
                        if (typ === "absicht") {
                            window.pywebview.api.update_absicht(update_value, id).then(response => {
                                load_absicht_2();
                                information_bar(response);
                            });
                        } else if(typ === "szenario") {
                            window.pywebview.api.update_szenario(update_value, id).then(response => {
                                load_szenario_2();
                                information_bar(response);
                            });
                        } else if(typ === "anmerkung") {
                            window.pywebview.api.update_anmerkung(update_value, id).then(response => {
                                load_anmerkung_2();
                                information_bar(response);
                            });
                        }
                        popup_schliessen();
                    }
                }

                popup_inhalt_container.appendChild(inputElement);
                popup_inhalt_container.appendChild(update_ab_sz_an_btn);
            }

            window.onload = function() {
                setTimeout(start_init_2, 100);
            };
        </script>
    """

body = r"""
        <div style="max-width:800px; margin-left:auto; margin-right:auto; padding: 5px;">
            <h1 style="text-align: center;">Absicht & Szenario & Anmerkung</h1>
            <form id="form_absicht_szenario" onsubmit="event.preventDefault(); input_absicht_szenario_2();" style="margin-bottom: 20px; width:500px; margin-left:auto; margin-right:auto; display:flex; flex-direction:column; justify-content:center">

                <div style="margin: 10px 0;">
                    <input type="radio" name="absicht_szenario_anmerkung_radio" value="absicht" checked>
                    <label for="absicht">Absicht</label>

                    <input type="radio" name="absicht_szenario_anmerkung_radio" value="szenario">
                    <label for="szenario">Szenario</label>

                    <input type="radio" name="absicht_szenario_anmerkung_radio" value="anmerkung">
                    <label for="anmerkung">Anmerkung</label>
                </div>

                <input type="text" name="absicht_szenario_anmerkung_text" placeholder="Absicht / Szenario / Anmerkung" required style="padding: 10px;"/>

                <button type="submit" style="padding: 5px 10px; width: 100%;">Add</button>
            </form>

            <button onclick="goToPage(1)" style="padding: 10px 20px; margin-bottom: 20px;">Zurück</button>
        </div>
        
        <div style="display: flex; gap: 5px; justify-content: center;">
            <div>
                <h2>Absicht</h2>
                <div id="absicht_list"></div>
            </div>
            <div>
                <h2>Szenario</h2>
                <div id="szenario_list"></div>
            </div>
            <div>
                <h2>Anmerkung</h2>
                <div id="anmerkung_list"></div>
            </div>
        </div>
    """