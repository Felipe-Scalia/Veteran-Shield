"""
Veteran Shield v3.0 — Escudo do Guerreiro
Design moderno, fullscreen, gamificação estilo Duolingo.
10 lições · 30+ perguntas · 22 conquistas · 5 verificadores
"""

import tkinter as tk
from tkinter import messagebox
import json, os, re
from datetime import datetime, date

# ══════════════════════════════════════════════
# PALETA
# ══════════════════════════════════════════════
C = {
    "bg":        "#0d0d1a",
    "surface":   "#141428",
    "card":      "#1c1c35",
    "card2":     "#222240",
    "border":    "#2e2e55",
    "primary":   "#5b5ef4",
    "primary_h": "#7b7ef8",
    "accent":    "#e94560",
    "success":   "#22c98a",
    "warning":   "#f5a623",
    "danger":    "#ff4d6d",
    "streak":    "#ff7043",
    "xp":        "#5b5ef4",
    "text":      "#eeeef8",
    "text2":     "#8888aa",
    "text3":     "#555575",
    "locked":    "#1a1a30",
    "gold":      "#ffd700",
    "silver":    "#c0c0c0",
    "bronze":    "#cd7f32",
}
FONT = "Segoe UI"

# ══════════════════════════════════════════════
# LIÇÕES
# ══════════════════════════════════════════════
LICOES = [
    {
        "id": 0, "titulo": "Mensagens Suspeitas", "emoji": "📱", "xp": 30,
        "desc": "Identifique golpes por WhatsApp e SMS",
        "perguntas": [
            {"q": "Você recebeu: 'URGENTE! Sua conta será bloqueada. Atualize seus dados agora clicando aqui.' O que você faz?",
             "ops": ["Clico no link rapidamente", "Ignoro e deleto a mensagem", "Encaminho para a família", "Respondo pedindo mais detalhes"],
             "ok": 1, "exp": "Bancos NUNCA bloqueiam contas por link em mensagem. Sempre delete esse tipo de conteúdo!"},
            {"q": "Uma mensagem diz que você ganhou R$ 5.000 em um sorteio que não participou. O que isso indica?",
             "ops": ["Tenho muita sorte!", "É promoção real do banco", "Quase certamente é um golpe", "Devo confirmar meus dados para receber"],
             "ok": 2, "exp": "Ofertas boas demais são sempre golpes. Ninguém ganha prêmios de sorteios que não participou!"},
            {"q": "Qual frase é um sinal de ALERTA claro em mensagens?",
             "ops": ["'Seu pedido foi confirmado'", "'Confirme sua senha AGORA ou perde o acesso'", "'Sua fatura está disponível'", "'Bem-vindo ao nosso serviço'"],
             "ok": 1, "exp": "Urgência + pedido de senha = golpe garantido. Golpistas usam pressa para você não pensar."},
            {"q": "Você recebe uma mensagem de número desconhecido dizendo 'Oi, tudo bem? Mudei de número, me salva!' O que fazer?",
             "ops": ["Salvo imediatamente", "Ligo para o número antigo da pessoa para confirmar", "Mando dinheiro se pedir", "Passo meu CPF para confirmar quem é"],
             "ok": 1, "exp": "O golpe do 'novo número' é muito comum. Sempre ligue para o número antigo ou contate a pessoa por outro meio para confirmar."},
            {"q": "Uma mensagem pede que você encaminhe um código de 6 dígitos que chegou no seu celular. O que é isso?",
             "ops": ["Confirmação normal de cadastro", "Código para desbloquear promoção", "Tentativa de roubar sua conta (WhatsApp ou e-mail)", "Código de desconto de loja"],
             "ok": 2, "exp": "Códigos SMS são usados para verificar sua identidade. Quem pede esse código quer invadir sua conta. NUNCA compartilhe!"},
        ]
    },
    {
        "id": 1, "titulo": "Links Perigosos", "emoji": "🔗", "xp": 35,
        "desc": "Identifique URLs falsas e armadilhas online",
        "perguntas": [
            {"q": "Qual URL é mais segura para acessar seu banco?",
             "ops": ["bit.ly/meubanco123", "http://bradesco-login.com", "https://bradesco.com.br", "bradesco.info.acesso.br"],
             "ok": 2, "exp": "O site oficial sempre tem HTTPS e o domínio real (.com.br). Links curtos e domínios estranhos são armadilhas!"},
            {"q": "Um link começa com 'http://' (sem o S). Isso significa:",
             "ops": ["É mais rápido de carregar", "É um site antigo mas seguro", "Conexão NÃO é criptografada — evite", "É igual ao https://"],
             "ok": 2, "exp": "O 'S' em HTTPS significa Seguro. Sem ele, seus dados podem ser interceptados por terceiros."},
            {"q": "Você recebeu 'bit.ly/premio-caixa'. O que deve fazer?",
             "ops": ["Clicar, parece ser da Caixa", "Encaminhar para amigos", "NÃO clicar — links curtos escondem o destino real", "Clicar só se tiver antivírus"],
             "ok": 2, "exp": "Links encurtados (bit.ly, goo.gl) escondem o endereço real. Golpistas os usam exatamente por isso!"},
            {"q": "Qual desses domínios parece ser uma cópia falsa do Banco do Brasil?",
             "ops": ["bb.com.br", "bancodobrasil.com.br", "bb-internet.com.br.login.info", "www.bb.com.br"],
             "ok": 2, "exp": "Domínios com muitos pontos e palavras extras (como .login.info) são falsos. O domínio real do BB é bb.com.br ou bancodobrasil.com.br."},
            {"q": "Um e-mail pede que você baixe um arquivo '.exe' para 'atualizar seu cadastro'. O que você faz?",
             "ops": ["Baixo e instalo, parece urgente", "NÃO baixo — arquivos .exe podem ser vírus", "Baixo mas não abro", "Encaminho para um amigo abrir primeiro"],
             "ok": 1, "exp": "Arquivos .exe enviados por e-mail não solicitado são quase sempre vírus ou malware. Nunca instale!"},
        ]
    },
    {
        "id": 2, "titulo": "Golpes do PIX", "emoji": "💸", "xp": 40,
        "desc": "Proteja seu dinheiro nas transferências PIX",
        "perguntas": [
            {"q": "Alguém diz ser do banco e pede que você faça um PIX 'teste' para verificar sua conta. O que é isso?",
             "ops": ["Procedimento normal do banco", "Um golpe — bancos nunca pedem PIX de teste", "Verificação legítima de segurança", "Pode ser verdade se vier por telefone"],
             "ok": 1, "exp": "Bancos JAMAIS pedem que você faça transferências para verificar sua conta. Isso é golpe 100% das vezes!"},
            {"q": "Antes de fazer um PIX, o que você SEMPRE deve verificar?",
             "ops": ["Só o valor", "Só a chave PIX", "Nome do destinatário, CPF/CNPJ e valor", "Nada, PIX é sempre seguro"],
             "ok": 2, "exp": "Sempre confira nome, documento e valor. Uma vez enviado, o PIX NÃO pode ser cancelado!"},
            {"q": "Um 'funcionário do banco' liga pedindo sua senha para 'proteger sua conta hackeada'. Você deve:",
             "ops": ["Fornecer a senha, é urgente", "Desligar e ligar no número oficial do banco", "Dar apenas os 4 primeiros dígitos", "Pedir nome do funcionário e aí fornecer"],
             "ok": 1, "exp": "Funcionários de banco NUNCA pedem senha por telefone. Desligue e ligue no número do verso do seu cartão."},
            {"q": "Você quer vender algo e o comprador diz que vai pagar R$200 mas manda um comprovante de R$2.000 pedindo o troco. O que é isso?",
             "ops": ["Um erro do banco, devo devolver o troco", "Golpe do comprovante falso — não existe troco de PIX", "Devo aceitar e devolver R$1.800", "É confiável se o comprovante parecer real"],
             "ok": 1, "exp": "Comprovantes podem ser falsificados! Nunca devolva 'troco' sem ver o dinheiro na sua conta. Confirme no app do banco antes de qualquer devolução."},
            {"q": "Qual dessas chaves PIX é mais arriscada de compartilhar publicamente?",
             "ops": ["Chave aleatória (UUID)", "E-mail dedicado para PIX", "CPF como chave PIX", "Número de telefone secundário"],
             "ok": 2, "exp": "Usar o CPF como chave PIX expõe um dado sensível. Prefira uma chave aleatória gerada pelo banco para transações com desconhecidos."},
        ]
    },
    {
        "id": 3, "titulo": "Proteção de Dados", "emoji": "🔐", "xp": 35,
        "desc": "Seus dados pessoais são valiosos — proteja-os",
        "perguntas": [
            {"q": "Você deve compartilhar seu CPF com:",
             "ops": ["Qualquer pessoa que pedir", "Atendentes de telemarketing desconhecidos", "Apenas instituições confiáveis que realmente precisam", "Amigos no WhatsApp"],
             "ok": 2, "exp": "Seu CPF é um dado sensível. Compartilhe apenas com empresas confiáveis em situações necessárias."},
            {"q": "Uma 'pesquisa' pede nome, CPF, data de nascimento e número do cartão. O que você faz?",
             "ops": ["Preencho, parece oficial", "Preencho só o nome", "NÃO preencho — pesquisas não precisam de dados bancários", "Preencho se vier por e-mail"],
             "ok": 2, "exp": "Pesquisas reais nunca precisam de número de cartão. Isso é phishing — tentativa de roubar seus dados!"},
            {"q": "Como deve ser uma senha segura?",
             "ops": ["Minha data de nascimento", "Nome do meu pet", "Combinação de letras, números e símbolos", "A mesma senha para tudo — fica fácil"],
             "ok": 2, "exp": "Uma boa senha mistura letras maiúsculas, minúsculas, números e símbolos. Nunca use dados pessoais!"},
            {"q": "O que é a autenticação em dois fatores (2FA)?",
             "ops": ["Ter duas senhas iguais", "Confirmação extra além da senha (código no celular)", "Entrar em dois dispositivos ao mesmo tempo", "Trocar a senha duas vezes por mês"],
             "ok": 1, "exp": "O 2FA adiciona uma camada extra de segurança. Mesmo que sua senha vaze, o invasor ainda precisaria do código do seu celular."},
            {"q": "Você recebe um e-mail do 'suporte' pedindo para confirmar sua senha. O que você faz?",
             "ops": ["Confirmo, pode ser importante", "Ignoro — serviços legítimos NUNCA pedem sua senha por e-mail", "Mando metade da senha por segurança", "Respondo perguntando se é verdadeiro"],
             "ok": 1, "exp": "Nenhum serviço legítimo pede sua senha por e-mail. Isso é phishing. Delete imediatamente e altere sua senha se clicar em algo."},
        ]
    },
    {
        "id": 4, "titulo": "Golpes por Telefone", "emoji": "📞", "xp": 40,
        "desc": "Reconheça o Vishing e chamadas fraudulentas",
        "perguntas": [
            {"q": "Uma ligação diz ser da 'central de segurança do banco' e pede seu cartão e senha. Você deve:",
             "ops": ["Fornecer, é a central do banco", "Desligar e ligar no número oficial impresso no cartão", "Dar só o número do cartão, não a senha", "Pedir para aguardar e confirmar pelos Correios"],
             "ok": 1, "exp": "Bancos NUNCA pedem dados completos por telefone. Sempre desligue e ligue você mesmo para o número oficial do cartão."},
            {"q": "O identificador de chamadas mostra o número oficial do banco. Isso garante que a ligação é legítima?",
             "ops": ["Sim, número real = ligação real", "Não — números podem ser falsificados (spoofing)", "Sim, se começar com 0800", "Depende do horário da ligação"],
             "ok": 1, "exp": "Golpistas usam spoofing para falsificar o número exibido. Sempre desconfie e ligue você mesmo para confirmar."},
            {"q": "Uma gravação diz: 'Sua conta foi comprometida. Digite sua senha para liberar.' O que você faz?",
             "ops": ["Digite a senha, é urgente", "Desligo imediatamente", "Digito uma senha errada para testar", "Aguardo para falar com atendente"],
             "ok": 1, "exp": "Gravações automáticas solicitando senhas são golpes. Desligue imediatamente e entre em contato com seu banco pelo app oficial."},
            {"q": "Alguém liga dizendo ser seu neto(a) em apuros e pede dinheiro urgente. Você deve:",
             "ops": ["Enviar o dinheiro imediatamente", "Ligar diretamente para o celular do neto(a) para confirmar", "Pedir o número da conta e enviar", "Passar o CPF para 'confirmar identidade'"],
             "ok": 1, "exp": "O 'golpe do neto' é muito comum com idosos. Sempre ligue diretamente para a pessoa antes de qualquer ação."},
            {"q": "Uma ligação oferece empréstimo com taxa zero mas pede uma 'taxa de cadastro' antecipada. Isso é:",
             "ops": ["Uma promoção legítima do banco", "Prática comum no mercado financeiro", "Golpe — operações legítimas não cobram taxa antecipada", "Pode ser real se vier de banco conhecido"],
             "ok": 2, "exp": "Cobrar taxa antecipada para liberar empréstimo é golpe garantido. Bancos e financeiras legítimas descontam taxas do próprio empréstimo."},
        ]
    },
    {
        "id": 5, "titulo": "Redes Sociais e Fake News", "emoji": "📣", "xp": 35,
        "desc": "Não caia em desinformação e perfis falsos",
        "perguntas": [
            {"q": "Você vê uma notícia chocante no WhatsApp que pede para encaminhar para todos. O que você deve fazer primeiro?",
             "ops": ["Encaminhar imediatamente", "Verificar a fonte antes de compartilhar", "Acreditar se vier de um familiar", "Compartilhar se parecer verdadeira"],
             "ok": 1, "exp": "Antes de compartilhar qualquer notícia, verifique em sites confiáveis de checagem (como Agência Lupa, Aos Fatos ou G1). Fake news se espalham rápido!"},
            {"q": "Um perfil de rede social de um parente pede dinheiro urgente via mensagem direta. Você deve:",
             "ops": ["Enviar imediatamente, é familiar", "Ligar para o parente pelo número real para confirmar", "Enviar e depois confirmar", "Pedir o CPF do parente para confirmar"],
             "ok": 1, "exp": "Perfis de redes sociais podem ser clonados ou hackeados. Sempre confirme por ligação antes de qualquer transferência."},
            {"q": "O que é um perfil 'verificado' em redes sociais?",
             "ops": ["Perfil com muitos seguidores", "Perfil com selo oficial confirmado pela plataforma", "Qualquer perfil com foto", "Perfil com mais de 1 ano de existência"],
             "ok": 1, "exp": "O selo de verificação (✓ azul ou dourado) é concedido pela própria plataforma e confirma autenticidade. Mas atenção: golpistas criam perfis parecidos sem o selo!"},
            {"q": "Uma foto viral mostra uma celebridade anunciando um produto milagroso. Como identificar se é real?",
             "ops": ["Se a celebridade é famosa, é verdade", "Procuro o anúncio no perfil oficial verificado da celebridade", "Compro se o preço for bom", "Compartilho para avisar as pessoas"],
             "ok": 1, "exp": "Golpistas usam fotos e vídeos de celebridades para vender produtos falsos. Sempre verifique no perfil oficial verificado antes de acreditar."},
            {"q": "Você vê uma 'enquete' no Instagram que pede seu CPF para participar de um sorteio. O que você faz?",
             "ops": ["Preencho, pode ganhar prêmio", "NÃO preencho — sorteios legítimos não pedem CPF em redes sociais", "Preencho só se o perfil tiver muitos seguidores", "Preencho e espero o resultado"],
             "ok": 1, "exp": "Sorteios legítimos não coletam CPF por formulários em redes sociais. Isso é coleta ilegal de dados para fraude."},
        ]
    },
    {
        "id": 6, "titulo": "Golpe do Falso Emprego", "emoji": "💼", "xp": 45,
        "desc": "Cuidado com vagas falsas e fraudes trabalhistas",
        "perguntas": [
            {"q": "Uma vaga de emprego oferece salário de R$8.000 para trabalhar 2h por dia em casa sem experiência. Isso é:",
             "ops": ["Uma ótima oportunidade", "Provavelmente um golpe", "Normal no mercado digital", "Real se vier de empresa grande"],
             "ok": 1, "exp": "Salários altíssimos para funções simples e sem experiência são iscas de golpes. Vagas legítimas são compatíveis com o mercado."},
            {"q": "Durante um processo seletivo online, a empresa pede seus dados bancários 'para agilizar o pagamento'. O que você faz?",
             "ops": ["Forneço, quero o emprego", "Recuso — dados bancários só são pedidos após contratação formal com contrato", "Forneço só o banco, não a conta", "Peço para confirmar por e-mail"],
             "ok": 1, "exp": "Empresas legítimas só solicitam dados bancários APÓS a contratação formal com contrato assinado. Pedido antes disso é golpe."},
            {"q": "Um 'recrutador' pede que você faça um depósito para 'reservar sua vaga'. Você deve:",
             "ops": ["Depositar, a vaga vale a pena", "Recusar — processos seletivos legítimos nunca cobram do candidato", "Depositar metade primeiro", "Depositar se a empresa parecer grande"],
             "ok": 1, "exp": "Nenhuma empresa legítima cobra do candidato para participar de processo seletivo. Cobrar = golpe."},
            {"q": "Uma proposta de emprego chega por WhatsApp de número desconhecido com link para 'cadastro'. O que fazer?",
             "ops": ["Clico no link e me cadastro", "Ignoro ou pesquiso a empresa nos canais oficiais antes", "Envio meus documentos pelo WhatsApp mesmo", "Aceito se o salário for bom"],
             "ok": 1, "exp": "Ofertas de emprego legítimas chegam por canais oficiais (LinkedIn, site da empresa, e-mail corporativo). Links por WhatsApp de desconhecidos são suspeitos."},
            {"q": "O que é o 'golpe do maquininha' em falsas vagas de entregador?",
             "ops": ["Cobrar taxa pela maquininha que nunca chega", "Problema técnico com pagamentos", "Tipo de maquininha específica para entregadores", "Desconto no salário pelo uso da maquininha"],
             "ok": 0, "exp": "No golpe da maquininha, a falsa empresa cobra uma taxa para 'liberar o equipamento' que nunca é enviado. A vaga não existe — é apenas para roubar o dinheiro da taxa."},
        ]
    },
    {
        "id": 7, "titulo": "Golpe do Amor", "emoji": "💔", "xp": 50,
        "desc": "Reconheça o romance scam e proteja seu coração",
        "perguntas": [
            {"q": "Uma pessoa muito atraente te adiciona nas redes sociais e começa a se declarar apaixonada em poucos dias. Isso pode ser:",
             "ops": ["Amor verdadeiro e rápido", "Um golpe de romance (romance scam)", "Normal nas redes sociais", "Sinal de que a pessoa é muito sincera"],
             "ok": 1, "exp": "Golpistas constroem relacionamentos rápidos e intensos online para ganhar confiança antes de pedir dinheiro. Desconfie de declarações muito rápidas de desconhecidos."},
            {"q": "Seu 'namorado(a) online' que nunca encontrou pessoalmente pede dinheiro para 'resolver uma emergência médica'. O que fazer?",
             "ops": ["Envio, estou preocupado(a)", "NÃO envio — peço uma videochamada ao vivo para confirmar quem é", "Envio metade como teste", "Peço foto como prova"],
             "ok": 1, "exp": "Fotos podem ser roubadas. Sempre exija uma videochamada ao vivo. Golpistas de romance sempre têm desculpas para não aparecer em vídeo."},
            {"q": "Seu contato online diz ser um militar/médico trabalhando no exterior e nunca consegue fazer videochamada. Isso é:",
             "ops": ["Compreensível pela profissão", "Sinal claro de possível golpe", "Normal com problemas de internet", "Prova de que é uma pessoa séria e ocupada"],
             "ok": 1, "exp": "A identidade de militar ou profissional no exterior é uma das histórias mais usadas em golpes de romance. A impossibilidade de videochamada é um sinal de alerta."},
            {"q": "Seu contato online quer te enviar um 'presente valioso do exterior' mas pede que você pague as 'taxas alfandegárias'. Isso é:",
             "ops": ["Normal, taxas de importação existem", "Golpe — o presente não existe", "Aceitável se você confiar na pessoa", "Real se vier com código de rastreio"],
             "ok": 1, "exp": "O 'golpe da encomenda presa na alfândega' é clássico. O presente não existe — o objetivo é apenas que você pague as 'taxas' e continue pagando por supostos problemas."},
            {"q": "Qual é o principal objetivo de um golpista de romance?",
             "ops": ["Encontrar um relacionamento real", "Obter dinheiro ou dados da vítima", "Praticar o idioma do país da vítima", "Fazer amizades internacionais"],
             "ok": 1, "exp": "O romance scam é 100% financeiro. O golpista investe semanas ou meses construindo uma relação falsa com um único objetivo: obter dinheiro da vítima."},
        ]
    },
    {
        "id": 8, "titulo": "Segurança em Senhas", "emoji": "🔑", "xp": 35,
        "desc": "Crie e gerencie senhas fortes para se proteger",
        "perguntas": [
            {"q": "Qual dessas senhas é mais segura?",
             "ops": ["123456", "joao1980", "M@r10_S3gur0#2024", "senha"],
             "ok": 2, "exp": "A senha segura mistura letras maiúsculas e minúsculas, números e símbolos especiais. Quanto mais aleatória, melhor!"},
            {"q": "O que acontece se você usa a mesma senha em vários sites?",
             "ops": ["Nada, é mais prático", "Se um site for hackeado, todas as suas contas ficam em risco", "É mais seguro porque você não esquece", "Só é problema se for site de banco"],
             "ok": 1, "exp": "Usar a mesma senha em múltiplos sites é perigoso. Se um site vazar, golpistas testam a mesma senha em outros serviços (ataque chamado 'credential stuffing')."},
            {"q": "O que é um gerenciador de senhas?",
             "ops": ["Um caderno onde escrevo minhas senhas", "Um software seguro que guarda e gera senhas complexas", "Alguém contratado para lembrar senhas", "Uma função do WhatsApp"],
             "ok": 1, "exp": "Gerenciadores de senhas (como Bitwarden, 1Password) guardam senhas criptografadas e geram senhas fortes automaticamente. São muito mais seguros que cadernos!"},
            {"q": "Com que frequência você deve trocar suas senhas importantes?",
             "ops": ["Nunca, se for uma boa senha", "A cada 1 a 2 anos, ou imediatamente após suspeita de vazamento", "Todo dia", "Só quando esquecer"],
             "ok": 1, "exp": "Trocar senhas periodicamente e imediatamente após qualquer suspeita de vazamento é uma boa prática de segurança digital."},
            {"q": "Qual desses é um exemplo de pergunta de segurança FRACA?",
             "ops": ["Uma frase longa e aleatória", "'Qual o nome da sua mãe?' — informação pública ou fácil de descobrir", "'Qual era a cor do meu terceiro carro?' — específica e pessoal", "Uma combinação de palavras sem sentido"],
             "ok": 1, "exp": "Perguntas de segurança com respostas públicas ou fáceis de descobrir (nome da mãe, cidade natal) são vulneráveis. Prefira respostas inventadas e as anote em local seguro."},
        ]
    },
    {
        "id": 9, "titulo": "Suporte Técnico Falso", "emoji": "💻", "xp": 40,
        "desc": "Não caia em golpes de 'técnicos' e falsas assistências",
        "perguntas": [
            {"q": "Uma janela pop-up no seu computador avisa: 'Seu PC está infectado! Ligue agora para o suporte Microsoft.' Você deve:",
             "ops": ["Ligar imediatamente", "Fechar a janela — Microsoft nunca contata usuários assim", "Baixar o programa que a janela indica", "Clicar em 'remover vírus' na própria janela"],
             "ok": 1, "exp": "A Microsoft, Apple e outras empresas NUNCA entram em contato por pop-ups. Esse é o 'golpe do suporte técnico falso'. Feche a janela e reinicie o navegador."},
            {"q": "Um 'técnico' pede acesso remoto ao seu computador para 'resolver um problema'. O que fazer?",
             "ops": ["Aceito, ele precisa ver o problema", "Recuso se não tiver solicitado o suporte eu mesmo", "Aceito se ele souber meu nome", "Aceito se for uma ligação gravada"],
             "ok": 1, "exp": "Só conceda acesso remoto a técnicos que VOCÊ contratou e ligou. Acesso remoto não solicitado dá controle total do seu computador ao golpista."},
            {"q": "Um 'antivírus' aparece do nada e diz que encontrou 57 vírus no seu computador. O que isso provavelmente é?",
             "ops": ["Um antivírus legítimo sendo útil", "Scareware — software que assusta para vender algo falso", "Normal, computadores têm muitos vírus", "Sinal de que preciso formatar o PC"],
             "ok": 1, "exp": "Scareware exibe alertas falsos de vírus para assustar e vender um 'antivírus' que na verdade é o próprio vírus. Só use antivírus de fontes conhecidas (Avast, Windows Defender, etc.)."},
            {"q": "Um e-mail diz que sua 'licença do Windows venceu' e pede pagamento. Como verificar se é real?",
             "ops": ["Pago imediatamente, não quero perder o Windows", "Verifico as configurações do meu Windows ou no site oficial da Microsoft diretamente", "Clico no link do e-mail para ver os detalhes", "Ligo para o número do e-mail"],
             "ok": 1, "exp": "Sempre verifique diretamente no sistema ou no site oficial da empresa. Links e números em e-mails suspeitos podem ser falsos."},
            {"q": "Qual desses é um sinal de que um 'técnico' é golpista?",
             "ops": ["Tem empresa com CNPJ", "Pede pagamento em gift cards, criptomoedas ou PIX para pessoa física", "Oferece nota fiscal", "Tem avaliações no Google"],
             "ok": 1, "exp": "Golpistas pedem pagamento em formas difíceis de rastrear (gift cards, cripto, PIX pessoal). Empresas legítimas emitem boleto, nota fiscal e têm CNPJ verificável."},
        ]
    },
]

