    function getAllSportperson(url) 
    {
        fetch(url, {
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        }
        })
        .then(response => response.json()) /*преобразование ответа в json*/
        .then(data => {
        const SportList = document.getElementById("sport-table");
            // Очистка таблицы перед добавлением новых данных
            while (SportList.rows.length > 1) {
                SportList.deleteRow(1);
            }
    
        (data.context).forEach(sportperson => {
            const sportHTMLElement = `
                <tr>
                    <td>${sportperson.name }</td>
                    <td>${ sportperson.surname }</td>
                    <td>${ sportperson.age }</td>
                    <td>${ sportperson.gender }</td>
                    <td>${ sportperson.spcat }</td>
                    <td>${sportperson.sptype }</td>
                    <td>${sportperson.id}</td>
                    <td> <button id="${sportperson.id}" class="button_edit" onclick="StartEdit(this)"> Редактировать </button></td>
                    <td> <input id="spcat-${sportperson.id}" type="text" placeholder="Введите новую категорию" class="input_scat">
                    <td> <button id="${sportperson.id}" class="button_delete" onclick="StartDelete(this)"> Удалить </button></td> 
                <tr>`
            SportList.innerHTML += sportHTMLElement;
        });
    });
    }

    // Функция поиска
    function searchSportspeople(url, query) 
    {
        fetch(url + "?q=" + encodeURIComponent(query), 
        {
            headers: 
            {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => response.json())
        .then(data => 
        {
            console.log("Данные с сервера:", data);
            const SportList = document.getElementById("sport-table");
            // Очистка таблицы перед добавлением новых данных
            while (SportList.rows.length > 1) 
            {
                SportList.deleteRow(1);
            }

            data.context.forEach(sportperson => 
            {
                const sportHTMLElement = `
                    <tr>
                        <td>${sportperson.name}</td>
                        <td>${sportperson.surname}</td>
                        <td>${sportperson.age}</td>
                        <td>${sportperson.gender}</td>
                        <td>${sportperson.spcat}</td>
                        <td>${sportperson.sptype}</td>
                        <td> <button id="${sportperson.id}" class="button_edit" onclick="StartEdit(this)"> Редактировать </button></td>
                        <td> <input id="spcat-${sportperson.id}" required type="text" placeholder="Введите новую категорию" class="input_scat">
                        <td> <button id="${sportperson.id}" class="button_delete" onclick="StartDelete(this)"> Удалить </button></td>
                    </tr>`;
                SportList.innerHTML += sportHTMLElement;
            });
        });
    }


//функция редактирования

function edit_sportperson(edit_url, id_button, input_spcat)
{
/*    const searchParams = new URLSearchParams({
        id: query, input: query1
    }).toString();*/
    fetch(edit_url + '?id=' + id_button + '&input=' + input_spcat, 
        {
        headers: 
            {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => response.json())
        .then(data =>
            {
                console.log("Данные с сервера", data);
                if (data.status === "Invalid request" || data.status === "Empty input") {
                    alert("Ошибка при обновлении данных: " + data.status);
                    return;
                }
                const SportList = document.getElementById("sport-table");
                // Очистка таблицы перед добавлением новых данных
                while (SportList.rows.length > 1) 
                {
                    SportList.deleteRow(1);
                }
                if (data.status === 'Success') 
                    {
                        const sportHTMLElement = `
                            <tr>
                                <td>${data.sportperson.name}</td>
                                <td>${data.sportperson.surname}</td>
                                <td>${data.sportperson.age}</td>
                                <td>${data.sportperson.gender}</td>
                                <td>${data.sportperson.spcat}</td>
                                <td>${data.sportperson.sptype}</td>
                                <td> <button id="${data.sportperson.id}" class="button_edit" onclick="StartEdit(this)"> Редактировать </button></td>
                                <td> <input id="spcat-${data.sportperson.id}" type="text" placeholder="Введите новую категорию" class="input_scat">
                                <td> <button id="${data.sportperson.id}" class="button_delete" onclick="StartDelete(this)"> Удалить </button></td> 
                            </tr>`;
                        SportList.innerHTML += sportHTMLElement;
                    }
                    else
                    {
                        alert("Ошибка при обновлении данных.");
                        if (data.status === 'Incorrect sport category') 
                        {
                            const errorMessage = data.message || "Введи без спецсимволов";
                            const errorContainer = document.getElementById('error-message');
                            errorContainer.style.display = 'block'; // Показываем блок с ошибкой
                            errorContainer.textContent = errorMessage;  // Выводим сообщение
                            return;
                        }
                    }
            });
        
            
}

//функция удаления
function delete_sportperson(delete_url, id_button)
{
/*    const searchParams = new URLSearchParams({
        id: query, input: query1
    }).toString();*/
    fetch(delete_url + '?id=' + id_button, 
        {
        headers: 
            {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => response.json())
        .then(data =>
            {
                console.log("Данные с сервера", data);
                if (data.status === "Invalid request" || data.status === "Empty input") {
                    alert("Ошибка при обновлении данных: " + data.status);
                    return;
                }
                const SportList = document.getElementById("sport-table");
                // Очистка таблицы перед добавлением новых данных
                while (SportList.rows.length > 1) 
                {
                    SportList.deleteRow(1);
                }
                data.context.forEach(sportperson => 
                {
                        const sportHTMLElement = `
                            <tr>
                                <td>${sportperson.name}</td>
                                <td>${sportperson.surname}</td>
                                <td>${sportperson.age}</td>
                                <td>${sportperson.gender}</td>
                                <td>${sportperson.spcat}</td>
                                <td>${sportperson.sptype}</td>
                                <td> <button id="${sportperson.id}" class="button_edit" onclick="StartEdit(this)"> Редактировать </button></td>
                                <td> <input id="spcat-${sportperson.id}" required type="text" placeholder="Введите новую категорию" class="input_scat">
                                <td> <button id="${sportperson.id}" class="button_delete" onclick="StartDelete(this)"> Удалить </button></td>
                            </tr>`;
                        SportList.innerHTML += sportHTMLElement;
                });

            })
        }
