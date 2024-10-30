FINAL PROJECT: NETWORK

1. Disclaimer:
        This project is built upon Project4 Network. I added a few new features to the project and reconcile the new design with the old.

2. Content:
        The main content of this project consists in Python, JavaScript and Django HTML(with Bootstrap 5).

        1. Register, login and logout. All three functions are already provided in Project4. A few modifications in style are applied to the original form.



        2. Edit Profile. The user, after registration, will be redirected to a page to edit their profile. The user is asked to give an alias, their date of birth, and their self-introduction.
            The alias has to be unique. The user will be warned if they breach this requirement, and the process will fail.
            In a similar way, date of birth has to follow the format [yyyy-mm-dd].
            All text fields have word limit.
            The user can leave the page without editing. In such cases, the user's username will be used to represent them, instead of alias.



        3. Index. On the index page, any user (authenticated or not) can view all posts.
            For an unauthenticated user, the post presents three parts:
                First, the latest content of the post to which this post is a reply to, provided this post is a reply. This part shows the (edited or unedited) content of the original post, its poster, and a hyperlink.
                The user will be redirected to the poster's profile by clicking the poster's alias (or username).
                The user will be redirected to a detailed view of the original post by clicking the hyperlink [see original post].

                Second, the post itself is presented in its content, its poster, its time, its number of comments, and its number of likes.
                The user will be redirected to the poster's profile by clicking the poster's alias (or username).

                Third, the user can click [View] button and be directed to a detailed view of the post.

            For an authenticated user, aside from these features, a post can be liked, unliked, replied to, and archived. They can also add post.
                When the user likes the post, the like count will increase by 1, and the button will change from [Like] to [Unlike], and vice versa.
                This feature above is asynchronous.

                The user can also write a reply to the post. When user clicks on [Reply] button, one will see the original content of the post preceded by [Re:].
                Below the original content, a textarea is used to input the reply. The textarea detects change and gives warning when conditions are not met.
                After change occurs in the textarea and conditions are met, a [Save] button appears and can upload the user's reply to the post to the database.
                The new post will be presented on top of the page as a reply to the original post.
                This process can always be cancelled by hitting the [Cancel] button which replaces the [Reply] button.

                The user can also archive the post. When they click on the [Archive] button, all their archives are presented as a list of checkboxes.
                After [Save] button is clicked, the post will be archived to all the archives selected.
                The list of archives is collapsable.
                The post can always be rearchived or dearchived via the same process.

                The user can add post by clicking the [Add Post] button from the navbar. The form is collapsable. This button is only available in the index page.

            If a user is at the same time the poster of the post, two more additional features are available.
                First, this user can always edit the content of their post. After [Edit] button is clicked, a textarea prefilled with the original content of the post appears.
                Similar to [Reply], this textarea listens for change and the meeting of conditions.
                The process can be cancelled by hitting the [Cancel] button that takes the place of the [Edit] button.
                After a change is made and conditions are met, the user can save the edit. The post will now present this edited content.

                Finally, this user can delete their post. Before a deletion is confirmed, the user can always rescind this action.
                After the post is deleted, any reply to this post, instead of showing the original post, will show ["The post replied to is deletd."].
        
            The user can leave the index page by using the navbar or accessing other hyperlinks. They can always come back to the index page through the [All Posts] button or the [Network] icon from the navbar.



        4. Detailed View. A detailed view of the post has all of the functionalities above available. There are three more additional features.
            First, for all users, authenticated or unauthenticated, comments under the post can be viewed. Each comment is numbered in descending order.
            The content of the comment, the commenter and a link to their profile, and the number of likes are parts of the presentation of each comment.
            Comments are accessed through clicking [View Comments] button, and they come as paginated.
            For authenticated users, aside from the above, comments can, similar to posts, be liked, unliked, and replied to.
            If the user is at the same time the commenter of a comment, the user can also edit or delete that comment.
            The authenticated user can always add comments by clicking [Add Comment] button and save the form.

            Second, users can see who liked the post by clicking the [View Likers] button.
            The user will see themselves appear if they first open the view of likers and then like the post.

            Third, users can see all replies to this post. Each reply can be accessed by clicking the [View] button.

        

        5. The user can go to a profile anytime the user clicks on a user's alias or username. A profile consists of three parts.
            First, the profile information. The profile owner's alias or username is displayed on top of their self-introduction.
            The profile owner's self-introduction is truncated over a certan length, and can be viewed in its totality if clicked.
            A count of the profile's followers and who they follow are displayed below the self-introduction.
            A [Follow] button to click on to follow the profile owner. This button is not made available to the user themselves or an unauthenticated user.

            Second, the section for additional information.
            For unauthenticated users, only followers of this profile-owner and who they follow are viewable. They can be viewed by clicking on [Show followers] or [Show who the user follows].
            Each view is collapsable.
            For authenticated users, the profile owner's public archives are also viewable through the [Show archives] button.
            Each of the archives on the list can be accessed by clicking on its name, which is a hyperlink. The view is collapsable.
            After clicking the archive name, the user will be redirected to that archive, and both the name of the archive and all the posts archived in the archive will be visible.
            If the user owns the profile, they can also [Create Archive] and [Edit Profile].
            By clicking on the [Create Archive] button, a text input field is uncollapsed. One puts into it the name for the new archive, which name cannot be a repetition of that of the user's other archives.
            One can also select if the archive is supposed to be private or public. If private, then only the user themselves could see and access it, after the user saves the form.
            When clicking on the [Edit Profile] button, one is redirected to an edit page of three text input fields.
            One is expected to give their alias, date of birth and a self-introduction.
            If the user has not yet created a profile, the three fields will be left empty. Else, all three fields are pre-filled with the user's current profile information.
            One can either save the changes made or cancel the process by going back to the profile. Warning will be given if constraints are not satisfied.

            Finally, a view of all the posts posted by the profile owner.



        6. Following. One can always navigate to the [Following] from the navbar and view only the posts from those one follows.



        7. Closing Account. Finally, one can choose to delete the account by clicking on the [Close this account] button from the navbar.
            By doing so, the user's account will be deleted after confirmation is given by the user, and the user will be redirected to the index page.
            None of the posts, comments or likes are deleted if the user has not actively deleted them before closing the account. Only they will now be kept anonymous under the generic title ["the user who has left"].

        

        8. Error Handling. Errors, especially if the requested object does not exist, are supposed to be handled. But more new trials and further tests are certainly needed.

