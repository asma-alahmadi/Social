document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.edit').forEach(btn =>{ 
        btn.onclick = function(){
            id = btn.dataset.postid
        let post = document.querySelector(`#content_${id}`)
        post.innerHTML = `
            <form id="edit_post" class="add_comment__form">
                <textarea id="edit_content" cols="30" rows="11" class="add_comment__textarea"  maxlength="500" required> ${post.innerHTML.trim()} </textarea>
                <input class="add_comment__submit" type="submit" value="Save" />
            </form>
        `
        btn.disabled = true;
        document.querySelector('#edit_post').onsubmit = function(e){
            e.preventDefault()
            const content = document.querySelector('#edit_content').value.trim()
            const post_id = btn.dataset.postid

            fetch('/edit',{
                method: 'PUT',
                body: JSON.stringify({content, post_id})
            }).then(response => response.json())
            .then(result =>{
                if (result.error){
                    console.log(`Error editing post: ${result.error}`)
                } else{
                    console.log(result.message)
                    post.innerHTML = content
                }
            }).catch(error => {
                console.log(error)
            })
            btn.disabled = false;
            
            return false;
        }
     }
        
 })
   
})