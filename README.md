# atlas-nuclea-ia

Monorepo de pacotes APM para distribuir skills corporativas da Núclea e seus kits de instalação. O desenho combina pacotes independentes, trunk-based development, releases imutáveis por pacote e consumo reprodutível pelo Kiro.

## O que este repositório entrega

- Uma skill por pacote em `skills/<nome>/`.
- Um kit agregador em `kits/all/` para instalar o conjunto oficial com um comando.
- Tags independentes no formato `<pacote>--v<semver>`.
- CI para estrutura, versão, segurança, testes e instalação APM.
- CD idempotente: uma tag publicada nunca é movida.
- Exemplo de consumo no Kiro com o MCP do SonarQube em modo somente leitura.
- Policy APM de referência e regras adicionais para validar `repositório + pasta + ref`.

## Estrutura

```text
skills/<nome>/
├── apm.yml
├── .apm/skills/<nome>/SKILL.md
├── .apm/skills/<nome>/references/
├── tests/cases.yml
├── CHANGELOG.md
└── catalog-info.yaml

kits/all/
├── apm.yml
└── CHANGELOG.md
```

O primeiro diretório delimita o pacote versionável; `.apm/skills/<nome>/` é o layout nativo que o APM entrega ao runtime.

## Desenvolvimento local

Requisitos: Python 3.11+, `pip`, Git e o [APM CLI](https://microsoft.github.io/apm/quickstart/). O CI fixa a versão do APM em `atlas.yml`; a versão atual é a primeira homologada neste scaffold com o target Kiro.

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validate_repo.py
```

Confirme que `apm --version` responde `Agent Package Manager` (algumas máquinas antigas ainda possuem o `apm` do Atom). Então:

```bash
apm audit --file skills/terraform-review/.apm/skills/terraform-review/SKILL.md
python tools/smoke_install.py --package skills/terraform-review
```

## Executar o Gerenciador de APMs

O gerenciador web permite consultar, criar e editar os APMs do repositório. Na raiz do projeto, prepare o ambiente e inicie o servidor:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python apps/apm-manager/server.py --port 4174
```

Abra [http://127.0.0.1:4174](http://127.0.0.1:4174) no navegador. Não abra o `index.html` diretamente: a interface usa a API local para carregar e salvar os APMs.

O botão **Salvar** altera os arquivos do pacote, valida o repositório, cria um commit e tenta enviá-lo ao remoto configurado. Use `Ctrl+C` no terminal para encerrar o servidor.

## Instalar todas as skills

Em um projeto consumidor, o Atlas deve gerar uma dependência para o kit completo. Para exploração manual:

```bash
apm install nuclea/atlas-nuclea-ia/kits/all#atlas-all--v1.1.0 --target kiro
```

Em produção, o PR gerado pelo Atlas deve preferir o SHA completo da release aprovada. O `apm.lock.yaml` e os arquivos gerados devem ser versionados; `apm_modules/` deve permanecer ignorado.

Veja [o guia do consumidor](docs/consumer-guide.md) e o [exemplo Kiro + Sonar](examples/consumer/README.md).

## Fluxo de publicação

1. O Atlas abre uma PR curta com a skill, `version` e changelog.
2. O CI valida o pacote e sua instalação em um projeto temporário.
3. Após aprovação e merge na `main`, o CD publica a tag e o GitHub Release.
4. A skill só é oficial depois que a publicação termina com sucesso.
5. A automação sincroniza `kits/all` por uma PR separada.
6. Projetos consumidores recebem PRs de atualização; não há atualização silenciosa.

Detalhes em [Arquitetura](docs/architecture.md), [Governança](docs/governance.md) e [Processo de release](docs/release-process.md).

## Configuração inicial

Antes de publicar, revise `atlas.yml`, especialmente `repository`, `owners` e `apm_version`. Configure rulesets e ambientes do GitHub conforme `docs/governance.md`. Nenhuma credencial deve ser gravada neste repositório.
