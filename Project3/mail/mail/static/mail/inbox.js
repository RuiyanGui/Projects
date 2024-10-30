document.addEventListener('DOMContentLoaded', () => {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

}


function send_email(e) {

  // Avoid default change of route
  e.preventDefault();
  
  // Get data
  const mail_recipient = document.querySelector('#compose-recipients').value;
  const mail_subject = document.querySelector('#compose-subject').value;
  const mail_body = document.querySelector('#compose-body').value;

  // Submit data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: mail_recipient,
        subject: mail_subject,
        body: mail_body
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox('sent')
  });
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get data from the given mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Display emails one by one
      emails.forEach(email => {

        const div = document.createElement('div');
        div.innerHTML = `
        <h5>Sender: ${email.sender}</h5>
        <h5>Subject: ${email.subject}</h5>
        <p>${email.timestamp}</p>
        `;

        // Check if email is read and change color
        if (email.read){
          div.className = 'read';
        } else {
          div.className = 'unread';
        }

        // Click to view the email
        div.addEventListener('click', () => {
          view_email(email.id)
        });
        document.querySelector('#emails-view').append(div);
      });
  });

}

function view_email(id) {

  // Get data of a particular email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // Display the particular email
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Display info of this email
    document.querySelector('#email-view').innerHTML = `
    <ul>
      <li>Sender: ${email.sender}</li>
      <li>Recipient: ${email.recipients}</li>
      <li>Subject: ${email.subject}</li>
      <li>Time: ${email.timestamp}</li>
      <li>Content: ${email.body}</li>
    </ul>
    `

    // Change to read
    if(!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    // Check if this email belongs to the Sent mailbox
    if (document.querySelector('#user').innerHTML !== email.sender) {
      const archive = document.createElement('button');

      // Archive or Unarchive
      if (email.archived) {
        archive.innerHTML = 'Unarchive';
      } else {
        archive.innerHTML = 'Archive';
      }
      archive.addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => {load_mailbox('inbox')})
      });
      document.querySelector('#email-view').append(archive);  
    }


    // Reply
    const reply = document.createElement('button');
    reply.innerHTML = "Reply"
    reply.addEventListener('click', () => {
      compose_email();

      // Check if reply is made to the user themselves
      if (document.querySelector('#user').innerHTML == email.sender) {
        document.querySelector('#compose-recipients').value = email.recipients;
      } else {
        document.querySelector('#compose-recipients').value = email.sender;
      }

      // Add 'Re:' to the subject
      let subject = email.subject;
      if(subject.split(' ', 1)[0] != "Re:") {
        subject = "Re: " + email.subject;
      }

      // Pre-fill the subject and the body
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n`;
    });
    document.querySelector('#email-view').append(reply);
    
  })
}
