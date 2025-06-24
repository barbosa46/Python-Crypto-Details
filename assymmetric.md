# Guião de Laboratório: Cifras Assimétricas em Python
**Instituto Superior Técnico, Universidade de Lisboa**  
**Fundamentos da Segurança**

## Introdução

Bem-vindos ao fascinante mundo das **cifras assimétricas**! Ao contrário das cifras simétricas (onde usamos a mesma chave para tudo), as cifras assimétricas usam **duas chaves diferentes mas matematicamente relacionadas**: uma chave **pública** e uma chave **privada**.

### O que são Cifras Assimétricas?
Imaginem que têm um cofre muito especial:
- **Chave Pública:** Qualquer pessoa pode usá-la para FECHAR o cofre
- **Chave Privada:** Só vocês têm esta chave e só ela pode ABRIR o cofre

Esta é a magia da criptografia assimétrica - permite comunicação segura sem partilhar segredos!

### Aplicações Principais
1. **Comunicação Segura:** Alice pode enviar mensagens secretas para Bob sem nunca se terem encontrado
2. **Assinaturas Digitais:** Provar que um documento foi realmente criado por uma pessoa específica
3. **Certificados Digitais:** Confirmar a identidade de websites e pessoas

### Objectivos do Laboratório
- Compreender o funcionamento das cifras assimétricas
- Gerar pares de chaves com OpenSSL e Python
- Criar e verificar assinaturas digitais
- Trabalhar com certificados digitais
- Implementar cifra RSA para imagens

## Preparação do Ambiente

### Passo 1: Instalar o OpenSSL no Windows

**Opção A: Usar Git Bash (Recomendado)**
1. Descarreguem e instalem o Git para Windows: https://git-scm.com/download/win
2. Durante a instalação, certifiquem-se que marcam "Git Bash"
3. O Git Bash inclui ferramentas Unix, incluindo o OpenSSL

**Opção B: Descarregar OpenSSL directamente**
1. Vão a: https://slproweb.com/products/Win32OpenSSL.html
2. Descarreguem a versão "Win64 OpenSSL" (não a Light)
3. Instalem e adicionem ao PATH do sistema

### Passo 2: Verificar a Instalação
Abram o **Git Bash** ou **Command Prompt** e testem:
```bash
openssl version
```
Deve aparecer algo como: "OpenSSL 3.x.x"

### Passo 3: Preparar o Ambiente Python
Se ainda não fizeram o laboratório anterior, instalem as bibliotecas:
```cmd
pip install cryptography
pip install pycryptodome
```

### Passo 4: Navegar para a Pasta do Projecto
```bash
cd Desktop/Python-Crypto
```

## Parte 1: Fundamentos do RSA

### O que é o RSA?
O **RSA** (Rivest-Shamir-Adleman) é o algoritmo de criptografia assimétrica mais famoso. Foi inventado em 1977 e baseia-se na dificuldade de factorizar números muito grandes.

### Como Funciona (Simplificado)
1. **Gerar Chaves:** Escolhem-se dois números primos gigantes (p e q)
2. **Chave Pública:** Baseada no produto n = p × q
3. **Chave Privada:** Baseada no conhecimento de p e q
4. **Segurança:** É computacionalmente impossível descobrir p e q conhecendo apenas n

### Tamanhos de Chave Típicos
- **1024 bits:** Mínimo aceitável (mas já considerado fraco)
- **2048 bits:** Padrão actual para a maioria das aplicações
- **4096 bits:** Muito seguro, mas mais lento

## Parte 2: Gerando Chaves com OpenSSL

### Experiência 1: Criar um Par de Chaves RSA

**Gerar a chave privada (contém também a pública):**
```bash
openssl genrsa -out intro/outputs/server.key 2048
```

**O que acontece aqui:**
- `genrsa`: Gera uma chave RSA
- `-out intro/outputs/server.key`: Ficheiro onde guardar
- `2048`: Tamanho da chave em bits

**Resultado:** Ficheiro `server.key` com a chave privada (e dados da pública)

**Extrair a chave pública:**
```bash
openssl rsa -in intro/outputs/server.key -pubout > intro/outputs/public.key
```

**Explicação:**
- `rsa -in server.key`: Lê a chave privada
- `-pubout`: Extrai apenas a parte pública
- `> public.key`: Redirige para ficheiro

