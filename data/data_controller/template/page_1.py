head = r""" 
        <title>Satz</title>
        <script>
            let json_anmerkungen_1 = [];
            let json_szenario_1 = [];
            let json_absicht_1 = [];
            
            let json_satze = [];

            function load_satz_1() {
                window.pywebview.api.show_satz().then(results => {
                    const satz_list = document.getElementById('satz_list');
                    satz_list.innerHTML = '';
                    results = JSON.parse(results);
                    json_satze = results;

                    const satz_table = document.createElement('table');
                    satz_table.style.border = "1px solid black";
                    satz_table.style.borderCollapse = "collapse";
                    satz_table.style.width = "100%";

                    const headerRow = document.createElement('tr');
                    const headers = ['Satz ID', 'Wort', 'Anmerkung', 'Szenario', 'Absicht', 'Delete'];
                    headers.forEach(headerText => {
                        const th = document.createElement('th');
                        th.textContent = headerText;
                        th.style.border = "1px solid black";
                        th.style.padding = "8px";
                        th.style.textAlign = "left";
                        headerRow.appendChild(th);
                    });
                    satz_table.appendChild(headerRow);

                    let color_array = [
                        '#D58C8C',
                        '#A8D8B9',
                        '#A3C1E0'
                    ];

                    let current_index_cell_color = 0;
                    let current_id = 0;
                    let satz_count = 0;

                    results.forEach(result => {
                        const row = document.createElement('tr');

                        if(result.satz_id !== current_id){
                            satz_count++;
                            current_index_cell_color++;
                            if(current_index_cell_color === color_array.length){
                                current_index_cell_color = 0;
                            }
                        }

                        current_id = result.satz_id;

                        const satzIdCell = document.createElement('td');
                        satzIdCell.textContent = result.satz_id;
                        satzIdCell.style.border = "1px solid black";
                        satzIdCell.style.padding = "8px";
                        row.appendChild(satzIdCell);

                        const wortCell = document.createElement('td');
                        wortCell.onclick = () => popup_wort_update_1(result.satz_id, result.wort_id, result.wort, result.anmerkung_id);
                        wortCell.style.cursor = 'pointer';
                        wortCell.style.backgroundColor = color_array[current_index_cell_color];
                        wortCell.textContent = result.wort;
                        wortCell.style.border = "1px solid black";
                        wortCell.style.padding = "8px";
                        row.appendChild(wortCell);

                        const anmerkungCell = document.createElement('td');
                        anmerkungCell.onclick = () => popup_wort_update_1(result.satz_id, result.wort_id, result.wort, result.anmerkung_id);
                        anmerkungCell.style.cursor = 'pointer';
                        anmerkungCell.textContent = result.anmerkung || '';
                        anmerkungCell.style.border = "1px solid black";
                        anmerkungCell.style.padding = "8px";
                        row.appendChild(anmerkungCell);

                        const szenarioCell = document.createElement('td');
                        szenarioCell.textContent = result.szenario;
                        szenarioCell.style.cursor = 'pointer';
                        szenarioCell.onclick = () => update_satz_1(result.satz_id, result.szenario_id, result.absicht_id);
                        szenarioCell.style.border = "1px solid black";
                        szenarioCell.style.padding = "8px";
                        row.appendChild(szenarioCell);

                        const absichtCell = document.createElement('td');
                        absichtCell.textContent = result.absicht;
                        absichtCell.style.cursor = 'pointer';
                        absichtCell.onclick = () => update_satz_1(result.satz_id, result.szenario_id, result.absicht_id);
                        absichtCell.style.border = "1px solid black";
                        absichtCell.style.padding = "8px";
                        row.appendChild(absichtCell);

                        const deleteCell = document.createElement('td');
                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.onclick = () => delete_satz_1(result.satz_id);
                        delete_btn.style.color = "white";
                        delete_btn.style.backgroundColor = "red";
                        delete_btn.style.border = "1px solid black";
                        delete_btn.style.padding = "8px";
                        delete_btn.style.cursor = "pointer";
                        deleteCell.appendChild(delete_btn);
                        row.appendChild(deleteCell);

                        satz_table.appendChild(row);
                    });

                    satz_list.appendChild(satz_table);

                    const total_satz = document.getElementById('total_satz');
                    total_satz.textContent = satz_count;
                });
            }

            function load_anmerkung_1() {
                window.pywebview.api.show_anmerkung().then(results => {
                    json_anmerkungen_1 = JSON.parse(results);
                });
            }

            function option_absicht_1(container){
                json_absicht_1.forEach(json_absicht => {
                    const optionElement = document.createElement("option");
                    optionElement.value = json_absicht.absicht_id;
                    optionElement.textContent = json_absicht.absicht;
                    container.appendChild(optionElement);
                });
            }

            function option_szenario_1(container){
                json_szenario_1.forEach(json_szenario => {
                    const optionElement = document.createElement("option");
                    optionElement.value = json_szenario.szenario_id;
                    optionElement.textContent = json_szenario.szenario;
                    container.appendChild(optionElement);
                });
            }

            function load_absicht_1() {
                window.pywebview.api.show_absicht().then(results => {
                    const absicht_select = document.getElementById("absicht_select");
                    absicht_select.innerHTML = '';
                    json_absicht_1 = JSON.parse(results);
                    option_absicht_1(absicht_select);
                });
            }

            function load_szenario_1() {
                window.pywebview.api.show_szenario().then(results => {
                    const szenario_select = document.getElementById("szenario_select");
                    szenario_select.innerHTML = '';
                    json_szenario_1 = JSON.parse(results);
                    option_szenario_1(szenario_select);
                });
            }

            let array_woerter_value_1 = [];

            function text_to_woerter_1() {
                array_woerter_value_1 = [];
                const woerter_array_editor = document.getElementById("woerter_array_editor");
                woerter_array_editor.innerHTML = '';
                const form_satz = document.getElementById("form_satz");
                const satz_text = form_satz.elements["satz_text"].value.trim().replace(/\s+/g, ' ');

                if (satz_text.length > 0) {
                    const woerter_array = satz_text.split(" ");
                    woerter_array.forEach(wort => {
                        const wortObject = {
                            wort: wort,
                            anmerkung_id: json_anmerkungen_1[0].anmerkung_id
                        };

                        array_woerter_value_1.push(wortObject);

                        const div = document.createElement('div');
                        div.style.display = "flex";

                        const wort_name = document.createElement('span');
                        wort_name.style.minWidth = "7%";
                        wort_name.style.fontWeight = 'bold';
                        wort_name.textContent = wort;



                        const selectElement = document.createElement("select");

                        selectElement.style.padding = "5px";
                        selectElement.style.marginLeft = "10px";

                        json_anmerkungen_1.forEach(json_anmerkung => {
                            const optionElement = document.createElement("option");
                            optionElement.value = json_anmerkung.anmerkung_id;
                            optionElement.textContent = json_anmerkung.anmerkung;
                            selectElement.appendChild(optionElement);
                        });

                        selectElement.onchange = () => {
                            const selectedAnmerkungId = selectElement.value;
                            wortObject.anmerkung_id = selectedAnmerkungId;
                        };

                        div.appendChild(wort_name);
                        div.appendChild(selectElement);

                        woerter_array_editor.appendChild(div);
                    });
                }
            }

            function upload_satz_1() {
                if (array_woerter_value_1.length > 0) {
                    const absicht_select = document.getElementById("absicht_select").value;
                    const szenario_select = document.getElementById("szenario_select").value;

                    const json_object = {
                        "absicht_id_value": absicht_select,
                        "szenario_id_value": szenario_select,
                        "satz_value": array_woerter_value_1
                    };

                    information_bar(JSON.stringify(json_object));

                    window.pywebview.api.add_satz(json_object).then(response => {
                        load_satz_1();
                        const form_satz = document.getElementById("form_satz");
                        form_satz.elements["satz_text"].value = "";
                        text_to_woerter_1();
                    });
                } else {
                    information_bar("es muss etwas ausgefüllt werden");
                }
            }

            function delete_satz_1(satz_id) {
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + satz_id);
                if (confirmDelete) {
                    window.pywebview.api.delete_satz(satz_id).then(response => {
                        load_satz_1();
                        information_bar(response);
                    });
                }
            }

            function get_satz_in_array(id) {
                let satz_result = [];
                json_satze.forEach(wort_json => {
                    if (wort_json.satz_id === id) {
                        satz_result.push(wort_json.wort);
                    }
                });
                return satz_result.join(" ");
            }

            function update_satz_1(satz_id, szenario_id, absicht_id) {
                const popup_container = document.getElementById('popup_container');
                const overlay_container = document.getElementById('overlay_container');
                popup_container.style.display = 'block';
                overlay_container.style.display = 'block';

                const popup_inhalt_container = document.getElementById('popup_inhalt_container');
                popup_inhalt_container.innerHTML = '';

                const satz_result = get_satz_in_array(satz_id);

                const satz_info_container = document.createElement("div");
                const id_satz = document.createElement("p");
                const text_satz = document.createElement("p");

                id_satz.style.fontWeight = 'bold';
                text_satz.style.fontWeight = 'bold';

                id_satz.textContent = "ID: " + satz_id;
                text_satz.textContent = get_satz_in_array(satz_id);

                satz_info_container.appendChild(id_satz);
                satz_info_container.appendChild(text_satz);

                const szenario_container = document.createElement("div");
                szenario_container.style.display = "flex";

                const label_szenario = document.createElement("span");
                label_szenario.style.fontWeight = 'bold';
                label_szenario.style.width = "30%";
                label_szenario.textContent = "Szenario";

                const select_szenario = document.createElement("select");
                select_szenario.style.padding = "3px";
                option_szenario_1(select_szenario);

                szenario_container.appendChild(label_szenario);
                szenario_container.appendChild(select_szenario);

                const absicht_container = document.createElement("div");
                absicht_container.style.display = "flex";

                const label_absicht = document.createElement("span");
                label_absicht.style.fontWeight = 'bold';
                label_absicht.style.width = "30%";
                label_absicht.textContent = "Absicht";

                const select_absicht = document.createElement("select");
                select_absicht.style.padding = "3px";
                option_absicht_1(select_absicht);

                absicht_container.appendChild(label_absicht);
                absicht_container.appendChild(select_absicht);

                select_szenario.value = szenario_id;
                
                select_absicht.value = absicht_id;

                const update_sz_ab_btn = document.createElement("button");
                update_sz_ab_btn.textContent = "Update";

                update_sz_ab_btn.style.padding = '10px 20px';
                update_sz_ab_btn.style.backgroundColor = 'green';
                update_sz_ab_btn.style.color = 'white';
                update_sz_ab_btn.style.border = 'none';
                update_sz_ab_btn.style.borderRadius = '5px';
                update_sz_ab_btn.style.cursor = 'pointer';
                update_sz_ab_btn.style.marginTop = '10px';

                update_sz_ab_btn.onclick = ()=> {
                    const confirmUpdate = confirm("Möchten Sie diesen Eintrag wirklich ändern? ID: " + satz_id + "\nSatz: " + satz_result);
                    if (confirmUpdate) {
                        window.pywebview.api.update_satz_sz_ab(satz_id, select_szenario.value, select_absicht.value).then(response => {
                            load_satz_1();
                            information_bar(response);
                            popup_schliessen();
                        });
                    }
                }

                popup_inhalt_container.appendChild(satz_info_container);
                popup_inhalt_container.appendChild(szenario_container);
                popup_inhalt_container.appendChild(absicht_container);
                popup_inhalt_container.appendChild(update_sz_ab_btn);
            }

            function start_init_1() {
                load_anmerkung_1();
                load_absicht_1();
                load_szenario_1();
                load_satz_1();
            }

            window.onload = function () {
                setTimeout(start_init_1, 100);
            };

            function popup_wort_update_1(satz_id, wort_id, wort, anmerkung_id) {
                const popup_container = document.getElementById('popup_container');
                const overlay_container = document.getElementById('overlay_container');
                popup_container.style.display = 'block';
                overlay_container.style.display = 'block';

                const popup_inhalt_container = document.getElementById('popup_inhalt_container');
                popup_inhalt_container.innerHTML = '';

                const wort_info = document.createElement("div");

                const id_satz = document.createElement("p");
                const text_satz = document.createElement("p");

                id_satz.style.fontWeight = 'bold';
                text_satz.style.fontWeight = 'bold';

                id_satz.textContent = "ID: " + satz_id;
                text_satz.textContent = get_satz_in_array(satz_id);

                wort_info.appendChild(id_satz);
                wort_info.appendChild(text_satz);

                const inputElement = document.createElement("input");
                inputElement.placeholder = "Wort";
                inputElement.value = wort;

                inputElement.style.padding = "5px";
                inputElement.style.width = "100%";
                inputElement.style.marginBottom = "5px";

                const selectElement = document.createElement("select");

                selectElement.style.padding = "5px";
                selectElement.style.width = "100%";
                selectElement.style.marginBottom = "5px";

                json_anmerkungen_1.forEach(json_anmerkung => {
                    const optionElement = document.createElement("option");
                    optionElement.value = json_anmerkung.anmerkung_id;
                    optionElement.textContent = json_anmerkung.anmerkung;
                    selectElement.appendChild(optionElement);
                });

                selectElement.value = anmerkung_id;

                const update_anmerkung_btn = document.createElement("button");
                update_anmerkung_btn.textContent = "Update";

                update_anmerkung_btn.style.padding = '10px 20px';
                update_anmerkung_btn.style.backgroundColor = 'green';
                update_anmerkung_btn.style.color = 'white';
                update_anmerkung_btn.style.border = 'none';
                update_anmerkung_btn.style.borderRadius = '5px';
                update_anmerkung_btn.style.cursor = 'pointer';
                update_anmerkung_btn.style.marginTop = '10px';

                update_anmerkung_btn.onclick = ()=> {
                    const confirmUpdate = confirm("Möchten Sie diesen Eintrag wirklich ändern?");
                    if (confirmUpdate) {
                        window.pywebview.api.update_wort(wort_id, selectElement.value, inputElement.value.trim().replace(/\s+/g, ' ')).then(response => {
                            load_satz_1();
                            information_bar(response);
                            popup_schliessen();
                        });
                    }
                }

                popup_inhalt_container.appendChild(wort_info);
                popup_inhalt_container.appendChild(inputElement);
                popup_inhalt_container.appendChild(selectElement);
                popup_inhalt_container.appendChild(update_anmerkung_btn);
            }
        </script>
    """

