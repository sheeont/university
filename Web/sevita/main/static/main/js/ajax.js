// AJAX запрос для добавления в избраное
// Получаем значени csrf токена из cookie
function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i])

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

const csrftoken = getCookie('csrftoken')

// Устанавливаем безопасное AJAX соединени
function csrfSafeMethod(method) {
    // Эти HTTP методы не требуют csrf защиту
    return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$.ajaxSetup({
    beforeSend: (xhr, settings) => {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

const add_to_favorites_url = '/catalog/add/'
const remove_from_favorites_url = '/catalog/remove/'
const favorites_api_url = '/catalog/api/'
const added_to_favorites_class = 'added'

function add_to_favorites() {
    $('.add-to-favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const type = $(el).data('type')
            const id = $(el).data('id')

            if($(e.target).hasClass(added_to_favorites_class)) {
                $.ajax ({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(added_to_favorites_class)
                        console.log("Объект с id=" + id + " удалён из избранного.")
                    }
                })
            } else {
                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(added_to_favorites_class)
                        console.log("Объект с id=" + id + " добавлен в избранное.")
                    }
                })
            }
        })
    })
}

function get_session_favorites() {
    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {
                $('.add-to-favorites').each((index, el) => {
                    const type = $(el).data('type')
                    const id = $(el).data('id')

                    if (json[i].type == type && json[i].id == id) {
                        $(el).addClass(added_to_favorites_class)
                    }
                })
            }
        }
    })
}

$(document).ready(function() {
    add_to_favorites()
    get_session_favorites()
})

// Содержится ли элемент elem в массиве arr
function contains(arr, elem) {
   return arr.indexOf(elem) != -1;
}

// С интервалом в минуту обновляет данные об избранных товарах
setInterval(function () {
    $.ajax({
        url: "/get_db_changes/",
        type: 'GET',
        dataType: 'json',

        success: function (json) {
            if (json.result) {
                $('.add-to-favorites').each((index, el) => {
                    for (let i = 0; i < json.favorite_ids.length; i++) {
                        const id = $(el).data('id')

                        if (json.favorite_ids[i] == id) {
                            $(el).addClass(added_to_favorites_class)
                        }
                        else if (!contains(json.favorite_ids, $(el).data('id')) && $(el).hasClass(added_to_favorites_class)) {
                            $(el).removeClass(added_to_favorites_class)
                        }
                    }
                })
            }
        }
    });
}, 30000);
