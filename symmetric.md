# Guião de Laboratório: Cifras Simétricas em Python
**Instituto Superior Técnico, Universidade de Lisboa**  
**Fundamentos da Segurança**

## Introdução

Bem-vindos ao mundo da criptografia! Este laboratório vai ensinar-vos os conceitos fundamentais das **cifras simétricas** - um tipo de encriptação onde usamos a mesma chave para cifrar e decifrar informações.

### O que são Cifras Simétricas?
Imaginem que têm um cofre com uma chave. Para fechar o cofre (cifrar) e para o abrir (decifrar), usam exactamente a mesma chave. É assim que funcionam as cifras simétricas - uma só chave serve para tudo!

### Objectivos do Laboratório
- Compreender como funcionam as cifras simétricas
- Ver os perigos de reutilizar chaves (One-Time Pads)
- Experimentar diferentes modos de cifra (ECB, CBC, OFB)
- Trabalhar com imagens para "ver" os efeitos da criptografia

## Preparação do Ambiente (Windows)

### Passo 1: Instalar o Python
1. Vão ao site oficial do Python: https://www.python.org/downloads/
2. Descarreguem a versão mais recente do Python 3
3. Durante a instalação, **muito importante**: marquem a opção "Add Python to PATH"
4. Para verificar se foi bem instalado:
   - Abram a **Linha de Comandos** (Windows + R, escrevem `cmd` e premem Enter)
   - Escrevem: `python --version`
   - Deve aparecer algo como "Python 3.x.x"

### Passo 2: Descarregar os Ficheiros do Laboratório
1. Abram um browser e vão a: https://github.com/tecnico-sec/Python-Crypto
2. Cliquem no botão verde "Code" e depois "Download ZIP"
3. Cliquem com o botão direito em cima do ficheiro descarregado e escolham a opção "Extrair"
4. Extraiam o ficheiro ZIP para uma pasta (por exemplo: `C:\Users\<Username no seu PC>\Desktop\Python-Crypto`, relembrem-se que esta diretoria é uma pasta chamada "Python-Crypto" no vosso habitual "Ambiente de Trabalho")

### Passo 3: Instalar as Bibliotecas Necessárias
Abram a Linha de Comandos **como Administrador** (botão direito no ícone da linha de comandos):

```cmd
pip install Pillow
pip install imageio
pip install numpy
pip install cryptography
pip install pycryptodome
```

**O que fazem estas bibliotecas?**
- **Pillow**: Permite trabalhar com imagens (abrir, modificar, guardar)
- **imageio**: Lê e escreve diversos formatos de imagem
- **numpy**: Operações matemáticas avançadas com arrays
- **cryptography**: Algoritmos criptográficos de alto nível
- **pycryptodome**: Primitivas criptográficas de baixo nível

### Passo 4: Navegar até à Pasta do Projecto
Na linha de comandos, naveguem até onde extraíram os ficheiros:
```cmd
cd C:\Users\SeuNome\Desktop\Python-Crypto
```

### Passo 5: Criar a Pasta de Outputs
```cmd
mkdir intro\outputs
```

## Parte 1: One-Time Pads (Cifras de Fluxo)

### O que é um One-Time Pad?
Um **One-Time Pad** é teoricamente a cifra mais segura que existe - **se** for usada correctamente. A regra de ouro é: **nunca reutilizar a chave!**

### Experiência 1: Gerando uma Chave Aleatória

**O que vamos fazer:** Criar uma imagem completamente aleatória que servirá como nossa chave secreta.

```cmd
python RandomImageGenerator.py intro\outputs\otp.png 480 480
```

**O que acontece aqui:**
- `RandomImageGenerator.py`: O programa que gera pixels aleatórios
- `intro\outputs\otp.png`: Onde a nossa chave será guardada (OTP = One-Time Pad)
- `480 480`: Dimensões da imagem (480x480 pixels)

**Resultado esperado:** Uma imagem com "ruído" colorido - cada pixel tem uma cor completamente aleatória.

### Experiência 2: Cifrando a Primeira Imagem

**O que vamos fazer:** Usar a operação XOR (operação lógica "ou" exclusivo) para "misturar" uma imagem com a nossa chave.

```cmd
python ImageXor.py intro\inputs\tecnico-0480.png intro\outputs\otp.png intro\outputs\encrypted-tecnico.png
```

**Explicação detalhada:**
- `ImageXor.py`: Programa que faz a operação XOR entre duas imagens
- `intro\inputs\tecnico-0480.png`: A imagem original (logótipo do IST)
- `intro\outputs\otp.png`: A nossa chave secreta
- `intro\outputs\encrypted-tecnico.png`: O resultado cifrado

**Resultado esperado:** Uma imagem que parece ruído - a imagem original foi "escondida" pela chave.

### Experiência 3: O Perigo da Reutilização de Chaves

**O que vamos fazer:** Reutilizar a mesma chave numa segunda imagem (ERRO GRAVE!).