body = r"""
            <div style="max-width:800px; margin-left:auto; margin-right:auto; padding: 5px;">
                <h1>Datenkontrolle</h1>

                <div style="display: flex; margin-bottom: 10px; justify-content: space-between;">
                    <button onclick="start_init_1()" style="padding: 10px 15px; border: 1px solid black; cursor: pointer;">Seite neu starten</button>
                    <button onclick="goToPage(2)" style="padding: 10px 15px; cursor: pointer;">Seite 2</button>
                </div>

                <div>
                    <form id="form_satz" onsubmit="event.preventDefault(); text_to_woerter_1();" style="margin-bottom: 20px;">
                        <input type="text" name="satz_text" placeholder="Satz" required style="padding: 10px; width: calc(100% - 20px); border: 1px solid #ccc; border-radius: 4px;">
                        <button type="submit" style="width: 100%; padding: 10px 15px; cursor: pointer; margin-top: 10px;">Split</button>
                    </form>

                    <div id="woerter_array_editor" style="margin-bottom: 20px; padding: 10px;"></div>

                    <div style="margin-bottom: 20px; display: flex; gap: 10px">
                        <h3 style="width:15%">Absicht</h3>
                        <select id="absicht_select" style="padding: 10px; width: 100%; margin-bottom: 10px;"></select>
                    </div>
                    <div style="margin-bottom: 20px; display: flex; gap: 10px">
                        <h3 style="width:15%">Szenario</h3>
                        <select id="szenario_select" style="padding: 10px; width: 100%; margin-bottom: 10px;"></select>
                    </div>

                    <button id="submit_satz" onclick="upload_satz_1()" style="width: 100%; padding: 10px 15px; cursor: pointer;">Upload</button>
                </div>
            </div>
            
            <div style="margin-top:10px; margin-left: 5px;"><b>Total:</b> <span id="total_satz">0</span></div>

            <div id="satz_list" style="margin: 0; padding: 2px 5px 10px 5px; overflow:visible"></div>
        """