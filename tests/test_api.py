def test_health(client):
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_version(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "abc1234")
    assert client.get("/version").json() == {"version": "abc1234"}


def test_cardapio_comeca_vazio_no_banco_de_teste(client):
    assert client.get("/cafes").json() == []


def test_criar_e_obter_cafe(client):
    criado = client.post("/cafes", json={"nome": "Cerrado", "preco": 12.5})
    assert criado.status_code == 201
    cafe_id = criado.json()["id"]
    obtido = client.get(f"/cafes/{cafe_id}")
    assert obtido.status_code == 200
    assert obtido.json()["nome"] == "Cerrado"


def test_listar_cafes_retorna_os_cadastrados(client):
    client.post("/cafes", json={"nome": "Bourbon", "preco": 9.0})
    client.post("/cafes", json={"nome": "Catuaí", "preco": 8.0})
    assert len(client.get("/cafes").json()) == 2


def test_cafe_duplicado_retorna_409(client):
    client.post("/cafes", json={"nome": "Geisha", "preco": 30.0})
    resposta = client.post("/cafes", json={"nome": "Geisha", "preco": 31.0})
    assert resposta.status_code == 409


def test_preco_invalido_retorna_422(client):
    resposta = client.post("/cafes", json={"nome": "Grátis", "preco": 0})
    assert resposta.status_code == 422


def test_cafe_inexistente_retorna_404(client):
    assert client.get("/cafes/999").status_code == 404


def test_preco_com_desconto_via_api(client):
    cafe_id = client.post("/cafes", json={"nome": "Mogiana", "preco": 10}).json()["id"]
    resposta = client.get(f"/cafes/{cafe_id}/preco?desconto=10")
    assert resposta.status_code == 200
    assert resposta.json()["preco_final"] == 9.0


def test_desconto_de_80_por_cento_e_rejeitado(client):
    cafe_id = client.post("/cafes", json={"nome": "Sul de Minas", "preco": 10}).json()["id"]
    resposta = client.get(f"/cafes/{cafe_id}/preco?desconto=80")
    assert resposta.status_code == 422


def test_criar_cafe_com_origem(client):
    criado = client.post(
        "/cafes", json={"nome": "Chapada", "preco": 15.0, "origem": "Bahia"}
    )
    assert criado.status_code == 201
    assert criado.json()["origem"] == "Bahia"