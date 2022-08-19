document.addEventListener('DOMContentLoaded', function(){  
    document.querySelectorAll('.comment__edit').forEach(btn =>{ 
        btn.onclick = function(){ 
                co_id = btn.dataset.commentid
                console.log(co_id)
                let comment = document.querySelector(`#comment_${co_id}`)
                console.log(comment.innerHTML)
                comment.innerHTML = `
                <form id="edit__comment" class="add_comment__form" style="width: auto; margin-left:0;">
                    <textarea id="edit_comment-content" class="add_comment__textarea" cols="10" rows="5" maxlength="300" required> ${comment.innerHTML.trim()} </textarea>
                    <input class="add_comment__submit" type="submit" value="Save" />
                </form>
             `
             btn.disabled = true;
                console.log(document.querySelector('#edit__comment'))
                document.querySelector('#edit__comment').onsubmit = function(e){
                    e.preventDefault() 
                    const comment_content = document.querySelector('#edit_comment-content').value.trim()
                    const comment__id = btn.dataset.commentid

                    fetch('/edit_comment',{
                        method: 'PUT',
                        body: JSON.stringify({comment_content, comment__id})
                    }).then(response => response.json())
                    .then(result =>{
                        if (result.error){
                            console.log(`Error editing comment: ${result.error}`)
                        } else{
                            console.log(result.message)
                            comment.innerHTML = comment_content
                        }
                    }).catch(error =>{
                        console.log(error)
                    })
                    btn.disabled = false;
                    return false;
                }
        }
    })
})