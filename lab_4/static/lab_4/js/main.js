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
                    <td> <input id="${sportperson.id}" type="text" placeholder="Введите новую категорию" class="input_scat"> 
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
                        <td> <input id="${sportperson.id}" type="text" placeholder="Введите новую категорию" class="input_scat"> 
                    </tr>`;
                SportList.innerHTML += sportHTMLElement;
            });
        });
    }


//функция редактирования

function edit_sportperson(url, query, query1)
{
    const searchParams = new URLSearchParams({
        id: query, input: query1
    }).toString();
    fetch(url + '?$' + {searchParams}, 
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
                            </tr>`;
                        SportList.innerHTML += sportHTMLElement;
                    });
            });

}

//функция удаления


document.addEventListener("click", function(event) {
  if (event.target.classList.contains("delete-button")) {
      const id = event.target.dataset.id;
      fetch(`/delete_sportperson/${id}/`, {
          method: "DELETE",
          headers: {
              "X-Requested-With": "XMLHttpRequest",
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              location.reload(); // Перезагружаем страницу
          } else {
              alert("Ошибка при удалении");
          }
      });
  }
});