**Vejam o conteúdo dos ficheiros:**
```bash
cat intro/outputs/server.key
cat intro/outputs/public.key
```

**O que devem ver:**
- Blocos de texto começados por "-----BEGIN..." e terminados por "-----END..."
- Conteúdo codificado em Base64

### Experiência 2: Análise das Chaves

**Ver detalhes da chave privada:**
```bash
openssl rsa -in intro/outputs/server.key -text -noout
```

**O que aparece:**
- **modulus (n):** O número público (produto de dois primos)
- **publicExponent (e):** Normalmente 65537
- **privateExponent (d):** O segredo que permite decifrar
- **prime1 (p) e prime2 (q):** Os números primos secretos!

**Importante:** Se alguém descobrir p e q, pode calcular a chave privada!

## Parte 3: Certificados Digitais

### O que são Certificados?
Um **certificado digital** é como um "bilhete de identidade" para chaves públicas. Confirma que uma chave pública pertence realmente a uma pessoa ou organização específica.

### Experiência 3: Criar um Certificate Signing Request (CSR)

```bash
openssl req -new -key intro/outputs/server.key -out intro/outputs/server.csr
```

**O que acontece:** O OpenSSL vai pedir informações:
- **Country Name:** PT
- **State:** Lisbon  
- **City:** Lisbon
- **Organization:** Instituto Superior Tecnico
- **Organizational Unit:** DEI
- **Common Name:** localhost (muito importante!)
- **Email:** o vosso email
- **Challenge password:** (deixem vazio)
- **Optional company name:** (deixem vazio)

**O CSR contém:**
- A chave pública
- As informações de identificação
- Uma assinatura feita com a chave privada (prova que têm a chave privada)

### Experiência 4: Auto-assinar o Certificado

```bash
openssl x509 -req -days 365 -in intro/outputs/server.csr -signkey intro/outputs/server.key -out intro/outputs/server.crt
```

**Explicação:**
- `x509`: Formato padrão de certificados
- `-req`: Processar um CSR
- `-days 365`: Certificado válido por 1 ano
- `-signkey server.key`: Auto-assinar com a própria chave
- `-out server.crt`: Certificado final

**Ver o certificado:**
```bash
openssl x509 -in intro/outputs/server.crt -text -noout
```

**Informações importantes:**
- **Subject:** Quem é o proprietário
- **Issuer:** Quem assinou (neste caso, nós próprios)
- **Validity:** Período de validade
- **Public Key:** A chave pública

### Experiência 5: Criar uma Autoridade de Certificação

Para podermos assinar certificados de outros, precisamos de uma base de dados:

```bash
echo 01 > intro/outputs/server.srl
```

Este ficheiro `.srl` contém o número de série do próximo certificado a emitir.

### Experiência 6: Certificado para um Utilizador

**Gerar chave para utilizador:**
```bash
openssl genrsa -out intro/outputs/user.key 2048
```

**Criar CSR do utilizador:**
```bash
openssl req -new -key intro/outputs/user.key -out intro/outputs/user.csr
```

**Assinar o certificado do utilizador com o nosso "servidor":**
```bash
openssl x509 -req -days 365 -in intro/outputs/user.csr -CA intro/outputs/server.crt -CAkey intro/outputs/server.key -out intro/outputs/user.crt
```

**Diferença importante:**
- `-CA server.crt`: Certificado da autoridade (nós)
- `-CAkey server.key`: Chave privada da autoridade
- Agora o **Issuer** será diferente do **Subject**!

## Parte 4: Assinaturas Digitais

### O que são Assinaturas Digitais?
As assinaturas digitais garantem:
1. **Autenticidade:** O documento foi realmente criado por quem diz que foi
2. **Integridade:** O documento não foi alterado
3. **Não-repúdio:** O autor não pode negar que assinou

### Como Funcionam?
1. **Assinar:** Calcular hash do documento → Cifrar hash com chave privada = Assinatura
2. **Verificar:** Calcular hash do documento → Decifrar assinatura com chave pública → Comparar

### Experiência 7: Assinar um Ficheiro

**Ver o conteúdo do ficheiro de notas:**
```bash
cat grades/inputs/grades.txt
```

**Calcular o hash SHA-256:**
```bash
openssl dgst -sha256 grades/inputs/grades.txt > intro/outputs/grades.sha256
```

**Ver o hash calculado:**
```bash
cat intro/outputs/grades.sha256
```

