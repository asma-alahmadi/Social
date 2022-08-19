document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.post__like').forEach(btn =>{
        btn.onclick = function(){
            post_id = btn.dataset.postid
            console.log(post_id)
            count = document.querySelector(`#like${post_id}`)
            let tag = document.querySelector(`.tag-${post_id}`)
            fetch('/like', {
                method: 'PUT',
                body: JSON.stringify({post_id})
            }).then(response => response.json())
            .then(result =>{
                if (result.error){
                    console.log(`Error like post: ${result.error}`)
                } else if(result.is_liked == true){
                    console.log(result.message)
                    console.log(result.likes_num)
                    console.log(`is_liked = ${result.is_liked}`)
                    tag.innerHTML =`<i class="fa-solid fa-heart post__like--red"></i>`
                } else if (result.is_liked == false){
                    tag.innerHTML = `<i class="fa-solid fa-heart post__like--white"></i>`
                    console.log(result.likes_num)
                    console.log(`is_liked = ${result.is_liked}`)
                }
                count.innerHTML = `<span>  ${result.likes_num}   Likes</span>`;
            }).catch (error => console.log(error))
            //localStorage.clear()
            return false;
        }
    })
})