# ══════════════════════════════════════════════
# CONQUISTAS
# ══════════════════════════════════════════════
CONQUISTAS = [
    # Primeiros passos
    {"id":"primeira_licao",  "nome":"Primeiro Escudo",     "emoji":"🛡️",  "cat":"Lições",     "desc":"Complete sua primeira lição",         "cond": lambda d: d["licoes_completas"]>=1},
    {"id":"tres_licoes",     "nome":"Em Progressão",       "emoji":"📈",  "cat":"Lições",     "desc":"Complete 3 lições",                   "cond": lambda d: d["licoes_completas"]>=3},
    {"id":"cinco_licoes",    "nome":"Meio Caminho",        "emoji":"⚡",  "cat":"Lições",     "desc":"Complete 5 lições",                   "cond": lambda d: d["licoes_completas"]>=5},
    {"id":"todas_licoes",    "nome":"Escudo Completo",     "emoji":"🏆",  "cat":"Lições",     "desc":"Complete todas as 10 lições",         "cond": lambda d: d["licoes_completas"]>=len(LICOES)},
    {"id":"perfeito",        "nome":"Sem Erros",           "emoji":"💎",  "cat":"Lições",     "desc":"Acerte 100% de uma lição",            "cond": lambda d: d.get("teve_100pct",False)},
    {"id":"tres_perfeitos",  "nome":"Sniper Digital",      "emoji":"🎯",  "cat":"Lições",     "desc":"Acerte 100% em 3 lições diferentes",  "cond": lambda d: d.get("total_100pct",0)>=3},
    # XP
    {"id":"xp_50",           "nome":"Recruta",             "emoji":"🌱",  "cat":"XP",         "desc":"Alcance 50 XP",                       "cond": lambda d: d["xp"]>=50},
    {"id":"xp_150",          "nome":"Soldado",             "emoji":"⭐",  "cat":"XP",         "desc":"Alcance 150 XP",                      "cond": lambda d: d["xp"]>=150},
    {"id":"xp_350",          "nome":"Sargento",            "emoji":"🌟",  "cat":"XP",         "desc":"Alcance 350 XP",                      "cond": lambda d: d["xp"]>=350},
    {"id":"xp_700",          "nome":"Tenente",             "emoji":"💫",  "cat":"XP",         "desc":"Alcance 700 XP",                      "cond": lambda d: d["xp"]>=700},
    {"id":"xp_1200",         "nome":"Coronel Digital",     "emoji":"🏅",  "cat":"XP",         "desc":"Alcance 1200 XP",                     "cond": lambda d: d["xp"]>=1200},
    # Streak
    {"id":"streak_3",        "nome":"Em Chamas",           "emoji":"🔥",  "cat":"Streak",     "desc":"3 dias seguidos",                     "cond": lambda d: d["streak"]>=3},
    {"id":"streak_7",        "nome":"Uma Semana",          "emoji":"📅",  "cat":"Streak",     "desc":"7 dias seguidos",                     "cond": lambda d: d["streak"]>=7},
    {"id":"streak_14",       "nome":"Determinado",         "emoji":"💪",  "cat":"Streak",     "desc":"14 dias seguidos",                    "cond": lambda d: d["streak"]>=14},
    {"id":"streak_30",       "nome":"Inabalável",          "emoji":"🗿",  "cat":"Streak",     "desc":"30 dias seguidos",                    "cond": lambda d: d["streak"]>=30},
    # Verificações
    {"id":"v_msg",           "nome":"Detetive",            "emoji":"🔍",  "cat":"Verificador","desc":"Use o verificador de mensagens",       "cond": lambda d: d.get("v_msg",0)>=1},
    {"id":"v_cpf",           "nome":"Auditor",             "emoji":"📋",  "cat":"Verificador","desc":"Valide 3 CPFs diferentes",             "cond": lambda d: d.get("v_cpf",0)>=3},
    {"id":"v_url",           "nome":"Caçador de Links",    "emoji":"🕵️",  "cat":"Verificador","desc":"Verifique 5 URLs",                    "cond": lambda d: d.get("v_url",0)>=5},
    {"id":"v_todos",         "nome":"Analista Completo",   "emoji":"🧪",  "cat":"Verificador","desc":"Use todos os 5 tipos de verificação",  "cond": lambda d: all(d.get(f"v_{t}",0)>=1 for t in ["msg","cpf","tel","email","url"])},
    # Secretas
    {"id":"s_madrugada",     "nome":"Coruja Noturna",      "emoji":"🦉",  "cat":"Secreta",    "desc":"Use o app entre 0h e 5h",             "cond": lambda d: d.get("s_madrugada",False)},
    {"id":"s_historico_20",  "nome":"Vigilante",           "emoji":"🦸",  "cat":"Secreta",    "desc":"Faça 20 verificações no total",       "cond": lambda d: len(d.get("historico",[]))>=20},
    {"id":"s_todas_conquistas","nome":"Lendário",          "emoji":"👑",  "cat":"Secreta",    "desc":"Desbloqueie todas as outras conquistas","cond": lambda d: len(d.get("conquistas",[]))>=21},
]

