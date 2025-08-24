import { useEffect, useState } from "react";
import { getAll, register } from "./services/user.service";
import type { UserProps } from "./types";

export default function App() {
  const [users, setUsers] = useState<UserProps[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    try {
      await register(name, email);
      setName("");
      setEmail("");
      const updatedUsers = await getAll();
      if ("error" in updatedUsers) {
        alert(updatedUsers.error);
      } else {
        setUsers(updatedUsers);
      }
    } catch (err) {
      console.error("Erro ao registrar usuário:", err);
      alert("Erro ao registrar usuário");
    }
  }

  useEffect(() => {
    getAll().then((data) => {
      if (!("error" in data)) {
        setUsers(data);
      }
    });
  }, []);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', margin: 20 }}>
      <h2>Cadastro de Usuários</h2>

      <div>
        <h3>Registrar Usuário</h3>
        <form onSubmit={handleRegister} style={{ marginBottom: 20 }}>
          <input
            type="text"
            placeholder="Nome"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{
              margin: 5,
              padding: 6,
              fontSize: 14
            }}
          />
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{
              margin: 5,
              padding: 6,
              fontSize: 14
            }}
          />
          <button
            type="submit"
            style={{
              padding: '6px 20px',
              fontSize: 14,
              cursor: 'pointer'
            }}
          >
            Registrar
          </button>
        </form>
      </div>

      <hr />

      <div>
        <h3>Usuários Cadastrados</h3>

        <ul style={{ listStyleType: 'none' }}>
          {users.map((user, index) => (
            <li key={index} style={{ margin: '5px 0' }}>
              {user.name} ({user.email})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}


