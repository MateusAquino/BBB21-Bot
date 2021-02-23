# 🌱 BBB21 Bot
O **BBB21 Bot** faz parte de um estudo sobre segurança da informação, processamento de imagem e redes neurais.  
Desenvolvido para fins de estudo. Sem nenhuma intenção de prejudicar o programa, a emissora ou qualquer participante em específico.  

Até a edição anterior do Big Brother Brasil, o [sistema de captcha implementado](https://www.youtube.com/watch?v=ll8ewMMFsPg) era de simples imagens 1:4 (1/5, 20%) com hashcash pra evitar o não cumprimento do captcha pelas requisições HTTP, porém recentemente eles atualizaram para o hCaptcha (uma versão alternativa ao reCAPTCHA), que foi configurado para o usuário identificar apenas fotos de bicicletas e barcos.  

Dito isto, configurei uma base de **828 arquivos** classificados manualmente (poderiam ser mais, porém foi o suficiente para mim) para serem trabalhados no Tensorflow (Keras).  

O projeto foi desenvolvido e testado no Linux (Arch Linux x86_64).
## ⚠️ Aviso
O algoritmo faz o recorte manual utilizando posições que estão **hardcoded** de acordo com o meu monitor/setup.  
Por ser um estudo e não uma aplicação para uso geral, não pretendo automatizar esse processo, caso queira testar esse algoritmo você terá que alterar manualmente nas variáveis iniciais em `bbb.py` (procure no arquivo por `log pos. mouse` e `log cor pixel`).

## 🚀 Instalação
O Tensorflow **não** está disponível para versões recentes do Python, recomendo que instale a versão `3.8.6`.  
Clone o repositório e execute em seguida:

    pip install -r requirements.txt

## ✨ Executar
Primeiro altere a posição dos elementos nas variáveis em `bbb.py`, logo após instalar os pré-requisitos, abra a página de votação do Gshow, abra um terminal e execute:

    python bbb.py

E volte à tela de votação do Gshow.  
Para parar o programa, interrompa manualmente digitando `Ctrl+C`.

## 🧠 Treinar
Caso queira adicionar mais imagens à rede neural, é possível obter mais imagens definindo a variável `keepImages = True` em `bbb.py`.  
Assim que classificá-las manualmente (movendo de `./runtime/` para `./data/`), para 'compilar' o novo modelo simplesmente definina a variável `train = True`, e execute:

    python classify.py


## 📜 Licença

[MIT](./LICENSE) &copy; [Mateus Aquino](https://www.linkedin.com/in/mateusaquino/)
