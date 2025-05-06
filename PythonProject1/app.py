from flask import Flask, request, render_template

# Inicialização da aplicação
app = Flask(__name__)

# Função para calcular as calorias diárias e macronutrientes
def calcular_macros(peso, altura, idade, sexo, atividade, objetivo):
    if sexo == "masculino":
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161

    # Ajuste para o nível de atividade
    if atividade == "sedentario":
        tdee = tmb * 1.2
    elif atividade == "leve":
        tdee = tmb * 1.375
    elif atividade == "moderado":
        tdee = tmb * 1.55
    elif atividade == "intenso":
        tdee = tmb * 1.725
    else:
        tdee = tmb * 1.9

    # Ajuste para o objetivo
    if objetivo == "emagrecer":
        calorias = tdee - 500
    elif objetivo == "manter":
        calorias = tdee
    else:
        calorias = tdee + 500

    # Macronutrientes (baseado em proporção 50% carbs, 25% proteínas, 25% gorduras)
    carbs = (calorias * 0.5) / 4
    proteinas = (calorias * 0.25) / 4
    gorduras = (calorias * 0.25) / 9

    return {
        "calorias": round(calorias),
        "carboidratos": round(carbs),
        "proteinas": round(proteinas),
        "gorduras": round(gorduras)
    }

def calcular_agua(peso):
    # Recomendação geral: 35 ml de água por kg de peso corporal
    agua_ml = peso * 35
    agua_litros = agua_ml / 1000
    return round(agua_litros, 2)

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    atividade_descricoes = {
        "sedentario": "Pouco ou nenhum exercício.",
        "leve": "Exercício leve (1-3 dias por semana).",
        "moderado": "Exercício moderado (3-5 dias por semana).",
        "intenso": "Exercício intenso (6-7 dias por semana).",
        "muito_intenso": "Exercício muito intenso ou trabalho físico pesado."
    }

    if request.method == "POST":
        # Coleta dos dados do formulário
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        idade = int(request.form["idade"])
        sexo = request.form["sexo"]
        atividade = request.form["atividade"]
        objetivo = request.form["objetivo"]

        # Calcula os resultados dos macros
        resultados_macros = calcular_macros(peso, altura, idade, sexo, atividade, objetivo)

        # Calcula a quantidade de água
        agua_diaria = calcular_agua(peso)

        return render_template(
            "resultado.html",
            resultados=resultados_macros,
            agua=agua_diaria
        )

    return render_template("index.html", atividade_descricoes=atividade_descricoes)

if __name__ == "__main__":
    app.run(debug=True)