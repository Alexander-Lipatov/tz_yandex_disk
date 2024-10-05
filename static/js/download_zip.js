

const btn = document.getElementById('checked_download') 

const checkboxAll = document.getElementById('checked-all')
const checkboxFiles = document.querySelectorAll('input.checked-file')

checkboxAll.addEventListener('change', function() {
    checkboxFiles.forEach(cb => cb.checked = checkboxAll.checked)
})

checkboxFiles.forEach(cb => cb.addEventListener('change', function() {
    const checkboxChecked = document.querySelectorAll('input.checked-file:checked')
    if (checkboxChecked.length > 0 ){
        console.log(checkboxChecked.length)

        btn.disabled = false
    }else{
        btn.disabled=true
    }

    
}))

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

btn.addEventListener('click', function() {
    let allCheckbox = document.querySelectorAll('input.checked-file:checked')
    const selectedValues = Array.from(allCheckbox).map(cb => cb.value);
    
    const data = {
        pk: allCheckbox[0].getAttribute('name'),
        files: selectedValues,
    }

    fetch('/download_zip/', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при обработке запроса');
        }
        return response.json(); // Получаем URL для скачивания архива
    })
    .then(downloadUrl => {
        
        window.location.href = downloadUrl.url; // Переход на URL для скачивания архива
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при скачивании файлов.');
    });
    
})