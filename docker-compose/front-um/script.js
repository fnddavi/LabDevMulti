// Função para registrar um usuário
document.getElementById('register-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;

  fetch('http://localhost:3001/api/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, email }),
  })
  .then(response => response.json())
  .then(data => {
    alert('Usuário registrado com sucesso!');
    listUsers(); // Atualiza a lista de usuários após o registro
    document.getElementById('register-form').reset(); // Limpa o formulário
  })
  .catch(error => {
    console.error('Erro ao registrar usuário:', error);
  });
});

// Função para listar todos os usuários
document.getElementById('list-users-btn').addEventListener('click', listUsers );

function listUsers() {
  fetch('http://localhost:3001/api/')
    .then(response => response.json())
    .then(users => {
      const usersList = document.getElementById('users-list');
      usersList.innerHTML = '';  // Limpa a lista antes de preencher

      users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `${user.name} - ${user.email}`;
        usersList.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Erro ao listar usuários:', error);
    });
}

// Chama a função para listar usuários quando a página é carregada
document.addEventListener('DOMContentLoaded', listUsers);