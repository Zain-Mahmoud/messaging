document.addEventListener('DOMContentLoaded', ()=>{
    if (window.localStorage.getItem('state')){
        if (window.localStorage.getItem('state') === 'home'){
            document.querySelector('#convo').style.display = 'none';
            document.querySelector('#currentchats').style.display = 'block';

        } else {
            loadChats(window.localStorage.getItem('state'), window.localStorage.getItem('user'));
        }
    } else {
        document.querySelector('#convo').style.display = 'none';
        window.localStorage.setItem('state', 'home')

    }
    document.querySelector('#viewchatbutton').addEventListener('click', () => {
        document.querySelector('#currentchats').style.display = 'block';
        document.querySelector('#convo').style.display = 'none';
        window.localStorage.setItem('state', 'home')

    })


    document.querySelectorAll('.chat').forEach(chat => {
        chat.addEventListener('click', () => {
            const chatid = chat.dataset.chatid;
            const user = chat.dataset.user;

            loadChats(chatid, user)
            window.localStorage.setItem('state', `${chatid}`)
            window.localStorage.setItem('user', `${user}`)
        })
    })

    document.querySelector('#logout').addEventListener('click', () => {
        window.localStorage.setItem('state', 'home')
    })
})


function loadChats(chatid, user){
    fetch(`/getchats/${chatid}`)
    .then(response => response.json())
    .then(result => {
        const messages = result['messages'];
        
        messages.forEach(message => {
            const text = message[0];
            const author_username = message[1];
            const messagediv = document.createElement('div');
            messagediv.className = 'chatmessage';
            messagediv.innerHTML = `<h5 class="message">${text}</h5>`;
            if (author_username === user) {
                messagediv.style.left = `${window.innerWidth - 100}px`;
            }
            document.querySelector('#chatview').appendChild(messagediv);
        })
    })
    document.querySelector('#textbox').querySelector('form').action = `/send/${chatid}`;
    document.querySelector('#textbox').querySelector('input').style.width = `${window.innerWidth}px`;
    document.querySelector('#convo').style.display = 'block';
    document.querySelector('#chatview').style.display = 'flex';
    document.querySelector('#chatview').style.flexDirection = 'column';
    document.querySelector('#currentchats').style.display = 'none';
}