3. Files:
        The main files for this project consist in 3 .py files (views.py, urls.py, and models.py), 1 .js file (script.js), and all 10 .html files.
        More information is available through the comments in those files.

        -- .py files:
                    1. views.py:
                        This file defines 16 functions and 4 ModelForms.

                    2. urls.py:
                        This file defines 15 paths, the last 4 of which are APIs.

                    3. models.py:
                        This file defines 9 ModelObjects.

        -- .js file:
                    1. script.js:
                        This file is structured around click events on 5 different kinds of buttons and defines the logic for each of them:
                        -- archive buttons
                        -- reply buttons
                        -- delete buttons
                        -- like/unlike buttons
                        -- edit buttons

                    2. other scripts:
                        These are mainly helper functions in post.html and profile.html to keep the view uncollapsed when turning to a new page.
                        Other helper functions include: a helper to get the csrf token, a helper to test the user's text input and give warnings respectively, and a helper to redirect in profile_edit.html.

        -- .html files:
                    1. layout.html:
                        This is the layout for the page, and consists mainly of the navbar.

                    2. index.html:
                        This defines the index page.

                    3. postsview.html:
                        This defines how the posts are to be displayed.

                    4. post.html:
                        This defines the detailed view of a post.

                    5. profile.html:
                        This defines the profile page.

                    6. profile_edit.html:
                        This defines the profile edit page.

                    7. archive.html:
                        This defines the archive page.
                    
                    8. following.html:
                        This defines the following page.

                    9. register.html:
                        This defines the registration page.

                    10. login.html:
                        This defines the login page.

4. Style:
        This site is designed via Bootstrap 5. All CSS are inline coded, for my unfamiliarity with this tool.
        The main components used are:
            -- Grid layout
            -- Navbar
            -- Buttons
            -- Cards
            -- Pagination
            -- Alerts
            -- Collapsables

5. YouTube:
        https://youtu.be/vQ9a2rcqgAU



Ruiyan Gui
Aug.5.2024