```cmd
python ImageXor.py intro\inputs\tux-0480.png intro\outputs\otp.png intro\outputs\encrypted-tux.png
```

**Abram as duas imagens cifradas:** `encrypted-tecnico.png` e `encrypted-tux.png`

**O que devem observar:** Ambas parecem ruído, mas há algo suspeito...

### Experiência 4: Revelando o Problema

**O que vamos fazer:** Fazer XOR entre as duas imagens cifradas para ver o desastre.

```cmd
python ImageXor.py intro\outputs\encrypted-tecnico.png intro\outputs\encrypted-tux.png intro\outputs\tecnico-tux.png
```

**Abram a imagem `tecnico-tux.png`**

**O que devem ver:** As duas imagens originais sobrepostas!

**Porquê isto acontece?**
```
Imagem1_Cifrada = Imagem1 ⊕ Chave
Imagem2_Cifrada = Imagem2 ⊕ Chave

Imagem1_Cifrada ⊕ Imagem2_Cifrada = (Imagem1 ⊕ Chave) ⊕ (Imagem2 ⊕ Chave)
                                  = Imagem1 ⊕ Imagem2 ⊕ Chave ⊕ Chave
                                  = Imagem1 ⊕ Imagem2 ⊕ 0
                                  = Imagem1 ⊕ Imagem2
```

**A chave cancelou-se!** Por isso é que se chama "One-Time" - só pode ser usada uma vez!

## Parte 2: Cifras por Blocos - AES

### O que é o AES?
O **AES (Advanced Encryption Standard)** é o algoritmo de cifra simétrica mais usado no mundo. Ao contrário dos One-Time Pads, o AES trabalha com blocos fixos de 128 bits (16 bytes).

### Modos de Operação
Como uma imagem é maior que 16 bytes, precisamos de uma estratégia para cifrar blocos sequenciais. Existem vários **modos de operação**:

#### Modo ECB (Electronic Code Book)
- **Funcionamento:** Cada bloco é cifrado independentemente
- **Fórmula:** `Bloco_Cifrado[i] = AES_Cifrar(Bloco_Original[i], Chave)`
- **Problema:** Blocos iguais produzem cifra igual (padrões visíveis!)

#### Modo CBC (Cipher Block Chaining)
- **Funcionamento:** Cada bloco é misturado com o bloco cifrado anterior antes de ser cifrado
- **Fórmula:** `Bloco_Cifrado[i] = AES_Cifrar(Bloco_Original[i] ⊕ Bloco_Cifrado[i-1], Chave)`
- **Vantagem:** Blocos iguais produzem cifras diferentes

#### Modo OFB (Output Feedback)
- **Funcionamento:** O AES é usado para gerar um "One-Time Pad" que é depois aplicado com XOR
- **Característica:** Transforma uma cifra por blocos numa cifra de fluxo

### Experiência 5: Gerando uma Chave AES

```cmd
python AESKeyGenerator.py w intro\outputs\aes.key
```

**O que acontece:**
- Gera uma chave AES de 256 bits (32 bytes) completamente aleatória
- Guarda-a no ficheiro `aes.key`

### Experiência 6: ECB - O Modo Inseguro

```cmd
python ImageAESCipher.py intro\inputs\glider-0480.png intro\outputs\aes.key ECB intro\outputs\glider-aes-ecb.png
```

**Abram a imagem `glider-aes-ecb.png`**

**O que devem ver:** A imagem original ainda é parcialmente visível! Os padrões não foram completamente escondidos.

**Porquê isto acontece?**
- O glider tem muitas áreas com a mesma cor
- No modo ECB, pixels com a mesma cor (mesmo bloco) produzem a mesma cifra
- Os padrões mantêm-se visíveis

**Experimentem com as outras imagens:**
```cmd
python ImageAESCipher.py intro\inputs\tecnico-0480.png intro\outputs\aes.key ECB intro\outputs\tecnico-aes-ecb.png
python ImageAESCipher.py intro\inputs\tux-0480.png intro\outputs\aes.key ECB intro\outputs\tux-aes-ecb.png
```

### Experiência 7: CBC - Melhorando a Segurança

```cmd
python ImageAESCipher.py intro\inputs\glider-0480.png intro\outputs\aes.key CBC intro\outputs\glider-aes-cbc.png
```

**Abram a imagem `glider-aes-cbc.png`**

**O que devem ver:** Agora sim, parece completamente aleatória! O modo CBC eliminou os padrões.

**Mas há um problema escondido...**
O código foi propositadamente enfraquecido - usa sempre o mesmo **Initialization Vector (IV)**.

**Cifremos as outras imagens:**
```cmd
python ImageAESCipher.py intro\inputs\tux-0480.png intro\outputs\aes.key CBC intro\outputs\tux-aes-cbc.png
python ImageAESCipher.py intro\inputs\tecnico-0480.png intro\outputs\aes.key CBC intro\outputs\tecnico-aes-cbc.png
```

**Abram as três imagens CBC e olhem para a primeira linha de pixels.**

**O que devem notar:** A primeira linha é igual em todas as imagens!