# ══════════════════════════════════════════════
# PALAVRAS DE RISCO
# ══════════════════════════════════════════════
PALAVRAS_RISCO = {
    "envie seus dados":3,"clique aqui":3,"confirme sua senha":3,"atualize seus dados":3,
    "sua conta foi":3,"código de verificação":3,"senha expira":3,"acesso bloqueado":3,
    "ganhou":2,"prêmio":2,"urgente":2,"bloqueada":2,"pix":2,"transferência":2,
    "taxa de cadastro":3,"acesso remoto":2,"suporte técnico":2,"vírus detectado":2,
    "conta":1,"cartão":1,"cpf":2,"link":1,"promoção":1,"grátis":1,"whatsapp":1,
    "gift card":3,"bitcoin":2,"criptomoeda":2,"novo número":2,"preciso de ajuda":1,
}

# ══════════════════════════════════════════════
# PERSISTÊNCIA
# ══════════════════════════════════════════════
ARQUIVO = "veteran_shield_dados.json"

def carregar():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO,"r",encoding="utf-8") as f:
                d=json.load(f)
                defaults={"xp":0,"streak":0,"ultimo":None,"licoes_completas":0,
                          "licoes_ids":[],"conquistas":[],"historico":[],
                          "teve_100pct":False,"total_100pct":0,
                          "v_msg":0,"v_cpf":0,"v_tel":0,"v_email":0,"v_url":0,
                          "s_madrugada":False}
                for k,v in defaults.items(): d.setdefault(k,v)
                return d
        except: pass
    return {"xp":0,"streak":0,"ultimo":None,"licoes_completas":0,
            "licoes_ids":[],"conquistas":[],"historico":[],
            "teve_100pct":False,"total_100pct":0,
            "v_msg":0,"v_cpf":0,"v_tel":0,"v_email":0,"v_url":0,
            "s_madrugada":False}

