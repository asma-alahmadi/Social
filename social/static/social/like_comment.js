document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.comment__like').forEach(btn =>{ 
        btn.onclick = function(){
            comment_id = btn.dataset.comment_id
            console.log(comment_id) 
            count = document.querySelector(`#like${comment_id}`)
            let tag = document.querySelector(`.tag-${comment_id}`)
            fetch('/like_comment',{
                method: 'PUT',
                body: JSON.stringify({comment_id})
            }).then(response => response.json())
            .then(result =>{
                if(result.error){
                    console.log(`Error like comment: ${result.error}`)
                }else if(result.is_liked == true){
                    console.log(result.message)
                    console.log(result.likes_num)
                    console.log(`is_liked = ${result.is_liked}`)
                    tag.innerHTML =`<i class="fa-solid fa-heart post__like--red"></i>`
                    //localStorage.clear()
                    
                } else if(result.is_liked == false){
                    tag.innerHTML =`<i class="fa-solid fa-heart post__like--white"></i>`
                    console.log(result.likes_num)
                    console.log(`is_liked = ${result.is_liked}`)
                    //localStorage.clear()
                }
                count.innerHTML = `<span>  ${result.likes_num} Likes</span>`;
                //localStorage.clear()
                window.location.reload();
            }).catch(error => console.log(error))
            
            return false;
        }
    })
})

