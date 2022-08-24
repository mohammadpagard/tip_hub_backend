function like(slug, id) {
    var element = document.getElementById('like')
    var count = document.getElementById('count')
    $.get(`/video/like/${slug}/${id}`).then(response =>{
        if(response['response'] === 'liked') {
            element.className = 'fa fa-heart liked'
            count.innerText = Number(count.innerText) + 1
        } else {
            element.className = 'fa fa-heart view-like'
            count.innerText = Number(count.innerText) - 1
        }
    })
}

like()
