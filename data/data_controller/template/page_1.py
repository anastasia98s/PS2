head = r""" 
        <script>
            let json_anmerkungen_1 = [];

            function load_satz_1() {
                window.pywebview.api.show_satz().then(results => {
                    const satz_list = document.getElementById('satz_list');
                    satz_list.innerHTML = '';
                    results = JSON.parse(results)
                    /*
                    results.forEach(result => {
                        const div = document.createElement('div');
                        div.style.display = "flex";
                        div.style.gap = "10px";

                        const span1 = document.createElement('span');
                        span1.textContent = result.satz_id;
                        div.appendChild(span1);

                        const span2 = document.createElement('span');
                        span2.textContent = result.wort;
                        div.appendChild(span2);

                        const span3 = document.createElement('span');
                        span3.textContent = result.anmerkung;
                        div.appendChild(span3);

                        const span4 = document.createElement('span');
                        span4.textContent = result.szenario;
                        div.appendChild(span4);

                        const span5 = document.createElement('span');
                        span5.textContent = result.absicht;
                        div.appendChild(span5);

                        satz_list.appendChild(div);
                    });
                    */

                    const satz_table = document.createElement('table');
                    satz_table.style.border = "1px solid black";

                    const headerRow = document.createElement('tr');
                    const headers = ['Satz ID', 'Wort', 'Anmerkung', 'Szenario', 'Absicht'];
                    headers.forEach(headerText => {
                        const th = document.createElement('th');
                        th.textContent = headerText;
                        th.style.border = "1px solid black";
                        headerRow.appendChild(th);
                    });
                    satz_table.appendChild(headerRow);

                    results.forEach(result => {
                        const row = document.createElement('tr');

                        const satzIdCell = document.createElement('td');
                        satzIdCell.textContent = result.satz_id;
                        satzIdCell.style.border = "1px solid black";
                        row.appendChild(satzIdCell);

                        const wortCell = document.createElement('td');
                        wortCell.textContent = result.wort;
                        wortCell.style.border = "1px solid black";
                        row.appendChild(wortCell);

                        const anmerkungCell = document.createElement('td');
                        anmerkungCell.textContent = result.anmerkung || '';
                        anmerkungCell.style.border = "1px solid black";
                        row.appendChild(anmerkungCell);

                        const szenarioCell = document.createElement('td');
                        szenarioCell.textContent = result.szenario;
                        szenarioCell.style.border = "1px solid black";
                        row.appendChild(szenarioCell);

                        const absichtCell = document.createElement('td');
                        absichtCell.textContent = result.absicht;
                        absichtCell.style.border = "1px solid black";
                        row.appendChild(absichtCell);

                        const delete_btn = document.createElement('button');
                        delete_btn.textContent = "Delete";
                        delete_btn.onclick = () => delete_satz_1(result.satz_id);
                        delete_btn.style.border = "1px solid black";
                        row.appendChild(delete_btn);

                        satz_table.appendChild(row);
                    });

                    satz_list.appendChild(satz_table);
                });
            }

            function load_anmerkung_1(){
                window.pywebview.api.show_anmerkung().then(results => {
                    json_anmerkungen_1 = JSON.parse(results)
                });
            }

            function load_absicht_1(){
                window.pywebview.api.show_absicht().then(results => {
                    const absicht_select = document.getElementById("absicht_select");
                    absicht_select.innerHTML = '';
                    json_absichten = JSON.parse(results)
                    
                    //const optionFirstElement = document.createElement("option");
                    //optionFirstElement.value = "";
                    //optionFirstElement.textContent = "0";
                    //absicht_select.appendChild(optionFirstElement);

                    json_absichten.forEach(json_absicht => {
                        const optionElement = document.createElement("option");
                        optionElement.value = json_absicht.absicht_id;
                        optionElement.textContent = json_absicht.absicht;
                        absicht_select.appendChild(optionElement);
                    });
                });
            }

            function load_szenario_1(){
                window.pywebview.api.show_szenario().then(results => {
                    const szenario_select = document.getElementById("szenario_select");
                    szenario_select.innerHTML = '';
                    json_szenarios = JSON.parse(results);

                    //const optionFirstElement = document.createElement("option");
                    //optionFirstElement.value = "";
                    //optionFirstElement.textContent = "0";
                    //szenario_select.appendChild(optionFirstElement);

                    json_szenarios.forEach(json_szenario => {
                        const optionElement = document.createElement("option");
                        optionElement.value = json_szenario.szenario_id;
                        optionElement.textContent = json_szenario.szenario;
                        szenario_select.appendChild(optionElement);
                    });
                });
            }

            let array_woerter_value_1 = []

            function text_to_woerter_1(){
                array_woerter_value_1 = []
                const woerter_array_editor = document.getElementById("woerter_array_editor");
                woerter_array_editor.innerHTML = '';
                const form_satz = document.getElementById("form_satz");
                const satz_text = form_satz.elements["satz_text"].value.trim().replace(/\s+/g, ' ');

                if(satz_text.length > 0){
                    const woerter_array = satz_text.split(" ");
                    woerter_array.forEach(wort => {
                        const wortObject = {
                            wort: wort,
                            anmerkung_id: json_anmerkungen_1[0].anmerkung_id
                        };

                        array_woerter_value_1.push(wortObject);

                        const div = document.createElement('div');
                        div.textContent = wort;

                        const selectElement = document.createElement("select");

                        json_anmerkungen_1.forEach(json_anmerkung => {
                            const optionElement = document.createElement("option");
                            optionElement.value = json_anmerkung.anmerkung_id;
                            optionElement.textContent = json_anmerkung.anmerkung;
                            selectElement.appendChild(optionElement);
                        });

                        selectElement.onchange = ()=>{
                            const selectedAnmerkungId = selectElement.value;
                            wortObject.anmerkung_id = selectedAnmerkungId;
                        }

                        div.appendChild(selectElement);

                        woerter_array_editor.appendChild(div);
                    });
                }
            }

            function upload_satz_1(){
                if(array_woerter_value_1.length > 0){
                    const absicht_select = document.getElementById("absicht_select").value;
                    const szenario_select = document.getElementById("szenario_select").value;

                    const json_object = {
                        "absicht_id_value": absicht_select,
                        "szenario_id_value": szenario_select,
                        "satz_value": array_woerter_value_1
                    };

                    information_bar(JSON.stringify(json_object));
                    
                    window.pywebview.api.add_satz(json_object).then(response => {
                        //information_bar(response);
                        load_satz_1();
                        const form_satz = document.getElementById("form_satz");
                        form_satz.elements["satz_text"].value = "";
                        text_to_woerter_1();
                    });
                }else{
                    information_bar("es muss etwas ausgefüllt werden");
                }
            }

            function delete_satz_1(satz_id){
                const confirmDelete = confirm("Möchten Sie diesen Eintrag wirklich löschen? ID: " + satz_id);
                window.pywebview.api.delete_satz(satz_id).then(response => {
                    load_satz_1();
                    information_bar(response);
                });
            }

            function start_init_1(){
                load_anmerkung_1();
                load_absicht_1();
                load_szenario_1();
                load_satz_1();
            }

            window.onload = function() {
                setTimeout(start_init_1, 100);
            };
        </script>
    """

body = r"""
            <h1>Satz</h1>
            <button onclick="start_init_1()">Seite neu starten</button>
            <form id="form_satz" onsubmit="event.preventDefault(); text_to_woerter_1();">
                <input type="text" name="satz_text" placeholder="Satz" required>
                <button type="submit">Split</button>
            </form>

            <div id="woerter_array_editor"></div>

            <h3>Absicht</h3>
            <select id="absicht_select"></select>
            <h3>Szenario</h3>
            <select id="szenario_select"></select>

            <button id="submit_satz" onclick="upload_satz_1()">Upload</button>

            <button onclick="goToPage(2)">Page 2</button>

            <div id="satz_list"></div>
        """