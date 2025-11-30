from flask import Blueprint, request, jsonify
import os, json

context_bp = Blueprint('context', __name__)

BASE_DIR = "data"

@context_bp.route("/salvar-json", methods=["POST"])
def salvar_json():
    data = request.get_json()
    fase = data.get("fase")
    tema = data.get("tema")
    nome = data.get("nome")
    conteudo = data.get("conteudo")

    path = os.path.join(BASE_DIR, fase, tema)
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, f"{nome}.json"), "w", encoding="utf-8") as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)

    return jsonify({"status": "ok", "message": f"{nome}.json salvo com sucesso."})

@context_bp.route("/carregar-json", methods=["GET"])
def carregar_json():
    fase = request.args.get("fase")
    tema = request.args.get("tema")
    nome = request.args.get("nome")

    path = os.path.join(BASE_DIR, fase, tema, f"{nome}.json")
    if not os.path.exists(path):
        return jsonify({"error": "Arquivo não encontrado."}), 404

    with open(path, "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    return jsonify({"conteudo": conteudo})

@context_bp.route("/listar-blocos", methods=["GET"])
def listar_blocos():
    fase = request.args.get("fase")
    tema = request.args.get("tema")
    path = os.path.join(BASE_DIR, fase, tema)

    if not os.path.exists(path):
        return jsonify({"blocos": []})

    arquivos = [f for f in os.listdir(path) if f.endswith(".json")]
    return jsonify({"blocos": arquivos})