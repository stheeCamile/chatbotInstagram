Bot de Resposta Automática para Comentários do Instagram
Este é um código em Python para um bot de resposta automática de comentários do Instagram. O bot utiliza a biblioteca Selenium para interagir com o navegador e o serviço de chat do OpenAI para gerar respostas com o auxílio do modelo de linguagem GPT.

Pré-requisitos
Python 3.7 ou superior
Bibliotecas Python:
pathlib
selenium
undetected_chromedriver
Certifique-se de ter instalado todas as bibliotecas necessárias antes de executar o código.

Como usar
Faça o login no Instagram: No trecho de código, defina o nome de usuário e a senha da sua conta do Instagram nas variáveis username e password, respectivamente.

Defina o link da postagem: No trecho de código, atribua o link da postagem na variável post_link.

Execute o código: Após configurar as informações, execute o código Python. O bot irá abrir uma janela do navegador automatizada, fazer login no Instagram e navegar até a postagem especificada.

Geração de respostas: O bot procurará os comentários na postagem que ainda não foram respondidos. Ele utilizará o serviço de chat do OpenAI para gerar uma resposta automática para cada comentário não respondido. As respostas serão enviadas como comentários no Instagram.

Encerrando o programa: Para encerrar o programa, digite "sair" quando solicitado.

Certifique-se de compreender as diretrizes e políticas do Instagram relacionadas a bots e automação antes de usar este código. O uso inadequado pode violar os termos de serviço do Instagram e resultar em restrições à sua conta.

Lembre-se de atualizar as bibliotecas e os drivers do navegador para suas versões mais recentes, caso ocorram problemas de compatibilidade.