document.addEventListener('DOMContentLoaded', () => {

    // Checker for toggle.
    let click_status = false;

    // Like button logic.
    document.addEventListener('click', function(e) {

        // Select button.
        let target = e.target.closest('.like-button');
        if (target) {

            // Initialize frontend counter equal to backend.
            const post_id = target.dataset.id;
            const likes = document.querySelector('#likes_' + post_id);
            let likes_count = likes.dataset.count;
            likes_count = Number(likes_count)

            // Select the dynamic likes-shower that updates the number of likes from frontend.
            const likes_display = document.querySelector('#click_likes_' + post_id);

            // Toggle the checker per click.
            click_status = !click_status;

            // Store Cookie.
            let csrftoken = getCookie('csrftoken');

            // If the post is initialized as not liked from backend:
            // the button shows "like".
            const status = target.innerHTML;
            if (status === "like") {

                // Change the post from unliked to liked from backend when button is clicked.
                fetch('/like', {
                    method: 'PUT',
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    body: JSON.stringify(
                        {
                            post_id: post_id
                        }
                    )
                })
                .then(() => {

                    // Reset the button to show "unlike".
                    target.innerHTML = 'unlike';

                    // Check: if one simply likes, counter++;
                    // if one first unlikes then likes, no change to the counter.
                    if (click_status) {
                        likes_count ++;
                    }

                    // Set the new count to the dynamic likes-shower.
                    string = likes_count.toString();
                    likes_display.innerHTML = 'liked by ' + string;

                    // Hide the static likes-shower.
                    likes.style.display = "none";

                    // Display the dynamic likes-shower.
                    likes_display.style.display = "block";
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
                            post_id: post_id
                        }
                    )
                })
                .then(() => {

                    // Reset the button to show "like".
                    target.innerHTML = 'like';

                    // Check: if one simply unlikes, counter--;
                    // if one first likes then unlikes, no change to the counter.
                    if (click_status) {
                        likes_count --;
                    }

                    // Set the new count to the dynamic likes-shower.
                    string = likes_count.toString();
                    likes_display.innerHTML = 'liked by ' + string;

                    // Hide the static likes-shower.
                    likes.style.display = "none";

                    // Display the dynamic likes-shower.
                    likes_display.style.display = "block";
                });
            };
        };
    });


    // Edit button logic.
    document.addEventListener('click', function(e) {

        // Select edit button.
        let target = e.target.closest('.edit-button');
        if (target) {

            // Get the information to send.
            const post_id = target.dataset.id;
            let csrftoken = getCookie('csrftoken');

            // Send request and get back the prefill content.
            fetch('/edit', {
                method: 'POST',
                headers: {
                    'X-CSRFTOKEN': csrftoken
                },
                body: JSON.stringify(
                    {
                        post_id: post_id
                    }
                )
            })
            .then(response => response.json())
            .then(data => {

                // Hide the content-shower.
                document.querySelector('#content_' + post_id).style.display="none";

                // Display the textarea with prefill content.
                const text_area = document.querySelector('#textarea_' + post_id)
                text_area.value = `${data}`;
                text_area.style.display = 'block'

                // Display the save button.
                const save_button = document.querySelector('#save_' + post_id);
                save_button.style.display = 'block';

                // Save button logic:
                // it is set to be able to fire only once everytime after edit button fires,
                // so its lifespan won't overstretch and be redundantly multiplied.
                save_button.addEventListener('click', (e) => {
                    e.preventDefault()

                    // Get the user input in the textarea.
                    let new_content = document.querySelector('#textarea_' + post_id).value;

                    // Upload the edited content to backend.
                    fetch('/edit', {
                        method: 'PUT',
                        headers: {
                            'X-CSRFTOKEN': csrftoken
                        },
                        body: JSON.stringify(
                            {
                                post_id: post_id,
                                new_content: new_content
                            }
                        )
                    })
                    .then(() => {

                        // Display the content-shower with new content.
                        document.querySelector('#content_' + post_id).innerHTML = `
                            ${new_content}
                        `
                        document.querySelector('#content_' + post_id).style.display='block';
                    })
                    .then(() => {

                        // Hide textarea and save button.
                        save_button.style.display = 'none';
                        text_area.style.display = 'none';
                    })
                }, { once: true })
            });
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