**Porquê?**
- Todas as imagens têm o fundo branco no topo
- O IV é sempre o mesmo
- O primeiro bloco cifrado é sempre igual para pixels iguais

### Experiência 8: OFB - Cifra de Fluxo com AES

```cmd
python ImageAESCipher.py intro\inputs\glider-0480.png intro\outputs\aes.key OFB intro\outputs\glider-aes-ofb.png
python ImageAESCipher.py intro\inputs\tux-0480.png intro\outputs\aes.key OFB intro\outputs\tux-aes-ofb.png
python ImageAESCipher.py intro\inputs\tecnico-0480.png intro\outputs\aes.key OFB intro\outputs\tecnico-aes-ofb.png
```

**Alternância rápida entre as imagens OFB**

**O que devem notar:** Conseguem "ver" as diferenças entre as imagens originais!

**Porquê?** O modo OFB com IV fixo comporta-se como um One-Time Pad reutilizado.

**Experimentem fazer XOR entre duas delas:**
```cmd
python ImageXor.py intro\outputs\glider-aes-ofb.png intro\outputs\tux-aes-ofb.png intro\outputs\glider-tux-ofb.png
```

**Resultado:** As duas imagens originais sobrepostas - o mesmo problema do One-Time Pad!

## Parte 3: Atacando Bases de Dados Cifradas

### O Cenário
Imaginemos que há uma base de dados com notas dos alunos. A base de dados está cifrada, mas vós sois "hackers éticos" e quereis demonstrar vulnerabilidades.

### Estrutura do Ficheiro `grades.txt`
- **64 bytes:** Nome do aluno
- **16 bytes:** Número do aluno  
- **16 bytes:** Idade
- **16 bytes:** Nota

### Experiência 9: Cifrando a Base de Dados

**ECB Mode:**
```cmd
python FileAESCipher.py grades\inputs\grades.txt intro\outputs\aes.key ECB intro\outputs\grades.ecb.aes
```

**CBC Mode:**
```cmd
python FileAESCipher.py grades\inputs\grades.txt intro\outputs\aes.key CBC intro\outputs\grades.cbc.aes
```

**OFB Mode:**
```cmd
python FileAESCipher.py grades\inputs\grades.txt intro\outputs\aes.key OFB intro\outputs\grades.ofb.aes
```

### O Desafio
O aluno "Thomas S. Cook" quer alterar a sua nota de forma não detectada. Como é que isto pode ser feito conhecendo apenas:
- A estrutura do ficheiro
- Os modos de operação
- Os ficheiros cifrados (mas não a chave!)

**Dica para ECB:** Blocos iguais têm cifras iguais. Se dois alunos têm a mesma nota, os blocos das notas são iguais.

**Dica para CBC/OFB:** Alterações num bloco cifrado afectam a decifra de forma previsível.

## Parte 4: Codificação Base64

### O que é Base64?
Base64 é uma forma de representar dados binários usando apenas caracteres ASCII "seguros". É como traduzir dados binários para um "alfabeto" que pode ser facilmente transmitido por email ou web.

### Experiência 10: Codificar e Descodificar

**Codificar:**
```cmd
python Base64Encode.py intro\outputs\grades.cbc.aes intro\outputs\grades.cbc.aes.b64
```

**Descodificar:**
```cmd
python Base64Decode.py intro\outputs\grades.cbc.aes.b64 intro\outputs\grades.cbc.aes.b64.decoded
```

**Verificar se são iguais:**
```cmd
fc /b intro\outputs\grades.cbc.aes intro\outputs\grades.cbc.aes.b64.decoded
```

**Se não aparecer nada:** Os ficheiros são idênticos!

### Análise de Tamanhos
**Vejam os tamanhos dos ficheiros:**
- Original: X bytes
- Base64: Y bytes
- Diferença: (Y-X)/X * 100 = ?%

**Questão:** Base64 fornece alguma segurança? 
**Resposta:** Não! É apenas uma forma de representação, não criptografia.

## Questões de Reflexão

1. **Porque é que nunca devemos reutilizar chaves em One-Time Pads?**

2. **Qual é o principal problema do modo ECB?**

3. **Porque é que o IV deve ser sempre diferente no modo CBC?**

4. **Em que situações usariam cifras simétricas vs assimétricas?**

5. **Base64 é seguro? Porquê?**

## Conceitos Importantes Aprendidos

- **Cifras simétricas** usam a mesma chave para cifrar e decifrar
- **One-Time Pads** são perfeitamente seguros se a chave nunca for reutilizada
- **Modos de operação** determinam como blocos sequenciais são cifrados
- **ECB é inseguro** porque revela padrões
- **CBC é mais seguro** mas precisa de IV aleatório
- **OFB** transforma cifra por blocos em cifra de fluxo
- **Base64** é codificação, não criptografia

## Próximos Passos
No próximo laboratório, vamos explorar as **cifras assimétricas** (chaves públicas e privadas), onde usamos chaves diferentes para cifrar e decifrar!
