"""
Veteran Shield - Escudo do Guerreiro
Sistema Avançado de Proteção contra Golpes para Veteranos
Versão 2.0 - Completa com análise avançada, persistência e múltiplos tipos de verificação
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import re

# ==============================
# CONFIGURAÇÕES E CONSTANTES
# ==============================

ARQUIVO_DADOS = "veteran_shield_dados.json"

# Cores do tema
CORES_ESCURO = {
    "fundo": "#1a1a2e",
    "fundo_card": "#16213e",
    "primaria": "#0f3460",
    "destaque": "#e94560",
    "sucesso": "#00d9a5",
    "alerta": "#ffc107",
    "perigo": "#ff4757",
    "texto": "#ffffff",
    "texto_sec": "#a0a0a0"
}

CORES_CLARO = {
    "fundo": "#f5f5f5",
    "fundo_card": "#ffffff",
    "primaria": "#2196F3",
    "destaque": "#e94560",
    "sucesso": "#4CAF50",
    "alerta": "#ff9800",
    "perigo": "#f44336",
    "texto": "#212121",
    "texto_sec": "#757575"
}

# Tema atual (padrão: escuro)
CORES = CORES_ESCURO.copy()

# ==============================
# BANCO DE DADOS DE PALAVRAS
# ==============================

palavras_suspeitas = {
    # Alto risco (3 pontos)
    "envie seus dados": 3,
    "clique aqui": 3,
    "confirme sua senha": 3,
    "atualize seus dados": 3,
    "seu banco": 3,
    "sua conta foi": 3,
    "código de verificação": 3,
    "senha expira": 3,
    
    # Médio risco (2 pontos)
    "ganhou": 2,
    "prêmio": 2,
    "urgente": 2,
    "bloqueada": 2,
    "pix": 2,
    "transferência": 2,
    "conta": 2,
    "cartão": 2,
    "limite": 2,
    "divida": 2,
    "cpf": 2,
    "rg": 2,
    
    # Baixo risco (1 ponto)
    "link": 1,
    "promoção": 1,
    "oferta": 1,
    "desconto": 1,
    "grátis": 1,
    "whatsapp": 1,
    "telegram": 1,
    "mensagem": 1
}

# Padrões regex para validação
PADROES = {
    "cpf": r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}',
    "telefone": r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}',
    "url": r'https?://[^\s]+',
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    "cpf_suspeito": r'\d{3}\.\d{3}\.\d{3}-\d{2}'
}

# ==============================
# SISTEMA DE PERSISTÊNCIA
# ==============================

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"historico": [], "configuracoes": {}}
    return {"historico": [], "configuracoes": {}}

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ==============================
# ANÁLISE AVANÇADA DE MENSAGEM
# ==============================

def analisar_mensagem(msg):
    """
    Analisa mensagem e retorna dicionário com detalhes
    """
    if not msg or len(msg.strip()) == 0:
        return {
            "nivel": "baixo",
            "score": 0,
            "motivos": [],
            "recomendacao": "Digite uma mensagem para analisar."
        }
    
    score = 0
    motivos = []
    msg_lower = msg.lower()
    
    # Verificar palavras suspeitas
    for palavra, peso in palavras_suspeitas.items():
        if palavra in msg_lower:
            score += peso
            motivos.append(f"Palavra suspeita: '{palavra}' (+{peso})")
    
    # Verificar padrões suspeitos
    if re.search(PADROES["url"], msg):
        score += 2
        motivos.append("Contém URL可疑 (link desconhecido)")
    
    if re.search(PADROES["cpf"], msg):
        score += 1
        motivos.append("Contém CPF (dado pessoal)")
    
    # Verificar caracteres suspeitos
    if "R$" in msg or "reais" in msg_lower:
        score += 1
        motivos.append("Menção a valores financeiros")
    
    # Verificar urgência (common scam tactic)
    if any(palavra in msg_lower for palavra in ["urgente", "immediate", "agora", "hoje"]):
        score += 1
        motivos.append("Linguagem de urgência")
    
    # Verificar promessas muito boas
    if any(palavra in msg_lower for palavra in ["ganhou", "prêmio", "grátis", "sorte"]):
        score += 1
        motivos.append("Promessa de benefício fácil")
    
    # Determinar nível
    if score >= 5:
        nivel = "alto"
    elif score >= 2:
        nivel = "medio"
    else:
        nivel = "baixo"
    
    # Gerar recomendação
    recomendacoes = {
        "alto": "⚠️ NÃO clique em nenhum link! Delete esta mensagem imediatamente.",
        "medio": "⚠️ Cuidado: Esta mensagem tem elementos suspeitos.",
        "baixo": "✅ Esta mensagem parece não ter indicadores óbvios de golpe."
    }
    
    return {
        "nivel": nivel,
        "score": score,
        "motivos": motivos,
        "recomendacao": recomendacoes[nivel]
    }

def validar_cpf(cpf):
    """Valida CPF com algoritmo oficial"""
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11:
        return {"valido": False, "motivo": "CPF deve ter 11 dígitos"}
    
    if cpf == cpf[0] * 11:
        return {"valido": False, "motivo": "CPF inválido (dígitos repetidos)"}
    
    # Validação primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        return {"valido": False, "motivo": "CPF inválido (dígito verificador incorreto)"}
    
    # Validação segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf[10]):
        return {"valido": False, "motivo": "CPF inválido (dígito verificador incorreto)"}
    
    return {"valido": True, "motivo": "CPF válido"}

def validar_telefone(telefone):
    """Valida formato de telefone brasileiro"""
    telefone = re.sub(r'\D', '', telefone)
    
    if len(telefone) == 10:  # Fixo
        return {"valido": True, "tipo": "Telefone fixo", "formatado": f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"}
    elif len(telefone) == 11:  # Celular
        return {"valido": True, "tipo": "Celular", "formatado": f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"}
    else:
        return {"valido": False, "motivo": "Telefone deve ter 10 ou 11 dígitos"}

def analisar_url(url):
    """Analisa URL para verificar segurança"""
    dominios_suspeitos = [
        "bit.ly", "goo.gl", "tinyurl", "t.co",
        "banco-do-brasil", "itau.com.br.fake", "bradesco.fake"
    ]
    
    url_lower = url.lower()
    
    # Verificar domínios curtos (often used in scams)
    if any(d in url_lower for d in dominios_suspeitos):
        return {
            "segura": False,
            "motivo": "URL com domínio缩短 ou suspeito"
        }
    
    # Verificar HTTPS
    if not url.startswith("https"):
        return {
            "segura": False,
            "motivo": "URL não possui HTTPS (não segura)"
        }
    
    return {
        "segura": True,
        "motivo": "URL parece ter formato básico seguro"
    }

# ==============================
# ASSISTENTE INTELIGENTE
# ==============================

def responder_pergunta(pergunta):
    """Responde perguntas do usuário com base de conhecimento"""
    pergunta = pergunta.lower()
    
    categorias = {
        "seguranca": {
            "palavras": ["golpe", "seguro", "link", "hacker", "fraude", "perigo", "phishing", "malware"],
            "resposta": "🛡️ Dicas de Segurança:\n\n"
                       "• Nunca clique em links desconhecidos\n"
                       "• Bancos NUNCA pedem senha por mensagem\n"
                       "• Desconfie de mensagens urgentes\n"
                       "• Ofertas boas demais são golpe\n"
                       "• Nunca compartilhe dados pessoais"
        },
        "banco": {
            "palavras": ["banco", "pix", "conta", "senha", "cartão", "transferência", "transferir"],
            "resposta": "🏦 Informações Bancárias:\n\n"
                       "• Use apenas apps oficiais do banco\n"
                       "• Nunca compartilhe sua senha\n"
                       "• Códigos de verificação são pessoais\n"
                       "• O banco nunca pede dados por mensagem\n"
                       "• Pix é seguro, mas verifique o destinatário"
        },
        "uso": {
            "palavras": ["como", "usar", "ajuda", "mexer", "funciona", "início"],
            "resposta": "📖 Como Usar o Sistema:\n\n"
                       "• Menu Aprender: Dicas de segurança\n"
                       "• Verificar: Analisa mensagens suspeita\n"
                       "• Assistente: Responde suas dúvidas\n"
                       "• Histórico: Verifica mensagens salvas\n"
                       "• Configurações: Personalize o app"
        },
        "tipos": {
            "palavras": ["verificar", "tipos", "cpf", "telefone", "url", "link"],
            "resposta": "🔍 Tipos de Verificação:\n\n"
                       "• Texto: Analisa palavras suspeitas\n"
                       "• CPF: Valida CPF brasileiro\n"
                       "• Telefone: Formata e valida telefone\n"
                       "• URL: Verifica segurança de links"
        }
    }

    for categoria, dados in categorias.items():
        for palavra in dados["palavras"]:
            if palavra in pergunta:
                return dados["resposta"]

    return "❓ Não entendi sua dúvida.\n\n" \
           "Tente perguntar sobre:\n" \
           "• Segurança (golpes, links)\n" \
           "• Banco (pix, senha, conta)\n" \
           "• Como usar o sistema\n" \
           "• Tipos de verificação"

# ==============================
# INTERFACE GRÁFICA
# ==============================

class Aplicativo:
    def __init__(self, root):
        self.root = root
        self.dados = carregar_dados()
        self.historico = self.dados.get("historico", [])
        
        self.configurar_janela()
        self.criar_estilos()
        self.tela_menu()
    
    def configurar_janela(self):
        """Configurações iniciais da janela"""
        self.root.title("Veteran Shield - Proteção Total")
        self.root.geometry("450x650")
        self.root.configure(bg=CORES["fundo"])
        self.root.resizable(True, True)
        
        # Variável para controlar fullscreen
        self.fullscreen = False
        
        # Bind da tecla F11 para fullscreen
        self.root.bind("<F11>", self._alternar_fullscreen)
        self.root.bind("<Escape>", self._sair_fullscreen)
    
    def _alternar_fullscreen(self, event=None):
        """Alterna entre modo fullscreen e normal"""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def _sair_fullscreen(self, event=None):
        """Sai do modo fullscreen"""
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)
    
    def criar_estilos(self):
        """Cria estilos personalizados para widgets"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Estilo para botões
        self.style.configure(
            "Botao.TButton",
            padding=10,
            font=("Arial", 11, "bold")
        )
        
        # Estilo para labels
        self.style.configure(
            "Titulo.TLabel",
            font=("Arial", 16, "bold"),
            background=CORES["fundo"],
            foreground=CORES["texto"]
        )
    
    def limpar_tela(self):
        """Remove todos os widgets da tela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def criar_cabecalho(self, titulo, subtitulo=None):
        """Cria cabeçalho padronizado"""
        frame = tk.Frame(self.root, bg=CORES["fundo"])
        frame.pack(fill="x", pady=(0, 10))
        
        # Título principal
        label_titulo = tk.Label(
            frame, text=titulo,
            font=("Arial", 18, "bold"),
            bg=CORES["fundo"], fg=CORES["destaque"]
        )
        label_titulo.pack(pady=(15, 5))
        
        # Subtítulo
        if subtitulo:
            label_sub = tk.Label(
                frame, text=subtitulo,
                font=("Arial", 10),
                bg=CORES["fundo"], fg=CORES["texto_sec"]
            )
            label_sub.pack()
    
    def criar_botao(self, texto, comando, cor=CORES["primaria"]):
        """Cria botão estilizado"""
        btn = tk.Button(
            self.root, text=texto,
            command=comando,
            font=("Arial", 11, "bold"),
            bg=cor, fg=CORES["texto"],
            activebackground=CORES["destaque"],
            activeforeground=CORES["texto"],
            relief="flat", bd=0,
            cursor="hand2",
            width=25, height=2
        )
        return btn
    
    def criar_card(self, conteudo, cor_fundo=CORES["fundo_card"]):
        """Cria card com informações"""
        card = tk.Frame(
            self.root,
            bg=cor_fundo,
            relief="flat",
            bd=0
        )
        card.pack(fill="x", padx=20, pady=5)
        
        label = tk.Label(
            card, text=conteudo,
            font=("Arial", 10),
            bg=cor_fundo, fg=CORES["texto"],
            justify="left", wraplength=380
        )
        label.pack(padx=10, pady=10)
        
        return card
    
    # ==============================
    # TELAS DO APLICATIVO
    # ==============================
    
    def tela_menu(self):
        """Tela principal do menu"""
        self.limpar_tela()
        
        # Logo/Título
        titulo = tk.Label(
            self.root, text="🛡️",
            font=("Arial", 40),
            bg=CORES["fundo"], fg=CORES["destaque"]
        )
        titulo.pack(pady=(20, 0))
        
        tk.Label(
            self.root, text="Veteran Shield",
            font=("Arial", 20, "bold"),
            bg=CORES["fundo"], fg=CORES["texto"]
        ).pack()
        
        tk.Label(
            self.root, text="Seu escudo contra golpes",
            font=("Arial", 10),
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        ).pack(pady=(0, 20))
        
        # Menu de opções
        botoes = [
            ("📚 Aprender", self.tela_aprender, CORES["primaria"]),
            ("🔍 Verificar Mensagem", self.tela_verificar_tipo, CORES["primaria"]),
            ("💬 Assistente Virtual", self.tela_assistente, CORES["primaria"]),
            ("📋 Histórico", self.tela_historico, CORES["primaria"]),
            ("⚙️ Configurações", self.tela_configuracoes, CORES["primaria"]),
        ]
        
        for texto, comando, cor in botoes:
            btn = self.criar_botao(texto, comando, cor)
            btn.pack(pady=5)
        
        # Rodapé
        tk.Label(
            self.root, text=f"Total verificado: {len(self.historico)} mensagens",
            font=("Arial", 8),
            bg=CORES["fundo"], fg=CORES["texto_sec"]
        ).pack(side="bottom", pady=10)
    
    def tela_aprender(self):
        """Tela de aprendizado com dicas de segurança"""
        self.limpar_tela()
        self.criar_cabecalho("📚 Dicas de Segurança", "Aprenda a se proteger")
        
        # Criar canvas com scroll
        canvas = tk.Canvas(self.root, bg=CORES["fundo"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame_scroll = tk.Frame(canvas, bg=CORES["fundo"])
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        dicas = [
            ("🔗 Links Desconhecidos", "Nunca clique em links de mensagens não solicitadas"),
            ("🏦 Dados Bancários", "Bancos nunca pedem senha ou dados por mensagem"),
            ("⏰ Urgência Falsa", "Golpes usam urgência para você agir sem pensar"),
            ("🎁 Ofertas Boas Demais", "Se parece bom demais, provavelmente é golpe"),
            ("📱 Apps Oficiais", "Sempre use aplicativos oficiais dos bancos"),
            ("🔐 Senhas Pessoais", "Nunca compartilhe suas senhas com ninguém"),
            ("📞 Verificação", "Se receber ligação suspeita, desligue e ligue no banco"),
            ("💰 Pix Seguro", "Verifique sempre o beneficiário antes de transferir")
        ]
        
        for icone_titulo, descricao in dicas:
            self.criar_card_em_frame(frame_scroll, f"{icone_titulo}\n{descricao}")
        
        # Botão voltar (dentro do frame scrollável)
        btn_voltar = self.criar_botao_em_frame(frame_scroll, "← Voltar", self.tela_menu, CORES["primaria"])
        btn_voltar.pack(pady=15)
    
    def criar_card_em_frame(self, frame, conteudo, cor_fundo=None):
        """Cria card dentro de um frame específico"""
        if cor_fundo is None:
            cor_fundo = CORES["fundo_card"]
        
        card = tk.Frame(frame, bg=cor_fundo, relief="flat", bd=0)
        card.pack(fill="x", padx=20, pady=5)
        
        label = tk.Label(card, text=conteudo, font=("Arial", 10), bg=cor_fundo, fg=CORES["texto"], justify="left", wraplength=380)
        label.pack(padx=10, pady=10)
        
        return card
    
    def criar_botao_em_frame(self, frame, texto, comando, cor=None):
        """Cria botão dentro de um frame específico"""
        if cor is None:
            cor = CORES["primaria"]
        
        btn = tk.Button(frame, text=texto, command=comando, font=("Arial", 11, "bold"), bg=cor, fg=CORES["texto"], activebackground=CORES["destaque"], activeforeground=CORES["texto"], relief="flat", bd=0, cursor="hand2", width=25, height=2)
        return btn
    
    def tela_verificar_tipo(self):
        """Tela de seleção do tipo de verificação"""
        self.limpar_tela()
        self.criar_cabecalho("🔍 Verificação", "Escolha o tipo de verificação")
        
        # Botões de verificação
        btn_texto = self.criar_botao("📝 Verificar Texto/Mensagem", self.tela_verificar, CORES["primaria"])
        btn_texto.pack(pady=5)
        
        btn_url = self.criar_botao("🔗 Verificar URL/Link", self.tela_verificar_url, CORES["primaria"])
        btn_url.pack(pady=5)
        
        btn_cpf = self.criar_botao("📋 Validar CPF", self.tela_verificar_cpf, CORES["primaria"])
        btn_cpf.pack(pady=5)
        
        btn_tel = self.criar_botao("📱 Validar Telefone", self.tela_verificar_telefone, CORES["primaria"])
        btn_tel.pack(pady=5)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_menu, CORES["primaria"])
        btn_voltar.pack(pady=20)
    
    def tela_verificar(self):
        """Tela de verificação de mensagens de texto"""
        self.limpar_tela()
        self.criar_cabecalho("🔍 Verificar Mensagem", "Digite a mensagem para analisar")
        
        # Campo de entrada
        entrada_frame = tk.Frame(self.root, bg=CORES["fundo"])
        entrada_frame.pack(fill="x", padx=20, pady=10)
        
        self.entrada_msg = tk.Entry(
            entrada_frame,
            font=("Arial", 12),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            relief="flat",
            width=35
        )
        self.entrada_msg.pack(pady=5)
        
        # Botão verificar
        btn_verificar = self.criar_botao("🔍 Analisar Mensagem", self._executar_verificacao, CORES["sucesso"])
        btn_verificar.pack(pady=10)
        
        # Área de resultado
        self.frame_resultado = tk.Frame(self.root, bg=CORES["fundo"])
        self.frame_resultado.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_verificar_tipo, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _executar_verificacao(self):
        """Executa a verificação da mensagem"""
        # Verificar se o campo de entrada existe
        if not hasattr(self, 'entrada_msg') or self.entrada_msg is None:
            messagebox.showerror("Erro", "Campo de entrada não encontrado. Tente novamente.")
            self.tela_verificar()
            return
        
        msg = self.entrada_msg.get()
        
        if not msg.strip():
            messagebox.showwarning("Aviso", "Digite uma mensagem para analisar!")
            return
        
        resultado = analisar_mensagem(msg)
        
        # Cores por nível
        cores_nivel = {
            "alto": CORES["perigo"],
            "medio": CORES["alerta"],
            "baixo": CORES["sucesso"]
        }
        
        icones_nivel = {
            "alto": "🚨",
            "medio": "⚠️",
            "baixo": "✅"
        }
        
        # Limpar resultado anterior
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()
        
        # Mostrar resultado
        frame_resultado = tk.Frame(
            self.frame_resultado,
            bg=CORES["fundo_card"],
            relief="flat"
        )
        frame_resultado.pack(fill="both", expand=True)
        
        # Nível
        tk.Label(
            frame_resultado,
            text=f"{icones_nivel[resultado['nivel']]} NÍVEL: {resultado['nivel'].upper()}",
            font=("Arial", 14, "bold"),
            bg=CORES["fundo_card"],
            fg=cores_nivel[resultado["nivel"]]
        ).pack(pady=10)
        
        # Score
        tk.Label(
            frame_resultado,
            text=f"Score de risco: {resultado['score']} pontos",
            font=("Arial", 11),
            bg=CORES["fundo_card"],
            fg=CORES["texto"]
        ).pack()
        
        # Motivos
        if resultado["motivos"]:
            tk.Label(
                frame_resultado,
                text="Motivos encontrados:",
                font=("Arial", 10, "bold"),
                bg=CORES["fundo_card"],
                fg=CORES["texto_sec"]
            ).pack(pady=(10, 5))
            
            for motivo in resultado["motivos"]:
                tk.Label(
                    frame_resultado,
                    text=f"• {motivo}",
                    font=("Arial", 9),
                    bg=CORES["fundo_card"],
                    fg=CORES["texto_sec"]
                ).pack(anchor="w", padx=20)
        
        # Recomendação
        tk.Label(
            frame_resultado,
            text=resultado["recomendacao"],
            font=("Arial", 10, "bold"),
            bg=CORES["fundo_card"],
            fg=cores_nivel[resultado["nivel"]],
            wraplength=350
        ).pack(pady=10)
        
        # Salvar no histórico
        self.historico.append({
            "tipo": "mensagem",
            "conteudo": msg[:50] + "..." if len(msg) > 50 else msg,
            "nivel": resultado["nivel"],
            "score": resultado["score"],
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        
        # Limitar histórico a 50 itens
        if len(self.historico) > 50:
            self.historico = self.historico[-50:]
        
        # Salvar dados
        self.dados["historico"] = self.historico
        salvar_dados(self.dados)
    
    def tela_verificar_url(self):
        """Tela de verificação de URL"""
        self.limpar_tela()
        self.criar_cabecalho("🔗 Verificar URL", "Cole o link para analisar")
        
        entrada_frame = tk.Frame(self.root, bg=CORES["fundo"])
        entrada_frame.pack(fill="x", padx=20, pady=10)
        
        self.entrada_url = tk.Entry(
            entrada_frame,
            font=("Arial", 12),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            relief="flat",
            width=35
        )
        self.entrada_url.pack(pady=5)
        
        btn_verificar = self.criar_botao("🔍 Analisar URL", self._executar_verificacao_url, CORES["sucesso"])
        btn_verificar.pack(pady=10)
        
        self.frame_resultado_url = tk.Frame(self.root, bg=CORES["fundo"])
        self.frame_resultado_url.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_verificar_tipo, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _executar_verificacao_url(self):
        """Executa verificação de URL"""
        url = self.entrada_url.get()
        
        if not url.strip():
            messagebox.showwarning("Aviso", "Digite uma URL para analisar!")
            return
        
        resultado = analisar_url(url)
        
        for widget in self.frame_resultado_url.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.frame_resultado_url, bg=CORES["fundo_card"], relief="flat")
        frame.pack(fill="both", expand=True)
        
        if resultado["segura"]:
            icone = "✅"
            cor = CORES["sucesso"]
        else:
            icone = "🚨"
            cor = CORES["perigo"]
        
        tk.Label(
            frame,
            text=f"{icone} {resultado['motivo']}",
            font=("Arial", 12, "bold"),
            bg=CORES["fundo_card"],
            fg=cor,
            wraplength=350
        ).pack(pady=20)
        
        # Salvar
        self.historico.append({
            "tipo": "url",
            "conteudo": url[:50] + "..." if len(url) > 50 else url,
            "nivel": "baixo" if resultado["segura"] else "alto",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        
        self.dados["historico"] = self.historico
        salvar_dados(self.dados)
    
    def tela_verificar_cpf(self):
        """Tela de validação de CPF"""
        self.limpar_tela()
        self.criar_cabecalho("📋 Validar CPF", "Digite o CPF para validar")
        
        entrada_frame = tk.Frame(self.root, bg=CORES["fundo"])
        entrada_frame.pack(fill="x", padx=20, pady=10)
        
        self.entrada_cpf = tk.Entry(
            entrada_frame,
            font=("Arial", 12),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            relief="flat",
            width=35
        )
        self.entrada_cpf.pack(pady=5)
        
        tk.Label(
            self.root,
            text="Formato: 000.000.000-00",
            font=("Arial", 9),
            bg=CORES["fundo"],
            fg=CORES["texto_sec"]
        ).pack()
        
        btn_verificar = self.criar_botao("🔍 Validar CPF", self._executar_verificacao_cpf, CORES["sucesso"])
        btn_verificar.pack(pady=10)
        
        self.frame_resultado_cpf = tk.Frame(self.root, bg=CORES["fundo"])
        self.frame_resultado_cpf.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_verificar_tipo, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _executar_verificacao_cpf(self):
        """Executa validação de CPF"""
        cpf = self.entrada_cpf.get()
        
        if not cpf.strip():
            messagebox.showwarning("Aviso", "Digite um CPF para validar!")
            return
        
        resultado = validar_cpf(cpf)
        
        for widget in self.frame_resultado_cpf.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.frame_resultado_cpf, bg=CORES["fundo_card"], relief="flat")
        frame.pack(fill="both", expand=True)
        
        if resultado["valido"]:
            icone = "✅"
            cor = CORES["sucesso"]
            texto = "CPF VÁLIDO!"
        else:
            icone = "🚨"
            cor = CORES["perigo"]
            texto = f"CPF INVÁLIDO\n{resultado['motivo']}"
        
        tk.Label(
            frame,
            text=f"{icone} {texto}",
            font=("Arial", 14, "bold"),
            bg=CORES["fundo_card"],
            fg=cor,
            wraplength=350
        ).pack(pady=20)
        
        # Salvar
        self.historico.append({
            "tipo": "cpf",
            "conteudo": cpf,
            "nivel": "baixo" if resultado["valido"] else "alto",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        
        self.dados["historico"] = self.historico
        salvar_dados(self.dados)
    
    def tela_verificar_telefone(self):
        """Tela de validação de telefone"""
        self.limpar_tela()
        self.criar_cabecalho("📱 Validar Telefone", "Digite o telefone para validar")
        
        entrada_frame = tk.Frame(self.root, bg=CORES["fundo"])
        entrada_frame.pack(fill="x", padx=20, pady=10)
        
        self.entrada_tel = tk.Entry(
            entrada_frame,
            font=("Arial", 12),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            relief="flat",
            width=35
        )
        self.entrada_tel.pack(pady=5)
        
        tk.Label(
            self.root,
            text="Formato: (00) 00000-0000",
            font=("Arial", 9),
            bg=CORES["fundo"],
            fg=CORES["texto_sec"]
        ).pack()
        
        btn_verificar = self.criar_botao("🔍 Validar Telefone", self._executar_verificacao_telefone, CORES["sucesso"])
        btn_verificar.pack(pady=10)
        
        self.frame_resultado_tel = tk.Frame(self.root, bg=CORES["fundo"])
        self.frame_resultado_tel.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_verificar_tipo, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _executar_verificacao_telefone(self):
        """Executa validação de telefone"""
        telefone = self.entrada_tel.get()
        
        if not telefone.strip():
            messagebox.showwarning("Aviso", "Digite um telefone para validar!")
            return
        
        resultado = validar_telefone(telefone)
        
        for widget in self.frame_resultado_tel.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.frame_resultado_tel, bg=CORES["fundo_card"], relief="flat")
        frame.pack(fill="both", expand=True)
        
        if resultado["valido"]:
            icone = "✅"
            cor = CORES["sucesso"]
            texto = f"TELEFONE VÁLIDO\nTipo: {resultado['tipo']}\nFormatado: {resultado['formatado']}"
        else:
            icone = "🚨"
            cor = CORES["perigo"]
            texto = f"TELEFONE INVÁLIDO\n{resultado['motivo']}"
        
        tk.Label(
            frame,
            text=f"{icone} {texto}",
            font=("Arial", 12, "bold"),
            bg=CORES["fundo_card"],
            fg=cor,
            wraplength=350
        ).pack(pady=20)
        
        # Salvar
        self.historico.append({
            "tipo": "telefone",
            "conteudo": telefone,
            "nivel": "baixo" if resultado["valido"] else "alto",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        
        self.dados["historico"] = self.historico
        salvar_dados(self.dados)
    
    def tela_assistente(self):
        """Tela do assistente virtual"""
        self.limpar_tela()
        self.criar_cabecalho("💬 Assistente Virtual", "Faça sua pergunta")
        
        # Campo de entrada
        entrada_frame = tk.Frame(self.root, bg=CORES["fundo"])
        entrada_frame.pack(fill="x", padx=20, pady=10)
        
        self.entrada_pergunta = tk.Entry(
            entrada_frame,
            font=("Arial", 12),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            relief="flat",
            width=35
        )
        self.entrada_pergunta.pack(pady=5)
        
        # Bind Enter key
        self.entrada_pergunta.bind("<Return>", lambda e: self._responder_pergunta())
        
        btn_perguntar = self.criar_botao("💬 Perguntar", self._responder_pergunta, CORES["sucesso"])
        btn_perguntar.pack(pady=10)
        
        # Área de resposta
        self.frame_resposta = tk.Frame(self.root, bg=CORES["fundo"])
        self.frame_resposta.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_menu, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _responder_pergunta(self):
        """Responde a pergunta do assistente"""
        pergunta = self.entrada_pergunta.get()
        
        if not pergunta.strip():
            messagebox.showwarning("Aviso", "Digite uma pergunta!")
            return
        
        resposta = responder_pergunta(pergunta)
        
        # Limpar resposta anterior
        for widget in self.frame_resposta.winfo_children():
            widget.destroy()
        
        # Mostrar resposta
        frame = tk.Frame(self.frame_resposta, bg=CORES["fundo_card"], relief="flat")
        frame.pack(fill="both", expand=True)
        
        tk.Label(
            frame,
            text=resposta,
            font=("Arial", 10),
            bg=CORES["fundo_card"],
            fg=CORES["texto"],
            justify="left",
            wraplength=380
        ).pack(padx=10, pady=15)
        
        # Limpar campo
        self.entrada_pergunta.delete(0, "end")
    
    def tela_historico(self):
        """Tela de histórico de verificações"""
        self.limpar_tela()
        self.criar_cabecalho("📋 Histórico", "Suas verificações recentes")
        
        if not self.historico:
            self.criar_card("Nenhuma verificação ainda.\nComece a verificar mensagens!")
        else:
            # Mostrar últimos 10
            for item in reversed(self.historico[-10:]):
                icones = {"alto": "🚨", "medio": "⚠️", "baixo": "✅"}
                texto = f"{icones.get(item['nivel'], '❓')} [{item['tipo'].upper()}] {item['conteudo']}\nData: {item.get('data', 'N/A')}"
                self.criar_card(texto)
        
        # Estatísticas
        total = len(self.historico)
        altos = sum(1 for h in self.historico if h.get("nivel") == "alto")
        medios = sum(1 for h in self.historico if h.get("nivel") == "medio")
        
        stats = f"Total: {total} | 🚨 Altos: {altos} | ⚠️ Médios: {medios}"
        tk.Label(
            self.root,
            text=stats,
            font=("Arial", 9),
            bg=CORES["fundo"],
            fg=CORES["texto_sec"]
        ).pack(pady=5)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_menu, CORES["primaria"])
        btn_voltar.pack(pady=15)
    
    def tela_configuracoes(self):
        """Tela de configurações"""
        self.limpar_tela()
        self.criar_cabecalho("⚙️ Configurações", "Personalize o aplicativo")
        
        # Mostrar tema atual
        nome_tema = "Claro" if CORES == CORES_CLARO else "Escuro"
        
        # Botões de configuração
        btn_notif = self.criar_botao("🔔 Notificações: Ativadas", self._alternar_notificacoes, CORES["primaria"])
        btn_notif.pack(pady=5)
        
        btn_tema = self.criar_botao(f"🎨 Tema: {nome_tema}", self._mostrar_info_tema, CORES["primaria"])
        btn_tema.pack(pady=5)
        
        btn_sobre = self.criar_botao("ℹ️ Sobre o Aplicativo", self._mostrar_sobre, CORES["primaria"])
        btn_sobre.pack(pady=5)
        
        btn_limpar = self.criar_botao("🗑️ Limpar Histórico", self._limpar_historico, CORES["perigo"])
        btn_limpar.pack(pady=15)
        
        btn_voltar = self.criar_botao("← Voltar", self.tela_menu, CORES["primaria"])
        btn_voltar.pack(pady=10)
    
    def _alternar_notificacoes(self):
        """Alterna estado das notificações"""
        if not hasattr(self, 'notificacoes_ativadas'):
            self.notificacoes_ativadas = True
        
        self.notificacoes_ativadas = not self.notificacoes_ativadas
        estado = "Ativadas" if self.notificacoes_ativadas else "Desativadas"
        messagebox.showinfo("Notificações", f"Notificações {estado}")
        self.tela_configuracoes()
    
    def _mostrar_info_tema(self):
        """Alterna entre tema claro e escuro"""
        global CORES
        
        # Verificar tema atual
        if CORES == CORES_ESCURO:
            CORES = CORES_CLARO.copy()
            mensagem = "Tema Claro ativado!"
        else:
            CORES = CORES_ESCURO.copy()
            mensagem = "Tema Escuro ativado!"
        
        messagebox.showinfo("Tema", mensagem)
        self.tela_menu()  # Recarrega o menu com novo tema
    
    def _mostrar_sobre(self):
        """Mostra informações sobre o aplicativo"""
        sobre = """Veteran Shield v2.0

Escudo do Guerreiro - Proteção contra golpes
para veteranos e idosos.

Recursos:
• Análise de mensagens
• Validação de CPF
• Verificação de URLs
• Assistente virtual
• Tema claro/escuro

© 2026 - Proteção Total"""
        messagebox.showinfo("Sobre", sobre)
    
    def _limpar_historico(self):
        """Limpa o histórico de verificações"""
        resposta = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja limpar todo o histórico?"
        )
        
        if resposta:
            self.historico = []
            self.dados["historico"] = []
            salvar_dados(self.dados)
            messagebox.showinfo("Sucesso", "Histórico limpo com sucesso!")
            self.tela_configuracoes()


# ==============================
# INICIAR APLICATIVO
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicativo(root)
    root.mainloop()