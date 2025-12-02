# 🏋️ Como contribuir no projeto Menjaro

Olá!! Esse arquivo tem como objetivo te orientar a como contribuir com o projeto com Pull Requests, toda feature ou correção é bem vinda!!

---

## 🚀 Como Você Pode Contribuir?

Você pode ajudar de diversas formas:

- Desenvolvendo novas funcionalidades
- Corrigindo erros e bugs detectados no sistema
- Sugerindo melhorias na interface (UI/UX)
- Melhorando a organização do backend
- Criando ou melhorando a documentação

> 💡 caso deseje relatar algum Bug, confira a aba [**Issues**](https://github.com/eduardohasantos/menjaro/issues/new) do repositório.

---

## ⚙️ Preparando Seu Ambiente

1. **Faça um fork do projeto**  
   Crie um fork do repositório [`eduardohasantos/menjaro`](https://github.com/eduardohasantos/menjaro) para a sua conta no GitHub.

2. **Clone o fork localmente**  
   ```bash
    git clone https://github.com/eduardohasantos/menjaro.git
   cd intellifit
   ```

3. **Crie uma nova branch para suas alterações**  
   ```bash
   git checkout -b nome-da-sua-nova-branch
   ```  
   Use nomes descritivos como `fix/bug-gerenciamento-treino` ou `feature/Receitas`.

---

## 🛠️ Configurando o Ambiente de Desenvolvimento

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Aplique as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

4. Execute o servidor local:

   ```bash
   python manage.py runserver
   ```

---

## ✅ Regras e Boas Práticas

- Mantenha o estilo visual consistente .
- Teste suas alterações antes de abrir um Pull Request.
- Utilize mensagens de commit claras e explicativas.

---


## 📄 Submetendo seu Pull Request

1. Commit suas alterações:

   ```bash
   git add .
   git commit -m "feat: adiciona funcionalidade X"
   ```

2. Envie sua branch para seu fork:

   ```bash
   git push origin nome-da-sua-branch-nova
   ```

3. Vá até o seu repositório no GitHub e clique em **"Compare & pull request"**.

4. Preencha o título e a descrição detalhando o que foi feito e por quê.

5. Aguarde a revisão e possíveis comentários da equipe.

## 📬 Contato

Dúvidas, sugestões ou problemas? Entre em contato com o time:

- [**Arthur Coelho**](https://github.com/ArthurMatias57) | [LinkedIn](https://www.linkedin.com/in/arthur-c-m-20079a335/) | E-mail:acmm@cesar.school
