#aqui vou demonstrar uma loja virtual simples, com uma programação e interface (o que o usuário ve) bem básica
import tkinter as tk
from tkinter import messagebox, font

# Dados dos produtos
produtos = {
    1: {"nome": "Camiseta", "preco": 30.00, "imagem": "imagens/camiseta.png"},
    2: {"nome": "Boné", "preco": 20.00, "imagem": "imagens/bone.png"},
    3: {"nome": "Tênis", "preco": 150.00, "imagem": "imagens/tenis.png"},
    4: {"nome": "Mochila", "preco": 100.00, "imagem": "imagens/mochila.png"}
}

carrinho = {}

class LojaVirtual:
    def __init__(self, root):
        self.root = root
        root.title("Loja Virtual")
        root.geometry("900x650")
        root.configure(bg="#f5f7fa")

        # Fontes
        self.fonte_titulo = font.Font(family="Segoe UI", size=22, weight="bold")
        self.fonte_produto = font.Font(family="Segoe UI", size=14)
        self.fonte_carrinho = font.Font(family="Segoe UI", size=12)
        self.fonte_botoes = font.Font(family="Segoe UI", size=11, weight="bold")

        # Título
        titulo = tk.Label(root, text="🛒 Loja Virtual", font=self.fonte_titulo, bg="#f5f7fa", fg="#333")
        titulo.pack(pady=(15, 10))

        # Container principal
        self.container = tk.Frame(root, bg="#f5f7fa")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame dos produtos — ocupa toda largura à esquerda, sem margem
        self.frame_produtos = tk.Frame(self.container, bg="#ffffff", bd=2, relief="groove")
        self.frame_produtos.pack(side="left", fill="both", expand=True, padx=0, pady=5)

        # Canvas com scrollbar para os produtos
        self.canvas = tk.Canvas(self.frame_produtos, bg="#ffffff", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_produtos, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.produtos_internos = tk.Frame(self.canvas, bg="#ffffff")
        self.produtos_internos_id = self.canvas.create_window((0, 0), window=self.produtos_internos, anchor="nw")

        self.imagens_produtos = {}

        self.mensagem = tk.Label(root, text="", bg="#f5f7fa", fg="#2e7d32", font=self.fonte_produto)
        self.mensagem.pack()

        # Criar itens produtos
        for codigo, info in produtos.items():
            self.criar_item_produto(codigo, info)

        self.produtos_internos.bind("<Configure>", self.atualizar_scrollregion)
        self.frame_produtos.bind("<Configure>", self.ajustar_largura_produtos)

        # Frame do carrinho — largura fixa, lado direito
        self.frame_carrinho = tk.Frame(self.container, bg="#ffffff", bd=2, relief="groove", width=320)
        self.frame_carrinho.pack(side="right", fill="y", pady=5)

        carrinho_label = tk.Label(self.frame_carrinho, text="🧾 Seu Carrinho", font=self.fonte_produto, bg="#ffffff", fg="#333")
        carrinho_label.pack(pady=(10, 5))

        self.frame_texto_carrinho = tk.Frame(self.frame_carrinho, bg="#fafafa", bd=1, relief="sunken")
        self.frame_texto_carrinho.pack(fill="both", expand=True, padx=10, pady=(0,10))

        self.scroll_carrinho = tk.Scrollbar(self.frame_texto_carrinho, orient="vertical")
        self.scroll_carrinho.pack(side="right", fill="y")

        self.texto_carrinho = tk.Text(self.frame_texto_carrinho, height=20, width=35, font=self.fonte_carrinho, bg="#fafafa",
                                     yscrollcommand=self.scroll_carrinho.set, state="disabled", wrap="word")
        self.texto_carrinho.pack(fill="both", expand=True)
        self.scroll_carrinho.config(command=self.texto_carrinho.yview)

        # Frame dos botões do carrinho
        botoes_frame = tk.Frame(self.frame_carrinho, bg="#ffffff")
        botoes_frame.pack(fill="x", pady=10, padx=10)

        # Botão finalizar compra
        self.btn_finalizar = tk.Button(botoes_frame, text="Finalizar Compra", bg="#4CAF50", fg="white",
                                      font=self.fonte_botoes, width=15, relief="flat", cursor="hand2",
                                      command=self.finalizar_compra)
        self.btn_finalizar.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.btn_finalizar.bind("<Enter>", lambda e: self.btn_finalizar.config(bg="#45a049"))
        self.btn_finalizar.bind("<Leave>", lambda e: self.btn_finalizar.config(bg="#4CAF50"))

        # Botão esvaziar carrinho
        self.btn_esvaziar = tk.Button(botoes_frame, text="Esvaziar Carrinho", bg="#e53935", fg="white",
                                      font=self.fonte_botoes, width=15, relief="flat", cursor="hand2",
                                      command=self.esvaziar_carrinho)
        self.btn_esvaziar.pack(side="left", expand=True, fill="x", padx=(5, 0))
        self.btn_esvaziar.bind("<Enter>", lambda e: self.btn_esvaziar.config(bg="#c62828"))
        self.btn_esvaziar.bind("<Leave>", lambda e: self.btn_esvaziar.config(bg="#e53935"))

        self.atualizar_carrinho()

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=0)

    def ajustar_largura_produtos(self, event):
        largura = event.width
        self.canvas.itemconfig(self.produtos_internos_id, width=largura)

    def atualizar_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def criar_item_produto(self, codigo, info):
        frame = tk.Frame(self.produtos_internos, bg="#f0f0f0", bd=1, relief="ridge", padx=10, pady=10)
        frame.pack(pady=8, padx=8, fill="x")

        try:
            imagem = tk.PhotoImage(file=info["imagem"]).subsample(12, 12)
            self.imagens_produtos[codigo] = imagem
        except Exception as e:
            print(f"Erro ao carregar imagem {info['imagem']}: {e}")
            imagem = None

        if imagem:
            label_img = tk.Label(frame, image=imagem, bg="#f0f0f0")
            label_img.pack(side="left", padx=(0,15))

        frame_info = tk.Frame(frame, bg="#f0f0f0")
        frame_info.pack(side="left", fill="both", expand=True)

        nome_preco = f"{info['nome']} - R$ {info['preco']:.2f}"
        label_nome = tk.Label(frame_info, text=nome_preco, font=self.fonte_produto, bg="#f0f0f0", anchor="w")
        label_nome.pack(anchor="w", pady=(0,8))

        botoes = tk.Frame(frame_info, bg="#f0f0f0")
        botoes.pack(anchor="w")

        btn_adicionar = tk.Button(botoes, text="+", width=3, font=self.fonte_botoes, bg="#81c784", fg="white",
                                  relief="flat", cursor="hand2",
                                  command=lambda c=codigo: self.adicionar_ao_carrinho(c))
        btn_adicionar.pack(side="left", padx=5)
        btn_adicionar.bind("<Enter>", lambda e: btn_adicionar.config(bg="#66bb6a"))
        btn_adicionar.bind("<Leave>", lambda e: btn_adicionar.config(bg="#81c784"))

        btn_remover = tk.Button(botoes, text="-", width=3, font=self.fonte_botoes, bg="#e57373", fg="white",
                                relief="flat", cursor="hand2",
                                command=lambda c=codigo: self.remover_do_carrinho(c))
        btn_remover.pack(side="left", padx=5)
        btn_remover.bind("<Enter>", lambda e: btn_remover.config(bg="#ef5350"))
        btn_remover.bind("<Leave>", lambda e: btn_remover.config(bg="#e57373"))

    def mostrar_mensagem(self, texto, cor="#2e7d32"):
        self.mensagem.config(text=texto, fg=cor)
        self.root.after(1800, lambda: self.mensagem.config(text=""))

    def adicionar_ao_carrinho(self, codigo):
        if codigo in carrinho:
            carrinho[codigo] += 1
        else:
            carrinho[codigo] = 1
        self.atualizar_carrinho()
        self.mostrar_mensagem(f"Adicionado {produtos[codigo]['nome']} ao carrinho!")

    def remover_do_carrinho(self, codigo):
        if codigo in carrinho:
            carrinho[codigo] -= 1
            if carrinho[codigo] <= 0:
                del carrinho[codigo]
            self.atualizar_carrinho()
            self.mostrar_mensagem(f"Removido {produtos[codigo]['nome']} do carrinho.", cor="#c62828")

    def atualizar_carrinho(self):
        self.texto_carrinho.config(state="normal")
        self.texto_carrinho.delete("1.0", tk.END)
        total = 0
        for codigo, qtd in carrinho.items():
            nome = produtos[codigo]["nome"]
            preco = produtos[codigo]["preco"]
            subtotal = preco * qtd
            total += subtotal
            self.texto_carrinho.insert(tk.END, f"{qtd}x {nome} - R$ {subtotal:.2f}\n")
        self.texto_carrinho.insert(tk.END, "\n")
        self.texto_carrinho.insert(tk.END, f"Total: R$ {total:.2f}")
        self.texto_carrinho.config(state="disabled")

    def finalizar_compra(self):
        if not carrinho:
            messagebox.showwarning("Carrinho Vazio", "Adicione produtos antes de finalizar a compra!")
            return
        total = sum(produtos[c]["preco"] * q for c, q in carrinho.items())
        messagebox.showinfo("Compra Finalizada", f"Compra realizada com sucesso!\nTotal: R$ {total:.2f}")
        carrinho.clear()
        self.atualizar_carrinho()

    def esvaziar_carrinho(self):
        if not carrinho:
            return
        if messagebox.askyesno("Esvaziar Carrinho", "Deseja realmente esvaziar o carrinho?"):
            carrinho.clear()
            self.atualizar_carrinho()

if __name__ == "__main__":
    root = tk.Tk()
    app = LojaVirtual(root)
    root.mainloop()
