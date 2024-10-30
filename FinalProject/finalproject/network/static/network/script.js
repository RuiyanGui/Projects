document.addEventListener('DOMContentLoaded', () => {


    // Archive button logic.
    document.addEventListener('click', function(e) {

        let target = e.target.closest('.dynamic-archive-button');
        if (target) {
            
            // Get data.
            const id = target.dataset.id;
            const checkboxes = document.querySelectorAll('.checkbox_' + id + ':checked');

            // Save data.
            let archives = [];
            for (i = 0; i < checkboxes.length; i++) {
                archives.push(checkboxes[i].value)
            }

            let csrftoken = getCookie('csrftoken');

            // Upload to backend.
            fetch('/archive', {
                method: 'PUT',
                headers: {
                    'X-CSRFTOKEN': csrftoken
                },
                body: JSON.stringify(
                    {
                        id: id,
                        archives: archives
                    }
                )
            })
    }

    })


    // Reply button logic.
    document.addEventListener('click', function(e) {
        let target = e.target.closest('.reply-button');

        // Get data.
        const id = target.dataset.id;
        const module = target.dataset.module;
        const content = target.dataset.content;

        // Reply action.
        if (target.innerHTML === 'Reply') {

            target.innerHTML = 'Cancel';

            let csrftoken = getCookie('csrftoken');

            let save_button;
            let text_area;
            let post = '';

            // Change display of comment.
            if (module === 'comment') {

                post = target.dataset.post;

                text_area = document.querySelector('#textarea_comment_' + id);
                text_area.style.display = 'block';
                save_button = document.querySelector('#save_comment_' + id);

                document.querySelector('#content_comment_' + id).innerHTML = 'Re:' + content;
                if (document.querySelector('#edit_button_comment_' + id)) {
                    document.querySelector('#edit_button_comment_' + id).style.display = 'none'
                }

                // Warning.
                text_area.addEventListener('change', () => {
                    test_length(e, text_area, module, id, save_button)
            })
                text_area.addEventListener('keyup', () => {
                    test_length(e, text_area, module, id, save_button)
            })
                text_area.addEventListener('paste', () => {
                    test_length(e, text_area, module, id, save_button)
            })

            // Change display of post.
            } else {
                text_area = document.querySelector('#textarea_' + id);
                text_area.style.display = 'block';
                if (document.querySelector('#edit_button_' + id)) {
                    document.querySelector('#edit_button_' + id).style.display = 'none'
                }

                document.querySelector('#content_' + id).innerHTML = 'Re:' + content;

                save_button = document.querySelector('#save_' + id);

                // Warning.
                text_area.addEventListener('change', () => {
                    test_length(e, text_area, module, id, save_button)
            })
                text_area.addEventListener('keyup', () => {
                    test_length(e, text_area, module, id, save_button)
            })
                text_area.addEventListener('paste', () => {
                    test_length(e, text_area, module, id, save_button)
            })

            }

            // Upload data to backend.
            save_button.addEventListener('click', (e) => {

                let new_content = text_area.value

                e.preventDefault()
                fetch('/reply', {
                    method: 'POST',
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    body: JSON.stringify(
                        {
                            id: id,
                            module: module,
                            content: new_content,
                            post_id: post
                        }
                    )
                })
                .then(() => {
    
                    window.location.reload()
    
                })    

            }, { once : true })

            // Cancel reply action and restore the original look.
        } else {
            target.innerHTML = 'Reply';
            if (module === 'post') {
                document.querySelector('#content_' + id).innerHTML = content;
                document.querySelector('#content_' + id).style.display = 'block';
                if (document.querySelector('#edit_button_' + id)) {
                    document.querySelector('#edit_button_' + id).style.display = 'block';
                }
                document.querySelector('#save_' + id).style.display = 'none';
                document.querySelector('#textarea_' + id).style.display = 'none';
                document.querySelector('#warning_' + id).innerHTML = '';
            } else {
                document.querySelector('#content_comment_' + id).innerHTML = content;
                document.querySelector('#content_comment_' + id).style.display = 'block';
                if (document.querySelector('#edit_button_comment' + id)) {
                    document.querySelector('#edit_button_comment_' + id).style.display = 'block';
                }
                document.querySelector('#save_comment_' + id).style.display = 'none';
                document.querySelector('#textarea_comment_' + id).style.display = 'none';
                document.querySelector('#warning_comment_' + id).innerHTML = '';
            }
        }
    })

    // Delete button logic.
    document.addEventListener('click', function(e) {

        let target = e.target.closest('.delete-button');
        if (target) {

            // Get data.
            const id = target.dataset.id;
            const module = target.dataset.module;
            const status = target.dataset.status;
            let csrftoken = getCookie('csrftoken');

            // Delete confirmation.
            let result;
            if (module === 'user') {
                result = confirm('If you close the account, your posts, comments and likes will be kept under anonymous.')
            } else {
                result = confirm('You sure you want to delete?')
            }

            // Upload data.
            if (result) {
                fetch('/delete', {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    body: JSON.stringify(
                        {
                            id: id,
                            module: module
                        }
                    )
                })

                // Change look of the page.
                .then(() => {
                    if (module == 'post' && status == 'true') {
                        document.querySelector('#post_view_' + id).remove();
                    } else if (module == 'comment') {
                        document.querySelector('#comment_view_' + id ).remove();
                    } else if (module == 'post' && status == 'false') {
                        window.location.href = '/';
                    } else if (module == 'user') {
                        window.location.reload();
                    } else {
                        window.location.href = '/profile/' + status;
                    }
                })
            }
        }
    })


    // Like button logic.
    document.addEventListener('click', function(e) {

        // Select button.
        let target = e.target.closest('.like-button');
        if (target) {

            // Get data.
            const id = target.dataset.id;
            const module = target.dataset.module;

            let likes;
            if (module === 'post') {
                likes = document.querySelector('#likes_' + id);
            } else {
                likes = document.querySelector('#likes_comment_' + id);
            }

            let csrftoken = getCookie('csrftoken');

            // If the post is initialized as not liked from backend:
            // the button shows "like".
            const status = target.innerHTML;
            if (status === "Like") {

                // Change the post from unliked to liked from backend when button is clicked.
                fetch('/like', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    body: JSON.stringify(
                        {
                            id: id,
                            module: module
                        }
                    )
                })
                .then(response => response.json())
                .then(data => {

                    // Reset the button to show "unlike".
                    target.innerHTML = 'Unlike';

                    // Set the new count to the dynamic likes-shower.
                    likes.innerHTML = 'liked by ' + data;

                    // Show the new like on page.
                    if (!document.querySelector('#static-self-show')) {
                        document.querySelector('#dynamic-self-show').style.display = 'block';
                    } else {
                        document.querySelector('#static-self-show').style.display = 'block';
                    }
                })    
            } else {

                // Else, the button shows "unlike", and delete like from backend on click.
                fetch('/like', {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    body: JSON.stringify(
                        {
                            id: id,
                            module: module
                        }
                    )
                })
                .then(response => response.json())
                .then(data => {

                    // Reset the button to show "like".
                    target.innerHTML = 'Like';

                    // Reset the count.
                    likes.innerHTML = 'liked by ' + data;

                    // Hide the old like.
                    if (!document.querySelector('#static-self-show')) {
                        document.querySelector('#dynamic-self-show').style.display = 'none';
                    } else {
                        document.querySelector('#static-self-show').style.display = 'none';
                    }
                });
            };
        };
    });


    // Edit button logic.
    document.addEventListener('click', function(e) {

        // Select edit button.
        let target = e.target.closest('.edit-button');
        const id = target.dataset.id;
        const module = target.dataset.module;

        if (target.innerHTML === 'Edit') {

            target.innerHTML = 'Cancel';

            // Get the information to send.
            let csrftoken = getCookie('csrftoken');

            // Send request and get back the prefill content.
            fetch('/edit', {
                method: 'POST',
                headers: {
                    'X-CSRFTOKEN': csrftoken
                },
                body: JSON.stringify(
                    {
                        id: id,
                        module: module
                    }
                )
            })
            .then(response => response.json())
            .then(data => {

                let save_button;
                let text_area;

                // Edit comment.
                if (module === 'comment') {
                    document.querySelector('#content_comment_' + id).style.display = 'none';
                    document.querySelector('#reply_button_comment_' + id).style.display = 'none';

                    // Display the textarea with prefill content.
                    text_area = document.querySelector('#textarea_comment_' + id);
                    text_area.value = `${data}`;
                    text_area.style.display = 'block'

                    // Display the save button.
                    save_button = document.querySelector('#save_comment_' + id);

                    // Warning.
                    text_area.addEventListener('change', () => {
                        test_length(e, text_area, module, id, save_button)
                })
                    text_area.addEventListener('keyup', () => {
                        test_length(e, text_area, module, id, save_button)
                })
                    text_area.addEventListener('paste', () => {
                        test_length(e, text_area, module, id, save_button)
                })

                // Edit post.
                } else {
                    document.querySelector('#content_' + id).style.display='none';
                    document.querySelector('#reply_button_' + id).style.display = 'none';

                    // Display the textarea with prefill content.
                    text_area = document.querySelector('#textarea_' + id)
                    text_area.value = `${data}`;
                    text_area.style.display = 'block'
    
                    // Display the save button.
                    save_button = document.querySelector('#save_' + id);

                    // Warning.
                    text_area.addEventListener('change', () => {
                        test_length(e, text_area, module, id, save_button)
                })
                    text_area.addEventListener('keyup', () => {
                        test_length(e, text_area, module, id, save_button)
                })
                    text_area.addEventListener('paste', () => {
                        test_length(e, text_area, module, id, save_button)
                })
            }


                // Save button logic:
                // it is set to be able to fire only once everytime after edit button fires,
                // so its lifespan won't overstretch and be redundantly multiplied.
                save_button.addEventListener('click', (e) => {
                    e.preventDefault()

                    // Get the user input in the textarea. Might need to reselect.
                    let new_content = text_area.value;

                    // Upload the edited content to backend.
                    fetch('/edit', {
                        method: 'PUT',
                        headers: {
                            'X-CSRFTOKEN': csrftoken
                        },
                        body: JSON.stringify(
                            {
                                id: id,
                                module: module,
                                new_content: new_content
                            }
                        )
                    })
                    .then(() => {

                        // Display the content-shower with new content.
                        if (module === 'post') {
                            document.querySelector('#content_' + id).innerHTML = `
                            ${new_content}
                        `
                        document.querySelector('#content_' + id).style.display = 'block';
                        document.querySelector('#reply_button_' + id).style.display = 'block';
                        target.innerHTML = 'Edit';
                        } else {
                            document.querySelector('#content_comment_' + id).innerHTML = `
                            ${new_content}
                        `
                        document.querySelector('#content_comment_' + id).style.display='block';
                        document.querySelector('#reply_button_comment_' + id).style.display = 'block';
                        target.innerHTML = 'Edit';
                        }
                    })
                    .then(() => {

                        // Hide textarea and save button.
                        save_button.style.display = 'none';
                        text_area.style.display = 'none';
                    })
                }, { once: true })
            });

        // Cancel edit action.
        } else {
            target.innerHTML = 'Edit';
            if (module === 'post') {
                document.querySelector('#content_' + id).style.display = 'block';
                document.querySelector('#reply_button_' + id).style.display = 'block';
                document.querySelector('#save_' + id).style.display = 'none';
                document.querySelector('#textarea_' + id).style.display = 'none';
                document.querySelector('#warning_' + id).innerHTML = '';
            } else {
                document.querySelector('#content_comment_' + id).style.display = 'block';
                document.querySelector('#reply_button_comment_' + id).style.display = 'block';
                document.querySelector('#save_comment_' + id).style.display = 'none';
                document.querySelector('#textarea_comment_' + id).style.display = 'none';
                document.querySelector('#warning_comment_' + id).innerHTML = '';
            }
        };
    });
});


// Helper to get cookie.
// The following function is copied from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check the cookie string.
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Helper to check the length of input and give warning accordingly.
function test_length(e, text_area, module, id, save_button) {
    if (module === 'comment') {
        warning = document.querySelector('#warning_comment_' + id);
    } else {
        warning = document.querySelector('#warning_' + id);
    }
    warning.innerHTML = '';
    save_button.style.display = 'none';
    if (text_area.value.length < 1) {
        warning.innerHTML = 'Please fill in content.';
        return result = false;
    } else if (module === 'post' && text_area.value.length > 1000) {
        warning.innerHTML = 'You have exceeded maximum length. Only 1000 characters are allowed.';
    } else if (module === 'comment' && text_area.value.length > 400) {
        warning.innerHTML = 'You have exceeded maximum length. Only 400 characters are allowed';
    } else {
        save_button.style.display = 'block';
    }
}
