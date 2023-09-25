from flask import Flask, request, jsonify

app = Flask(__name__)

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

class Carrinho:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def remover_produto(self, produto):
        if produto in self.produtos:
            self.produtos.remove(produto)

    def calcular_total(self):
        total = sum(produto.preco for produto in self.produtos)
        return total

    def finalizar_compra(self):
        total = self.calcular_total()
        return total

class Pedido:
    def __init__(self, produtos, total):
        self.produtos = produtos
        self.total = total

# Simulando alguns produtos e um carrinho
produto1 = Produto("Camiseta", 20.0, 10)
produto2 = Produto("Calça", 50.0, 5)
carrinho = Carrinho()
carrinho.adicionar_produto(produto1)
carrinho.adicionar_produto(produto2)

@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    data = request.json
    nome = data['nome']
    preco = data['preco']
    estoque = data['estoque']
    produto = Produto(nome, preco, estoque)
    carrinho.adicionar_produto(produto)
    return "Produto adicionado ao carrinho com sucesso!"

@app.route('/remover_produto', methods=['DELETE'])
def remover_produto():
    data = request.json
    nome = data['nome']
    for produto in carrinho.produtos:
        if produto.nome == nome:
            carrinho.remover_produto(produto)
            return "Produto removido do carrinho com sucesso!"
    return "Produto não encontrado no carrinho."

@app.route('/calcular_total', methods=['GET'])
def calcular_total():
    total = carrinho.calcular_total()
    return jsonify({"total": total})

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    total = carrinho.finalizar_compra()
    pedido = Pedido(carrinho.produtos, total)
    carrinho.produtos = []  # Limpa o carrinho após a compra
    return jsonify({"mensagem": "Compra finalizada com sucesso!", "total": total})

if __name__ == '__main__':
    app.run(debug=True)