**Assinar o hash com a chave privada do utilizador:**
```bash
openssl rsautl -sign -inkey intro/outputs/user.key -keyform PEM -in intro/outputs/grades.sha256 > intro/outputs/grades.sig
```

**O que acontece:**
- `rsautl`: Ferramenta RSA de baixo nível
- `-sign`: Operação de assinatura (cifrar com chave privada)
- `-inkey user.key`: Chave privada para assinar
- `-keyform PEM`: Formato da chave
- `grades.sha256`: Hash a assinar
- `grades.sig`: Assinatura resultante

### Experiência 8: Verificar a Assinatura

**Verificar com a chave privada (só para teste):**
```bash
openssl rsautl -verify -in intro/outputs/grades.sig -inkey intro/outputs/user.key
```

**Comparar com o hash original:**
```bash
openssl dgst -sha256 grades/inputs/grades.txt
```

**Os hashes devem ser idênticos!**

### Experiência 9: Verificar com a Chave Pública

**Extrair a chave pública do utilizador:**
```bash
openssl rsa -in intro/outputs/user.key -pubout > intro/outputs/user_public.key
```

**Verificar usando apenas a chave pública:**
```bash
openssl rsautl -verify -in intro/outputs/grades.sig -pubin -inkey intro/outputs/user_public.key
```

**Importância:** Qualquer pessoa com a chave pública pode verificar a assinatura, mas só quem tem a chave privada pode criar assinaturas válidas!

### Experiência 10: Teste de Integridade

**Alterem uma letra no ficheiro grades.txt:**
```bash
echo "Dados alterados maliciosamente" >> grades/inputs/grades.txt
```

**Tentem verificar a assinatura novamente:**
```bash
openssl dgst -sha256 grades/inputs/grades.txt
```

**O hash é diferente!** A assinatura já não é válida - detectámos a alteração!

## Parte 5: Conversão de Chaves para Python

### Porquê Converter?
O Python usa formatos diferentes do OpenSSL. Precisamos de converter as chaves para formato **DER** (binário) em vez de **PEM** (texto).

### Experiência 11: Conversões Necessárias

**Converter chave privada para formato texto detalhado:**
```bash
openssl rsa -in intro/outputs/server.key -text > intro/outputs/private_key.pem
```

**Converter para formato PKCS#8 DER (Python consegue ler):**
```bash
openssl pkcs8 -topk8 -inform PEM -outform DER -in intro/outputs/private_key.pem -out intro/outputs/private_key.der -nocrypt
```

**Converter chave pública para DER:**
```bash
openssl rsa -in intro/outputs/private_key.pem -pubout -outform DER -out intro/outputs/public_key.der
```

### Experiência 12: Ler Chaves em Python

```bash
python RSAKeyGenerator.py r intro/outputs/private_key.der intro/outputs/public_key.der
```

**O que acontece:**
- O programa Python lê as chaves convertidas
- Mostra informações sobre a chave (tamanho, componentes)
- Confirma que a conversão foi bem-sucedida

## Parte 6: Gerar Chaves Directamente em Python

### Experiência 13: Gerar Par de Chaves RSA

```bash
python RSAKeyGenerator.py w intro/outputs/python_private.key intro/outputs/python_public.key
```

**Vantagens de gerar em Python:**
- Integração directa com o código
- Controlo total sobre os parâmetros
- Formato já compatível com as bibliotecas Python

**Comparar com as chaves OpenSSL:**
```bash
python RSAKeyGenerator.py r intro/outputs/python_private.key intro/outputs/python_public.key
```

## Parte 7: Cifrar Imagens com RSA

### Limitações do RSA
⚠️ **Muito Importante:** O RSA tem limitações severas:
- **Tamanho dos dados:** Só pode cifrar blocos pequenos (< tamanho da chave)
- **Chave 2048 bits:** Máximo ~245 bytes por bloco
- **Velocidade:** Muito mais lento que AES
- **Uso prático:** Normalmente só para cifrar chaves AES (criptografia híbrida)

### Experiência 14: Implementar Cifra RSA para Imagens

Vamos criar os programas `ImageRSACipher.py` e `ImageRSADecipher.py` baseados no `ImageAESCipher.py`.

**Conceitos a implementar:**
1. **Dividir imagem em blocos pequenos** (ex: 100 bytes cada)
2. **Cifrar cada bloco separadamente** com a chave pública
3. **Juntar todos os blocos cifrados** num ficheiro
4. **Para decifrar:** Processo inverso com chave privada