def salvar(d):
    with open(ARQUIVO,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

def atualizar_streak(d):
    hoje=str(date.today())
    ult=d.get("ultimo")
    if ult==hoje: return d
    if ult:
        try:
            diff=(date.today()-date.fromisoformat(ult)).days
            d["streak"]=d["streak"]+1 if diff==1 else 1
        except: d["streak"]=1
    else: d["streak"]=1
    d["ultimo"]=hoje
    return d

def checar_conquistas(d):
    # Conquista secreta: madrugada
    h=datetime.now().hour
    if 0<=h<5: d["s_madrugada"]=True
    novas=[]
    for c in CONQUISTAS:
        if c["id"] not in d["conquistas"]:
            try:
                if c["cond"](d): d["conquistas"].append(c["id"]); novas.append(c)
            except: pass
    return d,novas

# ══════════════════════════════════════════════
# LÓGICA DE VERIFICAÇÃO
# ══════════════════════════════════════════════
def analisar_msg(msg):
    if not msg or not msg.strip(): return {"nivel":"baixo","score":0,"motivos":[]}
    score=0; motivos=[]; ml=msg.lower()
    for p,w in PALAVRAS_RISCO.items():
        if p in ml: score+=w; motivos.append(f"'{p}' (+{w}pt)")
    if "R$" in msg or "reais" in ml: score+=1; motivos.append("Valor financeiro (+1pt)")
    if any(p in ml for p in ["urgente","agora","hoje","imediato","último aviso"]): score+=1; motivos.append("Linguagem urgente (+1pt)")
    if any(p in ml for p in ["http://","https://","bit.ly","www.","clique","acesse"]): score+=2; motivos.append("Contém link/chamada de ação (+2pt)")
    nivel="alto" if score>=5 else "medio" if score>=2 else "baixo"
    return {"nivel":nivel,"score":score,"motivos":motivos}

def validar_cpf(cpf):
    cpf=re.sub(r'\D','',cpf)
    if len(cpf)!=11: return {"valido":False,"msg":"CPF deve ter 11 dígitos"}
    if cpf==cpf[0]*11: return {"valido":False,"msg":"CPF inválido (todos os dígitos iguais)"}
    soma=sum(int(cpf[i])*(10-i) for i in range(9))
    d1=(soma*10%11)%10
    if d1!=int(cpf[9]): return {"valido":False,"msg":"CPF inválido (dígito verificador incorreto)"}
    soma=sum(int(cpf[i])*(11-i) for i in range(10))
    d2=(soma*10%11)%10
    if d2!=int(cpf[10]): return {"valido":False,"msg":"CPF inválido (dígito verificador incorreto)"}
    fmt=f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return {"valido":True,"msg":f"CPF válido  ·  {fmt}"}

def validar_telefone(tel):
    t=re.sub(r'\D','',tel)
    if len(t)==10: return {"valido":True,"msg":f"Telefone fixo  ·  ({t[:2]}) {t[2:6]}-{t[6:]}"}
    if len(t)==11: return {"valido":True,"msg":f"Celular  ·  ({t[:2]}) {t[2:7]}-{t[7:]}"}
    return {"valido":False,"msg":"Telefone deve ter 10 ou 11 dígitos (com DDD)"}

def validar_email(email):
    padrao=r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    if re.match(padrao,email.strip()):
        dominio=email.split("@")[1].lower()
        suspeitos=["tempmail","mailinator","guerrillamail","10minutemail","yopmail","throwam","sharklasers","trashmail","dispostable"]
        if any(s in dominio for s in suspeitos):
            return {"valido":False,"msg":f"E-mail de domínio descartável suspeito: {dominio}"}
        return {"valido":True,"msg":f"Formato válido  ·  {email.strip()}"}
    return {"valido":False,"msg":"Formato de e-mail inválido"}

def analisar_url(url):
    suspeitos=["bit.ly","goo.gl","tinyurl","t.co","ow.ly","is.gd",".fake","-login","-atualizar","-acesso","login.","-seguro","-banco","acesso-"]
    ul=url.lower()
    if any(s in ul for s in suspeitos):
        return {"segura":False,"msg":"URL com encurtador ou padrão suspeito detectado"}
    if not url.startswith("https"):
        return {"segura":False,"msg":"URL não usa HTTPS — conexão sem criptografia"}
    partes=ul.replace("https://","").split("/")[0].split(".")
    if len(partes)>4:
        return {"segura":False,"msg":"Domínio com muitos subdomínios — padrão suspeito"}
    return {"segura":True,"msg":"URL parece segura (HTTPS, domínio sem padrões suspeitos)"}

# ══════════════════════════════════════════════
# APLICATIVO
# ══════════════════════════════════════════════
class App:
    def __init__(self,root):
        self.root=root
        self.root.title("Veteran Shield")
        self.root.configure(bg=C["bg"])
        self.root.attributes("-fullscreen",True)
        self.root.bind("<Escape>",lambda e: self.root.attributes("-fullscreen",False))
        self.root.bind("<F11>",  lambda e: self.root.attributes("-fullscreen",not self.root.attributes("-fullscreen")))
        self.dados=atualizar_streak(carregar())
        salvar(self.dados)
        self.tela_inicio()

    # ── helpers ──────────────────────────────
    def limpar(self):
        for w in self.root.winfo_children(): w.destroy()

    def W_(self): return self.root.winfo_width() or 1200
    def H_(self): return self.root.winfo_height() or 700

    def mk_scroll(self,parent):
        c=tk.Canvas(parent,bg=C["bg"],highlightthickness=0)
        sb=tk.Scrollbar(parent,orient="vertical",command=c.yview,
                        bg=C["surface"],troughcolor=C["border"],width=5)
        frame=tk.Frame(c,bg=C["bg"])
        frame.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
        c.create_window((0,0),window=frame,anchor="nw")
        c.configure(yscrollcommand=sb.set)
        c.pack(side="left",fill="both",expand=True)
        sb.pack(side="right",fill="y")
        c.bind_all("<MouseWheel>",lambda e:c.yview_scroll(int(-1*(e.delta/120)),"units"))
        return frame

    def btn(self,p,txt,cmd,bg=None,fg="#fff",sz=11,pad=12,w=0):
        return tk.Button(p,text=txt,command=cmd,font=(FONT,sz,"bold"),
                         bg=bg or C["primary"],fg=fg,
                         activebackground=C["primary_h"],activeforeground="#fff",
                         relief="flat",bd=0,cursor="hand2",pady=pad,width=w)

    def sep(self,p,cor=None,px=0,py=6):
        tk.Frame(p,bg=cor or C["border"],height=1).pack(fill="x",padx=px,pady=py)

    def progress(self,p,val,mx,w=300,h=6,cor=None):
        pct=min(val/mx,1.0) if mx else 0
        c=tk.Canvas(p,width=w,height=h,bg=C["border"],highlightthickness=0,bd=0)
        if pct>0: c.create_rectangle(0,0,int(w*pct),h,fill=cor or C["primary"],outline="")
        return c

    def topbar(self,p,titulo,voltar=None):
        bar=tk.Frame(p,bg=C["surface"],pady=14)
        bar.pack(fill="x")
        if voltar:
            tk.Button(bar,text="←  Voltar",command=voltar,
                      font=(FONT,10),bg=C["surface"],fg=C["text2"],
                      activebackground=C["card"],activeforeground=C["text"],
                      relief="flat",bd=0,cursor="hand2",padx=16).pack(side="left")
        tk.Label(bar,text=titulo,font=(FONT,14,"bold"),
                 bg=C["surface"],fg=C["text"]).pack(side="left",padx=8)
        tk.Label(bar,text="F11 = tela cheia  ·  ESC = janela",
                 font=(FONT,8),bg=C["surface"],fg=C["text3"]).pack(side="right",padx=16)

    def resultado_box(self,p,ok,texto):
        cor=C["success"] if ok else C["danger"]
        icon="✅" if ok else "🚨"
        f=tk.Frame(p,bg=C["card"],padx=20,pady=16)
        f.pack(fill="x",padx=28,pady=8)
        tk.Label(f,text=f"{icon}  {texto}",font=(FONT,12,"bold"),
                 bg=C["card"],fg=cor,wraplength=900,justify="left").pack(anchor="w")

    def entrada_campo(self,p,ph,multi=False,h=5):
        if multi:
            e=tk.Text(p,font=(FONT,11),bg=C["card2"],fg=C["text"],
                      insertbackground=C["text"],relief="flat",height=h,wrap="word",
                      highlightthickness=1,highlightcolor=C["primary"],
                      highlightbackground=C["border"])
            e.pack(fill="x"); e.insert("1.0",ph)
            e.bind("<FocusIn>",lambda ev:e.delete("1.0","end") if e.get("1.0","end").strip()==ph else None)
            return e, lambda:e.get("1.0","end").strip()
        else:
            f=tk.Frame(p,bg=C["card2"],highlightthickness=1,
                       highlightcolor=C["primary"],highlightbackground=C["border"])
            f.pack(fill="x")
            e=tk.Entry(f,font=(FONT,12),bg=C["card2"],fg=C["text"],
                       insertbackground=C["text"],relief="flat")
            e.pack(fill="x",ipady=10,padx=10)
            e.insert(0,ph)
            e.bind("<FocusIn>",lambda ev:e.delete(0,"end") if e.get()==ph else None)
            e.bind("<FocusOut>",lambda ev:e.insert(0,ph) if not e.get() else None)
            return e, lambda:("" if e.get()==ph else e.get().strip())

    # ══════════════════════════════════════════
    # TELA INÍCIO
    # ══════════════════════════════════════════
    def tela_inicio(self):
        self.limpar()
        self.root.update_idletasks()

        # Sidebar
        side=tk.Frame(self.root,bg=C["surface"],width=270)
        side.pack(side="left",fill="y"); side.pack_propagate(False)

        tk.Label(side,text="🛡️",font=(FONT,48),bg=C["surface"],fg=C["accent"]).pack(pady=(40,2))
        tk.Label(side,text="Veteran Shield",font=(FONT,16,"bold"),bg=C["surface"],fg=C["text"]).pack()
        tk.Label(side,text="Escudo do Guerreiro",font=(FONT,9),bg=C["surface"],fg=C["text2"]).pack(pady=(0,24))
        self.sep(side,px=20)

        d=self.dados
        total_xp_max=sum(l["xp"] for l in LICOES)
        prox_nivel=next((n for n in [50,150,350,700,1200,9999] if n>d["xp"]),9999)
        pct_nivel=min(d["xp"]/prox_nivel,1.0)

        for ico,val,sub,cor in [
            ("🔥",f"{d['streak']}","dias de streak",C["streak"]),
            ("⭐",str(d["xp"]),f"de {total_xp_max} XP possível",C["xp"]),
            ("🏅",f"{len(d['conquistas'])}/{len(CONQUISTAS)}","conquistas",C["gold"]),
            ("📚",f"{d['licoes_completas']}/{len(LICOES)}","lições completas",C["success"]),
        ]:
            sf=tk.Frame(side,bg=C["card"],padx=14,pady=10)
            sf.pack(fill="x",padx=16,pady=4)
            row=tk.Frame(sf,bg=C["card"]); row.pack(fill="x")
            tk.Label(row,text=ico,font=(FONT,20),bg=C["card"]).pack(side="left",padx=(0,10))
            info=tk.Frame(row,bg=C["card"]); info.pack(side="left")
            tk.Label(info,text=val,font=(FONT,15,"bold"),bg=C["card"],fg=cor).pack(anchor="w")
            tk.Label(info,text=sub,font=(FONT,8),bg=C["card"],fg=C["text2"]).pack(anchor="w")

        # Barra XP para próximo nível
        self.sep(side,px=16,py=8)
        tk.Label(side,text=f"Próximo nível: {prox_nivel} XP",
                 font=(FONT,8),bg=C["surface"],fg=C["text2"]).pack(padx=16,anchor="w")
        pb=self.progress(side,d["xp"],prox_nivel,w=238,h=5,cor=C["xp"])
        pb.pack(padx=16,pady=(2,12))

        self.sep(side,px=16)
        self.btn(side,"F11 — Tela Cheia",
                 lambda:self.root.attributes("-fullscreen",not self.root.attributes("-fullscreen")),
                 bg=C["card"],fg=C["text2"],sz=9,pad=7).pack(fill="x",padx=16,pady=6)
        tk.Label(side,text="ESC sai da tela cheia",font=(FONT,7),
                 bg=C["surface"],fg=C["text3"]).pack()
        tk.Label(side,text="Veteran Shield v3.0 · © 2026",font=(FONT,7),
                 bg=C["surface"],fg=C["text3"]).pack(side="bottom",pady=10)

        # Área principal
        main=tk.Frame(self.root,bg=C["bg"])
        main.pack(side="left",fill="both",expand=True)

        # Header
        hdr=tk.Frame(main,bg=C["bg"])
        hdr.pack(fill="x",padx=40,pady=(36,4))
        tk.Label(hdr,text="O que você quer fazer hoje?",
                 font=(FONT,20,"bold"),bg=C["bg"],fg=C["text"],anchor="w").pack(fill="x")
        tk.Label(hdr,text="Aprenda a se proteger contra golpes digitais e verifique conteúdos suspeitos.",
                 font=(FONT,10),bg=C["bg"],fg=C["text2"],anchor="w").pack(fill="x",pady=(2,0))

        # Streak banner se streak > 1
        if d["streak"]>1:
            banner=tk.Frame(main,bg="#1e1206",padx=20,pady=10)
            banner.pack(fill="x",padx=40,pady=(10,0))
            tk.Label(banner,text=f"🔥  {d['streak']} dias seguidos! Continue assim, guerreiro!",
                     font=(FONT,10,"bold"),bg="#1e1206",fg=C["streak"]).pack(anchor="w")

        # Grid de opções
        scr=tk.Frame(main,bg=C["bg"]); scr.pack(fill="both",expand=True)
        frame=self.mk_scroll(scr)

        grid=tk.Frame(frame,bg=C["bg"]); grid.pack(padx=40,pady=20,fill="x")

        opcoes=[
            ("📚","Lições Diárias",       f"{d['licoes_completas']}/{len(LICOES)} completas",  C["primary"],self.tela_licoes),
            ("🔍","Verificar Mensagem",    "Analise textos suspeitos",                          C["accent"], lambda:self.tela_verificar("msg")),
            ("📋","Validar CPF",           "Cheque a autenticidade de um CPF",                 C["card"],   lambda:self.tela_verificar("cpf")),
            ("📱","Validar Telefone",      "Valide números de telefone brasileiros",            C["card"],   lambda:self.tela_verificar("tel")),
            ("✉️","Verificar E-mail",      "Analise endereços de e-mail",                       C["card"],   lambda:self.tela_verificar("email")),
            ("🔗","Verificar URL",         "Cheque a segurança de links",                      C["card"],   lambda:self.tela_verificar("url")),
            ("🏅","Conquistas",            f"{len(d['conquistas'])}/{len(CONQUISTAS)} desbloqueadas", C["card"],self.tela_conquistas),
            ("📖","Histórico",             f"{len(d.get('historico',[]))} verificações",       C["card"],   self.tela_historico),
        ]

        cols=4
        for i,(ico,titulo,sub,bg_c,cmd) in enumerate(opcoes):
            r2,c2=divmod(i,cols)
            if c2==0:
                row=tk.Frame(grid,bg=C["bg"]); row.pack(fill="x",pady=4)
            cf=tk.Frame(row,bg=C["card"],padx=18,pady=16,cursor="hand2")
            cf.pack(side="left",padx=6,expand=True,fill="x")
            is_primary=(bg_c==C["primary"] or bg_c==C["accent"])
            bg_icon=C["primary"] if bg_c==C["primary"] else (C["accent"] if bg_c==C["accent"] else C["card2"])
            ico_f=tk.Frame(cf,bg=bg_icon,width=40,height=40); ico_f.pack(anchor="w"); ico_f.pack_propagate(False)
            tk.Label(ico_f,text=ico,font=(FONT,18),bg=bg_icon).place(relx=.5,rely=.5,anchor="center")
            tk.Label(cf,text=titulo,font=(FONT,11,"bold"),bg=C["card"],fg=C["text"]).pack(anchor="w",pady=(8,1))
            tk.Label(cf,text=sub,font=(FONT,8),bg=C["card"],fg=C["text2"],wraplength=180,justify="left").pack(anchor="w")

            def bind_card(frame,fn):
                frame.bind("<Button-1>",lambda e:fn())
                for ch in frame.winfo_children():
                    ch.bind("<Button-1>",lambda e,f=fn:f())
                    for cc in ch.winfo_children():
                        cc.bind("<Button-1>",lambda e,f=fn:f())
            bind_card(cf,cmd)

            bg_h=C["card2"]
            def hover_on(e,f=cf):
                f.configure(bg=bg_h)
                for ch in f.winfo_children(): ch.configure(bg=bg_h)
            def hover_off(e,f=cf):
                f.configure(bg=C["card"])
                for ch in f.winfo_children(): ch.configure(bg=C["card"])
            cf.bind("<Enter>",hover_on); cf.bind("<Leave>",hover_off)

        tk.Frame(frame,bg=C["bg"],height=30).pack()

    # ══════════════════════════════════════════
    # TELA LIÇÕES
    # ══════════════════════════════════════════
    def tela_licoes(self):
        self.limpar()
        self.topbar(self.root,"📚  Lições Diárias",self.tela_inicio)

        feitas=len([l for l in LICOES if l["id"] in self.dados["licoes_ids"]])
        total=len(LICOES)

        info=tk.Frame(self.root,bg=C["bg"])
        info.pack(fill="x",padx=28,pady=(14,4))
        tk.Label(info,text=f"Progresso: {feitas} de {total} lições  ·  {sum(l['xp'] for l in LICOES)} XP disponível",
                 font=(FONT,10),bg=C["bg"],fg=C["text2"],anchor="w").pack(fill="x")
        self.progress(info,feitas,total,w=self.W_()-80,h=7).pack(anchor="w",pady=(4,0))

        scr=tk.Frame(self.root,bg=C["bg"]); scr.pack(fill="both",expand=True)
        frame=self.mk_scroll(scr)

        for i,lic in enumerate(LICOES):
            completa=lic["id"] in self.dados["licoes_ids"]
            bloqueada=i>0 and LICOES[i-1]["id"] not in self.dados["licoes_ids"]
            bg_c=C["locked"] if bloqueada else C["card"]

            cf=tk.Frame(frame,bg=bg_c,padx=22,pady=16)
            cf.pack(fill="x",padx=28,pady=5)
            row=tk.Frame(cf,bg=bg_c); row.pack(fill="x")

            emoji="✅" if completa else ("🔒" if bloqueada else lic["emoji"])
            tk.Label(row,text=emoji,font=(FONT,28),bg=bg_c).pack(side="left",padx=(0,16))

            info2=tk.Frame(row,bg=bg_c); info2.pack(side="left",fill="x",expand=True)
            n_perguntas=len(lic["perguntas"])
            cor_t=C["text2"] if bloqueada else C["text"]
            tk.Label(info2,text=lic["titulo"],font=(FONT,13,"bold"),bg=bg_c,fg=cor_t,anchor="w").pack(fill="x")
            tk.Label(info2,text=f"{lic['desc']}  ·  {n_perguntas} perguntas",
                     font=(FONT,9),bg=bg_c,fg=C["text2"],anchor="w").pack(fill="x")

            lado=tk.Frame(row,bg=bg_c); lado.pack(side="right",padx=8)
            xp_cor=C["success"] if completa else (C["text3"] if bloqueada else C["xp"])
            tk.Label(lado,text=f"+{lic['xp']} XP",font=(FONT,12,"bold"),bg=bg_c,fg=xp_cor).pack()
            if completa:
                tk.Label(lado,text="✓ feita",font=(FONT,8),bg=bg_c,fg=C["success"]).pack()

            if not bloqueada:
                txt_b="Revisar ↻" if completa else "Começar →"
                bg_b=C["card2"] if completa else C["accent"]
                self.btn(cf,txt_b,lambda l=lic:self.iniciar_quiz(l),
                         bg=bg_b,sz=10,pad=8).pack(anchor="e",pady=(10,0))

        tk.Frame(frame,bg=C["bg"],height=30).pack()

    # ══════════════════════════════════════════
    # QUIZ
    # ══════════════════════════════════════════
    def iniciar_quiz(self,lic):
        self.lic=lic; self.qi=0; self.acertos=0; self.xp_ganho=0
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        self.limpar()
        lic=self.lic; qi=self.qi; p=lic["perguntas"][qi]; total=len(lic["perguntas"])
        self.topbar(self.root,f"{lic['emoji']}  {lic['titulo']}")

        prog=tk.Frame(self.root,bg=C["bg"]); prog.pack(fill="x",padx=28,pady=(10,4))
        self.progress(prog,qi,total,w=self.W_()-80,h=6,cor=C["accent"]).pack(anchor="w")
        tk.Label(prog,text=f"Pergunta {qi+1} de {total}  ·  {self.acertos} acerto(s) até agora",
                 font=(FONT,9),bg=C["bg"],fg=C["text2"]).pack(anchor="w",pady=(3,0))
        self.sep(self.root,px=28)

        qf=tk.Frame(self.root,bg=C["card"],padx=28,pady=20)
        qf.pack(fill="x",padx=28,pady=(0,10))
        tk.Label(qf,text=p["q"],font=(FONT,13),bg=C["card"],fg=C["text"],
                 wraplength=self.W_()-120,justify="left").pack(anchor="w")

        self.op_btns=[]
        for i,op in enumerate(p["ops"]):
            b=tk.Button(self.root,text=f"  {chr(65+i)}.  {op}",
                        command=lambda idx=i:self.responder(idx),
                        font=(FONT,11),bg=C["card2"],fg=C["text"],
                        activebackground=C["primary"],activeforeground="#fff",
                        relief="flat",bd=0,cursor="hand2",anchor="w",
                        padx=20,pady=12,wraplength=self.W_()-80)
            b.pack(fill="x",padx=28,pady=3)
            self.op_btns.append(b)

        self.fb_frame=tk.Frame(self.root,bg=C["bg"]); self.fb_frame.pack(fill="x",padx=28,pady=6)

    def responder(self,escolha):
        p=self.lic["perguntas"][self.qi]; ok=p["ok"]
        for b in self.op_btns: b.config(state="disabled",cursor="arrow")
        xp_p=max(1,self.lic["xp"]//len(self.lic["perguntas"]))
        if escolha==ok:
            self.op_btns[ok].config(bg="#0d2b1f",fg=C["success"])
            self.acertos+=1; self.xp_ganho+=xp_p
            cor=C["success"]; icon="✅"; msg=f"Correto! +{xp_p} XP\n{p['exp']}"
        else:
            self.op_btns[escolha].config(bg="#2b0d15",fg=C["danger"])
            self.op_btns[ok].config(bg="#0d2b1f",fg=C["success"])
            cor=C["danger"]; icon="❌"; msg=f"Incorreto.\n{p['exp']}"

        for w in self.fb_frame.winfo_children(): w.destroy()
        tk.Label(self.fb_frame,text=f"{icon}  {msg}",font=(FONT,10),
                 bg=C["bg"],fg=cor,wraplength=self.W_()-80,justify="left").pack(anchor="w",pady=4)

        txt="Próxima →" if self.qi+1<len(self.lic["perguntas"]) else "Ver resultado ✓"
        self.btn(self.fb_frame,txt,self.proxima,bg=C["primary"],sz=10,pad=8).pack(anchor="w",pady=(6,0))

    def proxima(self):
        if self.qi+1<len(self.lic["perguntas"]): self.qi+=1; self.mostrar_pergunta()
        else: self.resultado()

    def resultado(self):
        self.limpar()
        lic=self.lic; total=len(lic["perguntas"])
        pct=int(self.acertos/total*100)

        self.dados["xp"]+=self.xp_ganho
        if lic["id"] not in self.dados["licoes_ids"]:
            self.dados["licoes_ids"].append(lic["id"])
            self.dados["licoes_completas"]=len(self.dados["licoes_ids"])
        if pct==100:
            self.dados["teve_100pct"]=True
            self.dados["total_100pct"]=self.dados.get("total_100pct",0)+1
        self.dados,novas=checar_conquistas(self.dados)
        salvar(self.dados)

        self.topbar(self.root,"Resultado da Lição")
        centro=tk.Frame(self.root,bg=C["bg"]); centro.pack(expand=True,fill="both",padx=80,pady=20)

        emoji_res="🎉" if pct>=80 else ("👍" if pct>=50 else "😅")
        msg_res="Excelente, guerreiro!" if pct>=80 else ("Bom trabalho!" if pct>=50 else "Continue praticando!")
        tk.Label(centro,text=emoji_res,font=(FONT,52),bg=C["bg"]).pack(pady=(16,4))
        tk.Label(centro,text="Lição concluída!",font=(FONT,20,"bold"),bg=C["bg"],fg=C["accent"]).pack()
        tk.Label(centro,text=msg_res,font=(FONT,11),bg=C["bg"],fg=C["text2"]).pack(pady=(2,20))

        sf=tk.Frame(centro,bg=C["bg"]); sf.pack()
        for lab,val,cor in [("Acertos",f"{self.acertos}/{total}",C["success"]),
                             ("XP Ganho",f"+{self.xp_ganho}",C["xp"]),
                             ("Aproveit.",f"{pct}%",C["warning"])]:
            f=tk.Frame(sf,bg=C["card"],padx=28,pady=16); f.pack(side="left",padx=8)
            tk.Label(f,text=lab,font=(FONT,9),bg=C["card"],fg=C["text2"]).pack()
            tk.Label(f,text=val,font=(FONT,20,"bold"),bg=C["card"],fg=cor).pack()

        if pct==100:
            self.sep(centro,py=10)
            tk.Label(centro,text="💎  Aproveitamento perfeito! Parabéns!",
                     font=(FONT,11,"bold"),bg=C["bg"],fg=C["gold"]).pack()

        if novas:
            self.sep(centro,py=10)
            tk.Label(centro,text="🏅  Nova(s) conquista(s) desbloqueada(s)!",
                     font=(FONT,11,"bold"),bg=C["bg"],fg=C["warning"]).pack(pady=(0,4))
            for c in novas:
                cf=tk.Frame(centro,bg=C["card"],padx=16,pady=8)
                cf.pack(fill="x",pady=3)
                tk.Label(cf,text=f"{c['emoji']}  {c['nome']}",font=(FONT,11,"bold"),
                         bg=C["card"],fg=C["gold"]).pack(side="left")
                tk.Label(cf,text=c["desc"],font=(FONT,9),
                         bg=C["card"],fg=C["text2"]).pack(side="left",padx=12)

        self.sep(centro,py=14)
        row=tk.Frame(centro,bg=C["bg"]); row.pack()
        self.btn(row,"Próxima lição →",self.tela_licoes,bg=C["success"],sz=11,pad=10).pack(side="left",padx=8)
        self.btn(row,"← Início",self.tela_inicio,bg=C["card"],fg=C["text2"],sz=11,pad=10).pack(side="left",padx=8)

    # ══════════════════════════════════════════
    # VERIFICAÇÕES
    # ══════════════════════════════════════════
    VMETA={
        "msg":   ("🔍  Verificar Mensagem", "Cole ou digite a mensagem suspeita aqui...", True),
        "cpf":   ("📋  Validar CPF",         "000.000.000-00",                            False),
        "tel":   ("📱  Validar Telefone",     "(00) 00000-0000",                           False),
        "email": ("✉️   Verificar E-mail",     "exemplo@dominio.com",                      False),
        "url":   ("🔗  Verificar URL",        "https://...",                               False),
    }

    def tela_verificar(self,tipo):
        self.limpar()
        titulo,ph,multi=self.VMETA[tipo]
        self.topbar(self.root,titulo,self.tela_inicio)
        self.sep(self.root,px=28)

        area=tk.Frame(self.root,bg=C["bg"]); area.pack(fill="x",padx=28,pady=10)
        self._entrada,self._get=self.entrada_campo(area,ph,multi=multi,h=6)
        self._tipo=tipo
        self._res=tk.Frame(self.root,bg=C["bg"]); self._res.pack(fill="both",expand=True,padx=0)

        LABELS={"msg":"Analisar mensagem","cpf":"Validar CPF","tel":"Validar telefone",
                "email":"Analisar e-mail","url":"Verificar link"}
        row=tk.Frame(self.root,bg=C["bg"]); row.pack(fill="x",padx=28,pady=8)
        self.btn(row,f"🔍  {LABELS[tipo]}",self._exec_v,bg=C["accent"],pad=10).pack(side="left",padx=(0,10))
        self.btn(row,"← Voltar",self.tela_inicio,bg=C["card"],fg=C["text2"],pad=10).pack(side="left")

        # Dica contextual
        dicas={"msg":"💡 Cole uma mensagem de WhatsApp, SMS ou e-mail que pareça suspeita.",
               "cpf":"💡 O CPF pode ser digitado com ou sem formatação (pontos e traço).",
               "tel":"💡 Digite o telefone com DDD. Ex: (61) 99999-9999 ou 61999999999",
               "email":"💡 Detectamos domínios de e-mail descartáveis usados em golpes.",
               "url":"💡 Cole o link completo incluindo http:// ou https://"}
        tk.Label(self.root,text=dicas.get(tipo,""),font=(FONT,9),
                 bg=C["bg"],fg=C["text3"],anchor="w").pack(fill="x",padx=28,pady=(0,4))

    def _exec_v(self):
        val=self._get()
        if not val: messagebox.showwarning("Aviso","Preencha o campo antes de verificar."); return
        for w in self._res.winfo_children(): w.destroy()

        tipo=self._tipo
        # Atualizar contador de verificações
        self.dados[f"v_{tipo}"]=self.dados.get(f"v_{tipo}",0)+1

        if tipo=="msg":
            r=analisar_msg(val)
            cn={"alto":C["danger"],"medio":C["warning"],"baixo":C["success"]}
            en={"alto":"🚨","medio":"⚠️","baixo":"✅"}
            tn={"alto":"RISCO ALTO — NÃO responda nem clique em links!",
                "medio":"ATENÇÃO — Mensagem tem elementos suspeitos.",
                "baixo":"PARECE SEGURA — Nenhum indicador óbvio de golpe."}
            n=r["nivel"]
            f=tk.Frame(self._res,bg=C["card"],padx=24,pady=18)
            f.pack(fill="x",padx=28,pady=8)
            tk.Label(f,text=f"{en[n]}  {tn[n]}",font=(FONT,13,"bold"),
                     bg=C["card"],fg=cn[n],wraplength=self.W_()-100,justify="left").pack(anchor="w")
            tk.Label(f,text=f"Pontuação de risco: {r['score']} pontos",
                     font=(FONT,10),bg=C["card"],fg=C["text2"]).pack(anchor="w",pady=(8,0))
            if r["motivos"]:
                self.sep(f,py=6)
                tk.Label(f,text="Indicadores detectados:",font=(FONT,10,"bold"),
                         bg=C["card"],fg=C["text"]).pack(anchor="w",pady=(0,4))
                for m in r["motivos"]:
                    tk.Label(f,text=f"  • {m}",font=(FONT,9),
                             bg=C["card"],fg=C["text2"],anchor="w").pack(fill="x")
            nivel=n
        elif tipo=="cpf":
            r=validar_cpf(val); ok=r["valido"]
            self.resultado_box(self._res,ok,r["msg"]); nivel="baixo" if ok else "alto"
        elif tipo=="tel":
            r=validar_telefone(val); ok=r["valido"]
            self.resultado_box(self._res,ok,r["msg"]); nivel="baixo" if ok else "alto"
        elif tipo=="email":
            r=validar_email(val); ok=r["valido"]
            self.resultado_box(self._res,ok,r["msg"]); nivel="baixo" if ok else "alto"
        elif tipo=="url":
            r=analisar_url(val); ok=r["segura"]
            self.resultado_box(self._res,ok,r["msg"]); nivel="baixo" if ok else "alto"

        # Checar conquistas de verificação
        self.dados,novas=checar_conquistas(self.dados)
        if novas:
            for c in novas:
                nf=tk.Frame(self._res,bg="#1e1a06",padx=16,pady=10)
                nf.pack(fill="x",padx=28,pady=4)
                tk.Label(nf,text=f"🏅  Conquista desbloqueada: {c['emoji']} {c['nome']}",
                         font=(FONT,10,"bold"),bg="#1e1a06",fg=C["gold"]).pack(anchor="w")

        self.dados["historico"].append({
            "tipo":tipo,"nivel":nivel,
            "conteudo":val[:80]+("..." if len(val)>80 else ""),
            "data":datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        if len(self.dados["historico"])>100:
            self.dados["historico"]=self.dados["historico"][-100:]
        salvar(self.dados)

    # ══════════════════════════════════════════
    # CONQUISTAS
    # ══════════════════════════════════════════
    def tela_conquistas(self):
        self.limpar()
        ganhas=self.dados["conquistas"]
        self.topbar(self.root,f"🏅  Conquistas  ·  {len(ganhas)} de {len(CONQUISTAS)} desbloqueadas",self.tela_inicio)

        # Resumo por categoria
        cats={}
        for c in CONQUISTAS:
            cat=c["cat"]; cats.setdefault(cat,{"total":0,"ganhas":0})
            cats[cat]["total"]+=1
            if c["id"] in ganhas: cats[cat]["ganhas"]+=1

        catbar=tk.Frame(self.root,bg=C["bg"]); catbar.pack(fill="x",padx=28,pady=(10,4))
        for cat,(dados) in cats.items():
            cf=tk.Frame(catbar,bg=C["card"],padx=14,pady=8)
            cf.pack(side="left",padx=5)
            tk.Label(cf,text=cat,font=(FONT,9,"bold"),bg=C["card"],fg=C["text2"]).pack()
            cor=C["gold"] if dados["ganhas"]==dados["total"] else C["text"]
            tk.Label(cf,text=f"{dados['ganhas']}/{dados['total']}",
                     font=(FONT,12,"bold"),bg=C["card"],fg=cor).pack()

        self.sep(self.root,px=28,py=8)
        scr=tk.Frame(self.root,bg=C["bg"]); scr.pack(fill="both",expand=True)
        frame=self.mk_scroll(scr)

        # Agrupar por categoria
        cat_atual=None
        for c in CONQUISTAS:
            if c["cat"]!=cat_atual:
                cat_atual=c["cat"]
                tk.Label(frame,text=f"  {cat_atual}",font=(FONT,10,"bold"),
                         bg=C["bg"],fg=C["text2"]).pack(anchor="w",padx=28,pady=(14,4))

            earned=c["id"] in ganhas
            bg_c=C["card"] if earned else C["locked"]
            cf=tk.Frame(frame,bg=bg_c,padx=18,pady=12)
            cf.pack(fill="x",padx=28,pady=3)
            row=tk.Frame(cf,bg=bg_c); row.pack(fill="x")

            emo_show=c["emoji"] if earned else "🔒"
            if c["cat"]=="Secreta" and not earned: emo_show="❓"
            tk.Label(row,text=emo_show,font=(FONT,22),bg=bg_c).pack(side="left",padx=(0,14))

            info=tk.Frame(row,bg=bg_c); info.pack(side="left",fill="x",expand=True)
            nome_show=c["nome"] if (earned or c["cat"]!="Secreta") else "???"
            desc_show=c["desc"] if (earned or c["cat"]!="Secreta") else "Conquista secreta — continue explorando!"
            tk.Label(info,text=nome_show,font=(FONT,11,"bold"),bg=bg_c,
                     fg=C["gold"] if earned else C["text3"]).pack(anchor="w")
            tk.Label(info,text=desc_show,font=(FONT,9),bg=bg_c,fg=C["text2"],
                     wraplength=self.W_()-200,justify="left").pack(anchor="w")

            if earned:
                tk.Label(row,text="✓",font=(FONT,18,"bold"),
                         bg=bg_c,fg=C["success"]).pack(side="right",padx=8)

        tk.Frame(frame,bg=C["bg"],height=30).pack()

    # ══════════════════════════════════════════
    # HISTÓRICO
    # ══════════════════════════════════════════
    def tela_historico(self):
        self.limpar()
        hist=self.dados.get("historico",[])
        self.topbar(self.root,f"📖  Histórico  ·  {len(hist)} verificações realizadas",self.tela_inicio)

        def apagar_historico():
            if messagebox.askyesno("Apagar histórico","Tem certeza que deseja apagar todo o histórico? Esta ação não pode ser desfeita."):
                self.dados["historico"]=[]
                salvar(self.dados)
                self.tela_historico()

        if hist:
            self.btn(self.root,"🗑️  Apagar histórico",apagar_historico,
                     bg=C["danger"],sz=9,pad=6).pack(anchor="e",padx=28,pady=(6,0))

        if not hist:
            tk.Label(self.root,
                     text="Nenhuma verificação ainda.\nUse as ferramentas do menu para começar!",
                     font=(FONT,12),bg=C["bg"],fg=C["text2"],justify="center").pack(pady=60)
            return

        # Mini stats
        altos=sum(1 for h in hist if h.get("nivel")=="alto")
        medios=sum(1 for h in hist if h.get("nivel")=="medio")
        baixos=sum(1 for h in hist if h.get("nivel")=="baixo")

        sb=tk.Frame(self.root,bg=C["bg"]); sb.pack(fill="x",padx=28,pady=(10,4))
        for lbl,val,cor in [("🚨 Alto risco",str(altos),C["danger"]),
                             ("⚠️ Atenção",str(medios),C["warning"]),
                             ("✅ Seguros",str(baixos),C["success"])]:
            f=tk.Frame(sb,bg=C["card"],padx=16,pady=8); f.pack(side="left",padx=5)
            tk.Label(f,text=lbl,font=(FONT,8),bg=C["card"],fg=C["text2"]).pack()
            tk.Label(f,text=val,font=(FONT,14,"bold"),bg=C["card"],fg=cor).pack()

        self.sep(self.root,px=28,py=6)
        scr=tk.Frame(self.root,bg=C["bg"]); scr.pack(fill="both",expand=True)
        frame=self.mk_scroll(scr)

        icones={"alto":"🚨","medio":"⚠️","baixo":"✅"}
        cores={"alto":C["danger"],"medio":C["warning"],"baixo":C["success"]}
        tipos={"msg":"Mensagem","cpf":"CPF","tel":"Telefone","email":"E-mail","url":"URL"}

        for item in reversed(hist[-60:]):
            n=item.get("nivel","baixo")
            cf=tk.Frame(frame,bg=C["card"],padx=18,pady=12)
            cf.pack(fill="x",padx=28,pady=3)
            row=tk.Frame(cf,bg=C["card"]); row.pack(fill="x")
            tk.Label(row,text=icones.get(n,"❓"),font=(FONT,16),bg=C["card"]).pack(side="left",padx=(0,12))
            info=tk.Frame(row,bg=C["card"]); info.pack(side="left",fill="x",expand=True)
            tk.Label(info,text=item.get("conteudo",""),font=(FONT,10),
                     bg=C["card"],fg=C["text"],anchor="w",
                     wraplength=self.W_()-180,justify="left").pack(fill="x")
            tk.Label(info,text=f"{tipos.get(item.get('tipo',''),'?')}  ·  {item.get('data','')}",
                     font=(FONT,8),bg=C["card"],fg=C["text2"]).pack(anchor="w")
            tk.Label(row,text=n.upper(),font=(FONT,9,"bold"),
                     bg=C["card"],fg=cores.get(n,C["text2"])).pack(side="right")

        tk.Frame(frame,bg=C["bg"],height=30).pack()

# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════
if __name__=="__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()