### Experiência 15: Cifrar uma Imagem Pequena

```bash
python ImageRSACipher.py intro/inputs/tecnico-0480.png intro/outputs/python_public.key intro/outputs/tecnico-rsa.encrypted
```

**O que deve acontecer:**
- Imagem original: ~100KB
- Imagem cifrada: ~200KB+ (RSA aumenta o tamanho!)
- Tempo: Muito mais lento que AES

### Experiência 16: Decifrar a Imagem

```bash
python ImageRSADecipher.py intro/outputs/tecnico-rsa.encrypted intro/outputs/python_private.key intro/outputs/tecnico-rsa-decrypted.png
```

**Verificar se funcionou:**
- Abrir `tecnico-rsa-decrypted.png`
- Deve ser idêntica à original


## Questões de Reflexão

### 1. Conceptuais
- **Quando usar cifras simétricas vs assimétricas?**
- **Porque é que o RSA é lento comparado com AES?**
- **O que acontece se perdermos a chave privada?**
- **Porque é que a criptografia híbrida é tão popular?**

### 2. Práticas
- **Como distribuir chaves públicas de forma segura?**
- **Que informações devem estar num certificado?**
- **Como detectar se um certificado foi comprometido?**
- **Que tamanho de chave RSA usar em 2024?**

### 3. Segurança
- **Que ataques são possíveis contra RSA?**
- **Porque é que o padding é importante?**
- **Como garantir que uma assinatura é única?**
- **O que é Perfect Forward Secrecy?**

## Conceitos Importantes Aprendidos

### Cifras Assimétricas
- **Duas chaves diferentes:** Pública (partilhável) e privada (secreta)
- **Aplicações:** Comunicação segura, assinaturas, certificados
- **Limitações:** Lentas, blocos pequenos, matematicamente complexas

### RSA Especificamente
- **Baseia-se** na dificuldade de factorizar números grandes
- **Chave pública:** Pode cifrar e verificar assinaturas
- **Chave privada:** Pode decifrar e criar assinaturas
- **Tamanhos:** 2048 bits mínimo, 4096 bits para alta segurança

### Assinaturas Digitais
- **Garantem:** Autenticidade, integridade, não-repúdio
- **Processo:** Hash + cifra com chave privada
- **Verificação:** Decifra com chave pública + compara hashes

### Certificados Digitais
- **Propósito:** Ligar identidades a chaves públicas
- **Componentes:** Chave pública, identidade, assinatura da CA
- **Hierarquia:** CAs raiz → CAs intermédias → certificados finais


## Aplicações no Mundo Real

### 1. HTTPS/TLS
- Certificados para autenticar servidores
- RSA ou ECDH para acordo de chaves
- AES para cifrar dados da sessão

### 2. Email Seguro (S/MIME, PGP)
- Assinaturas para autenticar remetente
- Cifra para proteger conteúdo
- Certificados para distribuir chaves públicas

### 3. Assinaturas de Software
- Garantir que software não foi alterado
- Confirmar publisher legítimo
- Detectar malware injectado

### 4. Blockchain/Criptomoedas
- Assinaturas para autorizar transacções
- Chaves públicas como "endereços"
- Proof of identity sem revelar identidade

## Próximos Passos

### Projectos Sugeridos

1. **Sistema de assinaturas** para documentos
2. **Email Seguro**: Instalar e usar PGP

### Ferramentas Profissionais
- **Hardware Security Modules (HSMs):** Para chaves críticas
- **Certificate Authorities comerciais:** Let's Encrypt, DigiCert
- **Bibliotecas criptográficas:** OpenSSL, libsodium, Bouncy Castle

## Conclusão

As cifras assimétricas revolucionaram a criptografia moderna, permitindo comunicação segura entre estranhos e criando a base para a internet segura que conhecemos hoje. 

Embora sejam mais complexas e lentas que as cifras simétricas, as suas capacidades únicas - especialmente para distribuição de chaves e assinaturas digitais - tornam-nas indispensáveis.

A combinação inteligente de ambos os tipos (criptografia híbrida) oferece o melhor dos dois mundos e é a base da segurança digital moderna.

**Lembrem-se:** A criptografia é uma ferramenta poderosa, mas deve ser usada correctamente. Pequenos erros de implementação podem comprometer completamente a segurança!
